import common_functions as cf
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def create_data_model(city_origin_name, filename, sheet):
    """Stores the data for the problem."""
    dima, name_cities, index_cities = cf.create_and_prepare_csv(city_origin_name, filename, sheet)
    return {
               'distance_matrix': dima,
               'num_vehicles': 1
           }, name_cities, index_cities


def print_solution(manager, routing, solution, name_cities):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()} miles')
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f'{name_cities[manager.IndexToNode(index)]} -> '
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += '{}\n'.format(name_cities[manager.IndexToNode(index)])
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def main(city_origin_name, filename, sheet):
    """Entry point of the program."""
    # Instantiate the data problem.
    data, name_cities, index_cities = create_data_model(city_origin_name, filename, sheet)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], index_cities[city_origin_name])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution, name_cities)


if __name__ == '__main__':
    main("Sydney", "data.xlsx", "sheet1")
