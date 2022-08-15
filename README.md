# travelling_salesman_problem_lp

<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="pythonLogo" style="height:50px"/>
    <img src="https://user-images.githubusercontent.com/59691442/174799409-9bd85fe6-b58e-4ba3-a4a4-cdfaaa5b91f0.jpg" alt="googleOrtoolsLogo" style="height:50px"/>
</p>

## Description

Travelling salesman problem solver using linear programming with Google Or-Tools.

The Travelling Salesman Problem also known as TSP is an NP-hard problem in combinatorial optimization.  
Imagine a set of city disposed on a map, you have a set of salesman (population) and they must all go to every city in
the least amount of time/distance.  
The optimization solution is the one where a salesman goes through all the cities with the least distance or/and time.

In the image below you can see a representation of the tsp problem with cities named A, B, C. Going from a city to
another take more or less time than other depending on the distance.

<!-- <p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/165635831-5bfc72b5-0dd3-4a9f-afb0-b5ffd402ee88.png" alt="tspExampleImage" style="height:400px"/>
</p> -->

<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/175610459-6ff46e53-08f3-45a1-b2c6-3d17761158c7.png" alt="tspExampleImage" style="height:300px"/>
</p>

## Problem modeling

Below is the problem modeling in Linear Programming.

- Parameters:
    1. $i,j$: indices on set V of customers
    2. $d_{i,j}$: distance between customers i and j

- Variables: for each $i \ne j \in V, x_{i,j} = 1$ if the salesman travels directly from i to j and 0 otherwise.

- Objective function:

$$min {\sum_{i \ne j \in V}}{d_{ij} x{ij}}$$

- Constraints

    1. (one successor) $$\forall i \in V \sum x_{i,j} = 1$$
    2. (one predecessor) $$\forall j \in V \sum x_{i \in V,i \ne j} = 1$$
    3. (sub-tour elimination) $$\forall S \nsubseteq V {\sum_{i \in S,j \in V \backslash S}}{x_{ij}} \geq 1$$

<!--
<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/169556846-231900f0-2195-478d-be14-0990f52ea1b4.png" alt="tspExampleImage" style="height:400px"/>
</p>
-->

## Linear Programming

Linear programming implementation is completely set in the solve function.

Output :

```
Objective value = 11669 miles
Route:
Sydney -> S.C.G. -> Carrara -> Gabba -> Riverway Stadium -> Cazaly's Stadium -> Marrara Oval -> Traeger Park -> Perth Stadium -> Adelaide Oval -> Eureka Stadium -> Kardinia Park -> Docklands -> M.C.G. -> York Park -> Bellerive Oval -> Manuka Oval -> Sydney
```

## Routing implementation

To verify the app output result from the linear programming. We created a file named `example_with_routings.py` that will
solve our tsp problem but
by using routing.

Output :

```
Objective value = 11669 miles
Route:
Sydney -> S.C.G. -> Carrara -> Gabba -> Riverway Stadium -> Cazaly's Stadium -> Marrara Oval -> Traeger Park -> Perth Stadium -> Adelaide Oval -> Eureka Stadium -> Kardinia Park -> Docklands -> M.C.G. -> York Park -> Bellerive Oval -> Manuka Oval -> Sydney
```

## Quick start

### Use the linear_prog_res.py script

You need python3 to start the app. you also need some packages that are listed in the `requirements.txt`.  
To install them all type the following command :

```bash
pip install -r requirements.txt
```

You can then start the program by starting the `linear_prog_res.py` file like below:

```bash
py linear_prog_res.py <city> <path/to/excel> <sheet_name>
```

Example :

```bash
py linear_prog_res.py "Sydney" data.xlsx sheet1 
```

### Use the routings_res.py script

This script use routing system to solve the problem.

To start it, use it exactly the same way as the `linear_prog_res.py` script.

```bash
py routings_res.py <city> <path/to/excel> <sheet_name>
```

Example :

```bash
py routings_res.py "Sydney" data.xlsx sheet1
```

## Unit test

To start the test file just run the following command :

```bash
py unit_test.py
```

An assertion will be returned if any difference of output happen between the linear programming script and the routing
script.

A GitHub actions is set with the project explained below.

## GitHub actions

[![Python application](https://github.com/Im-Rises/travelling_salesman_problem_lp/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/Im-Rises/travelling_salesman_problem_lp/actions/workflows/python-app.yml)

The app state is verified with a test script detailed in the sections `Start Unit Test Python script`.

A GitHub actions workflow is set to verify the good behaviour of the script while creating a pull request to the main
branch.

### Use another Excel file

Our project contains an Excel file that is load by our app.
The Excel contains the distances of all cities relatively from each other.

**CSV Example :**

The Excel file you load send as a parameter at the script needs to be formed like below:

|               | M.C.G. | Docklands | Adelaide Oval |
|---------------|--------|-----------|---------------|
| M.C.G.        | 0      | 3         | 657           |
| Docklands     | 3      | 0         | 654           |
| Adelaide Oval | 657    | 654       | 0             |

The Excel is loaded in our scripts, it will search the city by the name you set as starting city. The script will
internally move the row and column of the target city at index [0,0] of the internal array to start the travel from this city.

For example, if you want to begin your travel from Adelaide Oval, the data will look like below :

**CSV internal script modification example :**

|               | M.C.G. | Docklands | Adelaide Oval |
|---------------|--------|-----------|---------------|
| M.C.G.        | 0      | 3         | 657           |
| Docklands     | 3      | 0         | 654           |
| Adelaide Oval | 657    | 654       | 0             |

will become:

|               | Adelaide Oval | M.C.G. | Docklands |
|---------------|---------------|--------|-----------|
| Adelaide Oval | 0             | 657    | 654       |
| M.C.G.        | 657           | 0      | 3         |
| Docklands     | 654           | 3      | 0         |

## Documentations and API

Google Or-Tools :  
<https://developers.google.com/optimization/>

TSP solvers Or-Tools :  
<https://developers.google.com/optimization/routing/tsp>

TSP Linear Programming solver :  
<https://hal.archives-ouvertes.fr/hal-02947086/document>

## Contributors

Quentin Morel :

- @Im-Rises
- <https://github.com/Im-Rises>

Clément Reiffers :

- @clementreiffers
- <https://github.com/clementreiffers>

[![GitHub contributors](https://contrib.rocks/image?repo=im-rises/travelling_salesman_problem_lp)](https://github.com/im-rises/travelling_salesman_problem_lp/graphs/contributors)
