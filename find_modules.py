from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()


def get_tasks_files():
    matches = []
    matches.extend(list(Path(".").rglob("tasks/*.yaml")))
    matches.extend(list(Path(".").rglob("tasks/*.yml")))
    matches.extend(list(Path(".").rglob("handlers/*.yaml")))
    matches.extend(list(Path(".").rglob("handlers/*.yml")))
    return matches


# Take a list as input, for each item find a key that contains dots, split the key
# by dots and if the resulting list has 3 items, return the key
def get_module_from_list(data: list):
    modules: list[str] = []
    for item in data:
        for key in item:
            if "." not in key:
                continue
            elif len(key.split(".")) == 3:
                modules.append(key)
                break
        else:
            print(f"module not found for task {item.get('name')}")
    return modules


# Take a Path object as input, read the content, parse it with ruamel.yaml
# and for each dict in the resulting list, return the key that contains dots
def get_modules_from_file(file: Path):
    modules: list[str] = []
    if not file.is_file():
        return modules
    with open(file, "r") as f:
        data = yaml.load(f)
        if not data:
            return modules
        return get_module_from_list(data)


# find all modules used in tasks and handlers
def get_modules():
    modules = []
    for file in get_tasks_files():
        modules.extend(get_modules_from_file(file))
    return modules


# Take a list as input, split each item by dots and return a set of the first 2 items
def get_collections(modules: list[str]):
    collections = set()
    for module in modules:
        collections.add(".".join(module.split(".")[:2]))
    return collections


print(get_collections(get_modules()))
