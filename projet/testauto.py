# -*- coding: utf-8 -*-
"""
Code de test des fonctions.
"""

from automate import Automate
from state import State
from transition import Transition

print("\nFabrication des automates . . .\n")

# auto1
s0_1 = State(0, True, True)
s1_1 = State(1, False, False)
t1_1 = Transition(s0_1, "a", s0_1)
t2_1 = Transition(s0_1, "b", s1_1)
t3_1 = Transition(s1_1, "a", s1_1)
t4_1 = Transition(s1_1, "b", s0_1)
trans1 = [t1_1, t2_1, t3_1, t4_1]
auto1 = Automate(trans1, label="auto1")

# auto2
s0_2 = State(0, True, False)
s1_2 = State(1, False, True)
t1_2 = Transition(s0_2, "b", s0_2)
t2_2 = Transition(s0_2, "a", s1_2)
t3_2 = Transition(s1_2, "b", s1_2)
t4_2 = Transition(s1_2, "a", s0_2)
trans2 = [t1_2, t2_2, t3_2, t4_2]
auto2 = Automate(trans2, label="auto2")


# auto3
s1_3 = State(1, True, False)
s2_3 = State(2, False, False)
s3_3 = State(3, False, True)
t1_3 = Transition(s1_3, "a", s1_3)
t2_3 = Transition(s1_3, "a", s2_3)
t3_3 = Transition(s2_3, "a", s3_3)
t4_3 = Transition(s2_3, "b", s2_3)
t5_3 = Transition(s3_3, "a", s1_3)
t6_3 = Transition(s3_3, "b", s2_3)
t7_3 = Transition(s3_3, "b", s3_3)
trans3 = [t1_3, t2_3, t3_3, t4_3, t5_3, t6_3, t7_3]
auto3 = Automate(trans3, label="auto3")

# auto4
s0_4 = State(0, True, False)
s1_4 = State(1, False, False)
s2_4 = State(2, False, True)
t1_4 = Transition(s0_4, "a", s0_4)
t2_4 = Transition(s0_4, "b", s1_4)
t3_4 = Transition(s1_4, "a", s2_4)
t4_4 = Transition(s1_4, "b", s1_4)
t5_4 = Transition(s2_4, "a", s2_4)
t6_4 = Transition(s2_4, "b", s2_4)
trans4 = [t1_4, t2_4, t3_4, t4_4, t5_4, t6_4]
auto4 = Automate(trans4, label="auto4")

# auto5
s0_5 = State(0, True, False)
s1_5 = State(1, False, False)
s2_5 = State(2, False, True)
t1_5 = Transition(s0_5, "a", s0_5)
t2_5 = Transition(s0_5, "b", s0_5)
t3_5 = Transition(s0_5, "a", s1_5)
t4_5 = Transition(s1_5, "b", s2_5)
t5_5 = Transition(s2_5, "a", s2_5)
t6_5 = Transition(s2_5, "b", s2_5)
trans5 = [t1_5, t2_5, t3_5, t4_5, t5_5, t6_5]
auto5 = Automate(trans5, label="auto5")


# cmplt = Automate.completeAutomate(auto1,"ab")
# deter = Automate.determinisation(auto3)
# cmplm = Automate.complementaire(auto1, auto1.getAlphabetFromTransitions())
# inter = Automate.intersection(auto4, auto5)
# union = Automate.union(auto1, auto2)
# conca = Automate.concatenation(auto1, auto2)
etoil = Automate.etoile(auto3)

# auto1.show("auto1")
# auto2.show("auto2")
auto3.show("auto3")
# auto4.show("auto4")
# auto5.show("auto5")
# deter.show("determinisation")
# cmplm.show("complementaire")
# inter.show("intersection")
# union.show("union")
# conca.show("concatenation")
etoil.show("etoile")

print("\n/!\ Automates prets extermination humains /!\\\n")