from typing import Dict, List
from betterjson import BetterJson
from exams import Exam

class Day:
    def __init__(self, exams: List[Dict[str,str|List[str]]], date: str) -> None:
        self.exams = {}
        for exam_dict in exams:
            try:
                self.exams[exam_dict["name"]] = Exam(exam_dict["name"], date, exam_dict["tags"]) #type:ignore
            except:
                print("Err: Could not create exam object, check json data")
                return
    
    def __str__(self) -> str:
        return "# " + ", ".join(list(self.exams.keys())) + " #"

data = BetterJson("data.json")
days = []

for date in ["01/01", "02/01", "03/01", "04/01", "05/01"]:
    days.append(Day(data.get(f"exams.{date}"), date))

print([str(day) for day in days])
    