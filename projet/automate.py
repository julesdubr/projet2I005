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

        puit = State(puitId, False, False,"puit")
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
        
        # ensemble des etats initiaux de auto
        etatsFinaux = {s for s in auto.getListFinalStates()}
        # liste des ensembles d'états à traiter
        etatsATraiter = [{s for s in auto.getListInitialStates()}]

        # compteur des états à traiter
        cpt = 0

        # Liste des états de l'automate déterminisé (initialisé par la liste des états initiaux de auto)
        listeEtats = [State(0, True, len(etatsFinaux & etatsATraiter[0]) > 0, etatsATraiter[0])]
        # Liste des transition de l'automate déterminisé
        listeTrans = []
        
        for S in listeEtats:
            # on crée un dictionnaire (etiquette, destination) pour toutes les transitions de tous les états à traiter
            temp = {(t.etiquette, t.stateDest) for s in etatsATraiter[cpt] for t in auto.getListTransitionsFrom(s) }
            # dictionnaire (étiquette, {destinations})
            tempD = dict()
            for (k, v) in temp:
                if k not in tempD:      # si l'étiquette n'existe pas dans tempD,
                    tempD[k] = {v}      # on crée un ensemble de destination associé à l'étiquette
                else:                   
                    tempD[k].add(v)     # sinon on ajoute la destination à l'ensemble des destinations déja existant

            for k, v in tempD.items():
                if v not in etatsATraiter:      # si l'ensemble des destinations associé à l'étiquette n'est pas dans la liste des ensemble d'états à traiter
                    etatsATraiter.append(v)     # on l'ajoute à la liste
                                                # on crée un nouvel état contenant les destinations de l'étiquette
                                                # et une nouvelle transition d'étiquette k partant de S et allant vers le dernier etat ajouté
                    listeEtats.append(State(len(listeEtats), False, len(etatsFinaux & etatsATraiter[len(listeEtats)]) > 0, etatsATraiter[len(listeEtats)]))
                    listeTrans.append(Transition(S, k, listeEtats[-1]))
                else:
                    # sinon on ajoute une transition d'étiquette k partant de S et allant vers l'ensemble des états correspondant
                    listeTrans.append(Transition(S, k, listeEtats[etatsATraiter.index(v)]))

            # on incrémente le compteur des états à traiter
            cpt += 1

        return Automate(listeTrans)

        # listeTrans = []
        # etatsD = {s for s in auto.getListInitialStates()}
        # etatsATraiter = [{s for s in auto.getListInitialStates()}]

        # while etatsATraiter != []:
        #     P = etatsATraiter.pop(0)
        #     for a in auto.getAlphabetFromTransitions():
        #         P_ = auto.succ(P, a)
        #         t = Transition(P, a, P_)
        #         etatsD.append(P_)
        #         listeTrans.append(t)
        
        # autoD = Automate(listeTrans, etatsD, "autoDetermine")
        # return autoD

    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        autoCompletDeter = Automate.completeAutomate(Automate.determinisation(auto),alphabet)
        for state in autoCompletDeter.listStates:
            state.fin = not state.fin

        return autoCompletDeter
     

    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        inits = list(product(auto0.getListInitialStates(), auto1.getListInitialStates()))
        finals = list(product(auto0.getListFinalStates(), auto1.getListFinalStates()))

        cpt = 0
        cptToTuple = inits
        Ss = []
        Ts = []
        for cpt in range(0, len(inits)):
            Ss.append(State(cpt, True, inits[cpt] in finals, inits[cpt]))


        print(cptToTuple, cptToTuple[0], cptToTuple[0][0], cptToTuple[0][1])
        print(auto0.getListTransitionsFrom(cptToTuple[0][0])[0])

        cpt = 0
        for S in Ss:
            tempLeft = [(t.etiquette, t.stateDest) for t in auto0.getListTransitionsFrom(cptToTuple[cpt][0])]
            tempRight = [(t.etiquette, t.stateDest) for t in auto1.getListTransitionsFrom(cptToTuple[cpt][1])]

            tempDLeft = dict()
            tempDRight = dict()
            for (k, v) in tempLeft:
                if k not in tempDLeft:
                    tempDLeft[k] = {v}
                else:
                    tempDLeft[k].add(v)
            for (k, v) in tempRight:
                if k not in tempDRight:
                    tempDRight[k] = {v}
                else:
                    tempDRight[k].add(v)
            print(tempDLeft, tempDRight)
            for (k, v) in tempDLeft.items():
                if k not in tempDRight: continue
                prod = list(product(list(v), list(tempDRight[k])))
                #print(prod)
                for label in prod:
                    if label not in cptToTuple:
                        cptToTuple.append(label)
                        Ss.append(State(len(Ss), False, label in finals, label))
                        Ts.append(Transition(S, k, Ss[-1]))
                    else:
                        Ts.append(Transition(S, k, Ss[cptToTuple.index(label)]))
            cpt += 1

        return Automate(Ts)


    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return
        

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """

        # Union des états d'auto1 et auto2
        listState = auto1.listStates + auto2.listStates

        # mise à jour des id
        for i in range(len(auto2.listStates)-1, len(listState)):
            if listState[i].id < listState[i-1].id:
                listState[i].id = listState[i-1].id + 1

        # récuperation des transitions vers le final de l'auto1
        listTransToRedirect = []
        listTrans = [] 
        for state in listState:
            for trans in auto1.getListTransitionsFrom(state):
                listTrans.append(trans)
                if trans.stateDest in auto1.getListFinalStates():
                    listTransToRedirect.append(trans)
            
        return Automate(listTrans, listState)

#/////////////////////////////////////////////////////////////////////////////// 

@staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        H: les etats des deux automates ont des ids differents
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        auto1Bis = copy.deepcopy(auto1)
        auto2Bis = copy.deepcopy(auto2)
        areNotEqual = str(auto1Bis) != str(auto2Bis) 
        if areNotEqual:
            Ts = auto1Bis.listTransitions + auto2Bis.listTransitions
        else:
            Ts = auto1Bis.listTransitions
        Ss1 = auto1Bis.listStates
        Ss2 = auto2Bis.listStates
        for s in Ss1:
            ts = auto1Bis.getListTransitionsFrom(s)
            for t in ts:
                if t.stateDest in auto1Bis.getListFinalStates():
                    for i in auto2Bis.getListInitialStates():
                        Ts.append(Transition(t.stateSrc, t.etiquette, i))
        if not Automate.accepte(auto2, "") and areNotEqual:
            for s in Ss1:
                s.fin = False
        if not Automate.accepte(auto1, "") and areNotEqual:
            for s in Ss2:
                s.init = False

        Ss = Ss1 + Ss2
        return Automate(Ts, Ss)

#//////////////////////////////////////////////////////////////////////////////    


    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        autoEtoile = Automate.concatenation(auto, auto)
        autoEtoile.addState(State(len(autoEtoile.listStates) + 1, True, True, "Eps"))
        return autoEtoile


