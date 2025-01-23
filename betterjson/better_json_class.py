from typing import Dict, Any
import json
from json.decoder import JSONDecodeError

class BetterJson:
    def __init__(self, json_path: str="", _dict: Dict[Any, Any]={}) -> None:
        assert not ( json_path == "" and _dict == {} )

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
    
    def get(self, path: str) -> Any:
        current = self.data.copy()
        for location in path.split("."):
            try:
                if type(current) == list:
                    current = current[int(location)]
                elif type(current) == dict:
                    current = current[location]
                else:
                    print(f"Err: Type of {current} is invalid, needs to be dict or list.")
                    return ""
            except KeyError:
                print(f"Err: Invalid key '{location}', not in ({', '.join(list(current.keys()))})")
                return ""

        return current


if __name__ == "__main__":
    test = BetterJson("i--test.json")
    # print(test.get("bad"))
    # print(test.get("exams"))
    print(test.get("exams.01/01"))
    for exam in test.get("exams.01/01"):
        print(f"{exam['name']}: ({', '.join(exam['tags'])})")
