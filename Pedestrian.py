class Pedestrian:

    def __init__(self, x_loc, y_loc, meters=0, speed=1.33, owed=0):

        self.x = x_loc
        self.y = y_loc
        self.meters = meters
        self.speed = speed
        self.owed = owed
