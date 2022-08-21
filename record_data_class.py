class RecordMotorData(object):
    def __init__(self):
        self.position_data = [] #initialise
        self.velocity_data = []
        self.acceleration_data = []
        self.current_data = []

    def position(self,position):
        self.position_data.append(position)
        return None

    def velocity(self, velocity):
        self.velocity_data.append(velocity)
        return None

    def acceleration(self, acceleration):
        self.acceleration_data.append(acceleration)
        return None

    def current(self, current):
        self.current_data.append(current)
        return None

class RecordLinkData(object):
    def __init__(self):
        self.position_data = []  # initialise
        self.velocity_data = []
        self.acceleration_data = []

    def position(self, position):
        self.position_data.append(position)
        return None

    def velocity(self, velocity):
        self.velocity_data.append(velocity)
        return None

    def acceleration(self, acceleration):
        self.acceleration_data.append(acceleration)
        return None


