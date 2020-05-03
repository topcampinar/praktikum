class Pedestrian:

    def __init__(self, x_loc, y_loc, meters=0, speed=1.40, owed=0):

        self.x = x_loc
        self.y = y_loc
        self.meters = meters
        self.speed = speed
        self.owed = owed

        #for speed we can add a default variable here and send the percentage as parameter and multiply it with the default one.