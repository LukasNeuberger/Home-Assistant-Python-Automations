import home
import custom_logging


# called before a connection to the home Assistant server is established, no entity state known yet
def intialize():
    custom_logging.log(__name__, "App is initializing")
    home.register_state_initialized_callback(state_initialized_callback)
    home.register_state_changed_callback(state_changed_callback)


# called after the connection is established an all entity states have been loaded
def state_initialized_callback(state):
    custom_logging.log(__name__, "State of entities when connection was established: %r" % state)


# called when a state_change or a deconz_event message is received
def state_changed_callback(entity, new_state, old_state):
    all_states = home.get_state()
    custom_logging.log(__name__, "Current state of entities: %r" % all_states)

    # service of home Assistant can be invoked
    home.send_command("light", "turn_off", "all")
