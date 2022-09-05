import json, re
from typing import Dict, List, Optional

from handbook import NodeType, RequirementNode
from hardcode_course_reqs import EXPECTED_RE

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
        '''
        Looks at requirements token by token (separated by space) in ONE pass
        and creates a RequirementNode tree.
        '''
        tok_buffer: List['RequirementNode'] = []
        unused_tokens: List['str'] = []
        mode: NodeType = NodeType.LEAF
        
        while True:
            try:
                token = next(self.gen_tokens())
                if token == "(":
                    node = self.parse()
                    # Check if it's a "xUOC IN (COURSE0001 OR COURSE0002)" construction
                    if len(unused_tokens) == 2:
                        assert(m := re.fullmatch(r"(\d+)UOC", unused_tokens[0]))
                        uoc = int(m.group(1))
                        assert(node.type is NodeType.OR)
                        # Turns out it is. Same as normal OR node, except with non-0 uoc property.
                        node.uoc = uoc
                        unused_tokens = []
                        
                    tok_buffer.append(node)
                elif token == ")":
                    break
                elif len(unused_tokens) == 1 or len(unused_tokens) == 2:
                    dbg(unused_tokens)
                    Parser.parse_UOC_req(unused_tokens, tok_buffer, token)
                elif re.fullmatch(r"\d+UOC", token):
                    # We dont' know yet if it's a lone xUOC, or xUOC in ABCD[1-9]? or xUOC in (GRUP0001 OR ...)
                    unused_tokens.append(token)
                elif re.fullmatch(r"[A-Z]{4}[1-9][0-9]{3}", token):
                    tok_buffer.append(RequirementNode(NodeType.LEAF, pre_subj=token))
                elif m := re.fullmatch(r"AND", token):
                    # Assumes that each layer only has one of AND and OR i.e.
                    # None of this: "ABC OR DEF AND GHI" -> "ABC OR (DEF AND GHI)" is valid though. 
                    mode = NodeType.AND
                elif m := re.fullmatch(r"OR", token):
                    mode = NodeType.OR
            except StopIteration:
                break
        
        if len(unused_tokens) == 1:
            dbg(f"had unused tokens at end")
            Parser.parse_UOC_req(unused_tokens, tok_buffer)
        else:
            assert(len(unused_tokens) == 0)
            
        if tok_buffer:
            if len(tok_buffer) == 1:
                # Leaf node
                return tok_buffer[0]
            else:
                # AND/OR node with multiple children
                return RequirementNode(mode, children=tok_buffer)
        else:
            return RequirementNode(NodeType.LEAF)

    @staticmethod
    def parse_UOC_req(unused_tokens: List[str], tok_buffer: List['RequirementNode'], token: Optional[str]=None):
        assert(m := re.fullmatch(r"(\d+)UOC", unused_tokens[0]))
        uoc = int(m.group(1))
    
        if len(unused_tokens) == 1:
            if token == "IN":
                unused_tokens.append(token)
                return
            
            # An AND/OR/None (end of requirement string) token terminates a lone xUOC token
            assert(token == "AND" or token == "OR" or token is None)           
            tok_buffer.append(RequirementNode(NodeType.LEAF, uoc=uoc))
            unused_tokens = []
        else:
            # Dealing with a xUOC IN ABCD[1-9]? construction here
            # xUOC IN (GRUP0001 OR ...) is handled with the brackets logic
            assert(len(unused_tokens) == 2)
            if not (token and re.match(r'[A-Z]{4}\d{0,1}', token)):
                print(f"unexpectedly got {token=}")
            tok_buffer.append(RequirementNode(NodeType.LEAF, uoc=uoc, pre_subj=token))
            unused_tokens.clear()
        
    def gen_tokens(self):
        '''
        Yields the tokens of the requirement string one by one in ONE pass
        global of any recursive calls of parse().
        '''
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
        if ' '.join(p.tokens) != EXPECTED_RE[name]:
            raise Exception(f"{name} failed. Expected\n{EXPECTED_RE[name]} but got\n{' '.join(p.tokens)}\n")
        
        if name:
            print(f"==={name}===")
            p.parse().print_req_structure()
            