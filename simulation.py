import sys
from Obstacle import *
from Pedestrian import *
from Target import *
from Environment import *
import random

def main():

    get_model_environment()

def get_model_environment():

    # This method is used to get the input from the user interactively to create the simulation environment.
    # in order to run the program, the user can type python3 simulation.py in command line, or
    # %run simulation.py inside a jupyter notebook that is created in the same directory as this project.
    # After obtaining the user input, method creates the Pedestrians, Obstacles, Target objects,
    # and calls init_simulation method to initialize the simulation.

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

    speed_or_not = int(input("Please type 0 for simulation without speed involved. Else, type 1.\n"))

    if not speed_or_not:
        mode = int(input( "Please enter the simulation mode. Write 0 for simulation by using Eucledian Distance, and Write 1 for simulation by using a cost function. \n"))


        while not(mode == 1 or mode == 0):
            sys.stdout.write("Invalid mode.")
            mode = int(input("Please enter the simulation mode. Write 0 for simulation by using Eucledian Distance, and Write 1 for simulation by using a cost function. \n"))

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
                read_from_file(pedestrian_list, obstacle_list, size_x, size_y, 1)
            elif not(any(i in ["o", "p"] for i in ["o", "p"])):
                sys.stdout.write("Invalid object.")
            else:
                add_to_map(req, size_x, size_y, obstacle_list, pedestrian_list)
    else:
        mode = 1
        size_x = int(input("Please indicate the width of the area\n"))

        size_y = int(input("Please indicate the height of the area\n"))

        target = input("\nPlease indicate the target location with a space between. (ex: '25 25')\n")

        target.strip()
        i = target.index(" ")
        x = int(target[0:i])
        y = int(target[i + 1:])
        target = Target(y,x)

        rmax = int(input("\nPlease indicate the minimum distance between pedestrians for pedestrian avoidance.\n"))

        default_speed_not = int(input("\nDefault pedestrian speed is 1.33 m/s. Please type 0 for manual speed input for pedestrians. Else, type 1.\n"))

        if default_speed_not:
            sys.stdout.write(
                "\nPlease indicate the location of obstacles OR pedestrians as stated below, with locations, from "
                "0 until cell size you provided (that is excluded.)\n\nFor obstacles: 'o x y'"
                ", where x and y indicate the x and y coordinate locations.\nFor pedestrians: 'p x y', where x and "
                "y indicate the x and y coordinate locations.\n\n"
                "If you want to add objects from txt file, please write 'text' and the name of the file as 'example.txt'\n\n"
                "When you are done, please write 'exit'\n\n")

            obstacle_list = []
            pedestrian_list = []

            while True:
                req = input("Please enter the request.")
                req.strip()
                if req == "exit":
                    sys.stdout.write("\n")
                    break
                elif req == "text":
                    read_from_file(pedestrian_list, obstacle_list, size_x, size_y, 2)
                elif not (any(i in ["o", "p"] for i in ["o", "p"])):
                    sys.stdout.write("Invalid object.")
                else:
                    add_to_map2(req, size_x, size_y, obstacle_list, pedestrian_list)

        else:
            speed_range_or_not = int(input("\nPlease type 0 for giving a speed range for whole pedestrians. Please note that speed will be assigned randomly. Else, type 1 to provide speed manually.\n"))

            if not speed_range_or_not:
                lower = float(input("Please provide a lower limit for speed.\n"))
                upper = float(input("Please provide a upper limit for speed.\n"))
                sys.stdout.write(
                    "\nPlease indicate the location of obstacles OR pedestrians as stated below, with locations, from "
                    "0 until cell size you provided (that is excluded.)\n\nFor obstacles: 'o x y'"
                    ", where x and y indicate the x and y coordinate locations.\nFor pedestrians: 'p x y', where x and "
                    "y indicate the x and y coordinate locations.\n\n"
                    "If you want to add objects from txt file, please write 'text' and the name of the file as 'example.txt'\n\n"
                    "When you are done, please write 'exit'\n\n")

                obstacle_list = []
                pedestrian_list = []

                while True:
                    req = input("Please enter the request.")
                    req.strip()
                    if req == "exit":
                        sys.stdout.write("\n")
                        break
                    elif req == "text":
                        read_from_file(pedestrian_list, obstacle_list, size_x, size_y, 3, lower, upper)
                    elif not(any(i in ["o", "p"] for i in ["o", "p"])):
                        sys.stdout.write("Invalid object.")
                    else:
                        add_to_map3(req, size_x, size_y, obstacle_list, pedestrian_list, lower, upper)

            else:
                sys.stdout.write(
                    "\nPlease indicate the location of obstacles OR pedestrians as stated below, with locations, from "
                    "0 until cell size you provided (that is excluded.)\n\nFor obstacles: 'o x y'"
                    ", where x and y indicate the x and y coordinate locations.\nFor pedestrians: 'p x y s', where x and "
                    "y indicate the x and y coordinate locations and s indicates the speed.\n\n"
                    "If you want to add objects from txt file, please write 'text' and the name of the file as 'example.txt'\n\n"
                    "When you are done, please write 'exit'\n\n")

                obstacle_list = []
                pedestrian_list = []

                while True:
                    req = input("Please enter the request.")
                    req.strip()
                    if req == "exit":
                        sys.stdout.write("\n")
                        break
                    elif req == "text":
                        read_from_file(pedestrian_list, obstacle_list, size_x, size_y, 4)
                    elif not(any(i in ["o", "p"] for i in ["o", "p"])):
                        sys.stdout.write("Invalid object.")
                    else:
                        add_to_map4(req, size_x, size_y, obstacle_list, pedestrian_list)


    init_simulation(time, size_x, size_y, pedestrian_list, obstacle_list, target, rmax, mode, speed_or_not)


