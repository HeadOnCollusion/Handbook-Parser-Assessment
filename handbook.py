"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json
from tkinter import ALL
from typing import Dict, List

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS: Dict = json.load(f)
    f.close()

ALL_COURSES = list()

class Subject(object):
    def __init__(self, name: str, dirty_reqs: str) -> None:
        self.name = name
        self.reqs = self.parse_reqs(dirty_reqs)

    @staticmethod
    def parse_reqs(dirty_reqs: str) -> List['Requirement']:
        pass

    def is_unlocked(self, courses_list: List[str]) -> bool:
        uoc = len(courses_list) * 6
        for req in self.reqs:
            pass

class Requirement(object):
    """
    A requirement which could be atomic, or (recursively) contain requirement/s. Ex:
        COMP1511
        Req()
    """
    def __init__(self) -> None:
        self.uoc = None
        pass

    def req_met(self, uoc_done: int, courses_list: List[str]):
        if self.uoc is not None:
            if uoc_done < self.uoc:
                return False
        

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    
    # TODO: COMPLETE THIS FUNCTION!!!
    
    return True

if __name__ == "__main__":
    # print(CONDITIONS)
    for name, dirty_reqs in CONDITIONS.items():
        ALL_COURSES.append(Subject(name, dirty_reqs))



    