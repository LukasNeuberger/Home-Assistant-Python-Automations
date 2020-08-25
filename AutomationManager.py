import sys
import os
import importlib

automations = []

def loadAutomations():
  sys.path.insert(0, os.path.abspath("./Automations"))
  onlyfiles = [f for f in os.listdir("Automations") if (
      os.path.isfile(os.path.join("Automations", f)) and f.endswith(".py"))]

  importlib.invalidate_caches()
  modules = [importlib.import_module(f[:f.rfind(".py")]) for f in onlyfiles]

  modulesWithInitiaialize = [m for m in modules if "initialize" in dir(m)]
  for m in modulesWithInitiaialize:
      getattr(m, "initialize")()
      automations.append(m)
      print("Initialized Automation %s" % m)

def unloadAutomations():
  modulesWithCleanup = [m for m in modules if "cleanup" in dir(m)]
  for m in modulesWithCleanup:
      getattr(m, "cleanup")()
      print("Cleaned up Automation %s" % m)
  automations = []

def realoadAutomations():
  unloadAutomations()
  loadAutomations()