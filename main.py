from typing import Any, Dict, List
from betterjson import BetterJson
from exams import Exam
from rich.table import Table
from rich import print

class ExamList:
    def __init__(self, exams: List[Exam], date: str) -> None:
        self.exams = exams
        self.date = date
    
    def get_matching_exams(self, tags: List[str], force_exact: bool=False) -> "ExamList":
        matching = ExamList([exam for exam in self.exams if exam.match_tags(tags, force_exact=force_exact)], self.date)
        return matching
    
    def __str__(self) -> str:
        return "# " + ", ".join([f'{exam.name}{exam.tags}' for exam in self.exams]) + " #"
    
    def __iter__(self) -> Any:
        return iter(self.exams)

def ExamListConstructor(exams: List[Dict[str,str|List[str]]], date: str) -> ExamList:
    temp_examlist = ExamList([], "99/99")
    temp_examlist.exams = []
    temp_examlist.date = date
    for exam_dict in exams:
        try:
            temp_examlist.exams.append(Exam(exam_dict["name"], date, exam_dict["tags"])) #type:ignore
        except:
            print("Err: Could not create exam object, check json data")
            break
    return temp_examlist

def get_week(week: List[str], data: BetterJson, tag_list: List[str]=[]) -> Table:
    # days = []
    week_table = Table(title=f"{week[0]} -> {week[-1]}", show_lines=True)
    am, pm = [], []
    week_table.add_column()

    for date in week:
        current_day = ExamListConstructor(data.get(f"exams.{date}"), date)

        # days.append(current_day)
        am.append("\n".join([exam.name for exam in current_day.get_matching_exams(["am"]).get_matching_exams(tag_list)]))
        pm.append("\n".join([exam.name for exam in current_day.get_matching_exams(["pm"]).get_matching_exams(tag_list)]))
        week_table.add_column(date)
        
    week_table.add_row("AM", *am)
    week_table.add_row("PM", *pm)

    return week_table

test_data = BetterJson("data.json")
exam_data = BetterJson("exams.json")

print(get_week(["10/02", "11/02", "12/02", "13/02", "14/02"], exam_data))
print(get_week(["24/02", "25/02", "26/02", "27/02", "28/02"], exam_data))
