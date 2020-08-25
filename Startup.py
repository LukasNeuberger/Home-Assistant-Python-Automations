import Home
import AutomationManager


print("Loading Automations")
AutomationManager.loadAutomations()
print("Start Home Assistant Connection")
Home.run()
