import math
from time import process_time
from file_reader import file_reader
from greedy_method import greedy_cvrp
from local_search import local_search


def annealing():
    return


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

    greedy_results = greedy_cvrp(
        data[0], data[1], data[2], data[3], data[4].copy(), data[5])

#     annealing_results = annealing()

#     print("\nSimulated Annealing results - " + file)
#     print("Distance: " + str(annealing_results[0]))
#     print("Routes: " + str(annealing_results[1]))
#     print("Individual Distances: " + str(annealing_results[2]))

#     output += file.replace('lib/CVRP/', '').replace('.vrp', '') + ':'
#     output += f' Total distance traveled: {annealing_results[0]}, Routes: {str(annealing_results[1])}, Individual route distance: {str(annealing_results[2])}, Execution time: {annealing_results[3]:.30f} s\n'

# with open('local_annealing_results.txt', 'w') as output_file:
#     output_file.write('Simulated Annealing Output:\n' + output + f'total time:{ (process_time() - initial_time)} s')
