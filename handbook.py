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
from test_handbook import *

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS: Dict = json.load(f)
    f.close()

class Subject(object):
    def __init__(self, name: str, dirty_reqs: str) -> None:
        self.name = name
        self.reqs_head = self.parse_reqs(dirty_reqs)

    @staticmethod
    def parse_reqs(dirty_reqs: str) -> 'RequirementNode':
        if name == 'COMP1521':
            return COMP1521_req
        elif name == 'COMP2511':
            return COMP2511_req
        elif name == 'COMP3153':
            return COMP3153_req
        elif name == 'COMP4952':
            return COMP4952_req
        else:
            return RequirementNode(NodeType.LEAF)

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
                 uoc=0, pre_subj: Optional[str]=None) -> None:
        if req_type is not NodeType.LEAF:
            assert(pre_subj is None)
            
        self.uoc = uoc
        self.pre_subj = pre_subj
        self.type = req_type
        self.children = children

    def req_met(self, courses_list: List[str], uoc_done) -> bool:
        if self.type == NodeType.LEAF:
            if self.pre_subj is None:
                return uoc_done >= self.uoc
            elif m := re.fullmatch(r'[A-Z]{4}[1-9]?', self.pre_subj):
                return len([lambda c_name: re.fullmatch(m.group(0), c_name), courses_list]) * 6 >= self.uoc
            else:
                return self.pre_subj in courses_list
        elif self.type == NodeType.AND:
            return all(child.req_met(courses_list, uoc_done) for child in self.children)
        else:
            return any(child.req_met(courses_list, uoc_done) for child in self.children)
        
COMP1511 = RequirementNode(NodeType.LEAF, pre_subj="COMP1511")
COMP1531 = RequirementNode(NodeType.LEAF, pre_subj="COMP1531")
COMP1911 = RequirementNode(NodeType.LEAF, pre_subj="COMP1911")
COMP1917 = RequirementNode(NodeType.LEAF, pre_subj="COMP1917")
COMP1927 = RequirementNode(NodeType.LEAF, pre_subj="COMP1927")
COMP2521 = RequirementNode(NodeType.LEAF, pre_subj="COMP2521")
DPST1091 = RequirementNode(NodeType.LEAF, pre_subj="DPST1091")

COMP2511_reqA = RequirementNode(NodeType.OR, children=[COMP1927, COMP2521])

COMP1521_req = RequirementNode(NodeType.OR, children=[COMP1511, DPST1091, COMP1911, COMP1917])
COMP2511_req = RequirementNode(NodeType.AND, children=[COMP1531, COMP2511_reqA])
COMP3153_req = RequirementNode(NodeType.LEAF, pre_subj="MATH1081")
COMP4952_req = RequirementNode(NodeType.LEAF, pre_subj="COMP4951")

all_courses: List[Subject] = list()
for name, dirty_reqs in CONDITIONS.items():
    all_courses.append(Subject(name, dirty_reqs))

def is_unlocked(courses_list, target_course):
    """
    Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    
    target_course_obj: Subject = next(filter(lambda s: s.name == target_course, all_courses))
    return target_course_obj.is_unlocked(courses_list)

if __name__ == '__main__':
    test_no_reqs()
    test_single_reqs()
    test_simple_OR_AND()
    # test_single()
    