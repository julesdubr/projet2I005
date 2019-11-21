# -*- coding: utf-8 -*-
"""
Code de test des fonctions.
"""

from automate import Automate
from state import State
from transition import Transition

print("\nDEBUT PROGRAMME\n")


s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)
t1 = Transition(s0, "a", s0)
t2 = Transition(s0, "a", s1)
t3 = Transition(s1, "a", s2)
t4 = Transition(s1, "b", s2)
t5 = Transition(s2, "b", s1)

states = [s0, s1, s2]
trans = [t1, t2, t3, t4, t5]

auto = Automate(trans, label="auto")
complet = Automate.completeAutomate(auto,"ab")

auto.show("auto")
complet.show("complet")

print("FIN PROGRAMME\n")