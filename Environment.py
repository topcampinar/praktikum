import sys
from Block import *
import math
from Target import *
from Pedestrian import *
from Obstacle import *
from ShortestPath import *
import copy

class Environment:

    def __init__(self, s, p, o, t, rmax):

        self.size = s
        self.pedestrian_list = p
        self.obstacle_list = o
        self.target = t
        self.block_list = []
        self.environment_array = []
        self.block_costs = []
        self.rmax = rmax

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
        #self.run_simulation()
        self.run_simulation2()



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


    def get_dijkstra_costs(self):

        sp = ShortestPath(self.environment_array, self.target)
        dijkstra_costs = sp.get_path_costs()
        return dijkstra_costs


    def assign_initial_costs(self):

        block_costs = []
        dijkstra_costs = self.get_dijkstra_costs()
        size = self.size
        environment_array = self.environment_array

        for i in range(0, size):
            list = [0] * size
            block_costs.append(list)

        for dc in dijkstra_costs:
            x = int(dc / size)
            y = dc % size

            if isinstance(environment_array[x][y], Obstacle):
                block_costs[x][y] = math.inf
            else:
                block_costs[x][y] = dijkstra_costs[dc]

        self.block_costs = block_costs

    def update_pedestrian_avoidance_cost(self, pedestrian, cost_for_pedestrian):

        pedestrian_list = self.pedestrian_list
        nr_of_pedestrians = len(pedestrian_list)
        ind = pedestrian_list.index(pedestrian)
        size = self.size
        rmax = self.rmax
        #cost_for_pedestrian = self.block_costs.copy()
        p = 0

        while p < nr_of_pedestrians:
            if p != ind:
                pedestrian2 = pedestrian_list[p]
                px = pedestrian2.x
                py = pedestrian2.y
                #avoidance_cost = self.pedestrian_avoidance_cost(pedestrian.x, pedestrian2.x, pedestrian.y, pedestrian2.y)
                #old_cost = cost_for_pedestrian[pedestrian2.x][pedestrian2.y]
                #cost_for_pedestrian[pedestrian2.x][pedestrian2.y] = old_cost + avoidance_cost

                for i in range(0, size):
                    for j in range(0, size):
                        d = math.sqrt(math.pow((i-px), 2) + math.pow((j-py), 2))
                        if d < rmax:
                            avoidance_cost = self.pedestrian_avoidance_cost(i, px, j, py)
                            old_cost = cost_for_pedestrian[i][j]
                            cost_for_pedestrian[i][j] = old_cost + avoidance_cost
                        if px == i:
                            if py == j:
                                cost_for_pedestrian[i][j] = math.inf
            p = p + 1
        return cost_for_pedestrian


    def pedestrian_avoidance_cost(self, x1, x2, y1, y2):

        rmax = self.rmax
        distance = math.sqrt(math.pow((x1-x2), 2) + math.pow((y1-y2), 2))
        cost = 0
        if distance < rmax:
            cost = math.exp(1 / (math.pow(distance, 2) - math.pow(rmax, 2)))
        return cost

    def get_new_location(self, block_costs, pedestrian):

        i = pedestrian.x
        j = pedestrian.y
        least_cost = math.inf
        newx = i
        newy = j
        size = self.size
        #print(block_costs)

        if (i - 1) >= 0:
            if (j - 1) >= 0:
                cost = block_costs[i - 1][j - 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i - 1
                    newy = j - 1

            if (j + 1) < size:
                cost = block_costs[i - 1][j + 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i - 1
                    newy = j + 1

            cost = block_costs[i - 1][j]
            if cost < least_cost:
                least_cost = cost
                newx = i - 1
                newy = j

        if (i + 1) < size:
            if (j - 1) >= 0:
                cost = block_costs[i + 1][j - 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i + 1
                    newy = j - 1

            if (j + 1) < size:
                cost = block_costs[i + 1][j + 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i + 1
                    newy = j + 1

            cost = block_costs[i + 1][j]
            if cost < least_cost:
                least_cost = cost
                newx = i + 1
                newy = j

        if (j - 1) >= 0:
            cost = block_costs[i][j - 1]
            if cost < least_cost:
                least_cost = cost
                newx = i
                newy = j - 1

        if (j + 1) < size:
            cost = block_costs[i][j + 1]
            if cost < least_cost:
                least_cost = cost
                newx = i
                newy = j + 1

        cost = block_costs[i][j]
        if cost < least_cost:
            least_cost = cost
            newx = i
            newy = j

        return newx, newy


    def move_pedestrian_with_cost(self, pedestrian_list):

        environment_array = self.environment_array
        block_costs = copy.deepcopy(self.block_costs)
        for p in pedestrian_list:
            x = p.x
            y = p.y

            costs_for_pedestrian = self.update_pedestrian_avoidance_cost(p, block_costs)
            newx, newy = self.get_new_location(costs_for_pedestrian, p)
            environment_array[x][y] = Block(x, y)
            p.x = newx
            p.y = newy
            i = self.pedestrian_list.index(p)
            self.pedestrian_list[i].x = newx
            self.pedestrian_list[i].y = newy
            environment_array[newx][newy] = p

        self.environment_array = environment_array
        return pedestrian_list

    def run_simulation2(self):
        pedestrians_reached = 0

        size = self.size
        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        environment_array = self.environment_array

        pedestrian_nr = len(pedestrian_list)
        not_arrived = pedestrian_list
        self.assign_initial_costs()
        while pedestrians_reached < pedestrian_nr:
            not_arrived = self.move_pedestrian_with_cost(not_arrived)

            self.visualize_environment2()

            tx = target.x
            ty = target.y

            arrived_list = []
            for i in range(0, len(not_arrived)):
                p = not_arrived[i]
                x = p.x
                y = p.y

                if x == tx:
                    if y == ty:
                        pedestrians_reached = pedestrians_reached + 1
                        #not_arrived.pop(i)
                        arrived_list.append(i)

            for i in range(0, len(arrived_list)):
                not_arrived.pop(arrived_list[i])



