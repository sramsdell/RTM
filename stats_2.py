import random, math, pygame

SIZE = (400,400)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255,100,100)
WHITE = (255, 255, 255)
OFF_SET = 50
MAX_POINTS = 2000

class UI():
    def __init__(self):
        self.points = set([])
        self.N = 0
        self.total = 0
        self.ave = 0
        self.dist_len = 40
        self.dist_10 = [0] * self.dist_len

    def get_dist_len(self):
        return self.dist_len
    
    def get_dist_10(self):
        return self.dist_10

    def add_dist_10(self, index):
        self.dist_10[index] += 1

    def get_points(self):
        return self.points

    def add_point(self, point):
        self.points.add(point)
        
    def get_N(self):
        return self.N

    def add_N(self):
        self.N += 1

    def get_total(self):
        return self.total

    def add_total(self, val):
        self.total += val

    def get_ave(self):
        return self.ave

    def alt_ave(self, val):
        self.ave = val


class Point():
    def __init__(self, x, y):
        self._pos = [x, y]
        self._radius = 2

    def get_pos(self):
        return self._pos
    
    def get_radius(self):
        return self._radius
    
    def update(self):
        pass

    def render(self, screen):
        pygame.draw.circle(screen, RED, self._pos, self._radius)


def plot(x, p = False):
    """takes uniform.rand.var as argument, and passes through inverse
    function"""
    y = math.log(1 - x)
    # one bus every half hour, or 2 buses every hour
    lamb = 2
    hour_to_min = 60
    if (p):
        print ((-1/lamb) * y) * hour_to_min
    return ((-1/lamb) * y) * hour_to_min


def spawn_points(count, ui, speed = 2):
    if (count % speed == 0):
        hoz = SIZE[0] - OFF_SET
        #random.random is python's uniform 
        rand = int(plot(random.random()))
        vert = rand + OFF_SET
        for point in ui.get_points():
            if (point.get_pos()[0] == vert):
                hoz = hoz - point.get_radius() * 2
        
        a_point = Point(vert, hoz)
        ui.add_point(a_point)

        return rand
    return 0
