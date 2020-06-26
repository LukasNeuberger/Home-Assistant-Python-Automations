import sys
import os
import importlib

apps = []

def loadApps():
  sys.path.insert(0, os.path.abspath("./Apps"))
  onlyfiles = [f for f in os.listdir("Apps") if (
      os.path.isfile(os.path.join("Apps", f)) and f.endswith(".py"))]

  importlib.invalidate_caches()
  modules = [importlib.import_module(f[:f.rfind(".py")]) for f in onlyfiles]

  modulesWithInitiaialize = [m for m in modules if "initialize" in dir(m)]
  for m in modulesWithInitiaialize:
      getattr(m, "initialize")()
      apps.append(m)
      print("Initialized App %s" % m)

def unloadApps():
  modulesWithCleanup = [m for m in modules if "cleanup" in dir(m)]
  for m in modulesWithCleanup:
      getattr(m, "cleanup")()
      print("Cleaned up App %s" % m)
  apps = []

def realoadApps():
  unloadApps()
  loadApps()