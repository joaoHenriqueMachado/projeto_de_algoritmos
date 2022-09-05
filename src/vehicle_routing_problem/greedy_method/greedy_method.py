from time import process_time
from file_reader import file_reader 
import math

'''
    This function receives a graph, its dimension and format, the delivery capacity, the demand and the depots
    It returns the distance traveled, the load of each truck, the routes and the execution time
'''
def greedy_cvrp(graph, dimension, capacity, graph_format, demand, depot):

    full_demand = 0
    for x in demand:
        full_demand += x

    min_trucks_needed = float(full_demand / capacity).__ceil__()

    j = 0
    points = list()
    trucks = list()
    while j < min_trucks_needed:
        trucks.append(capacity)
        points.append(list())
        j+=1
    
    # Estratégia de balanceamento de carga
    while full_demand > 0:
        max_delivery = 0
        max_space = 0
        delivery_index = 0
        for x in demand:
            if x > max_delivery and x <= capacity:
                max_delivery = x
                delivery_index = demand.index(x)
        for x in trucks:
            if x > trucks[max_space]:
                max_space = trucks.index(x)
        if(trucks[max_space] >= max_delivery):
            trucks[max_space] -= max_delivery
            full_demand -= max_delivery
            demand[delivery_index] = 0
            points[max_space].append(delivery_index) 
        else:
            trucks.append(capacity - max_delivery)
            points.append(list())
            full_demand -= max_delivery
            demand[delivery_index] = 0
            points[trucks.__len__() - 1].append(delivery_index)

    print(trucks)
    print(points)

    ''' Estratégia de máxima carga disponível
    trucks = list()
    points = list()
    truck_capacity = capacity
    points.append(1)
    while full_demand > 0:
        max_delivery = 0
        delivery_index = -1
        for x in demand:
            if x > max_delivery and x <= truck_capacity:
                max_delivery = x
                delivery_index = demand.index(x)
        if max_delivery > 0:
            truck_capacity -= max_delivery
            full_demand -= max_delivery
            demand[delivery_index] = 0
            points.append(delivery_index)
        else:
            trucks.append(points)
            truck_capacity = capacity
            points = []
            points.append(1)
    trucks.append(points)
    print(trucks)
    '''

    j = 0
    while j < len(trucks):
            trucks[j] = capacity - trucks[j]
            j+=1

    # Calculating routes and distances
    if graph_format == 'EUC_2D':
        traveled_distance = 0
        routes = []
        distance_list = []
        j = 0
        while j < points.__len__():     
            start_position = 0
            next_index = 0
            distance = -1
            route_distance = 0
            routes.append(list())
            routes[j].append(0)

            while len(points[j]) > 0:
                for y in points[j]:
                    if distance == -1:
                        distance = math.sqrt(pow(graph[start_position][0] - graph[y][0], 2) + 
                                        pow(graph[start_position][1] - graph[y][1], 2))
                    else:
                        if math.sqrt(pow(graph[start_position][0] - graph[y][0], 2) + pow(graph[start_position][1] - graph[y][1], 2)) < distance:
                            distance = math.sqrt(pow(graph[start_position][0] - graph[y][0], 2) + 
                                        pow(graph[start_position][1] - graph[y][1], 2))
                    next_index = points[j].index(y)
                    points[j].pop(next_index)
                    routes[j].append(y)
                    start_position = y
                    traveled_distance += distance
                    route_distance += distance
            traveled_distance += math.sqrt(pow(graph[start_position][0] - graph[0][0], 2) + 
                                        pow(graph[start_position][1] - graph[0][1], 2))
            route_distance += math.sqrt(pow(graph[start_position][0] - graph[0][0], 2) + 
                                        pow(graph[start_position][1] - graph[0][1], 2))
            routes[j].append(0)
            distance_list.append(route_distance)
            j += 1
    elif graph_format == 'LOWER_COL': 
        print("Lower side matrix")
        
    end_time = process_time()
    return traveled_distance, trucks, routes, distance_list, end_time - start_time

start_time = process_time()

files = (
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
    
    results = greedy_cvrp(data[0], data[1], data[2], data[3], data[4].copy(), data[5])
    output += file.replace('lib/CVRP/', '').replace('.vrp', '') + ':'
    output += f' Total distance traveled: {results[0]}, Truck load: {str(results[1])}, Routes: {str(results[2])}, Individual route distance: {str(results[3])}, Execution time: {results[4]:.30f} s\n'
    with open('greedy_results.txt', 'w') as output_file:
        output_file.write('Greedy Output:\n' + output + f'total time:{ (process_time() - start_time)} s')
