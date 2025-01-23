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
        matching = [exam for exam in self.exams if exam.match_tags(tags, force_exact=force_exact)]
        return matching
    
    def __str__(self) -> str:
        return "# " + ", ".join([exam.name for exam in self.exams]) + " #"

data = BetterJson("data.json")
days = []
week = ["01/01", "02/01", "03/01", "04/01", "05/01"]

week_table = Table(title=f"{week[0]} -> {week[-1]}", show_lines=True)
am, pm = [], []
week_table.add_column()

for date in week:
    current_day = Day(data.get(f"exams.{date}"), date)

    days.append(current_day)
    
    am.append("\n".join([exam.name for exam in current_day.get_matching_exams(["am"])]))
    pm.append("\n".join([exam.name for exam in current_day.get_matching_exams(["pm"])]))
    week_table.add_column(date)
    
week_table.add_row("AM", *am)
week_table.add_row("PM", *pm)

print(week_table)
