from typing import List


class Exam:
    def __init__(self, name: str, date: str, tags: List[str]) -> None:
        self.name = name
        self.date = date
        self.tags = tags
    
    def match_tag(self, tags: List[str], force_exact: bool=False) -> bool:
        for tag in tags:
            if force_exact:
                if tag not in self.tags:
                    return False
            else:
                if tag in self.tags:
                    return True
        return False