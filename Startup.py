import Home
import AppManager


print("Loading Apps")
AppManager.loadApps()
print("Start Home Assistant Connection")
Home.run()
