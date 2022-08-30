from handbook import RequirementNode, NodeType

def make_leaf(pre_subj: str) -> RequirementNode:
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

