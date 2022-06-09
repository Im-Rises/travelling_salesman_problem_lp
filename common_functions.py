import numpy as np
import pandas as pd


def create_and_prepare_csv(city_origin_name, filename, sheet):
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

    # Swap dictionaries indexes and names
    name_cities[0], name_cities[index_city_start] = name_cities[index_city_start], name_cities[0]

    # Swap dictionaries indexes and names
    city1, city2 = (name_cities[0], name_cities[index_city_start])
    index_cities[city1], index_cities[city2] = index_cities[city2], index_cities[city1]

    return dima, name_cities, index_cities
