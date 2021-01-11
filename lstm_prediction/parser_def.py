import re
import sys
from os import listdir
from os.path import isfile, join

import pickle


class MlDatabase:
    def __init__(self):
        self.playerList = dict()  # chiave: nome, valore:lista (o struttura con liste di azioni e mappe (con timestamp))


class MlPlayer:
    def __init__(self, name):
        self.nome = name
        self.act_list = []  # tupla (x, y, azion, info (dist in polare o bersaglio shoot))
        self.team = None
        self.coord = None
        self.flagToCatch = None

