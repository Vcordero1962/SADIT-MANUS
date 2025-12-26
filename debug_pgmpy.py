import importlib
import pkgutil
import pgmpy.models

print("Searching for DiscreteBayesianNetwork in pgmpy.models...")


def search_class(package):
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            module = importlib.import_module(modname)
            if hasattr(module, 'DiscreteBayesianNetwork'):
                print(f"FOUND: {modname}.DiscreteBayesianNetwork")
            if hasattr(module, 'BayesianNetwork'):
                print(f"Found BayesianNetwork in {modname}")
        except Exception as e:
            pass


search_class(pgmpy.models)
