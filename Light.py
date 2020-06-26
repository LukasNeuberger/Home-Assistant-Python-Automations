import Home


class Light:
    def __init__(self, entity_id):
        self.id = entity_id

    def isOn(self):
        return Home.getState()[self.id]["state"] == "on"

    def turnOn(self):
        Home.sendCommand("light", "turn_on", {"entity_id": self.id})

    def turnOff(self):
        Home.sendCommand("light", "turn_off", {"entity_id": self.id})
