from typing import Dict, Any
import json
from json.decoder import JSONDecodeError

class BetterJson:
    def __init__(self, json_path: str="", _dict: Dict[Any, Any]={}) -> None:
        assert not ( json_path == "" and _dict == {} )
        self.path = json_path

        if json_path != "":
            try:
                self.data = json.load(open(json_path))
            except FileNotFoundError:
                print(f"Err: File {json_path} not found")
                quit()
            except JSONDecodeError:
                print(f"Err: File {json_path} has incorrect json syntax")
                quit()
        elif _dict != {}:
            self.data = _dict
        else:
            print(f"Err: json_path or _dict must be set to a value")
    
    def get(self, path: str, show_errors: bool=True) -> Any:
        current = self.data.copy()
        for location in path.split("."):
            try:
                if type(current) == list:
                    current = current[int(location)]
                elif type(current) == dict:
                    current = current[location]
                else:
                    if show_errors:
                        print(f"Err: Type of {current} is invalid, needs to be dict or list.")
                    return ""
            except KeyError:
                if show_errors:
                    if type(current) == dict:
                        print(f"Err: Invalid key '{location}', not in ({', '.join(list(current.keys()))})")
                    elif type(current) == list:
                        print(f"Err: Invalid index '{location}' not in list {', '.join(current)}")
                    else:
                        print(f"Err: {current} is not valid type, cannot index")
                return ""

        return current
    
    def set(self, path: str, value: Any, show_errors: bool=True) -> None:
        self.set_rec(self.data, path, value)
        return
    
    def set_rec(self, data: Dict[Any, Any], path: str, value: Any, show_errors: bool=True) -> None:
        current = data
        location = path.split(".")[0]
        try:
            remaining = path.split(".",maxsplit=1)[1]
        except IndexError:
            current[location] = value
            return
        try:
            if type(current) == list:
                self.set_rec(data[int(location)], remaining, value)
            elif type(current) == dict:
                self.set_rec(data[location], remaining, value)
            else:
                if show_errors:
                    print(f"Err: Type of {current} is invalid, needs to be dict or list.")
                return
        except KeyError:
            if show_errors:
                if type(current) == dict:
                    print(f"Err: Invalid key '{location}', not in ({', '.join(list(current.keys()))})")
                elif type(current) == list:
                    print(f"Err: Invalid index '{location}' not in list {', '.join(current)}")
                else:
                    print(f"Err: {current} is not valid type, cannot index")
            return
        return
    
    def append(self, path: str, value: Any) -> None:
        replace_value = self.get(path)
        replace_value.append(value)
        self.set(path, replace_value)
    
    def remove(self, path) -> None:
        #TODO rename all variables TODO#
        remove_path = ".".join(path.split(".")[:-1])
        remove_name = path.split(".")[-1]
        remove_value = self.get(remove_path)
        remove_value = {
            key: value
            for key, value in remove_value.items() if key != remove_name
        }
        self.set(remove_path, remove_value)

    def pop(self, path):
        pass
    #for lists
    
    def commit(self) -> None:
        if self.path == "":
            return
        json.dump(self.data, open(self.path, "w"))
    
    def reload(self) -> None:
        self.__init__(self.path)


if __name__ == "__main__":
    test = BetterJson("calendar_module/betterjson/test.json")
    print(test.get("items.tomato"))
    test.remove("items.tomato.sidj")
    print(test.get("items.tomato"))
