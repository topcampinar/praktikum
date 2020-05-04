import sys
from Obstacle import *
from Pedestrian import *
from Target import *
from Environment import *


def main():

    get_model_environment()

def get_model_environment():

    sys.stdout.write("Hello! Welcome to our simulation. The instructions below are designed to have an interactive "
                     "simulation process.\n\nAfter you read the instructions, please type 'ok' to continue.\n\n"
                     "First, ypu have to indicate the environment area. Please type the length of cell size after "
                     "you are asked.\n\nThen, please indicate the target location with a space between. (ex: '25 25') "
                     "after you are asked. \n\nAfter that, please indicate the location of obstacles OR pedestrians as "
                     "stated below. \n\n\nFor obstacles: 'o x y', where x and y indicate the x and y coordinate "
                     "locations, from 0 until cell size you provided (that is excluded.).\n\n\n"
                     "For pedestrians: 'p x y', where x and y indicate the x and y coordinate locations.\n\n"
                     "When you are done, please write 'exit'. Thank you!\n\n")

    time = int(input("Please enter the simulation run time. (Ex: 25) If there is no specific time requirement, please write 0.\n"))

    mode = int(input( "Please enter the simulation mode. Write 0 for simulation by using Eucledian Distance, and Write 1 for imulation by using a cost function. \n"))

    while not(mode == 1 or mode == 0):
        sys.stdout.write("Invalid mode.")
        mode = int(input("Please enter the simulation mode. Write 0 for simulation by using Eucledian Distance, and Write 1 for imulation by using a cost function. \n"))

    size_x = int(input("Please indicate the width of the area\n"))

    size_y = int(input("Please indicate the height of the area\n"))

    target = input("\nPlease indicate the target location with a space between. (ex: '25 25')\n")

    rmax = int(input("\nPlease indicate the minimum distance between pedestrians for pedestrian avoidance.\n"))

    sys.stdout.write("\nPlease indicate the location of obstacles OR pedestrians as stated below, with locations, from "
                     "0 until cell size you provided (that is excluded.)\n\nFor obstacles: 'o x y'"
                     ", where x and y indicate the x and y coordinate locations.\nFor pedestrians: 'p x y', where x and "
                     "y indicate the x and y coordinate locations.\n\n"
                     "If you want to add objects from txt file, please write 'text' and the name of the file as 'example.txt'\n\n"
                     "When you are done, please write 'exit'\n\n")

    target.strip()
    i = target.index(" ")
    x = int(target[0:i])
    y = int(target[i + 1:])
    #target = Target(x,y)
    target = Target(y,x)

    obstacle_list = []
    pedestrian_list = []

    while True:
        req = input("Please enter the request.")
        req.strip()
        if req == "exit":
            sys.stdout.write("\n")
            break
        elif req == "text":
            read_from_file(pedestrian_list, obstacle_list, size_x, size_y)
        elif not(any(i in ["o", "p"] for i in ["o", "p"])):
                sys.stdout.write("Invalid object.")
        else:
            add_to_map(req, size_x, size_y, obstacle_list, pedestrian_list)

    init_simulation(time, size_x, size_y, pedestrian_list, obstacle_list, target, rmax, mode)

def read_from_file(pedestrian_list, obstacle_list, size_x, size_y):
    while True:
        filename = input("Please enter the path of text file. (ex: 'example.txt'). \n"
                         "If you want to exit text mode please write 'q'. \n")
        if filename == "q":
            break
        try:
            with open(filename) as file_in:
                for line in file_in:
                    line.strip()
                    add_to_map(line, size_x, size_y, obstacle_list, pedestrian_list)
            sys.stdout.write("Objects are successfully read from the file.")
            break
        except FileNotFoundError:
            sys.stdout.write("Invalid file path.")

def add_to_map(req, size_x, size_y, obstacle_list, pedestrian_list):
    i1 = req.index(" ")
    i2 = req.index(" ", i1 + 1)

    x = int(req[i1 + 1:i2])
    y = int(req[i2 + 1:])

    if x >= size_x or y >= size_y or x < 0 or y < 0:
        sys.stdout.write("Invalid location.")
    else:
        if "o" in req:
            # o = Obstacle(x, y)
            o = Obstacle(y, x)
            obstacle_list.append(o)
        elif "p" in req:
            p = Pedestrian(y, x)
            pedestrian_list.append(p)

def init_simulation(time, sx, sy, p, o, t, rmax, mode):

    simulation_environment = Environment(time, sx, sy, p, o, t, rmax)
    simulation_environment.create_environment()
    if mode == 0:
        simulation_environment.run_simulation()
    elif mode == 1:
        simulation_environment.run_simulation3()
        #simulation_environment.run_simulation2()
    #simulation_environment.get_dijkstra_costs()


if __name__ == '__main__':
    main()