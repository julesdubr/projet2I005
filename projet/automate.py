# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase


#TEST DE MODIF D'UN FICHIER ...

class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ(self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        successeurs = []
        # # s: Etats
        for state in listStates:
            for t in self.getListTransitionsFrom(state):
                if t.etiquette == lettre and t.stateDest not in successeurs:
                    successeurs.append(t.stateDest)
        return successeurs



    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """        
        res = auto.getListInitialStates()

        for l in mot:
            res = auto.succ(res, l)

        return State.isFinalIn(res)



    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        for state in auto.listStates:
            for a in alphabet:
                if auto.succElem(state, a) == []:
                    return False
        return True



    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        alphabet = auto.getAlphabetFromTransitions()
        for a in alphabet:
            for state in auto.listStates:
                if len(auto.succElem(state,a)) > 1:
                    return False
        return True
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        autocopy = copy.deepcopy(auto)
        puitId = 0
        for state in auto.listStates:
            if puitId <= state.id:
                puitId = state.id + 1

        puit = State(puitId, False, False, "puit")
        autocopy.addState(puit)

        for state in autocopy.listStates:
            for a in alphabet:
                if autocopy.succElem(state, a) == []:
                    t = Transition(state, a, puit)
                    autocopy.addTransition(t)
            
        return autocopy



    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        alphabet = auto.getAlphabetFromTransitions()

        etatsInit = set(auto.getListInitialStates())
        etatsATraiter = [ etatsInit ]
        dejaTraites = []

        listeEtats = [ State(0, True, State.isFinalIn(etatsInit), str(etatsInit)) ]
        listeTrans = []

        while etatsATraiter != []:
            setSrc = etatsATraiter.pop()        # on récupère un set d'états aléatoire parmis les états à traiter
            dejaTraites.append(setSrc)          # on l'ajoute à la liste des états déjà traités
            for etat in listeEtats:             # on récupère l'indice dans listeEtats de l'état source correspondant
                if str(etat.label) == str(setSrc):
                    idSrc = listeEtats.index(etat)

            for lettre in alphabet:
                setDst = set(auto.succ(setSrc, lettre))     # on récupère le set d'états d'arrivée     
                if setDst != set():
                    if setDst not in dejaTraites:           # on l'ajoute aux états a traiter si on ne l'a pas déja traité
                        etatsATraiter.append(setDst)

                    isIn = False
                    for etat in listeEtats:     # si l'état dest existe déjà on récupère son indice
                        if str(etat.label) == str(setDst):
                            isIn = True
                            listeTrans.append(Transition(listeEtats[idSrc], lettre, listeEtats[listeEtats.index(etat)]))

                    if not isIn:                # sinon on le crée
                        listeEtats.append(State(len(listeEtats), False, State.isFinalIn(setDst), str(setDst)))
                        listeTrans.append(Transition(listeEtats[idSrc], lettre, listeEtats[-1]))

        return Automate(listeTrans)



    @staticmethod
    def complementaire(auto, alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        autoComplementaire = Automate.completeAutomate(Automate.determinisation(auto), alphabet)
        for state in autoComplementaire.listStates:
            state.fin = not state.fin

        return autoComplementaire
     


    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        alphabet = auto0.getAlphabetFromTransitions()
        
        etatsInit = list(product(auto0.getListInitialStates(), auto1.getListInitialStates()))
        etatsFinal = list(product(auto0.getListFinalStates(), auto1.getListFinalStates()))

        etatsATraiter = etatsInit
        dejaTraites = []

        listeEtats = [ State(0, True, etat in etatsFinal, str(etat)) for etat in etatsInit ]
        listeTrans = []
        
        while etatsATraiter != []:
            coupleSrc = etatsATraiter.pop()     # on récupère un couple d'états aléatoire parmis les états à traiter
            dejaTraites.append(coupleSrc)       # on l'ajoute à la liste des états déjà traités
            for etat in listeEtats:             # on récupère l'indice dans listeEtats de l'état source correspondant
                if str(etat.label) == str(coupleSrc):
                    idSrc = listeEtats.index(etat)

            for lettre in alphabet:
                setDst0 = auto0.succElem(coupleSrc[0], lettre)  # le set d'états d'arrivée partant de l'état source de l'auto0
                setDst1 = auto1.succElem(coupleSrc[1], lettre)  # le set d'états d'arrivée partant de l'état source de l'auto0
                couplesDst = set(product(setDst0, setDst1))     # le produit des ensembles d'arrivée

                if couplesDst != set():
                    for couple in couplesDst:           # on ajoute le couple aux états à traiter si on ne l'a jamais traité
                        if couple not in dejaTraites:
                            etatsATraiter.append(couple)

                        isIn = False
                        for etat in listeEtats:
                            if str(etat.label) == str(couple):  # si l'état des existe déjà on récupère son indice
                                isIn = True
                                listeTrans.append(Transition(listeEtats[idSrc], lettre, listeEtats[listeEtats.index(etat)]))
                        
                        if not isIn:                            # sinon on le crée
                            isFinal = (couple[0].fin == True and couple[1].fin == True)
                            listeEtats.append(State(len(listeEtats), False, isFinal, str(couple)))
                            listeTrans.append(Transition(listeEtats[idSrc], lettre, listeEtats[-1]))
            
        return Automate(listeTrans)



    @staticmethod
    def union (auto0, auto1):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        auto0_copie = copy.deepcopy(auto0)
        auto1_copie = copy.deepcopy(auto1)
        listeTrans = []

        # modification des états initiaux et finaux
        for etat in list(set(auto0_copie.listStates + auto1_copie.listStates)):
            etat.init = etat in list(set(auto0_copie.getListInitialStates() + auto1_copie.getListInitialStates()))
            etat.fin = etat in list(set(auto0_copie.getListFinalStates() + auto1_copie.getListFinalStates()))

        # union des transitions
        for trans in auto0_copie.listTransitions + auto1_copie.listTransitions:
            if trans not in listeTrans:
                listeTrans.append(trans)

        return Automate(listeTrans)



    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage la concatenation des langages des deux automates
        """
        auto1_copie = copy.deepcopy(auto1)
        auto2_copie = copy.deepcopy(auto2)
        listeTrans = auto1_copie.listTransitions + auto2_copie.listTransitions
    
        # modification des ids
        idMax = 0
        for etat in auto1_copie.listStates:
            idMax = max(idMax, etat.id + 1)
        for etat in auto2_copie.listStates:
            etat.id = idMax
            etat.label = etat.id
            idMax += 1

        # transitions vers les états finaux de l'auto1 copiées vers initaux de l'auto2
        for trans in auto1_copie.listTransitions:
            if trans.stateDest in auto1.getListFinalStates():
                for etat in auto2_copie.getListInitialStates():
                    listeTrans.append(Transition(trans.stateSrc, trans.etiquette, etat))

        # modification des états initiaux et finaux
        if not Automate.accepte(auto2, ""):     
            for etat in auto1_copie.getListFinalStates():
                etat.fin = False
        if not Automate.accepte(auto1, ""):     
            for etat in auto2_copie.getListFinalStates():
                etat.init = False

        return Automate(listeTrans)



    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        autoEtoile = Automate.concatenation(auto, auto)
        autoEtoile.addState(State(len(autoEtoile.listStates) + 1, True, True, "eps"))
        return autoEtoile
