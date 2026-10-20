class EmulatorRegistry:
    def __init__(self):

        self.emulators = {}

    def register(self, emulator_id, data):

        self.emulators[emulator_id] = data

    def get(self, emulator_id):

        return self.emulators.get(emulator_id)
