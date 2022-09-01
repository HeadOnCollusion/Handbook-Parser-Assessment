import re

"""
{
    "COMP1511": "",
    "COMP1521": "COMP1511 OR DPST1091 OR COMP1911 OR COMP1917",
    "COMP1531": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP2041": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921.",
    "COMP2111": "MATH1081 AND (COMP1511 OR DPST1091 OR COMP1917 OR COMP1921)",
    "COMP2121": "COMP1917 OR COMP1921 OR COMP1511 OR DPST1091 OR COMP1521 OR DPST1092 OR (COMP1911 AND MTRN2500)",
    "COMP2511": "COMP1531 AND (COMP2521 OR COMP1927)",
    "COMP2521": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP3121": "COMP1927 OR COMP2521.",
    "COMP3131": "COMP2511 OR COMP2911",
    "COMP3141": "COMP1927 OR COMP2521.",
    "COMP3151": "COMP1927 OR ((COMP1521 OR DPST1092) AND COMP2521)",
    "COMP3153": "MATH1081",
    "COMP3161": "COMP2521 OR COMP1927",
    "COMP3211": "COMP3222 OR ELEC2141",
    "COMP3900": "COMP1531 AND (COMP2521 OR COMP1927) AND 102 units of credit",
    "COMP3901": "12 units of credit in level 1 COMP courses AND 18 units of credit in level 2 COMP courses",
    "COMP3902": "COMP3901 AND 12 units of credit in level 3 COMP courses",
    "COMP4121": "COMP3121 OR COMP3821",
    "COMP4128": "COMP3821 OR (COMP3121 AND 12 units of credit in level 3 COMP courses)",
    "COMP4141": "MATH1081 AND (COMP1927 OR COMP2521)",
    "COMP4161": "Completion of 18 units of credit",
    "COMP4336": "COMP3331.",
    "COMP4418": "COMP3411",
    "COMP4601": "(COMP2511 OR COMP2911) AND completion of 24 units of credit",
    "COMP4951": "36 units of credit in COMP courses",
    "COMP4952": "4951",
    "COMP4953": "4952",
    "COMP9301": "12 units of credit in (COMP6443, COMP6843, COMP6445, COMP6845, COMP6447)",
    "COMP9302": "(COMP6441 OR COMP6841) AND 12 units of credit in (COMP6443, COMP6843, COMP6445, COMP6845, COMP6447)",
    "COMP9417": "MATH1081 AND ((COMP1531 OR COMP2041) OR (COMP1927 OR COMP2521))",
    "COMP9418": "MATH5836 OR COMP9417",
    "COMP9444": "COMP1927 OR COMP2521 OR MTRN3500",
    "COMP9447": "COMP6441 OR COMP6841 OR COMP3441",
    "COMP9491": "18 units oc credit in (COMP9417, COMP9418, COMP9444, COMP9447)"
}
"""

class Parser(object):
    def __init__(self, whole_req: str):
        tokens1 = re.sub(r'\s+', ' ', whole_req.upper())
        tokens2 = re.sub(r'PR[A-Z-]*:*\s*', '', tokens1)
        tokens3 = re.sub(r'(\d+)\s*(?:UOC|U.*?\b \b.*?\b CR.*?\b)', r'\1UOC', tokens2)
        tokens4 = re.sub(r'(\d+)UOC IN L.*?\b ([1-9]) ([A-Z]{4}) (?:COURS.*?\b)', r'\1UOC IN \3\2', tokens3)
        self.tokens = re.sub(r'COMPLE.*?\b (?:OF)? (?=\d+)', '', tokens4)
        print(self.tokens)

    def lex(self, string: str):
        tok_buffer = []
        for i, token in self.tokens:
            if re.fullmatch(r"[A-Z]{4}[1-9][0-9]{3}", "".join(buffer)):
                pass

if __name__ == "__main__":
    Parser("COMP1511    or DPST1091 or COMP1911 or COMP1917")
    Parser("MATH1081 AND    (COMP1511 OR DPST1091 OR COMP1917 OR COMP1921)")
    Parser("COMP1927    OR ((COMP1521 or DPST1092) AND COMP2521)")
    Parser("Pre-requisite: MATH1081 and (COMP1927 or COMP2521)")
    Parser("COMP1531 AND (COMP2521 OR COMP1927) AND 102 units of credit")
    Parser("18 units oc credit in (COMP9417, COMP9418, COMP9444, COMP9447)")
    Parser("(COMP6441 OR COMP6841) AND 12 units of credit in (COMP6443, COMP6843, COMP6445, COMP6845, COMP6447)")
    Parser("Prerequisite: 12 units of credit in  level 1 COMP courses and 18 units of credit in level 2 COMP courses")
    Parser("(COMP2511 or COMP2911) and completion of 24 units of credit")
