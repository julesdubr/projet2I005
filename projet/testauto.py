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

# cmplt = Automate.completeAutomate(auto1,"ab")
# deter = Automate.determinisation(auto3)
# cmplm = Automate.complementaire(auto1, auto.getAlphabetFromTransitions())
# inter = Automate.intersection(auto1, auto2)
union = Automate.union(auto1, auto2)
# conca = Automate.concatenation(auto1, auto2)

# auto1.show("auto1")
auto3.show("auto3")
# deter.show("determinisation")
# cmplm.show("complementaire")
# inter.show("intersection")
union.show("union")
# conca.show("concatenation")

print("\n/!\ Automates prets pour detruire le monde /!\\\n")