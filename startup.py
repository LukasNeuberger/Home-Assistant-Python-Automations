import home
import automation_manager
import custom_logging


custom_logging.log(__name__, "Loading Automations")
automation_manager.load_automations()
custom_logging.log(__name__, "Start home Assistant Connection")
home.run()
