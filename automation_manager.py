import sys
import os
import importlib
import custom_logging

automations = []
modules = []


def load_automations():
    sys.path.insert(0, os.path.abspath("./Automations"))
    only_files = [f for f in os.listdir("Automations") if (os.path.isfile(os.path.join("Automations", f)) and f.endswith(".py"))]

    importlib.invalidate_caches()
    for f in only_files:
        try:
            modules.append(importlib.import_module(f[:f.rfind(".py")]))
        except Exception as ex:
            custom_logging.log(__name__, "Error while loading %s: %s %s" % (f, type(ex), str(ex)))

    modules_with_initiaialize = [m for m in modules if "initialize" in dir(m)]
    for m in modules_with_initiaialize:
        try:
            getattr(m, "initialize")()
            automations.append(m)
            custom_logging.log(__name__, "Initialized Automation %s" % m)
        except Exception as ex:
            custom_logging.log(__name__, "Error while initializing %s: %s %s" % (str(m), type(ex), str(ex)))


def unload_automations():
    global automations
    global modules
    modules_with_cleanup = [m for m in modules if "cleanup" in dir(m)]
    for m in modules_with_cleanup:
        try:
            getattr(m, "cleanup")()
            custom_logging.log(__name__, "Unloaded Automation %s" % m)
        except Exception as ex:
            custom_logging.log(__name__, "Error while unloading %s: %s %s" % (str(m), type(ex), str(ex)))
    automations = []
    modules = []


def reaload_automations():
    unload_automations()
    load_automations()
