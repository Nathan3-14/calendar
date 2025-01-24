from typing import List


class Exam:
    def __init__(self, name: str, date: str, tags: List[str]) -> None:
        self.name = name
        self.date = date
        self.tags = tags
        
        for tag in self.tags:
            if tag.lower() in self.name.lower():
                self.name.replace(tag.lower(), f"[blue]{tag.capitalize()}[/blue]") #TODO FIX!
    
    def match_tags(self, tags: List[str], force_exact: bool=False) -> bool:
        if tags == []:
            return True
        for tag in tags:
            if force_exact:
                if tag not in self.tags:
                    return False
            else:
                if tag in self.tags:
                    return True
        return False