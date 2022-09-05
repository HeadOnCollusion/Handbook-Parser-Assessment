from handbook import RequirementNode, NodeType

def make_leaf(pre_subj: str) -> 'RequirementNode':
    return RequirementNode(NodeType.LEAF, pre_subj=pre_subj)

COMP1511 = make_leaf("COMP1511")
COMP1531 = make_leaf("COMP1531")
COMP1911 = make_leaf("COMP1911")
COMP1917 = make_leaf("COMP1917")
COMP1927 = make_leaf("COMP1927")

COMP2511 = make_leaf("COMP2511")
COMP2521 = make_leaf("COMP2521")
COMP2911 = make_leaf("COMP2911")

COMP3121 = make_leaf("COMP3121")
COMP3821 = make_leaf("COMP3821")

COMP6441 = make_leaf("COMP6441")
COMP6443 = make_leaf("COMP6443")
COMP6445 = make_leaf("COMP6445")
COMP6447 = make_leaf("COMP6447")
COMP6845 = make_leaf("COMP6845")
COMP6841 = make_leaf("COMP6841")
COMP6843 = make_leaf("COMP6843")

COMP9417 = make_leaf("COMP9417")
COMP9418 = make_leaf("COMP9418")
COMP9444 = make_leaf("COMP9444")
COMP9447 = make_leaf("COMP9447")

DPST1091 = make_leaf("DPST1091")

UOC24 = RequirementNode(NodeType.LEAF, uoc=24)
UOC12LVL3COMP = RequirementNode(NodeType.LEAF, uoc=12, pre_subj="COMP3")
COMP1927_OR_2521 = RequirementNode(NodeType.OR, children=[COMP1927, COMP2521])
COMP2511_OR_2911 = RequirementNode(NodeType.OR, children=[COMP2511, COMP2911])
COMP3121_AND_UOC12LVL3COMP = RequirementNode(NodeType.AND,
                            children=[COMP3121, UOC12LVL3COMP])
COMP6441_OR_6841 = RequirementNode(NodeType.OR, children=[COMP6441, COMP6841])
UOC12_IN_GROUP_A = RequirementNode(NodeType.OR, uoc=12, children=[COMP6443, COMP6843,
    COMP6445, COMP6845, COMP6447])

COMP1521_req = RequirementNode(NodeType.OR, children=[COMP1511, DPST1091, COMP1911, COMP1917])
COMP2511_req = RequirementNode(NodeType.AND, children=[COMP1531, COMP1927_OR_2521])
COMP3153_req = RequirementNode(NodeType.LEAF, pre_subj="MATH1081")

COMP4128_req = RequirementNode(NodeType.OR, children=[COMP3821, COMP3121_AND_UOC12LVL3COMP])
COMP4601_req = RequirementNode(NodeType.AND, children=[COMP2511_OR_2911, UOC24])
COMP4952_req = RequirementNode(NodeType.LEAF, pre_subj="COMP4951")

COMP9302_req = RequirementNode(NodeType.AND, children=[COMP6441_OR_6841, UOC12_IN_GROUP_A])
COMP9491_req = RequirementNode(NodeType.OR, uoc=18, children=[COMP9417, COMP9418, COMP9444, COMP9447])

# Expect regex substitutions to arrive at the following:
EXPECTED_RE = {
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
