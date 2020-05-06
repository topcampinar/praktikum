class Pedestrian:
    """
    Pedestrian(x_loc, y_loc, meters, speed, owed)

    It is the class that is used to create Pedestrians on the simulation area.

    Attributes:

        x: int
            x coordinate of the Pedestrian on the simulation area.
        y: int
            y coordinate of the Pedestrian on the simulation area.
        meters: int
            Meters walked by the Pedestrian while walking. Becomes 0 after the end of each second.
        speed: int
            speed of the Pedestrian (in m/s).
        owed: int
            location of the pedestrian inside the cell at the end of the walking process at the end of each second.

    Parameters:

        x_loc: int
            x coordinate of the Pedestrian on the simulation area.
        y_loc: int
            y coordinate of the Pedestrian on the simulation area.
        meters: int
            Meters (in centimeters) walked by the Pedestrian while walking. Becomes 0 after the end of each second. (Default = 0)
        speed: int
            speed of the Pedestrian (in m/s). (Default = 1.33 m/s)
        owed: int
            location of the pedestrian inside the cell at the end of the walking process at the end of each second.
            (in centimeters.)
            (Default = 0)

    """

    def __init__(self, x_loc, y_loc, meters=0, speed=1.33, owed=0):

        self.x = x_loc
        self.y = y_loc
        self.meters = meters
        self.speed = speed
        self.owed = owed
