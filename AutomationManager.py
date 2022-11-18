import sys
import os
import importlib
import Logging

automations = []
modules = []


def loadAutomations():
    sys.path.insert(0, os.path.abspath("./Automations"))
    onlyfiles = [f for f in os.listdir("Automations") if (
        os.path.isfile(os.path.join("Automations", f)) and f.endswith(".py"))]

    importlib.invalidate_caches()
    for f in onlyfiles:
        try:
            modules.append(importlib.import_module(f[:f.rfind(".py")]))
        except Exception as ex:
            Logging.Log(__name__, "Error while loading %s: %s" % (f, str(ex)))

    modulesWithInitiaialize = [m for m in modules if "initialize" in dir(m)]
    for m in modulesWithInitiaialize:
        try:
            getattr(m, "initialize")()
            automations.append(m)
            Logging.Log(__name__, "Initialized Automation %s" % m)
        except Exception as ex:
            Logging.Log(__name__, "Error while initializing %s: %s" % (str(m), str(ex)))


def unloadAutomations():
    global automations
    global modules
    modulesWithCleanup = [m for m in modules if "cleanup" in dir(m)]
    for m in modulesWithCleanup:
        try:
            getattr(m, "cleanup")()
            print("Unloaded Automation %s" % m)
        except Exception as ex:
            Logging.Log(__name__, "Error while unloading %s: %s" %
                        (str(m), str(ex)))
    automations = []
    modules = []


def realoadAutomations():
    unloadAutomations()
    loadAutomations()
