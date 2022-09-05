import json, re
from os import stat
from typing import Dict, List, Literal, Optional, Union

from handbook import NodeType, RequirementNode

expected = {
    "COMP1511": "",
    "COMP1521": "COMP1511 OR DPST1091 OR COMP1911 OR COMP1917",
    "COMP1531": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP2041": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP2111": "MATH1081 AND ( COMP1511 OR DPST1091 OR COMP1917 OR COMP1921 )",
    "COMP2121": "COMP1917 OR COMP1921 OR COMP1511 OR DPST1091 OR COMP1521 OR DPST1092 OR ( COMP1911 AND MTRN2500 )",
    "COMP2511": "COMP1531 AND ( COMP2521 OR COMP1927 )",
    "COMP2521": "COMP1511 OR DPST1091 OR COMP1917 OR COMP1921",
    "COMP3121": "COMP1927 OR COMP2521",
    "COMP3131": "COMP2511 OR COMP2911",
    "COMP3141": "COMP1927 OR COMP2521",
    "COMP3151": "COMP1927 OR ( ( COMP1521 OR DPST1092 ) AND COMP2521 )",
    "COMP3153": "MATH1081",
    "COMP3161": "COMP2521 OR COMP1927",
    "COMP3211": "COMP3222 OR ELEC2141",
    "COMP3900": "COMP1531 AND ( COMP2521 OR COMP1927 ) AND 102UOC",
    "COMP3901": "12UOC IN COMP1 AND 18UOC IN COMP2",
    "COMP3902": "COMP3901 AND 12UOC IN COMP3",
    "COMP4121": "COMP3121 OR COMP3821",
    "COMP4128": "COMP3821 OR ( COMP3121 AND 12UOC IN COMP3 )",
    "COMP4141": "MATH1081 AND ( COMP1927 OR COMP2521 )",
    "COMP4161": "18UOC",
    "COMP4336": "COMP3331",
    "COMP4418": "COMP3411",
    "COMP4601": "( COMP2511 OR COMP2911 ) AND 24UOC",
    "COMP4951": "36UOC IN COMP",
    "COMP4952": "COMP4951",
    "COMP4953": "COMP4952",
    "COMP9301": "12UOC IN ( COMP6443 OR COMP6843 OR COMP6445 OR COMP6845 OR COMP6447 )",
    "COMP9302": "( COMP6441 OR COMP6841 ) AND 12UOC IN ( COMP6443 OR COMP6843 OR COMP6445 OR COMP6845 OR COMP6447 )",
    "COMP9417": "MATH1081 AND ( ( COMP1531 OR COMP2041 ) OR ( COMP1927 OR COMP2521 ) )",
    "COMP9418": "MATH5836 OR COMP9417",
    "COMP9444": "COMP1927 OR COMP2521 OR MTRN3500",
    "COMP9447": "COMP6441 OR COMP6841 OR COMP3441",
    "COMP9491": "18UOC IN ( COMP9417 OR COMP9418 OR COMP9444 OR COMP9447 )"
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
        reqs = re.sub(r'\(', ' ( ', reqs) # Expand brackets
        reqs = re.sub(r'\)', ' ) ', reqs)
        reqs = re.sub(r',', ' OR ', reqs)
        reqs = re.sub(r'\s+', ' ', reqs) # Remove multiple spaces again
        self.tokens = re.sub(r'[.!]*$', r'', reqs.strip()).split()
        self.i = 0
        
    def parse(self) -> 'RequirementNode':
        tok_buffer: List['RequirementNode'] = []
        unused_tokens: List['str'] = []
        mode: NodeType = NodeType.LEAF
        
        while True:
            try:
                token = next(self.gen_tokens())
                if token == "(":
                    node = self.parse()
                    if len(unused_tokens) == 2:
                        assert(m := re.fullmatch(r"(\d+)UOC", unused_tokens[0]))
                        uoc = int(m.group(1))
                        assert(node.type is NodeType.OR)
                        node.uoc = uoc
                        unused_tokens = []
                    tok_buffer.append(node)
                elif token == ")":
                    break
                elif len(unused_tokens) == 1 or len(unused_tokens) == 2:
                    dbg(unused_tokens)
                    Parser.foo(unused_tokens, tok_buffer, token)
                elif re.fullmatch(r"\d+UOC", token):
                    unused_tokens.append(token)
                elif re.fullmatch(r"[A-Z]{4}[1-9][0-9]{3}", token):
                    tok_buffer.append(RequirementNode(NodeType.LEAF, pre_subj=token))
                elif m := re.fullmatch(r"AND", token):
                    mode = NodeType.AND
                elif m := re.fullmatch(r"OR", token):
                    mode = NodeType.OR
            except StopIteration:
                break
        
        if len(unused_tokens) == 1:
            dbg(f"unused tokens at end")
            Parser.foo(unused_tokens, tok_buffer)
        else:
            assert(len(unused_tokens) == 0)
        if tok_buffer:
            if len(tok_buffer) == 1:
                return tok_buffer[0]
            else:
                return RequirementNode(mode, children=tok_buffer)
        else:
            return RequirementNode(NodeType.LEAF)

    @staticmethod
    def foo(unused_tokens: List[str], tok_buffer: List['RequirementNode'], token: Optional[str]=None):
        assert(m := re.fullmatch(r"(\d+)UOC", unused_tokens[0]))
        uoc = int(m.group(1))
    
        if len(unused_tokens) == 1:
            if token == "IN":
                unused_tokens.append(token)
                return
            
            if token is None:
                pass
            else:    
                assert(token == "AND" or token == "OR")           
            tok_buffer.append(RequirementNode(NodeType.LEAF, uoc=uoc))
            unused_tokens = []
        else:
            if not (token and re.match(r'[A-Z]{4}\d{0,3}', token)):
                print(f"unexpectedly got {token=}")
            tok_buffer.append(RequirementNode(NodeType.LEAF, uoc=uoc, pre_subj=token))
            unused_tokens.clear()
        
    def gen_tokens(self):
        while True:
            try:
                yield self.tokens[self.i]
            except:
                break
            finally:
                self.i += 1

DBG = False
def dbg(*args: object):
    if DBG:
        print(*args, flush=True)
              
if __name__ == "__main__":
    DBG = True
    with open("./conditions.json") as f:
        CONDITIONS: Dict = json.load(f)
        f.close()
    for name, dirty_reqs in CONDITIONS.items():
        p = Parser(dirty_reqs)
        if ' '.join(p.tokens) != expected[name]:
            raise Exception(f"{name} failed. Expected\n{expected[name]} but got\n{' '.join(p.tokens)}\n")
        
        if name:
            print(f"==={name}===")
            p.parse().print_req_structure()
            