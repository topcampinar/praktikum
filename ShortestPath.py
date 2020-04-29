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

        print(graph_dictionary)