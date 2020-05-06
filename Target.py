class Target:
    """
    Target(x_loc, y_loc)

    It is the class that is used to create Block on the simulation area.

    Attributes:

        x: int
            x coordinate of the Target on the simulation area.
        y: int
            y coordinate of the Target on the simulation area.

    Parameters:

        x_loc: int
            x coordinate of the Target on the simulation area.
        y_loc: int
            y coordinate of the Target on the simulation area.

    """
    def __init__(self, x_loc, y_loc):
        self.x = x_loc
        self.y = y_loc