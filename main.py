import numpy as np
import pandas as pd
from ortools.linear_solver import pywraplp


def solve(distances: np.ndarray):
    """
    :param distances: la matrice avec toutes les distances
    :return:  solution X, model, status
    """
    # on vérifie que la matrice reçue a bien 2 dimensions et après que
    # ses 2 dimensions contiennent le même nombre de distances, car on
    # travaille avec une matrice carrée
    if distances.ndim != 2 and distances.shape[0] != distances.shape[1]:
        raise ValueError("Invalid dima dimensions detected. Square matrix expected.")

    # on détermine le nombre de villes et on cree des variables qui vont servir à itérer dessus
    nombre_de_villes = distances.shape[0]
    index_villes = range(nombre_de_villes)
    index_villes_sauf_premiere = range(1, nombre_de_villes)

    # on cree le modele en mode scip
    model = pywraplp.Solver.CreateSolver('SCIP')
    model.EnableOutput()

    # on génère les variables de decisions sous forme de booleen pour savoir si on passer par cette ville ou pas
    x = {}
    for i in index_villes:
        for j in index_villes:
            x[(i, j)] = model.BoolVar(f"x_i{i}j{j}")

    # on initialise les variables de decision
    u = {i: model.IntVar(0, nombre_de_villes, f"u_i{i}") for i in index_villes}

    # contrainte : on veut un seul successeur
    for i in index_villes:
        model.Add(sum(x[(i, j)] for j in index_villes) == 1)

    # contrainte : on veut un seul prédécesseur
    for j in index_villes:
        model.Add(sum(x[(i, j)] for i in index_villes) == 1)

    # ici on vérifie que l'on fait bien une seule fois le tour
    # contrainte : on commence par la premiere ville
    model.Add(u[0] == 1)

    # on crée un chemin avec toutes les villes, (donc en ne partant pas de la première sinon ça fait doublon et on
    # ne veut pas)
    for i in index_villes_sauf_premiere:
        model.Add(u[i] >= 2)
        model.Add(u[i] <= nombre_de_villes)

    for i in index_villes_sauf_premiere:
        for j in index_villes_sauf_premiere:
            model.Add(u[i] - u[j] + 1 <= (nombre_de_villes - 1) * (1 - x[(i, j)]))

    # on veut que la distance soir la plus petite possible
    model.Minimize(sum(x[(i, j)] * distances[(i, j)] for i in index_villes for j in index_villes))

    status = model.Solve()

    return u, model, status


def print_solution(u, cities):
    """
    :param u: tous les nœuds
    :param cities: le tableau qu'on a récupéré de toutes les villes
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
    # Load dataset and drop useless/empty rows
    df = pd.read_excel(filename, sheet)

    # Create dictionaries
    name_cities = np.array(df.columns.values)
    name_cities = np.delete(name_cities, 0, axis=0)
    index_cities = dict(zip(name_cities, range(len(name_cities))))
    name_cities = dict(zip(range(len(name_cities)), name_cities))

    # Convert df to numpy array
    dima = np.asarray(df)
    dima = np.delete(dima, 0, axis=1)  # Delete rows' city name

    # Find index of starting city
    index_city_start = index_cities[city_origin_name]

    # Swap city origin tsp to row 0 of array
    dima[(0, index_city_start), :] = dima[(index_city_start, 0), :]

    # Swap city origin tsp to column 0 of array
    dima[:, [0, index_city_start]] = dima[:, [index_city_start, 0]]
    print(dima)

    # Swap dictionaries indexes and names
    name_cities[0], name_cities[index_city_start] = name_cities[index_city_start], name_cities[0]

    # Swap dictionaries indexes and names
    city1,city2 = (name_cities[0],name_cities[index_city_start])
    index_cities[city1], index_cities[city2] = index_cities[city2], index_cities[city1]

    # now solve problem
    u, model, status = solve(dima)

    # check problem response
    if status == pywraplp.Solver.OPTIMAL:
        print(f'Objective value = {str(model.Objective().Value())}')
        print_solution(u, name_cities)
    elif status == pywraplp.Solver.INFEASIBLE:
        print("le probleme n'est pas solvable")
    else:
        print(f"le probleme n'a pas pu être resolu, le probleme est : {status}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main("Sydney", "data.xlsx", "sheet1")
