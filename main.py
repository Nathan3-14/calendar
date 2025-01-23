from typing import Dict, List
from betterjson import BetterJson
from exams import Exam
from rich.table import Table
from rich import print

class Day:
    def __init__(self, exams: List[Dict[str,str|List[str]]], date: str) -> None:
        self.exams = []
        for exam_dict in exams:
            try:
                self.exams.append(Exam(exam_dict["name"], date, exam_dict["tags"])) #type:ignore
            except:
                print("Err: Could not create exam object, check json data")
                return
    
    def get_matching_exams(self, tags: List[str], force_exact: bool=False) -> List[Exam]:
        #TODO Replace with code from am and pm TODO#
        return []
    
    def am(self, as_str: bool=False) -> List[Exam] | str:
        matching = [exam for exam in self.exams if exam.match_tag(["am"])]
        if as_str:
            return "\n".join([exam.name for exam in matching])
        return matching
    
    def pm(self, as_str: bool=False) -> List[Exam] | str:
        matching = [exam for exam in self.exams if exam.match_tag(["pm"])]
        if as_str:
            return "\n".join([exam.name for exam in matching])
        return matching
    
    def __str__(self) -> str:
        return "# " + ", ".join([exam.name for exam in self.exams]) + " #"

data = BetterJson("data.json")
days = []
week = ["01/01", "02/01", "03/01", "04/01", "05/01"]

for date in week:
    days.append(Day(data.get(f"exams.{date}"), date))

#TODO Combine with above TODO#
temp_table = Table(title=f"{week[0]} -> {week[-1]}", show_lines=True)
am = []
pm = []
temp_table.add_column()
for index, date in enumerate(week):
    am.append(days[index].am(as_str=True))
    pm.append(days[index].pm(as_str=True))
    temp_table.add_column(date)
temp_table.add_row("AM", *am)
temp_table.add_row("PM", *pm)

print(temp_table)
