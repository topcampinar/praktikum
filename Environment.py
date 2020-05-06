import sys
from Block import *
import math
from Target import *
from Pedestrian import *
from Obstacle import *
from ShortestPath import *
import copy

class Environment:

    """
    Environment(time, sx, sy, p, o, t, rmax)

    It is the class that is used to create Environment of the simulation.

    Attributes:

        size_x: int
            x coordinate of the Pedestrian on the simulation area.
        size_y: int
            y coordinate of the Pedestrian on the simulation area.
        pedestrian_list: list
            list that holds the Pedestrian objects created by the user.
        obstacle_list: list
            list that holds the Obstacle objects created by the user.
        target: Target
            target of the simulation area.
        block_list: list
            list of blocks (cells) in the simulation area.
        environment_array: list
            list that holds each object in their locations on the simulation area.
        block_costs: list
            cost of each cell determined by calculating the cost function for each cell to the target
        rmax: int
            pedestrian avoidance value.
        time: int
            time ticks requested for simulation run.

    Parameters:

        time: int
            time ticks requested for simulation run.
        sx: int
            x coordinate of the Pedestrian on the simulation area.
        sy: int
            y coordinate of the Pedestrian on the simulation area.
        p: list
            list that holds the Pedestrian objects created by the user.
        o: list
            list that holds the Obstacle objects created by the user.
        t: Target
            target of the simulation area.
        rmax: int
            pedestrian avoidance value.

    """

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
        # This method creates the environment by using the information provided by the user, such as
        # pedestrian locations, size of the simulation area, obstacle locations, target location.
        # A list is used to act like a row and hold the objects in their locations.
        # Another list acts as the environment itself and holds the lists that represent each row.
        # This list is called environment_array and is an attribute of the environment object.
        # This method is called when the simulation begins.

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


    def visualize_environment2(self):

        # This method is use to visualize the current situation of the environment.
        # Locations of pedestrians, obstacles and target on the simulation area can be seen.
        # Pedestrians are represented by 'P', obstacles are represented by 'O' and target is
        # represented by 'T'. Free cells are represented by '*'.
        # environment_array attribute of the Environment object holds the current situation
        # of the environment and this attribute is used for visualization. Visualization is
        # achieved by converting the environment_array to string and is printed on the console.

        size_x = self.size_x
        size_y = self.size_y
        environment_array = self.environment_array
        environment_structure = ""

        for i in range(0, size_x):
            for j in range(0, size_y):
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


    """
        MOVEMENT BY EUCLIDEAN DISTANCE.
    """

    def run_simulation(self):

        # This method is used to run the simulation with Euclidean Cost. Until the
        # required time is passed, or until every pedestrian reached to the target,
        # this method keeps running. In each iteration, in order to choose the next
        # location for the pedestrians, move_pedestrian method is called. Then, it
        # is checked whether the pedestrian reached to target or not. If yes, that
        # pedestrian is not moved anymore in later iterations. Also, the situation
        # of the environment after each iteratio is provided by calling the method
        # visualize_environment.

        pedestrians_reached = 0
        time = self.time
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
                arrived_list = []
                for i in range(0, len(not_arrived)):
                    p = not_arrived[i]
                    x = p.x
                    y = p.y

                    if x == tx:
                        if y == ty:
                            pedestrians_reached = pedestrians_reached + 1
                            #arrived_list.append(i)
                            arrived_list.append(p)

                for i in range(0, len(arrived_list)):
                    j = not_arrived.index(arrived_list[i])
                    not_arrived.pop(j)
        else:
            time_passed = 0
            while time_passed < time:
                print('Time ', time_passed)
                if pedestrians_reached < pedestrian_nr:

                    self.move_pedestrian(not_arrived)
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
                                arrived_list.append(p)

                    for i in range(0, len(arrived_list)):
                        j = not_arrived.index(arrived_list[i])
                        not_arrived.pop(j)
                else:
                    self.visualize_environment2()

                time_passed = time_passed + 1


    def move_pedestrian(self, pedestrian_list):

        # This method is used to choose the next location of the pedestrian based on
        # Euclidean distance. The idea is that, for each neighbor cell of pedestrian's
        # current cell, calculate the distance from that cell to target and whichever
        # cell has the least distance, the new x and y coordinates of the pedestrian
        # will be that cell's x and y coordinates. environment_array is updated based
        # on new coordinates.

        size_x = self.size_x
        size_y = self.size_y
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

            cost_for_pedestrian = []
            for i in range(0, size_y):
                l = [0] * size_x
                cost_for_pedestrian.append(l)
            avoidance_cost = self.update_pedestrian_avoidance_cost(p, cost_for_pedestrian)

            if not((x-1) < 0):
                b = environment_array[x-1][y]
                c = avoidance_cost[x-1][y]

                if isinstance(b, Target):
                    p.x = x-1
                    #environment_array[x - 1][y] = p
                    environment_array[x][y] = Block(x,y)
                    least_dist = 0
                    least_x = x-1
                    least_y = y
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y
                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y

                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y


                if not ((y-1) < 0):
                    b = environment_array[x - 1][y-1]
                    c = avoidance_cost[x - 1][y-1]
                    if isinstance(b, Target):
                        p.x = x - 1
                        p.y = y-1
                        environment_array[x][y] = Block(x, y)
                        least_dist = 0
                        least_x = x + 1
                        least_y = y
                        continue
                    elif isinstance(b, Block):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = b.x
                            least_y = b.y
                    elif isinstance(b, Obstacle):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = x
                            least_y = y

                if not ((y+1) >= size_y):
                    b = environment_array[x - 1][y+1]
                    c = avoidance_cost[x - 1][y+1]
                    if isinstance(b, Target):
                        p.x = x - 1
                        p.y = y+1
                        environment_array[x][y] = Block(x, y)
                        least_dist = 0
                        least_x = x + 1
                        least_y = y
                        continue
                    elif isinstance(b, Block):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = b.x
                            least_y = b.y
                    elif isinstance(b, Obstacle):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = x
                            least_y = y

            if not((x+1) >= size_x):
                b = environment_array[x+1][y]
                c = avoidance_cost[x + 1][y]

                if isinstance(b, Target):
                    p.x = x+1
                    #environment_array[x + 1][y] = p
                    environment_array[x][y] = Block(x,y)
                    least_dist = 0
                    least_x = x+1
                    least_y = y
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y
                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y

                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y

                if not ((y-1) < 0):
                    b = environment_array[x + 1][y-1]
                    c = avoidance_cost[x + 1][y-1]
                    if isinstance(b, Target):
                        p.x = x + 1
                        p.y = y-1
                        environment_array[x][y] = Block(x, y)
                        least_dist = 0
                        least_x = x + 1
                        least_y = y
                        continue
                    elif isinstance(b, Block):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = b.x
                            least_y = b.y
                    elif isinstance(b, Obstacle):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = x
                            least_y = y

                if not ((y+1) >= size_y):
                    b = environment_array[x + 1][y+1]
                    c = avoidance_cost[x + 1][y+1]
                    if isinstance(b, Target):
                        p.x = x + 1
                        p.y = y+1
                        environment_array[x][y] = Block(x, y)
                        least_dist = 0
                        least_x = x + 1
                        least_y = y
                        continue
                    elif isinstance(b, Block):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = b.x
                            least_y = b.y
                    elif isinstance(b, Obstacle):
                        d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2)) + c
                        if d < least_dist:
                            least_dist = d
                            least_x = x
                            least_y = y

            if not((y-1) < 0):
                b = environment_array[x][y-1]
                c = avoidance_cost[x][y-1]

                if isinstance(b, Target):
                    p.y = y-1
                    environment_array[x][y] = Block(x,y)
                    least_dist = 0
                    least_x = x
                    least_y = y-1
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y
                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y

                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y

            if not((y+1) >= size_y):
                b = environment_array[x][y+1]
                c = avoidance_cost[x][y + 1]

                if isinstance(b, Target):
                    p.y = y+1
                    environment_array[x][y] = Block(x,y)
                    least_dist = d
                    least_x = x
                    least_y = y+1
                    continue

                elif isinstance(b, Block):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = b.x
                        least_y = b.y
                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx - b.x), 2) + math.pow((ty - b.y), 2))
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y

                elif isinstance(b, Obstacle):
                    d = math.sqrt(math.pow((tx-b.x), 2) + math.pow((ty-b.y), 2)) + c
                    if d < least_dist:
                        least_dist = d
                        least_x = x
                        least_y = y

            if least_dist > 0:
                environment_array[x][y] = Block(x, y)
                p.x = least_x
                p.y = least_y
                environment_array[least_x][least_y] = p
        self.environment_array = environment_array


    """
        MOVEMENT BY USING A COST FUNCTION.
    """
    def get_dijkstra_costs(self):

        # Initial cost values for each cell based on the cost function that employs
        # Dijkstra algorithm. ShortestPath class contains the methods for calculating
        # the costs.
        # return: list in dimensions of the environment with the initial costs.

        sp = ShortestPath(self.environment_array, self.target)
        dijkstra_costs = sp.get_path_costs()
        return dijkstra_costs

    def assign_initial_costs(self):

        # This method is called when the simulation is run with cost function option.
        # Shortest path distance cost is calculated at the beginning of the simulation
        # and it is not changed during the simulation runtime. This method calls the
        # method get_dijkstra_costs in order to get the costs. Then, assigns those costs
        # to the attribute of the Environment object, that is, block_costs.
        # block_costs attribute of Environment object is used during simulation runtime
        # while determining the new location for the pedestrians.

        block_costs = []
        dijkstra_costs = self.get_dijkstra_costs()
        size_x = self.size_x
        size_y = self.size_y
        environment_array = self.environment_array

        for i in range(0, size_x):
            list = [0] * size_y
            block_costs.append(list)

        for dc in dijkstra_costs:
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

        # This method is used to determine the pedestrian avoidance cost during
        # simulation runtime. pedestrian_avoidance_cost method is called to get the
        # cost as the result of the avoidance function present on the exercise sheet.
        # Pedestrian avoidance costs are dependent on pedestrians' current locations
        # on the simulation area.
        # This cost may or may not affect cells. They are added to the initial cell
        # costs in each iteration for each pedestrian. a matrix-like list that holds
        # the final cost values is returned to be used in get_new_location2 method.
        # return: cost_for_pedestrian

        pedestrian_list = self.pedestrian_list
        nr_of_pedestrians = len(pedestrian_list)
        ind = pedestrian_list.index(pedestrian)
        size_x = self.size_x
        size_y = self.size_y
        rmax = self.rmax
        p = 0

        while p < nr_of_pedestrians:
            if p != ind:
                pedestrian2 = pedestrian_list[p]
                px = pedestrian2.x
                py = pedestrian2.y

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
        #print(cost_for_pedestrian)
        return cost_for_pedestrian

    def pedestrian_avoidance_cost(self, x1, x2, y1, y2):

        # This method calculates the avoidance cost function present on the exercise sheet
        # based on the two locations.
        # return: cost value calculated.

        rmax = self.rmax
        distance = math.sqrt(math.pow((x1-x2), 2) + math.pow((y1-y2), 2))
        cost = 0
        if distance < rmax:
            cost = math.exp(1 / (math.pow(distance, 2) - math.pow(rmax, 2)))
        return cost

    def get_new_location(self, block_costs, pedestrian):

        # This method is to determine the new location for a pedestrian based on its
        # neighbor cells and the cell costs. The cell with the least cost is selected.
        # Obstacle cells and the cells with a pedestrian cannot be selected.
        # return: x and y coordinates for moving.

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

        if least_cost == math.inf:
            cost = block_costs[i][j]
            if cost < least_cost:
                least_cost = cost
                newx = i
                newy = j

        return newx, newy

    def move_pedestrian_with_cost(self, pedestrian_list):

        # This method is called for run_simulation2 method, to move each non-arrived
        # pedestrian in one time tick. In order to select the new location for the
        # pedestrians, get_new_location method is called. The coordinates returned by
        # the method is used to update the pedestrian's location. Environment object's
        # attribute environment_array is also updated since one pedestrian changed its
        # location.
        # return: pedestrian list with the updated coordinates.

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
            if not isinstance(environment_array[newx][newy], Target):
                environment_array[newx][newy] = p

        self.environment_array = environment_array
        return pedestrian_list

    def run_simulation2(self):

        # This method is used when there is no speed and there is cost function instead
        # of Euclidean distance. First assign_initial_costs method is called to determine
        # the cell costs based on Dijkstra algorithm shortest paths.
        # Then, until the time limit is reached, or until every pedestrian arrives to the
        # target, move_pedestrian_with cost is called to move the pedestrian for one cell.
        # then the list of pedestrians who moved are obtained. After each iteration, the
        # environment is visualized on the console by calling visualize_environment method.

        pedestrians_reached = 0
        time = self.time
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
                            arrived_list.append(i)

                for i in range(0, len(arrived_list)):
                    not_arrived.pop(arrived_list[i])
        else:
            time_passed = 0
            while time_passed < time:
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
                                arrived_list.append(i)

                    for i in range(0, len(arrived_list)):
                        not_arrived.pop(arrived_list[i])
                else:
                    self.visualize_environment2()

                time_passed = time_passed + 1

    """
        MOVE WITH SPEED ON CELLS WITH DEFINED CELL SIZES. 
    """

    def get_new_location2(self, block_costs, pedestrian):

        # This method is used to determine the next location for a pedestrian
        # based on costs of cells. Also, cell type is returned, that is used
        # to determine whether the pedestrian moved diagonally or straightly.
        # cell type is 0 if the pedestrian moved straightly, and 1 otherwise.
        # return: x and y coordinates of the next location and the cell type

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

        if least_cost == math.inf:
            cost = block_costs[i][j]
            if cost < least_cost:
                least_cost = cost
                newx = i
                newy = j

        return newx, newy, cell_type


    def move_pedestrian_with_speed(self, pedestrian_list, cellsize, pedestrians_reached):

        # This method is used when the speed of the pedestrians are important in the simulation.
        # this method moves the pedestrians that are not arrived to target yet for one second.
        # Now, cell sizes are also important. Our cell sizes are 40 centimeters.
        # Each pedestrian has a movement limit in one second, that is (speed * 100) centimeters.
        # If a pedestrian reaches to the target before before one second finishes, it does not
        # move anymore.
        # after each movement, pedestrians location is updated and environment_array is also
        # updated.
        # return: not arrived pedestrians at the end of this second, and arrived pedestrians
        # before the second finishes.


        environment_array = self.environment_array
        block_costs = copy.deepcopy(self.block_costs)
        tx = self.target.x
        ty = self.target.y
        pedestrians_completed = 0
        pedestrian_nr = len(pedestrian_list)
        for p in pedestrian_list:
            p.meters = 0
        nr = 0
        not_arrived = pedestrian_list
        while ((pedestrians_completed < pedestrian_nr) and len(not_arrived) > 0):
            for p in not_arrived:
                speed = p.speed * 100
                if p.meters < speed:
                    nr = nr + 1
                    x = p.x
                    y = p.y
                    speed = p.speed * 100

                    i = self.pedestrian_list.index(p)

                    costs_for_pedestrian = self.update_pedestrian_avoidance_cost(p, block_costs)
                    newx, newy, cell_type = self.get_new_location2(costs_for_pedestrian, p)
                    environment_array[x][y] = Block(x, y)
                    p.x = newx
                    p.y = newy

                    if p.owed > 0:
                        p.meters = p.meters - p.owed
                        p.owed = 0

                    if cell_type == 0:
                        if speed-p.meters < cellsize:
                            p.owed = speed-p.meters
                            pedestrians_completed += 1
                            p.meters = speed
                        else:
                            p.meters += cellsize

                    else:
                        diagonal_cell_size = round(cellsize * math.sqrt(2), 2)
                        if speed-p.meters < diagonal_cell_size:
                            p.owed = speed-p.meters
                            pedestrians_completed += 1
                            p.meters = speed
                        else:
                            p.meters += diagonal_cell_size

                    self.pedestrian_list[i].x = newx
                    self.pedestrian_list[i].y = newy
                    self.pedestrian_list[i].owed = p.owed
                    self.pedestrian_list[i].meters = p.meters

                    if not isinstance(environment_array[newx][newy], Target):
                        environment_array[newx][newy] = p

            arrived_list = []
            for i in range(0, len(not_arrived)):
                p = not_arrived[i]
                x = p.x
                y = p.y
                if x == tx:
                    if y == ty:
                        arrived_list.append(i)

            for i in range(0, len(arrived_list)):
                 if len(not_arrived) > 0:
                    not_arrived.pop(arrived_list[i])
                    pedestrian_nr = pedestrian_nr - 1
                    pedestrians_reached = pedestrians_reached + 1

        self.environment_array = environment_array
        self.visualize_environment2()
        return not_arrived, pedestrians_reached

    def run_simulation3(self):

        # This method is used when the speed of pedestrians are important in simulation.
        # First, cell costs are assigned by calling assign_initial_costs method that uses
        # Dijkstra's algorithm for determining the cell costs.
        # Then, until the time limit is reached, or all the pedestrians reach to the target
        # this method calls move_pedestrian_with_speed method to determine the next location
        # after one second.
        # After each second, the structure of the environment is visualized.

        pedestrians_reached = 0
        time = self.time

        pedestrian_list = self.pedestrian_list
        obstacle_list = self.obstacle_list
        target = self.target
        environment_array = self.environment_array
        pedestrian_nr = len(pedestrian_list)

        not_arrived = pedestrian_list
        self.assign_initial_costs()
        nr = 0

        if time == None:
            while pedestrians_reached < pedestrian_nr:
                not_arrived, pedestrians_reached = self.move_pedestrian_with_speed(not_arrived, 40, pedestrians_reached)
                print('Number of pedestrians reached::  ', pedestrians_reached)
                tx = target.x
                ty = target.y
                nr = nr + 1
        else:
            while nr < time:
                while pedestrians_reached < pedestrian_nr:
                    not_arrived, pedestrians_reached = self.move_pedestrian_with_speed(not_arrived, 40,  pedestrians_reached)
                    print('Number of pedestrians reached::  ', pedestrians_reached)
                    tx = target.x
                    ty = target.y
                    nr = nr + 1

        print('Seconds after all pedestrians reached :: ', nr)

