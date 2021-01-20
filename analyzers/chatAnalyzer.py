import pickle
import time
from datetime import datetime
from threading import Thread
import re

from numpy import array

from data_structure import gameStatus
from nlp import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer


def chatAnalysis(vectorizer, model_misogyny):
    """
    Analyze every chat's message to update information about the game and all the players' actions
    Also analyze every message from other player to determine if it contains offensive language or not
    :param vectorizer: tfidf_vectorizer
    :param model_misogyny: prediction model
    """
    received = gameStatus.sharedList.pop()  # è coppia stringa timestamp
    received_str = received[0]
    received_time = received[1]
    # print('\n TIME: ' + str(received_time) + '\n')
    tmp = re.split(' |\n', received_str)
    if tmp[0] == '#GLOBAL':
        if tmp[1] == '@GameServer':
            None
            # notifiche di sistema
    else:
        if tmp[1] == '@GameServer':
            # notifiche del server relative alla partita
            if tmp[2] == 'Now':
                gameStatus.game.state = 'ACTIVE'
            if tmp[2] == 'Game':
                gameStatus.game.state = 'FINISHED'
            if tmp[2] == 'Hunting':
                gameStatus.game.stage = 1
                # 654324 @GameServer Hunting season open!
            if tmp[2] == 'You':
                gameStatus.game.stage = 2
                # 104223 @GameServer You can now catch the flag!
            if tmp[2] == 'EMERGENCY':
                if tmp[4] == 'Called':
                    gameStatus.game.emergencyMeeting = 1
                    # EM, fai votare karen
                if tmp[4] == 'condamned':
                    # espulso da EM, metti a KILLED il suo stato
                    if gameStatus.game.me.name == tmp[5]:
                        gameStatus.game.me.state = 'KILLED'

                    for i in gameStatus.game.allies.keys():
                        if gameStatus.game.allies.get(i).name == tmp[5]:
                            gameStatus.game.allies.get(i).state = 'KILLED'
                            break
                    for i in gameStatus.game.enemies.keys():
                        if gameStatus.game.enemies.get(i).name == tmp[5]:
                            gameStatus.game.enemies.get(i).state = 'KILLED'

                            break

            if tmp[3] == 'shot':
                # aggiungo 'spara' a lista azioni player
                if gameStatus.game.allies.get(tmp[2]) is not None:
                    gameStatus.game.allies.get(tmp[2]).actionList.append(0)    #(tmp[4], received_time))

                elif gameStatus.game.enemies.get(tmp[2]) is not None:
                    gameStatus.game.enemies.get(tmp[2]).actionList.append(0)   #(tmp[4], received_time))


            if tmp[3] == 'hit':
                # 654324 @GameServer pinko2 hit pinko
                # aggiungo pinko a lista killed di pinko2

                if gameStatus.game.allies.get(tmp[2]) is not None:
                    gameStatus.game.allies.get(tmp[2]).kills.append((tmp[4], received_time))

                elif gameStatus.game.enemies.get(tmp[2]) is not None:
                    gameStatus.game.enemies.get(tmp[2]).kills.append((tmp[4], received_time))

                if gameStatus.game.me.name == tmp[4]:
                    gameStatus.game.me.state = 'KILLED'

                for i in gameStatus.game.allies.keys():
                    if gameStatus.game.allies.get(i).name == tmp[4]:
                        gameStatus.game.allies.get(i).state = 'KILLED'

                        break
                for i in gameStatus.game.enemies.keys():
                    if gameStatus.game.enemies.get(i).name == tmp[4]:
                        gameStatus.game.enemies.get(i).state = 'KILLED'

                        break
                # aggiorna status del giocatore ucciso in MORTO

        else:
            # messaggi player
            preprocessed = preprocessing.pre_process(received_str.lower(), False)
            sentence = vectorizer.transform([preprocessed]).toarray()

            # 1 offensive, 0 not offensive
            is_offensive = int(model_misogyny.predict(array(sentence).reshape(1, -1))[0])

            for k in gameStatus.game.allies.keys():
                if gameStatus.game.allies.get(k).name == tmp[1]:
                    gameStatus.game.allies.get(k).messages.append((received_str, received_time))
                    if is_offensive == 1:
                        gameStatus.game.allies.get(k).offensivePlayer = True
                    break

            for k in gameStatus.game.enemies.keys():
                if gameStatus.game.enemies.get(k).name == tmp[1]:
                    gameStatus.game.enemies.get(k).messages.append((received_str, received_time))
                    if is_offensive == 1:
                        gameStatus.game.enemies.get(k).offensivePlayer = True
                    break


def load_file(filename):
    with open(filename, "rb") as fin:
        file = pickle.load(fin)

    return file


class chatAnalyzer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.model_misoginy = load_file('nlp/model_english_log_reg_tfidf.pk')
        self.name = name
        self.vectorizer = load_file('nlp/vectorizer.pk')

    def run(self):
        dt1 = datetime.now()
        t1 = dt1.time()

        while True:
            time.sleep(0.1)

            # If something arrives in chat, analyze it
            if len(gameStatus.sharedList) > 0:
                chatAnalysis(self.vectorizer, self.model_misoginy)
