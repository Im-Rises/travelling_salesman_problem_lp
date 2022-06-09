import sys
import numpy as np
import common_functions as cf
from ortools.linear_solver import pywraplp


def create_array(city_origin_name, filename, sheet):
    # Load dataset and drop useless/empty rows
    return cf.create_and_prepare_csv(city_origin_name, filename, sheet)


def solve(distances: np.ndarray):
    """
    :param distances: The matrix containing all the distances
    :return: solution X, model, status
    """
    # We check the matrix is 2 dimensioned and it's 2 dimensions
    # contains the same numbers of distances (squared matrix)
    if distances.ndim != 2 and distances.shape[0] != distances.shape[1]:
        raise ValueError("Invalid dima dimensions detected. Square matrix expected.")

    # get the number of cities and we begin iterate
    number_of_cities = distances.shape[0]
    index_cities = range(number_of_cities)
    index_cities_except_first = range(1, number_of_cities)

    # Model creation in SCIP
    model = pywraplp.Solver.CreateSolver('SCIP')
    model.EnableOutput()

    # Decision variables generation as boolean if we cross the city
    x = {}
    for i in index_cities:
        for j in index_cities:
            x[(i, j)] = model.BoolVar(f"x_i{i}j{j}")

    # Decision variable instantiation
    u = {i: model.IntVar(0, number_of_cities, f"u_i{i}") for i in index_cities}

    # Constraints : Only one successor
    for i in index_cities:
        model.Add(sum(x[(i, j)] for j in index_cities) == 1)

    # Constraints : Only one predecessor
    for j in index_cities:
        model.Add(sum(x[(i, j)] for i in index_cities) == 1)

    # Check if we only do one tour of the cities
    # Constraints : Begin by the first city
    model.Add(u[0] == 1)

    # We begin the journey through all the cities without beginning by the first one to not count it twice
    for i in index_cities_except_first:
        model.Add(u[i] >= 2)
        model.Add(u[i] <= number_of_cities)

    for i in index_cities_except_first:
        for j in index_cities_except_first:
            model.Add(u[i] - u[j] + 1 <= (number_of_cities - 1) * (1 - x[(i, j)]))

    # Minimization (the minimum way through all the cities)
    model.Minimize(sum(x[(i, j)] * distances[(i, j)] for i in index_cities for j in index_cities))

    status = model.Solve()

    return u, model, status


def print_solution(u, cities):
    """
    :param u: all the nodes
    :param cities: cities index to name dictionary
    :return: None
    """
    num_nodes = len(u)
    all_nodes = range(num_nodes)
    solution = {int(u[i].solution_value()): i for i in all_nodes}
    solution = sorted(solution.items())
    print("\nvilles dans l'ordre : ")
    for i in solution:
        print(f"{cities[i[1]]} -> ", end="")
    print(cities[solution[0][1]])


def main(city_origin_name, filename, sheet):
    # Create and update array of distances
    dima, name_cities, index_cities = create_array(city_origin_name, filename, sheet)

    # now solve problem
    u, model, status = solve(dima)

    # check problem response
    if status == pywraplp.Solver.OPTIMAL:
        print(f'Objective value = {str(model.Objective().Value())}')
        print_solution(u, name_cities)
        return model.Objective().Value()
    elif status == pywraplp.Solver.INFEASIBLE:
        print("le probleme n'est pas solvable")
        return -1
    else:
        print(f"le probleme n'a pas pu être resolu, le probleme est : {status}")
        return -1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main("Sydney", "data.xlsx", "sheet1")
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Not enought argutments:"
              "Usage : routings_res.py <city> <path/to/excel> <sheet_name>")
