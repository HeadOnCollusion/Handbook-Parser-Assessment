import json, re
from typing import Dict

expected = {
    "COMP1511": "",
    "COMP1521": "COMP1511 OR DPST1091 OR COMP1911 OR COMP1917",
    "COMP1531": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP2041": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP2111": "MATH1081 AND (COMP1511 OR DPST1091 OR COMP1917 OR COMP1921)",
    "COMP2121": "COMP1917 OR COMP1921 OR COMP1511 OR DPST1091 OR COMP1521 OR DPST1092 OR (COMP1911 AND MTRN2500)",
    "COMP2511": "COMP1531 AND (COMP2521 OR COMP1927)",
    "COMP2521": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP3121": "COMP1927 OR COMP2521",
    "COMP3131": "COMP2511 OR COMP2911",
    "COMP3141": "COMP1927 OR COMP2521",
    "COMP3151": "COMP1927 OR ((COMP1521 OR DPST1092) AND COMP2521)",
    "COMP3153": "MATH1081",
    "COMP3161": "COMP2521 OR COMP1927",
    "COMP3211": "COMP3222 OR ELEC2141",
    "COMP3900": "COMP1531 AND (COMP2521 OR COMP1927) AND 102UOC",
    "COMP3901": "12UOC IN COMP1 AND 18UOC IN COMP2",
    "COMP3902": "COMP3901 AND 12UOC IN COMP3",
    "COMP4121": "COMP3121 OR COMP3821",
    "COMP4128": "COMP3821 OR (COMP3121 AND 12UOC IN COMP3)",
    "COMP4141": "MATH1081 AND (COMP1927 OR COMP2521)",
    "COMP4161": "18UOC",
    "COMP4336": "COMP3331",
    "COMP4418": "COMP3411",
    "COMP4601": "(COMP2511 OR COMP2911) AND 24UOC",
    "COMP4951": "36UOC IN COMP",
    "COMP4952": "COMP4951",
    "COMP4953": "COMP4952",
    "COMP9301": "12UOC IN (COMP6443, COMP6843, COMP6445, COMP6845, COMP6447)",
    "COMP9302": "(COMP6441 OR COMP6841) AND 12UOC IN (COMP6443, COMP6843, COMP6445, COMP6845, COMP6447)",
    "COMP9417": "MATH1081 AND ((COMP1531 OR COMP2041) OR (COMP1927 OR COMP2521))",
    "COMP9418": "MATH5836 OR COMP9417",
    "COMP9444": "COMP1927 OR COMP2521 OR MTRN3500",
    "COMP9447": "COMP6441 OR COMP6841 OR COMP3441",
    "COMP9491": "18UOC IN (COMP9417, COMP9418, COMP9444, COMP9447)"
}

class Parser(object):
    def __init__(self, whole_req: str):
        reqs = re.sub(r'\s+', ' ', whole_req.upper().strip()) # Capitalise and remove multiple spaces
        reqs = re.sub(r'PR[A-Z-]*:*\s*', '', reqs) # Remove redundant "prerequisite:"
        reqs = re.sub(r'(\d+)\s*(?:UOC|U.*?\b (?:\b.*?\b )?CR.*?\b)(?# IN [A-Z]{4})', r'\1UOC', reqs)
        reqs = re.sub(r'(\d+)UOC IN L.*?\b ([1-9]) ([A-Z]{4}) (?:COURS.*?\b)', r'\1UOC IN \3\2', reqs)
        reqs = re.sub(r'\b([1-9][0-9]{3})\b', r'COMP\1', reqs) # Assume it's a COMP course if bare 4 digit code
        reqs = re.sub(r'\b(COURS.*?)\b', r'', reqs) # Remove redundant "courses"
        reqs = re.sub(r'COMPLE.*?\b (?:OF)? (?=\d+)', '', reqs) # Remove redundant "completion of"
        self.tokens = re.sub(r'[.!]*$', r'', reqs.strip()).split()

    def lex(self, string: str):
        tok_buffer = []
        for i, token in self.tokens:
            if re.fullmatch(r"[A-Z]{4}[1-9][0-9]{3}", "".join(buffer)):
                pass

if __name__ == "__main__":
    with open("./conditions.json") as f:
        CONDITIONS: Dict = json.load(f)
        f.close()
    for name, dirty_reqs in CONDITIONS.items():
        p = Parser(dirty_reqs)
        try:
            assert(p.tokens == expected[name])
        except:
            print(f"{name} failed. Expected\n{expected[name]} but got\n{p.tokens}\n")