def init_simulation(time, sx, sy, p, o, t, rmax, mode, speed_or_not):

    # Initializes the simulation by the input obtained from get_model_environment method by
    # creating an Environment object instance and calls create_environment method with the
    # user inputs. Then, calls the appropriate run_simulation method based on the simulation mode.

    simulation_environment = Environment(time, sx, sy, p, o, t, rmax)
    simulation_environment.create_environment()
    if mode == 0:
        simulation_environment.run_simulation()
    elif mode == 1:
        if speed_or_not:
            simulation_environment.run_simulation3()
        else:
            simulation_environment.run_simulation2()


def read_from_file(pedestrian_list, obstacle_list, size_x, size_y, num, lower=None, upper=None):

    # This function is for reading objects from txt files. It takes the filename as input
    # and then sends the objects to the according scenario mapping functions.

    while True:
        filename = input("Please enter the path of text file. (ex: 'example.txt'). \n"
                         "If you want to exit text mode please write 'q'. \n")
        if filename == "q":
            break
        try:
            with open(filename) as file_in:
                for line in file_in:
                    line.strip()
                    if num == 1:
                        add_to_map(line, size_x, size_y, obstacle_list, pedestrian_list)
                    elif num == 2:
                        add_to_map2(line, size_x, size_y, obstacle_list, pedestrian_list)
                    elif num == 3:
                        add_to_map3(line, size_x, size_y, obstacle_list, pedestrian_list, lower, upper)
                    elif num == 4:
                        add_to_map4(line, size_x, size_y, obstacle_list, pedestrian_list)
            sys.stdout.write("Objects are successfully read from the file.")
            break
        except FileNotFoundError:
            sys.stdout.write("Invalid file path.")


# following 4 functions are similar on what they do, with minor differences. They all add objects to the scenario.
def add_to_map(req, size_x, size_y, obstacle_list, pedestrian_list):

    # takes the request and sorts the object as pedestrian or obstacle, adds the object to specified coordinates

    i1 = req.index(" ")
    i2 = req.index(" ", i1 + 1)

    x = int(req[i1 + 1:i2])
    y = int(req[i2 + 1:])

    if x >= size_x or y >= size_y or x < 0 or y < 0:
        sys.stdout.write("Invalid location.")
    else:
        if "o" in req:
            o = Obstacle(y, x)
            obstacle_list.append(o)
        elif "p" in req:
            p = Pedestrian(y, x)
            pedestrian_list.append(p)


def add_to_map2(req, size_x, size_y, obstacle_list, pedestrian_list):

    # takes the request and sorts the object as pedestrian or obstacle, adds the object to specified coordinates

    if "o" in req:
        i1 = req.index(" ")
        i2 = req.index(" ", i1 + 1)

        x = int(req[i1 + 1:i2])
        y = int(req[i2 + 1:])
        if x >= size_x or y >= size_y or x < 0 or y < 0:
            sys.stdout.write("Invalid location.")
        else:
            o = Obstacle(y, x)
            obstacle_list.append(o)
    elif "p" in req:
        i1 = req.index(" ")
        i2 = req.index(" ", i1 + 1)

        x = int(req[i1 + 1:i2])
        y = int(req[i2 + 1:])
        if x >= size_x or y >= size_y or x < 0 or y < 0:
            sys.stdout.write("Invalid location.")
        else:
            p = Pedestrian(y, x)
            pedestrian_list.append(p)


def add_to_map3(req, size_x, size_y, obstacle_list, pedestrian_list, lower, upper):
    # takes the request and sorts the object as pedestrian or obstacle, adds the object to specified coordinates.
    # different from the previous functions, this method gets the lower and upper bound for speed range as a parameter
    # generates the speed randomly and adds it to related pedestrian object.

    if "o" in req:
        i1 = req.index(" ")
        i2 = req.index(" ", i1 + 1)

        x = int(req[i1 + 1:i2])
        y = int(req[i2 + 1:])
        if x >= size_x or y >= size_y or x < 0 or y < 0:
            sys.stdout.write("Invalid location.")
        else:
            o = Obstacle(y, x)
            obstacle_list.append(o)
    elif "p" in req:
        i1 = req.index(" ")
        i2 = req.index(" ", i1 + 1)

        x = int(req[i1 + 1:i2])
        y = int(req[i2 + 1:])
        s = round(random.uniform(lower, upper), 2)
        print(s)
        if x >= size_x or y >= size_y or x < 0 or y < 0:
            sys.stdout.write("Invalid location.")
        else:
            p = Pedestrian(y, x, speed=s)
            pedestrian_list.append(p)


def add_to_map4(req, size_x, size_y, obstacle_list, pedestrian_list):
    # this method gets the speed from the given request manually and adds it to pedestrian object.

    if "o" in req:
        i1 = req.index(" ")
        i2 = req.index(" ", i1 + 1)
        x = int(req[i1 + 1:i2])
        y = int(req[i2 + 1:])
        if x >= size_x or y >= size_y or x < 0 or y < 0:
            sys.stdout.write("Invalid location.")
        else:
            o = Obstacle(y, x)
            obstacle_list.append(o)
    elif "p" in req:
        i1 = req.index(" ")
        i2 = req.index(" ", i1 + 1)
        i3 = req.index(" ", i2 + 1)
        x = int(req[i1 + 1:i2])
        y = int(req[i2 + 1:i3])
        s = float(req[i3 + 1:])
        if x >= size_x or y >= size_y or x < 0 or y < 0:
            sys.stdout.write("Invalid location.")
        else:
            p = Pedestrian(y, x, speed=s)
            pedestrian_list.append(p)


if __name__ == '__main__':
    main()