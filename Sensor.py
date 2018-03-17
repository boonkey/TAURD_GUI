from random import uniform

class Sensor:
    def __init__(self, s_id, name, low, high):
        self.id = s_id
        self.name = name
        self.low_val = low
        self.high_val = high
        self.value = str((eval(low)+eval(high))/2)
        if self.value == 0:
            self.value = "50"
        self.history = []

    def update(self, new_value):
        self.value = new_value
        self.history += [new_value]

    def __str__(self):
        return "id: %s\n" \
               "name: %s\n" \
               "Current Value: %s\n" \
               "low_value: %s\n" \
               "high_value: %s\n" %(self.id, self.name, self.value, self.low_val, self.high_val)