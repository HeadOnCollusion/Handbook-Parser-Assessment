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
import json, re
from typing import Dict, List, Optional
from enum import Enum

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS: Dict = json.load(f)
    f.close()

class Subject(object):
    def __init__(self, name: str, dirty_reqs: str) -> None:
        self.name = name
        self.reqs_head = self.parse_reqs(dirty_reqs)

    def parse_reqs(self, dirty_reqs: str) -> 'RequirementNode':
        # Alternatively, return the hardcoded node trees
        # from hardcode_course_reqs import (
        #     COMP1521_req, COMP2511_req, COMP3153_req, COMP4128_req,
        #     COMP4601_req, COMP4952_req, COMP9302_req, COMP9491_req
        # )

        from lexer_parser import Parser
        return Parser(dirty_reqs).parse()

    def is_unlocked(self, courses_list: List[str]) -> bool:
        """
        Given the list of courses a student has completed, returns true
        or false on whether the Subject is unlocked.
        """
        uoc_done = len(courses_list) * 6
        return self.reqs_head.req_met(courses_list, uoc_done)

class NodeType(Enum):
    LEAF = '0'
    AND = '1'
    OR = '2'

class RequirementNode(object):
    """
    A requirement which could be a single course and/or UOC (LEAF node), or
    (recursively) contain requirement/s.
    If LEAF node and non-zero UOC:
        and pre_subj is None, then just need X UOC anywhere.
        and pre_subj matches ^[A-Z]{4}$, then need X UOC from ABCD subjects.
        and pre_subj matches ^[A-Z]{4}[1-9]$, then need X UOC from that Nth level course of ABCD subjects.
    If OR node and none-zero UOC, then at least X UOC from the children courses must have been completed.
    
    Ex:
        COMP1511: LEAF-type node as head with UOC=0 and pre_subj=None
        COMP3153: LEAD-type node as head with UOC=0 and pre_subj='MATH1081'
        COMP2111: "MATH1081 AND (COMP1511 OR DPST1091 OR COMP1917 OR COMP1921)": AND-type node as head
        with 2 children:
            - 'MATH1081' LEAF-type node, and
            - OR-type child node containing LEAF-type children for each 4 of the courses
        COMP3901: AND-type node as head with 2 children:
            - LEAF-type node with UOC=12 and pre_subj='COMP1'
            - LEAF-type node with UOC-18 and pre_subj='COMP2'
        COMP9491: OR-type node as head with UOC=18 and 4 LEAF-type children for each of the 4 courses
    """
    def __init__(self, req_type: NodeType, *, 
                 children: List['RequirementNode']=[],
                 uoc: int=0, pre_subj: Optional[str]=None) -> None:
        if req_type is not NodeType.LEAF:
            assert(pre_subj is None)
            
        self.uoc = uoc
        self.pre_subj = pre_subj
        self.type = req_type
        self.children = children

    def req_met(self, courses_list: List[str], uoc_done) -> bool:
        if self.type == NodeType.LEAF:
            if self.pre_subj is None:
                # Plain uoc check
                return uoc_done >= self.uoc
            elif m := re.fullmatch(r'[A-Z]{4}[1-9]?', self.pre_subj):
                # Uoc check in subject prefix, or a specific level in subject
                return len([c_name for c_name in courses_list if re.match(m.group(0), c_name) is not None]) * 6 >= self.uoc
            else:
                # Plain subject check
                return self.pre_subj in courses_list
        elif self.type == NodeType.AND:
            return all(child.req_met(courses_list, uoc_done) for child in self.children)
        elif self.uoc > 0:
            # Check at least X uoc is done within certain group (assuming 6 UOC)
            return sum(6 for child in self.children if child.req_met(courses_list, uoc_done)) >= self.uoc
        else:
            # Plain OR node
            return any(child.req_met(courses_list, uoc_done) for child in self.children)

    def print_req_structure(self, lvl: int=0) -> None:
        print('\t' * lvl, end="")
        if self.type is NodeType.LEAF:
            print(self.pre_subj, self.uoc)
        else:
            if self.type is NodeType.AND:
                print("AND")
            else:
                print("OR", self.uoc)
            for child in self.children:
                child.print_req_structure(lvl + 1)

PARSED = False
all_courses: List[Subject] = list()

def is_unlocked(courses_list, target_course):
    """
    Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    global PARSED
    if not PARSED:
        for name, dirty_reqs in CONDITIONS.items():
            all_courses.append(Subject(name, dirty_reqs))
        PARSED = True
    
    target_course_obj: Subject = next(filter(lambda s: s.name == target_course, all_courses))
    return target_course_obj.is_unlocked(courses_list)
    