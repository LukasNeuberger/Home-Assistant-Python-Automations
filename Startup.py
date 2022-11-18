import Home
import AutomationManager
import Logging


Logging.Log(__name__, "Loading Automations")
AutomationManager.loadAutomations()
Logging.Log(__name__, "Start Home Assistant Connection")
Home.run()
