"""
====================TESTS====================
You may add your own tests if you would like.
"""
from handbook import is_unlocked

def test_no_reqs():
    assert is_unlocked([], "COMP1511") == True
    print("COMP1511 passed")
    
def test_single_reqs():
    assert is_unlocked([], "COMP3153") == False
    assert is_unlocked(["MATH1081"], "COMP3153") == True
    print("COMP3153 passed")
    
    assert is_unlocked(["COMP1511"], "COMP4952") == False
    assert is_unlocked(["COMP4951"], "COMP4952") == True
    print("COMP4952 passed")

def test_simple_OR_AND():
    assert is_unlocked([], "COMP1521") == False
    assert is_unlocked(["MATH1081", "ENGG1000"], "COMP1521") == False
    assert is_unlocked(["COMP1511"], "COMP1521") == True
    assert is_unlocked(["COMP1511", "COMP2521"], "COMP1521") == True
    assert is_unlocked(["MATH1081", "ENGG1000", "COMP1911"], "COMP1521") == True
    print("COMP1521 passed")
    
    assert is_unlocked([], "COMP2511") == False
    assert is_unlocked(["COMP1531"], "COMP2511") == False
    assert is_unlocked(["COMP2521", "MATH1241"], "COMP2511") == False
    assert is_unlocked(["COMP1531", "COMP1927"], "COMP2511") == True
    assert is_unlocked(["COMP1531", "ENGG1000", "COMP2521"], "COMP2511") == True
    print("COMP2511 passed")

def test_UOC_leaves():
    assert is_unlocked(["COMP1511", "COMP2521", "COMP3121"], "COMP4128") == False
    assert is_unlocked(["COMP1511", "COMP2521", "COMP3821"], "COMP4128") == True
    assert is_unlocked(["COMP1511", "COMP2521", "COMP3121", "COMP3311"], "COMP4128") == True
    print("COMP4128 passed")
    assert is_unlocked(["COMP1511", "COMP1531", "COMP2511"], "COMP4601") == False
    assert is_unlocked(["COMP2911"], "COMP4601") == False
    assert is_unlocked(["COMP1511", "COMP1531", "COMP2521", "COMP2511"], "COMP4601") == True
    print("COMP4601 passed")


def test_UOC_ors():
    assert is_unlocked(["COMP6441", "COMP6443", "COMP3121"], "COMP9302") == False
    assert is_unlocked(["COMP1511", "COMP6841", "COMP6843", "COMP6445"], "COMP9302") == True
    assert is_unlocked(["COMP6841", "COMP2521", "COMP6445", "COMP6447"], "COMP9302") == True
    print("COMP9302 passed")
    assert is_unlocked(["COMP9315", "COMP9417", "COMP9418"], "COMP9491") == False
    assert is_unlocked(["COMP9315", "COMP9417", "COMP9418", "COMP9444"], "COMP9491") == True
    assert is_unlocked(["COMP9418", "COMP9444", "COMP9447"], "COMP9491") == True
    print("COMP9491 passed")

    
##############################################################

def test_empty():
    # assert is_unlocked([], "COMP1511") == True
    assert is_unlocked([], "COMP9301") == False

def test_single():
    assert is_unlocked(["MATH1081"], "COMP3153") == True
    assert is_unlocked(["ELEC2141"], "COMP3211") == True
    assert is_unlocked(["COMP1511", "COMP1521", "COMP1531"], "COMP3153") == False

def test_compound():
    assert is_unlocked(["MATH1081", "COMP1511"], "COMP2111") == True
    assert is_unlocked(["COMP1521", "COMP2521"], "COMP3151") == True
    assert is_unlocked(["COMP1917", "DPST1092"], "COMP3151") == False

def test_simple_uoc():
    assert is_unlocked(["COMP1511", "COMP1521", "COMP1531", "COMP2521"], "COMP4161") == True
    assert is_unlocked(["COMP1511", "COMP1521"], "COMP4161") == False

def test_annoying_uoc():
    assert is_unlocked(["COMP9417", "COMP9418", "COMP9447"], "COMP9491") == True
    assert is_unlocked(["COMP6441"], "COMP9302") == False
    assert is_unlocked(["COMP6441", "COMP64443", "COMP6843", "COMP6445"], "COMP9302") == True
    assert is_unlocked(["COMP1234", "COMP5634", "COMP4834"], "COMP9491") == False
    assert is_unlocked(["COMP3901"], "COMP3902") == False
    assert is_unlocked(["COMP3901", "COMP6441", "COMP6443"], "COMP3902") == False
    assert is_unlocked(["COMP3901", "COMP3441", "COMP3443"], "COMP3902") == True

def test_cross_discipline():
    assert is_unlocked(["COMP1911", "MTRN2500"], "COMP2121") == True
    assert is_unlocked(["COMP1521"], "COMP2121") == True

if __name__ == '__main__':
    test_no_reqs()
    test_single_reqs()
    test_simple_OR_AND()
    test_UOC_leaves()
    test_UOC_ors()
