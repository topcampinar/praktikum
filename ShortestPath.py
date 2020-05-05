import math
import queue
from Obstacle import *
class ShortestPath:

    def __init__(self, environment_array, target):

        self.environment_array = environment_array
        self.target = target
        self.size_y = len(environment_array)
        self.size_x = len(environment_array[0])

    def obtain_graph(self):

        environment_array = self.environment_array
        target = self.target

        nr = 0
        graph_dictionary = {}
        size_y = len(environment_array)
        size_x = len(environment_array[0])

        for j in range(0, size_y):
            for i in range(0, size_x):

                neighbor_list = {}

                if (i-1) >= 0:
                    if (j-1) >=0:
                        #neighbor_nr = size * (i-1) + (j-1)
                        neighbor_nr = size_x * (j-1) + (i-1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    if (j+1) < size_y:
                        neighbor_nr = size_x * (j+1) + (i-1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    neighbor_nr = size_x * j + (i-1)
                    neighbor_list[neighbor_nr] = 1

                if (i+1) < size_x:
                    if (j-1) >=0:
                        neighbor_nr = size_x * (j-1) + (i+1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    if (j+1) < size_y:
                        neighbor_nr = size_x * (j+1) + (i+1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    neighbor_nr = size_x * j + (i+1)
                    neighbor_list[neighbor_nr] = 1


                if (j - 1) >= 0:
                    neighbor_nr = size_x * (j - 1) + i
                    neighbor_list[neighbor_nr] = 1

                if (j + 1) < size_y:
                    neighbor_nr = size_x * (j + 1) + i
                    neighbor_list[neighbor_nr] = 1

                graph_dictionary[nr] = neighbor_list
                nr = nr + 1

        #print(graph_dictionary)
        return graph_dictionary

        #print(graph_dictionary)


    def get_path_costs(self):

        graph_dictionary = self.obtain_graph()
        #size = len(self.environment_array)
        size_x = self.size_x
        size_y = self.size_y
        costs = {}

        target_nr = size_x * self.target.x + self.target.y
        for key,value in graph_dictionary.items():
            costs[key] = self.get_shortestpath2(key, target_nr,graph_dictionary)
            #costs[key] = self.get_shortestpath(key, target_nr,graph_dictionary)

        return costs
        #costs[0] = self.get_shortestpath(0, self.target ,graph_dictionary)

    def get_shortestpath(self, source, destination, graph_dictionary):

        distance_costs = []
        #size = len(self.environment_array)
        size_x = self.size_x
        size_y = self.size_y

        for i in range(0, size_x):
            distance_costs.append([])
            for j in range(0, size_y):
                distance_costs[i].append(math.inf)

        #x = int(source / size)
        #y = source % size

        if int(source/size_x) > 1:
            y = int(source / size_x)
            x = int(source % size_x)
        else:
            y = 0
            x = source

        distance_costs[x][y] = 0

        unseen_cells = []
        unseen_cells.append(source)
        unseen_cell_values = []
        unseen_cell_values.append(0)

        visited_cells = []

        while (len(unseen_cells) > 0):

            index = unseen_cell_values.index(min(unseen_cell_values))
            cell = unseen_cells.pop(index)
            dist = unseen_cell_values.pop(index)

            neighbors = graph_dictionary[cell]

            for neighbor in neighbors:
                #x = int(neighbor / size)
                #y = neighbor % size
                if int(neighbor / size_x) > 1:
                    y = int(neighbor / size_x)
                    x = int(neighbor % size_x)
                else:
                    y = 0
                    x = neighbor

                current_cost = distance_costs[x][y]
                update_cost = dist + neighbors[neighbor]

                if update_cost < current_cost:
                    distance_costs[x][y] = update_cost

                if not(neighbor in visited_cells):
                    if not(neighbor in unseen_cells):

                        #if neighbor not in visited_cells:
                        unseen_cells.append(neighbor)
                        unseen_cell_values.append(update_cost)

                visited_cells.append(cell)
            #print(unseen_cells)


        #x = int(destination / size)
        #y = destination % size

        print(destination)
        if int(destination / size_x) > 1:
            y = int(destination / size_x)
            x = int(destination % size_x)
        else:
            y = 0
            x = destination


        return round(distance_costs[x][y], 2)
        #print(distance_costs)



    def get_shortestpath2(self, source, destination, graph_dictionary):

        distance_costs = []
        #size = len(self.environment_array)

        size_x = self.size_x
        size_y = self.size_y
        environment_array = self.environment_array

        for i in range(0, size_y):
            l = [math.inf] * size_x
            distance_costs.append(l)

        #x = int(source / size)
        #y = source % size

        if int(source/size_x) >= 1:
            x = int(source / size_x)
            y = int(source % size_x)
        else:
            x = 0
            y = source

        distance_costs[x][y] = 0

        #unseen_cells = []
        #unseen_cells.append(source)
        #unseen_cell_values = []
        #unseen_cell_values.append(0)

        q = queue.PriorityQueue()
        q.put((0, source))

        unseen_cells = set()
        unseen_cells.add(source)

        visited_cells = set()

        while not(q.empty()):

            #index = unseen_cell_values.index(min(unseen_cell_values))
            #cell = unseen_cells.pop(index)
            #dist = unseen_cell_values.pop(index)
            element = q.get()
            dist = element[0]
            cell = element[1]

            neighbors = graph_dictionary[cell]

            for neighbor in neighbors:
                #x = int(neighbor / size)
                #y = neighbor % size

                if int(neighbor / size_x) >= 1:
                    x = int(neighbor / size_x)
                    y = int(neighbor % size_x)
                else:
                    x = 0
                    y = neighbor

                current_cost = distance_costs[x][y]
                if not isinstance(environment_array[x][y], Obstacle):
                    update_cost = dist + neighbors[neighbor]
                else:
                    update_cost = math.inf

                if update_cost < current_cost:
                    distance_costs[x][y] = update_cost

                #if not(neighbor in visited_cells):
                if not(neighbor in unseen_cells):
                    unseen_cells.add(neighbor)
                    q.put((update_cost, neighbor))

            visited_cells.add(cell)
            #print(unseen_cells)


        #x = int(destination / size)
        #y = destination % size

        if int(destination / size_x) >= 1:
            x = int(destination / size_x)
            y = int(destination % size_x)
        else:
            x = 0
            y = destination

        return round(distance_costs[x][y], 2)
        #print(distance_costs)

























