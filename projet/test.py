# -*- coding: utf-8 -*-
"""
Code modifiable.
Vous avez dans le dossier test des fichiers 
qui permettent de tester vos fonctions.
Pour cela il suffit de décommenter le code 
de la fonction que vous souhaiter tester
"""

from automate import Automate
from state import State
from transition import Transition
from parser import *
#from essai import Essai

#import projet

print "DEBUT PROGRAMME\n"


s = State(1, False, False)
s2=State(1, True, False)
t = Transition(s,"a",s)
t2=Transition(s,"a",s2)
s.insertPrefix(2)
a= Automate([t,t2])
a.prefixStates(3)
a.show("justep")

"""
print "etat s " + s.id
print "s "+ str(s)
print "t "+ str(t)
print "a "+ str(a)
"""

print "s=s2? "+ str(s==s2)
print "t=t2? "+ str(t==t2)

s1=State(1, True, False)
s2=State(2, False, True)
t1= Transition(s1,"a",s1)
t2=Transition(s1,"a",s2)
t3=Transition(s1,"b",s2)
t4=Transition(s2,"a", s2)
t5=Transition(s2,"b",s2)
liste = [t1,t2,t3,t4,t5]
a=Automate(listStates=[], label="a", listTransitions=liste) 

print "a : "
print a
print a.listStates
#print a.getListStates()
#print a.getSetStates()
print a.getListInitialStates()
print a.getListFinalStates()
print a.getListTransitionsFrom(s1)
#a.show("nouvela")
a.prefixStates(0)
a.show("prefixe")



a.removeTransition(t5)
print a
a.removeTransition(t5)
print a

a.addTransition(t5)
print a

a.addTransition(Transition(s2,"c", s1))
print a

a.addTransition(Transition(s2,"c",s1))
print a 
#t = Transition("a", )

"""
#a.show("essai")
print a.succ1(s1,"a")
print a.succ1(s2,"c")
list = [s1,s2]
print a.succ(list,"c")
print a.succ(list,"b")
print "etats accessibles"
print a.acc()

print Automate.accepte(a, "abc")
print Automate.accepte(a, "aaabbcb")
print Automate.accepte(a, "abs")
"""

"""
print Automate.estComplet(a,["a","b","c"])
print Automate.estComplet(a, ["0","1"])
print Automate.estComplet(a, ["a","b"])
"""
print "Deterministe"
print Automate.estDeterministe(a)

#b=Automate.completeAuto(a,["a","b","c"])
#a.show("automate_a")
#b.show("b=a_aprescompletion")
#print b
"""
print b.getAlphabetFromTransitions()
print "etats accessibles"
print b.acc()
print Automate.accepteVide(b)
#b.show("automate_b")

print "determinisation"
c = Automate.determinisation(b)
#c.show("Determinisationb")
"""
"""
s3 = State("3",True,False)
c=Automate([])
c.addTransition(Transition(s3,"a",s3))
c.addTransition(Transition(s3,"b",s3))
s4 = State("4",False,True)
c.addTransition(Transition(s3,"c",s4))
c.show("automate_c")

d = Automate.unionND(b,c)
d.show("unionND_b_c")
#b.show("b_apres")

"""


my_parser=Parser.Auto()
result = my_parser("#E: 4 1 5 #I: 1 2 #F: 3 4 #T: (1 2 2)")
#result = my_parser("#E:ab c #I:z r #F:a ab #T: (1 a 2)")
#result = my_parser("E:42 12 3")
#result = my_parser("E: Q1 Q2 Q3 -I: Q1 Q2")
print "result ",result


fichier = open("../../test/testDeter.txt")
s = fichier.read()
print s
result = my_parser(s)
print result
fichier.close()

automate = Automate.creationAutomate("../../test/testDeter.txt")
print "AUTOMATE CREATION"
print automate 
automate.prefixStates(0)
print "PREFIXE"
print automate
automate.show("parser")


"""
print "\n TEST ACCEPTE_MOT \n"
a = Automate.initAutomate("test/testDeter.txt")
res = projet.accepteMot(a,"aaa")
print "Le mot aaa est il accepté par l'automate? => " + str (res)
res = projet.accepteMot (a,"aab")
print "Le mot aab est il accepté par l'automate? => " + str (res) + "\n"



print "\n TEST EST_COMPLET \n"
res = projet.estComplet(a)
if res == True :
	print "L'automate est complet."
else :
	print "L'automate n'est pas complet."



print "\n TEST EST_DETERMINISTE \n"
res = projet.estDeterministe(a)
if res == True :
	print "L'automate est déterministe."
else :
	print "L'automate n'est pas déterministe."



print "\n TEST DETERMINISATION \n"
a = Automate.initAutomate("test/testDeter.txt")
b = projet.determinisation(a)

a.affiche ("aavDeter")
b.affiche("apDeter")



print "\n TEST INTERSECTION \n"
c = Automate.initAutomate("test/testInterbis1.txt")
d = Automate.initAutomate("test/testInter2.txt")
e = projet.intersection(c,d)

c.affiche("aavInter1")
d.affiche("aavInter2")
e.affiche("apInter")



print "\n TEST UNION \n"
f = Automate.initAutomate("test/testUnion12.txt")
g = Automate.initAutomate("test/testUnion22.txt")
h = projet.union(f,g)

f.affiche("aavUnion1")
g.affiche("aavUnion2")
h.affiche("apUnion")



print "\n TEST COMPLEMENTAIRE \n"
i = Automate.initAutomate("test/testCompl.txt")
j = projet.complementaire(i)

i.affiche("aavCompl")
j.affiche("apCompl")



print "\n TEST PRODUIT \n"

k = Automate.initAutomate("test/testProduit11.txt")
l = Automate.initAutomate("test/testProduit21.txt")
m = projet.produit(k,l)

k.affiche("aavProduit11")
l.affiche("aavProduit21")
m.affiche("apProduit1")

p = Automate.initAutomate("test/testProduit1.txt")
q = Automate.initAutomate("test/testProduit2bis.txt")
r = projet.produit(p,q)

p.affiche("aavProduit1")
q.affiche("aavProduit2")
r.affiche("apProduit")



print "\n TEST SONT_EQUIVALENTS \n"
res = projet.sontEquivalents(k,m)
print "L'automate k et l'automate produit sont équivalents? => " + str(res)

res2 = projet.sontEquivalents(k,k)
print "L'automate k et l'automate k sont équivalents? => " + str(res2)



print "\n TEST ETOILE \n"
n = Automate.initAutomate("test/testEtoile.txt")
o = projet.etoile(n)

n.affiche("aavEtoile")
o.affiche("apEtoile")
"""



print "\nFIN PROGRAMME\n"
