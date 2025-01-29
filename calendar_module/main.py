from typing import Any, Dict, List, Tuple
try:
    from .betterjson import BetterJson
    from .exams import Exam
except:
    from betterjson import BetterJson
    from exams import Exam
try:
    from .rich.table import Table #type:ignore
    from .rich import print #type:ignore
except:
    from rich.table import Table #type:ignore
    from rich import print #type:ignore

class ExamList:
    def __init__(self, exams: List[Exam], date: str) -> None:
        self.exams = exams
        self.date = date
    
    def init(self) -> None:
        self.am = self.get_matching_exams(["am"])
        self.pm = self.get_matching_exams(["pm"])
    
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
    temp_examlist.init()
    return temp_examlist

class ExamInteractable:
    def __init__(self, data: BetterJson) -> None:
        self.exam_data = data
    
    def get_exams_on_dates(self, date_list: List[str], tag_list: List[str]=[], raw: bool=False) -> Table | Tuple[ExamList, ExamList]:
        days = []
        week_table = Table(title=f"{date_list[0]} -> {date_list[-1]}", show_lines=True)
        am, pm = ExamList([], "99/99"), ExamList([], "99/99")
        am_display, pm_display = [], []
        week_table.add_column()

        for date in date_list:
            if tag_list == []:
                current_day = ExamListConstructor(self.exam_data.get(f"exams.{date}"), date)
            else:
                current_day = ExamListConstructor(self.exam_data.get(f"exams.{date}"), date).get_matching_exams(tag_list)
            current_day.init()

            days.append(current_day)
            am = current_day.get_matching_exams(["pm"])
            pm = current_day.get_matching_exams(["pm"])
            am_display.append("\n".join([exam.name for exam in am]))
            pm_display.append("\n".join([exam.name for exam in pm]))
                
            
            week_table.add_column(date)
            
        week_table.add_row("AM", *am_display)
        week_table.add_row("PM", *pm_display)

        return days if raw else week_table

    def get_user(self, user_name: str, date_list: List[str]) -> Tuple[ExamList, ExamList]:
        # print(self.exam_data.get(f"users.{user_name.lower()}"))
        return self.get_exams_on_dates(date_list, self.exam_data.get(f"users.{user_name.lower()}"), raw=True) #type:ignore

if __name__ == "__main__":
    i_exam = ExamInteractable(BetterJson("exams.json"))
    for examlist in i_exam.get_user("Nathan", ["10/02", "11/02", "12/02", "13/02", "14/02"]):
        print(examlist)

