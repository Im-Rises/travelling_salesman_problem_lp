# travelling_salesman_problem_lp

<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="pythonLogo" style="height:50px"/>
    <img src="" alt="googleOrtoolsLogo" style="height:50px"/>
</p>

Travelling salesman problem solver using linear programming with Google Or-Tools.

## Description

The Travelling Salesman Problem also known as TSP is an NP-hard problem in combinatorial optimization.  
Imagine a set of city disposed on a map, you have a set of salesman (population) and they must all go to every city in
the least amount of time/distance.  
The optimization solution is the one where a salesman goes through all the cities with the least distance or/and time.

In the image below you can see a representation of the tsp problem with cities named A, B, C, D. Going from a city to
another take more or less time than other depending on the distance.

<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/165635831-5bfc72b5-0dd3-4a9f-afb0-b5ffd402ee88.png" alt="tspExampleImage" style="height:400px"/>
</p>

## Problem modelisation

Below is the problem modernisation in Linear Programming.

- Parameters:
    1. i,j: indices on set V of customers
    2. $$d_{i,j}$$: distance between customers i and j

- Variables: for each $$i \ne j \in V, x_{i,j} = 1$$ if the salesman travels directly from i to j and 0 otherwise.

- Objective function:

$$min {\sum_{i \ne j \in V}}{d_{ij} x{ij}}$$

- Constraints

    1. (one successor) $$\forall i \in V \sum x_{i,j} = 1$$
    2. (one predecessor) $$\forall j \in V \sum x_{i \in V,i \ne j} = 1$$
    3. (subtour elimination) $$\forall S \nsubseteq V {\sum_{i \in S,j \in V \backslash S}}{x_{ij}} \geq 1$$

<!--
<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/169556846-231900f0-2195-478d-be14-0990f52ea1b4.png" alt="tspExampleImage" style="height:400px"/>
</p>
-->

## Quick start

You need python3 to start the app. you also need some packages that are listed in the `requirements.txt`.  
To install them all type the following command :

```bash
pip install -r requirements.txt
```

You can then start the program by double-clicking the main.py file.

If you want to change the excel file to use or change the city to begin with in your tsp. Just change the last line of
the main.py file.

```bash
py main.py <city> <path/to/excel> <sheet_name>
```

Example :

```bash
py main.py "Sydney" data.xlsx sheet1 
```

## Test

To verify if the result of the script is good one, you can start the script `example_with_routings.py`.

### Use the example_with_routings script

It works exactly the same way as the `main.py` script.

```bash
py example_with_routings.py <city> <path/to/excel> <sheet_name>
```

Example :

```bash
py example_with_routings.py "Sydney" data.xlsx sheet1 
```

### Start Unit Test Python script

Placeholder

## Program implementation

### Strcuture

The program is made only of one file, the "main.py" file.

The python file load the dataset and then proceed all the linear programming calculs.

### Excel data

Our project contains a excel file that is load by our app.
The excel contains the distances of all cities relativeness from each other.

**CSV Example :**

| |M.C.G.|Docklands|Adelaide Oval|
|--|--|--|--|
|M.C.G.| 0| 3 |657 |
|Docklands| 3|0 |654 |
|Adelaide Oval| 657|654|0|

The excel is loaded in our app and it will search the city by the name you set in the variable `city_origin_name`. This
name will be used to move the row of the city at the beginning of our project.

For example, if you want to begin your travel from Adelaide Oval, the data will look like below :

**CSV Example :**

| |M.C.G.|Docklands|Adelaide Oval|
|--|--|--|--|
|Adelaide Oval| 657|654|0|
|M.C.G.| 0| 3 |657 |
|Docklands| 3|0 |654 |

### Linear Programming

Linear programming implementation is completely set in the solve function.

Below is a part of the function solve :

Output :

```
villes dans l'ordre : 
Sydney->S.C.G.->Carrara->Gabba->Riverway Stadium->Cazaly's Stadium->Marrara Oval->Traeger Park->Perth Stadium->Adelaide Oval->Eureka Stadium->Kardinia Park->Bellerive Oval->York Park->Manuka Oval->M.C.G.->Docklands->Sydney
```

### Routing implementation

To verify the app output result. We create a file named `example_with_routings.py` that will solve our tsp problem but
by using routing.

Output :

```
Objective: 11669 miles
Route for vehicle 0:
 0 -> 1 -> 9 -> 12 -> 2 -> 5 -> 13 -> 15 -> 3 -> 16 -> 6 -> 14 -> 7 -> 10 -> 4 -> 8 -> 11 -> 0
```

## Contributors

Clément Reiffers :

- @clementreiffers
- <https://github.com/clementreiffers>

Quentin Morel :

- @Im-Rises
- <https://github.com/Im-Rises>

Adrien Tirlemont :

- @Meatisdelicious
- <https://github.com/Meatisdelicious>

## Documentations and API

Google Or-Tools :  
<https://developers.google.com/optimization/>

TSP solvers Or-Tools :
<https://developers.google.com/optimization/routing/tsp>

TSP Linear Programming solver :  
<https://hal.archives-ouvertes.fr/hal-02947086/document>
