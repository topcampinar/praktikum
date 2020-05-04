import sys
from Block import *
import math
from Target import *
from Pedestrian import *
from Obstacle import *
from ShortestPath import *
import copy

class Environment:

    def __init__(self, time, sx, sy, p, o, t, rmax):

        self.size_x = sy
        self.size_y = sx
        self.pedestrian_list = p
        self.obstacle_list = o
        self.target = t
        self.block_list = []
        self.environment_array = []
        self.block_costs = []
        self.rmax = rmax
        if time > 0:
            self.time = time
        else:
            self.time = None

    def create_environment(self):

        size_x = self.size_x
        size_y = self.size_y
        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        block_list = self.block_list
        environment_array = self.environment_array

        for i in range(0, size_x):
            environment_array.append([])
            for j in range(0, size_y):
                b = Block(i,j)
                block_list.append(b)
                environment_array[i].append(b)

        environment_array[target.x][target.y] = target

        for o in obstacle_list:
            environment_array[o.x][o.y] = o

        for p in pedestrian_list:
            environment_array[p.x][p.y] = p


        self.visualize_environment2()
        #self.run_simulation()
        #self.run_simulation2()



    def run_simulation(self):
        pedestrians_reached = 0
        time = self.time
        #size = self.size
        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        environment_array = self.environment_array

        pedestrian_nr = len(pedestrian_list)
        not_arrived = pedestrian_list

        if time == None:
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
        else:
            time_passed = 0
            while time_passed < time:
                print('Time ', time_passed)
                if pedestrians_reached < pedestrian_nr:

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
                else:
                    self.visualize_environment2()

                time_passed = time_passed + 1




    def move_pedestrian(self, pedestrian_list):

        size_x = self.size_x
        size_y = self.size_y
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

            if not((x+1) >= size_x):
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


            if not((y+1) >= size_y):
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

        size_x = self.size_x
        size_y = self.size_y
        environment_array = self.environment_array
        environment_structure = ""

        for i in range(0, size_x):
            for j in range(0, size_y):
                #b = environment_array[i][j]
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
        size_x = self.size_x
        size_y = self.size_y
        environment_array = self.environment_array

        for i in range(0, size_x):
            list = [0] * size_y
            block_costs.append(list)

        for dc in dijkstra_costs:
            #x = int(dc / size)
            #y = dc % size
            if int(dc / size_y) >= 1:
                x = int(dc / size_y)
                y = int(dc % size_y)
            else:
                x = 0
                y = dc

            if isinstance(environment_array[x][y], Obstacle):
                block_costs[x][y] = math.inf
            else:
                block_costs[x][y] = dijkstra_costs[dc]

        self.block_costs = block_costs

    def update_pedestrian_avoidance_cost(self, pedestrian, cost_for_pedestrian):

        pedestrian_list = self.pedestrian_list
        nr_of_pedestrians = len(pedestrian_list)
        ind = pedestrian_list.index(pedestrian)
        size_x = self.size_x
        size_y = self.size_y
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

                for i in range(0, size_x):
                    for j in range(0, size_y):
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
        size_x = self.size_x
        size_y = self.size_y
        if (i - 1) >= 0:
            if (j - 1) >= 0:
                cost = block_costs[i - 1][j - 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i - 1
                    newy = j - 1

            if (j + 1) < size_y:
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

        if (i + 1) < size_x:
            if (j - 1) >= 0:
                cost = block_costs[i + 1][j - 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i + 1
                    newy = j - 1

            if (j + 1) < size_y:
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

        if (j + 1) < size_y:
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
            print('old:',x , y)
            costs_for_pedestrian = self.update_pedestrian_avoidance_cost(p, block_costs)
            newx, newy = self.get_new_location(costs_for_pedestrian, p)
            environment_array[x][y] = Block(x, y)
            p.x = newx
            p.y = newy
            print('new: ', p.x, p.y)
            i = self.pedestrian_list.index(p)
            self.pedestrian_list[i].x = newx
            self.pedestrian_list[i].y = newy
            environment_array[newx][newy] = p

        self.environment_array = environment_array
        return pedestrian_list

    def run_simulation2(self):
        pedestrians_reached = 0
        time = self.time
        #size = self.size
        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        environment_array = self.environment_array

        pedestrian_nr = len(pedestrian_list)
        not_arrived = pedestrian_list
        self.assign_initial_costs()
        if time == None:
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
        else:
            time_passed = 0
            while time_passed < time:
                print("Time ", time_passed)
                if pedestrians_reached < pedestrian_nr:
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
                else:
                    self.visualize_environment2()

                time_passed = time_passed + 1

    def move_pedestrian_with_speed(self, pedestrian_list, cellsize, pedestrians_reached):
        environment_array = self.environment_array
        block_costs = copy.deepcopy(self.block_costs)
        tx = self.target.x
        ty = self.target.y
        bitiren_insanlar = 0
        insan_sayisi = len(pedestrian_list)
        for p in pedestrian_list:
            p.meters = 0
        nr = 0
        not_arrived = pedestrian_list
        while ((bitiren_insanlar < insan_sayisi) and len(not_arrived) > 0):
            for p in not_arrived:
                speed = p.speed * 100
                if p.meters < speed:
                    nr = nr + 1
                    print('metreeeeee ', p.meters)
                    x = p.x
                    y = p.y

                    speed = p.speed * 100
                    print('speed', speed)

                    cells_walked = p.meters
                    #stepsize = int(speed / cellsize)  # calculate number of steps for pedestrian
                    steps_owed = p.owed
                    newx, newy = x, y
                    i = self.pedestrian_list.index(p)

                    #for j in range(stepsize):  # loop tamamlanınca 1 sn olucak
                    costs_for_pedestrian = self.update_pedestrian_avoidance_cost(p, block_costs)
                    newx, newy, cell_type = self.get_new_location2(costs_for_pedestrian, p)
                    print(newx, newy)
                    environment_array[x][y] = Block(x, y)
                    p.x = newx
                    p.y = newy

                    if p.owed > 0:
                        p.meters = p.meters - p.owed
                        print('p owed', p.owed)
                        p.owed = 0
                        print('p meters', p.meters)

                    if cell_type == 0:
                        if speed-p.meters < cellsize:
                            p.owed = speed-p.meters
                            bitiren_insanlar += 1
                            p.meters = speed
                            print('bitti? 1')
                            print('p meters', p.meters)

                        else:
                            p.meters += cellsize
                            print('p meters', p.meters)

                    else:
                        diagonal_cell_size = round(cellsize * math.sqrt(2), 2)
                        if speed-p.meters < diagonal_cell_size:
                            p.owed = speed-p.meters
                            bitiren_insanlar += 1
                            p.meters = speed
                            print('bitti? 2')
                            print('p meters', p.meters)
                        else:
                            p.meters += diagonal_cell_size
                            print('p meters', p.meters)

                    self.pedestrian_list[i].x = newx
                    self.pedestrian_list[i].y = newy
                    self.pedestrian_list[i].owed = p.owed
                    self.pedestrian_list[i].meters = p.meters
                    #self.pedestrian_list[i].meters = cells_walked

                    environment_array[newx][newy] = p

            arrived_list = []
            for i in range(0, len(not_arrived)):
                p = not_arrived[i]
                x = p.x
                y = p.y

                if x == tx:
                    if y == ty:
                        # not_arrived.pop(i)
                        arrived_list.append(i)


            for i in range(0, len(arrived_list)):
                 if len(not_arrived) > 0:
                    not_arrived.pop(arrived_list[i])
                    insan_sayisi = insan_sayisi - 1
                    pedestrians_reached = pedestrians_reached + 1

            #print('arrived:::', arrived_list)
            #print('bitiren insanlar', bitiren_insanlar)
            #print('insan sayisi', insan_sayisi)
            #print('not arrived ', not_arrived)


        print('kac kez döndü ', nr)
        self.environment_array = environment_array
        self.visualize_environment2()
        return not_arrived, pedestrians_reached

    def run_simulation3(self):
        pedestrians_reached = 0

        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        environment_array = self.environment_array
        #arrived_list = []
        pedestrian_nr = len(pedestrian_list)
        not_arrived = pedestrian_list  # all pedestrians varmadı
        self.assign_initial_costs()  # dijkstra costları
        nr = 0
        while pedestrians_reached < pedestrian_nr:  # targeta ulaşmamaış insanalr

            not_arrived, pedestrians_reached = self.move_pedestrian_with_speed(not_arrived, 40, pedestrians_reached)  # bu 1 adım bir sn TEK ADIM

            tx = target.x
            ty = target.y

            #arrived_list = []
            #for i in range(0, len(not_arrived)):
            #    p = not_arrived[i]
            #    x = p.x
            #    y = p.y

            #    if x == tx:
            #        if y == ty:
            #            pedestrians_reached = pedestrians_reached + 1
                        # not_arrived.pop(i)
            #            arrived_list.append(i)

            #for i in range(0, len(arrived_list)):
            #    not_arrived.pop(arrived_list[i])
            print('pedestrians_reached::  ', pedestrians_reached)
            print('not_arrived. ', not_arrived)
            nr = nr + 1
        print('Kac sn????', nr)


    def get_new_location2(self, block_costs, pedestrian):

        i = pedestrian.x
        j = pedestrian.y
        least_cost = math.inf
        newx = i
        newy = j
        size_x = self.size_x
        size_y = self.size_y

        cell_type = 0
        if (i - 1) >= 0:
            if (j - 1) >= 0:
                cost = block_costs[i - 1][j - 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i - 1
                    newy = j - 1
                    cell_type = 1

            if (j + 1) < size_y:
                cost = block_costs[i - 1][j + 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i - 1
                    newy = j + 1
                    cell_type = 1


            cost = block_costs[i - 1][j]
            if cost < least_cost:
                least_cost = cost
                newx = i - 1
                newy = j

        if (i + 1) < size_x:
            if (j - 1) >= 0:
                cost = block_costs[i + 1][j - 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i + 1
                    newy = j - 1
                    cell_type = 1

            if (j + 1) < size_y:
                cost = block_costs[i + 1][j + 1]
                if cost < least_cost:
                    least_cost = cost
                    newx = i + 1
                    newy = j + 1
                    cell_type = 1

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

        if (j + 1) < size_y:
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

        return newx, newy, cell_type

