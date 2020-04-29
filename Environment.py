import sys
from Block import *
import math
from Target import *
from Pedestrian import *
from Obstacle import *
from ShortestPath import *

class Environment:

    def __init__(self, s, p, o, t):

        self.size = s
        self.pedestrian_list = p
        self.obstacle_list = o
        self.target = t
        self.block_list = []
        self.environment_array = []

    def create_environment(self):

        size = self.size
        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        block_list = self.block_list
        environment_array = self.environment_array

        for i in range(0, size):
            environment_array.append([])
            for j in range(0, size):
                b = Block(i,j)
                block_list.append(b)
                environment_array[i].append(b)

        environment_array[target.x][target.y] = target

        for o in obstacle_list:
            environment_array[o.x][o.y] = o

        for p in pedestrian_list:
            environment_array[p.x][p.y] = p

        print(environment_array)

        self.visualize_environment2()
        self.run_simulation()



    def run_simulation(self):
        pedestrians_reached = 0

        size = self.size
        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        environment_array = self.environment_array

        pedestrian_nr = len(pedestrian_list)
        not_arrived = pedestrian_list

        while pedestrians_reached < pedestrian_nr:

            self.move_pedestrian(not_arrived)
            self.visualize_environment2()

            tx = target.x
            ty = target.y
            for i in range(0, len(not_arrived)):
                p = not_arrived[i]
                x = p.x
                y = p.y

                if x == tx:
                    if y == ty:
                        pedestrians_reached = pedestrians_reached + 1
                        not_arrived.pop(i)




    def move_pedestrian(self, pedestrian_list):

        size = self.size
        #pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        environment_array = self.environment_array
        tx = target.x
        ty = target.y
        for p in pedestrian_list:

            x = p.x
            y = p.y

            least_dist = 9999999999
            least_x = -1
            least_y = -1

            if not((x-1) < 0):
                b = environment_array[x-1][y]

                if isinstance(b, Target):
                    p.x = x-1
                    #environment_array[x - 1][y] = p
                    environment_array[x][y] = Block(x,y)
                    least_dist = 0
                    least_x = x-1
                    least_y = y
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y

            if not((x+1) >= size):
                b = environment_array[x+1][y]

                if isinstance(b, Target):
                    p.x = x+1
                    #environment_array[x + 1][y] = p
                    environment_array[x][y] = Block(x,y)
                    least_dist = 0
                    least_x = x+1
                    least_y = y
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y

            if not((y-1) < 0):
                b = environment_array[x][y-1]

                if isinstance(b, Target):
                    p.y = y-1
                    #environment_array[x][y-1] = p
                    environment_array[x][y] = Block(x,y)
                    least_dist = 0
                    least_x = x
                    least_y = y-1
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y


            if not((y+1) >= size):
                b = environment_array[x][y+1]

                if isinstance(b, Target):
                    p.y = y+1
                    #environment_array[x][y+1] = p
                    environment_array[x][y] = Block(x,y)
                    least_dist = d
                    least_x = x
                    least_y = y+1
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y


            if least_dist > 0:
                environment_array[x][y] = Block(x, y)
                p.x = least_x
                p.y = least_y
                environment_array[least_x][least_y] = p

        self.environment_array = environment_array


    def visualize_environment2(self):

        size = self.size
        environment_array = self.environment_array
        environment_structure = ""

        for i in range(0, size):
            for j in range(0, size):
                b = environment_array[i][j]
                if isinstance(b, Block):
                    environment_structure = environment_structure + "*"
                elif isinstance(b, Obstacle):
                    environment_structure = environment_structure + "O"
                elif isinstance(b, Pedestrian):
                    environment_structure = environment_structure + "P"
                elif isinstance(b, Target):
                    environment_structure = environment_structure + "T"
            environment_structure = environment_structure + "\n"

        print(environment_structure)


    def get_shortest_path(self):

        sp = ShortestPath(self.environment_array, self.target)
        sp.obtain_graph()



