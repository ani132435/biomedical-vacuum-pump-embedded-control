class StateMachine:

    OFF = 0
    STIMULATION = 1
    EXPRESSION = 2
    ERROR = 3

    def __init__(self):

        self.state = self.OFF

    def set_state(self, state):

        self.state = state

    def get_state(self):

        return self.state
