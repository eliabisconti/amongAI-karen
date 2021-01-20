from datetime import datetime
from datetime import timedelta

from threading import Thread
from data_structure import gameStatus
import time

from strategy.pathFinder import findPath


def turingTest(t1):
    """
    Check the speed of each player movement. Humans can move faster than AI
    """
    datetimeFormat = '%H:%M:%S.%f'

    positions_enemies_before = gameStatus.game.enemies
    positions_allies_before = gameStatus.game.allies
    time.sleep(1)  # AI possono fare al massimo 3 passi
    positions_enemies_after = gameStatus.game.enemies
    positions_allies_after = gameStatus.game.allies

    for i in gameStatus.game.enemies.keys():
        if positions_enemies_before.get(i).x == positions_enemies_after.get(i).x and positions_enemies_before.get(
                i).y == positions_enemies_after.get(i).y:
            continue
        else:
            name = gameStatus.game.enemies.get(i).name
            try:
                path = findPath(gameStatus.game.weightedMap, positions_enemies_before.get(i),
                                positions_enemies_after.get(i).x, positions_enemies_after.get(i).y)
                diff = len(path)
            except:
                diff = 2
            if diff > 3:
                gameStatus.game.enemies.get(i).turingScore = 0
                if gameStatus.game.enemies.get(i).judgedAs is not "H":
                    gameStatus.game.judgeList.append((name, 'H'))
                    gameStatus.game.enemies.get(i).judgedAs = "H"
            else:
                gameStatus.game.enemies.get(i).turingScore = 0.7

    gameStatus.game.me.turingScore = 1

    for i in gameStatus.game.allies.keys():
        if positions_allies_before.get(i).x == positions_allies_after.get(i).x and positions_allies_before.get(
                i).y == positions_allies_after.get(i).y:
            continue
        else:
            name = gameStatus.game.allies.get(i).name
            try:
                path = findPath(gameStatus.game.weightedMap, positions_allies_before.get(i),
                                positions_allies_after.get(i).x, positions_allies_after.get(i).y)
                diff = len(path)
            except:
                diff = 0
            if diff > 3:
                gameStatus.game.allies.get(i).turingScore = 0
                if gameStatus.game.allies.get(i).judgedAs is not "H":
                    gameStatus.game.judgeList.append((name, 'H'))
                    gameStatus.game.allies.get(i).judgedAs = "H"

            else:
                gameStatus.game.allies.playerList.get(i).turingScore = 0.7

    dt2 = datetime.now()
    t2 = dt2.time()
    diff = datetime.strptime(str(t2), datetimeFormat) - datetime.strptime(str(t1), datetimeFormat)
    if diff.seconds > 7:
        for i in gameStatus.game.enemies.keys():
            if gameStatus.game.enemies.get(i).turingScore != 0:
                gameStatus.game.enemies.get(i).turingScore = 1
                if gameStatus.game.enemies.get(i).judgedAs is not "AI":
                    gameStatus.game.judgeList.append((i, 'AI'))
                    gameStatus.game.enemies.get(i).judgedAs = "AI"

        for i in gameStatus.game.allies.keys():
            if gameStatus.game.allies.get(i).turingScore != 0:
                gameStatus.game.allies.get(i).turingScore = 1
                if gameStatus.game.allies.get(i).judgedAs is not "AI":
                    gameStatus.game.judgeList.append((i, 'AI'))
                    gameStatus.game.allies.get(i).judgedAs = "AI"
        # print('HO FINITO \n')
        # for i in gameStatus.db.playerList.keys():
        #   print('VALORE TURING: ' + str(gameStatus.db.playerList.get(i).turingScore) + '\n')
        # print('ADDIO MONDO CRUDELE \n')

        return


def socialDeduction():
    # controlla che abbia ucciso compagni di squadra
    for i in gameStatus.game.allies.keys():
        gameStatus.game.allies.get(i).sdScore = 0
        for j in gameStatus.game.allies.get(i).kills:

            if gameStatus.game.allies.get(j) is not None:
                # se sto in stage 2 controllo pure che il player sia lontano dalla flag per assegnare peso maggiore
                if gameStatus.game.stage == 2:
                    if gameStatus.game.allies.get(i).flagEuclideanDistance > gameStatus.game.wantedFlagMaxEuclideanDistance/2:
                        gameStatus.game.allies.get(i).sdScore += 0.4

                else:
                    gameStatus.game.allies.get(i).sdScore += 0.2


                if gameStatus.game.allies.get(i).sdScore > 0.8:
                    gameStatus.game.emergencyMeeting = 1




class playersAnalyzer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        dt1 = datetime.now()
        t1 = dt1.time()
        while gameStatus.game.state != "FINISHED":
            # From time to time update social deduction
            '''
            Riga incriminata v
            '''
            if (dt1 + timedelta(minutes=1)) < datetime.now():

                socialDeduction()
                dt1 = datetime.now()
                t1 = dt1.time()
            # From time to time update social deduction
            if True:
                turingTest(t1)
            time.sleep(0.2)
