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

    size = int(input("Please indicate the area length (e.g. 7 for 7x7 cell space)\n"))

    target = input("\nPlease indicate the target location with a space between. (ex: '25 25')\n")

    rmax = int(input("\nPlease indicate the minimum distance between pedestrians for pedestrian avoidance.\n"))

    sys.stdout.write("\nPlease indicate the location of obstacles OR pedestrians as stated below, with locations, from "
                     "0 until cell size you provided (that is excluded.)\n\nFor obstacles: 'o x y'"
                     ", where x and y indicate the x and y coordinate locations.\nFor pedestrians: 'p x y', where x and "
                     "y indicate the x and y coordinate locations.\n\n"
                     "When you are done, please write 'exit'\n\n")

    target.strip()
    i = target.index(" ")
    x = int(target[0:i])
    y = int(target[i + 1:])
    target = Target(x,y)

    obstacle_list = []
    pedestrian_list = []

    while True:
        req = input("Please enter the request.")
        req.strip()
        if req == "exit":
            sys.stdout.write("\n")
            break
        elif not(any(i in ["o", "p"] for i in ["o", "p"])):
                sys.stdout.write("Invalid object.")
        else:
            i1 = req.index(" ")
            i2 = req.index(" ", i1 + 1)

            x = int(req[i1 + 1:i2])
            y = int(req[i2 + 1:])

            if x >= size or y >= size or x < 0 or y < 0:
                sys.stdout.write("Invalid location.")
            else:
                if "o" in req:
                    o = Obstacle(x, y)
                    obstacle_list.append(o)
                elif "p" in req:
                    p = Pedestrian(x, y)
                    pedestrian_list.append(p)

    init_simulation(size, pedestrian_list, obstacle_list, target, rmax)

def init_simulation(s, p, o, t, rmax):

    simulation_environment = Environment(s, p, o, t, rmax)
    simulation_environment.create_environment()
    simulation_environment.get_dijkstra_costs()


if __name__ == '__main__':
    main()
