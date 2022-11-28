from time import process_time
from file_reader import file_reader 
from greedy_method import greedy_cvrp
import math

def getNeighbours(solution):
    neighbours = []
    
    for i in range(1,len(solution)):
        for j in range(i + 1, len(solution)-1):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbours.append(neighbour)
    
    return neighbours

def routeLength(graph, solution, graph_format):
    routeLength = 0

    # Calculating route length for adjacency matrix
    if graph_format == 'LOWER_COL' or graph_format == 'UPPER_ROW':
        for i in range(len(solution) - 1):
            routeLength += graph[solution[i]][solution[i + 1]]

    # Calculating routes for euclidean format
    elif graph_format == 'EUC_2D' or graph_format == 'ATT':
        for i in range(len(solution) - 1):
            routeLength += math.sqrt(pow(graph[solution[i]][0] - graph[solution[i + 1]][0], 2) + 
                                    pow(graph[solution[i]][1] - graph[solution[i + 1]][1], 2))
    return routeLength

def getBestNeighbour(graph, neighbours, graph_format):
    bestRouteLength = routeLength(graph, neighbours[0], graph_format)
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteLength = routeLength(graph,neighbour, graph_format)
        if currentRouteLength < bestRouteLength:
            bestRouteLength = currentRouteLength
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteLength

def local_search (graph, dimension, capacity, graph_format, demand, depot, distance, routes, individual_distances):
    start_time = process_time()
    bestRoutes = routes
    bestDistance = distance
    bestIndividualDistance = individual_distances
    currentRoute = routes
    currentIndividualDistances = individual_distances  

    i = 0
    currentDistance = 0
    while i < len(currentRoute):
        # Comparação para rotas com apenas 1 ponto
        if(len(currentRoute[i]) > 3):
            neighbours = getNeighbours(currentRoute[i])
            bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(graph, neighbours, graph_format)
            iterations = 5000
            while(currentIndividualDistances[i] <= bestNeighbourRouteLength and iterations > 0):
                bestNeighbour = currentRoute[i]
                neighbours = getNeighbours(currentRoute[i])
                bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(graph, neighbours, graph_format)
                currentRoute[i] = bestNeighbour
                iterations -= 1
            if(currentIndividualDistances[i] > bestNeighbourRouteLength):
                currentIndividualDistances[i] = bestNeighbourRouteLength
            currentDistance += currentIndividualDistances[i]
        i += 1

    if(currentDistance < bestDistance):
        bestDistance = currentDistance
        bestRoutes = currentRoute
        bestIndividualDistance = currentIndividualDistances

    return bestDistance, bestRoutes, bestIndividualDistance, process_time() - start_time

initial_time = process_time()

files = (
         'lib/CVRP/eil7.vrp/eil7.vrp',
         'lib/CVRP/eil13.vrp/eil13.vrp',
         'lib/CVRP/eil22.vrp/eil22.vrp',
         'lib/CVRP/eil23.vrp/eil23.vrp',
         'lib/CVRP/eil30.vrp/eil30.vrp',
         'lib/CVRP/eil33.vrp/eil33.vrp',
         'lib/CVRP/eil51.vrp/eil51.vrp',
         'lib/CVRP/eilA76.vrp/eilA76.vrp',
         'lib/CVRP/eilA101.vrp/eilA101.vrp',
         'lib/CVRP/eilB76.vrp/eilB76.vrp',
         'lib/CVRP/eilB101.vrp/eilB101.vrp',
         'lib/CVRP/eilC76.vrp/eilC76.vrp',
         'lib/CVRP/eilD76.vrp/eilD76.vrp',
        )

output = ''

for file in files:
    data = file_reader(file)
    print("\nData - " + file)
    print("Graph: " + str(data[0]))
    print("Dimension: " + str(data[1]))
    print("Capacity: " + str(data[2]))
    print("Format: " + str(data[3]))
    print("Demand: " + str(data[4]))
    print("Depot: " + str(data[5]))
    
    greedy_results = greedy_cvrp(data[0], data[1], data[2], data[3], data[4].copy(), data[5])

    search_results = local_search(data[0], data[1], data[2], data[3], data[4].copy(), data[5],
    greedy_results[0], greedy_results[2].copy(), greedy_results[3].copy())

    print("\nLocal search results - " + file)
    print("Distance: " + str(search_results[0]))
    print("Routes: " + str(search_results[1]))
    print("Individual Distances: " + str(search_results[2]))

    output += file.replace('lib/CVRP/', '').replace('.vrp', '') + ':'
    output += f' Total distance traveled: {search_results[0]}, Routes: {str(search_results[1])}, Individual route distance: {str(search_results[2])}, Execution time: {search_results[3]:.30f} s\n'

with open('local_search_results.txt', 'w') as output_file:
    output_file.write('Local Search Output:\n' + output + f'total time:{ (process_time() - initial_time)} s')