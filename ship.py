class Ship(object):
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __init__(self, name, orientation, dimension):
        d0, d1 = dimension
        self.name = name  # name of this ship
        self.orientation = orientation  # 'vertical' or 'horizontal'
        self.life = d0 * d1  # when life == 0, the ship is sunk
        self.coordinates = list()  # coordinates of where this ship lives on the board

    def add_coordinates(self, coord):
        self.coordinates.append(coord)

    def receive_shot(self):
        self.life -= 1

    def is_sunk(self):
        if self.life == 0:
            return True
        return False
