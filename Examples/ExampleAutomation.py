import Home
import Logging


# called before a connection to the Home Assistant server is established, no entity state known yet
def intialize():
    Logging.Log(__name__, "App is initializing")
    Home.registerStateInitializedCallback(stateInitializedCallback)
    Home.registerStateChangedCallback(stateChangedCallback)


# called after the connection is established an all entity states have been loaded
def stateInitializedCallback(state):
    Logging.Log(__name__, "State of entities when connection was established: %r" % state)


# called when a state_change or a deconz_event message is received
def stateChangedCallback(entity, newState, oldState):
    allStates = Home.getState()
    Logging.Log(__name__, "Current state of entities: %r" % allStates)

    # service of Home Assistant can be invoked
    Home.sendCommand("light", "turn_off", "all")
