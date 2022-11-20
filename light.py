import home


class Light:
    def __init__(self, entity_id):
        self.id = entity_id

    def is_on(self):
        return home.get_state()[self.id]["state"] == "on"

    def turn_on(self):
        home.send_command("light", "turn_on", {"entity_id": self.id})

    def turn_off(self):
        home.send_command("light", "turn_off", {"entity_id": self.id})
