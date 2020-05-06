import math
import queue
from Obstacle import *
class ShortestPath:

    """
    ShortestPath(environment_array, target)

    This class is used to determine the shortest path from all cells to the target. Then these costs become
    the initial costs of the cells.

    Attributes:

        environment_array: list
            x coordinate of the Block on the simulation area.
        target: Target
            y coordinate of the Block on the simulation area.
        size_x: int
            width of the simulation area
        size_y:int
            height of the simulation area

    Parameters:

        environment_array: list
            x coordinate of the Block on the simulation area.
        target: Target
            y coordinate of the Block on the simulation area.

    """

    def __init__(self, environment_array, target):

        self.environment_array = environment_array
        self.target = target
        self.size_y = len(environment_array)
        self.size_x = len(environment_array[0])

    def obtain_graph(self):

        # This method is used to obtain the neighbors of each cell. The cells are numbered and the numbers act as keys.
        # Neighbors of each cell is stored in a dictionary, where key is the cell number.
        # and all cells and their neighbor dictionary are also stored in a dictionary, where key is the cell number.
        # The dictionary that holds the cell number and neighbors of the cell is returned.
        # return:
        #   graph_dictionary: dictionary

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

        return graph_dictionary


    def get_path_costs(self):

        # This method is used to call get_shortespath method for each cell
        # to calculate the shortest path from every cell to the target by using Dijkstra's Algorithm.
        # The cost returned from get_shortespath method is stored on the dictionary called 'costs'
        # where the key is, again, the cell number.
        # return:
        #   costs: dictionary.

        graph_dictionary = self.obtain_graph()
        size_x = self.size_x
        size_y = self.size_y
        costs = {}

        target_nr = size_x * self.target.x + self.target.y
        for key,value in graph_dictionary.items():
            costs[key] = self.get_shortestpath2(key, target_nr,graph_dictionary)

        return costs


    def get_shortestpath2(self, source, destination, graph_dictionary):

        # inputs: source = source Block cell number, destination = destination Block cell number, hence, Target number.
        # This method is used to calculate the shortest path from a source to a destination.
        # Cell numbers are used to obtain the x and y coordinates since numbers are given rowwise.
        # Costs from source to all other cells are stored in distance_costs cell.
        # if x and y are destination's coordinates, then, distance_costs[x][y] is the shortest path cost
        # from source to destination.
        # return: round(distance_costs[x][y], 2)

        distance_costs = []

        size_x = self.size_x
        size_y = self.size_y
        environment_array = self.environment_array

        for i in range(0, size_y):
            l = [math.inf] * size_x
            distance_costs.append(l)

        if int(source/size_x) >= 1:
            x = int(source / size_x)
            y = int(source % size_x)
        else:
            x = 0
            y = source

        distance_costs[x][y] = 0

        q = queue.PriorityQueue()
        q.put((0, source))

        unseen_cells = set()
        unseen_cells.add(source)

        visited_cells = set()

        while not(q.empty()):

            element = q.get()
            dist = element[0]
            cell = element[1]

            neighbors = graph_dictionary[cell]

            for neighbor in neighbors:

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

                if not(neighbor in unseen_cells):
                    unseen_cells.add(neighbor)
                    q.put((update_cost, neighbor))

            visited_cells.add(cell)

        if int(destination / size_x) >= 1:
            x = int(destination / size_x)
            y = int(destination % size_x)
        else:
            x = 0
            y = destination

        return round(distance_costs[x][y], 2)

























