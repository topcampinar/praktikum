import math
class ShortestPath:

    def __init__(self, environment_array, target):

        self.environment_array = environment_array
        self.target = target

    def obtain_graph(self):

        environment_array = self.environment_array
        target = self.target

        nr = 0
        graph_dictionary = {}
        size = len(environment_array)

        for i in range(0, size):
            for j in range(0, size):

                neighbor_list = {}

                if (i-1) >= 0:
                    if (j-1) >=0:
                        neighbor_nr = size * (i-1) + (j-1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    if (j+1) < size:
                        neighbor_nr = size * (i-1) + (j+1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    neighbor_nr = size * (i-1) + j
                    neighbor_list[neighbor_nr] = 1

                if (i+1) < size:
                    if (j-1) >=0:
                        neighbor_nr = size * (i+1) + (j-1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    if (j+1) < size:
                        neighbor_nr = size * (i+1) + (j+1)
                        neighbor_list[neighbor_nr] = math.sqrt(2)

                    neighbor_nr = size * (i+1) + j
                    neighbor_list[neighbor_nr] = 1


                if (j - 1) >= 0:
                    neighbor_nr = size * i + (j - 1)
                    neighbor_list[neighbor_nr] = 1

                if (j + 1) < size:
                    neighbor_nr = size * i + (j + 1)
                    neighbor_list[neighbor_nr] = 1

                graph_dictionary[nr] = neighbor_list
                nr = nr + 1

        return graph_dictionary

        #print(graph_dictionary)


    def get_path_costs(self):

        graph_dictionary = self.obtain_graph()
        size = len(self.environment_array)
        costs = {}

        target_nr = size * self.target.x + self.target.y
        for key,value in graph_dictionary.items():
            costs[key] = self.get_shortestpath(key, target_nr,graph_dictionary)

        return costs
        #costs[0] = self.get_shortestpath(0, self.target ,graph_dictionary)

    def get_shortestpath(self, source, destination, graph_dictionary):

        distance_costs = []
        size = len(self.environment_array)

        for i in range(0, size):
            distance_costs.append([])
            for j in range(0, size):
                distance_costs[i].append(math.inf)

        x = int(source / size)
        y = source % size

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
                x = int(neighbor / size)
                y = neighbor % size

                current_cost = distance_costs[x][y]
                update_cost = dist + neighbors[neighbor]

                if update_cost < current_cost:
                    distance_costs[x][y] = update_cost

                if neighbor not in visited_cells:
                    unseen_cells.append(neighbor)
                    unseen_cell_values.append(update_cost)

                visited_cells.append(cell)


        x = int(destination / size)
        y = destination % size

        return round(distance_costs[x][y], 2)
        #print(distance_costs)





























