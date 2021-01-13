import time
import pickle
from threading import Thread
from numpy import array
import tensorflow as tf

from keras.utils import to_categorical
from scipy.spatial import distance

from data_structure import gameStatus
from strategy.onMapFunctions import findFireLineCoordinateForKilling


class gameAnalyzer(Thread):
    def __init__(self, name, maxWeight):
        Thread.__init__(self)
        self.name = name
        self.maxWeight = maxWeight

        while gameStatus.game.wantedFlagX is None or gameStatus.game.wantedFlagY is None:
            time.sleep(0.05)

        # calculate the max euclidean distance possible from the flag (used for fuzzy values)
        if gameStatus.game.wantedFlagX > gameStatus.game.mapWidth / 2:
            if gameStatus.game.wantedFlagY > gameStatus.game.mapHeight / 2:
                gameStatus.game.wantedFlagMaxEuclideanDistance = distance.euclidean([0, 0],
                                                                                    [gameStatus.game.wantedFlagX,
                                                                                     gameStatus.game.wantedFlagY])
            else:
                gameStatus.game.wantedFlagMaxEuclideanDistance = distance.euclidean([0, gameStatus.game.mapHeight],
                                                                                    [gameStatus.game.wantedFlagX,
                                                                                     gameStatus.game.wantedFlagY])
        else:
            if gameStatus.game.wantedFlagY < gameStatus.game.mapHeight / 2:
                gameStatus.game.wantedFlagMaxEuclideanDistance = distance.euclidean(
                    [gameStatus.game.mapWidth, gameStatus.game.mapHeight],
                    [gameStatus.game.wantedFlagX, gameStatus.game.wantedFlagY])
            else:
                gameStatus.game.wantedFlagMaxEuclideanDistance = distance.euclidean([gameStatus.game.mapWidth, 0],
                                                                                    [gameStatus.game.wantedFlagX,
                                                                                     gameStatus.game.wantedFlagY])

    def run(self):

        a_file = open("lstm_prediction\LSTM_model2.pickle", "rb")
        model = pickle.load(a_file)
        print("MODEL LOADED")
        while gameStatus.game.state == "ACTIVE":

            #if(gameStatus.game.me.symbol == "A"):
            #    print("inizio: " + str(time.time()))

            # update my euclidean distance from the flag
            gameStatus.game.wantedFlagEuclideanDistance = distance.euclidean(
                [gameStatus.game.me.x, gameStatus.game.me.y],
                [gameStatus.game.wantedFlagX, gameStatus.game.wantedFlagY])

            # update the number of non-dead enemies
            num_enemies = 0
            for k in gameStatus.game.enemies.keys():
                if gameStatus.game.enemies.get(k).state == "ACTIVE":
                    num_enemies += 1
                    gameStatus.game.enemies.get(k).flagEuclideanDistance = distance.euclidean(
                        [gameStatus.game.enemies.get(k).x, gameStatus.game.enemies.get(k).y],
                        [gameStatus.game.toBeDefendedFlagX, gameStatus.game.toBeDefendedFlagY])
            gameStatus.game.activeEnemies = num_enemies

            # update the number of non-dead allies
            num_allies = 0
            for k in gameStatus.game.allies.keys():
                if gameStatus.game.allies.get(k).state == "ACTIVE":
                    num_allies += 1
                    gameStatus.game.allies.get(k).flagEuclideanDistance = distance.euclidean(
                        [gameStatus.game.allies.get(k).x, gameStatus.game.allies.get(k).y],
                        [gameStatus.game.wantedFlagX, gameStatus.game.wantedFlagY])
            gameStatus.game.activeAllies = num_allies


            # update the nearestEnemyLinearDistance [None, None, None]
            # number of actions (half the manhattan distance) that can be done safely and the coordinates to the nearest enemy fireline
            nearestEnemy = [11, None, None]

            nearestAlly = [11, None, None]

            # update the nearestRecharge [None, None, None]
            # (half the manhattan distance, coordinates)
            nearestRecharge = [11, None, None]

            # slice the map, we will check only a submatrix 10x10 around me
            myx = gameStatus.game.me.x
            myy = gameStatus.game.me.y

            startX = myx - 10 if myx - 10 > 0 else 0
            startY = myy - 10 if myy - 10 > 0 else 0
            endX = myx + 10 if myx + 10 < gameStatus.game.mapWidth else gameStatus.game.mapWidth
            endY = myy + 10 if myy + 10 < gameStatus.game.mapHeight else gameStatus.game.mapHeight
            for i in range(startY, endY):
               for j in range(startX, endX):

                #for i in range(0, gameStatus.game.mapHeight):
                #    for j in range(0, gameStatus.game.mapWidth):


                if gameStatus.game.weightedMap[i][j] == self.maxWeight/2:
                    manhattan = distance.cityblock([myx, myy] , [j, i])
                    if nearestEnemy[0] > int(manhattan):
                        nearestEnemy = [int(manhattan), j, i]

            # if (gameStatus.game.me.symbol == "A"):
            #    print("fine: " + str(time.time()))

                if gameStatus.game.serverMap[i][j] == "$":
                    manhattan = distance.cityblock([myx, myy] , [j, i])
                    if nearestRecharge[0] > manhattan:
                        nearestRecharge = [int(manhattan), j, i]

                # if I'm impostor compute also the nearest ally linear distance
                if gameStatus.game.weightedImpostorMap is not None:

                    if gameStatus.game.weightedImpostorMap[i][j] == self.maxWeight / 2:
                        manhattan = distance.cityblock([myx, myy], [j, i])
                        if nearestEnemy[0] > int(manhattan):
                            nearestAlly = [int(manhattan), j, i]


            gameStatus.game.nearestRecharge = nearestRecharge
            gameStatus.game.nearestEnemyLinearDistance = nearestEnemy
            gameStatus.game.nearestAllyLinearDistance = nearestAlly

            # print("NEAREST ENEMY: " + str(gameStatus.game.nearestEnemyLinearDistance))


            '''
            Find the nearest safezone around me, max 3 position'''
            if gameStatus.game.weightedMap[gameStatus.game.me.y][gameStatus.game.me.x] == 1:
                gameStatus.game.d_SafeZone[0] = 0
                gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y
                gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x
            else:
                if gameStatus.game.weightedMap[gameStatus.game.me.y - 1][gameStatus.game.me.x] == 1:
                    gameStatus.game.d_SafeZone[0] = 1
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y - 1
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x

                elif gameStatus.game.weightedMap[gameStatus.game.me.y][gameStatus.game.me.x - 1] == 1:
                    gameStatus.game.d_SafeZone[0] = 1
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x - 1

                elif gameStatus.game.weightedMap[gameStatus.game.me.y][gameStatus.game.me.x + 1] == 1:
                    gameStatus.game.d_SafeZone[0] = 1
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x + 1

                elif gameStatus.game.weightedMap[gameStatus.game.me.y + 1][gameStatus.game.me.x] == 1:
                    gameStatus.game.d_SafeZone[0] = 1
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y + 1
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x

                elif gameStatus.game.weightedMap[gameStatus.game.me.y - 1][gameStatus.game.me.x - 1] == 1:
                    gameStatus.game.d_SafeZone[0] = 2
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y - 1
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x - 1

                elif gameStatus.game.weightedMap[gameStatus.game.me.y - 1][gameStatus.game.me.x + 1] == 1:
                    gameStatus.game.d_SafeZone[0] = 2
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y - 1
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x + 1

                elif gameStatus.game.weightedMap[gameStatus.game.me.y + 1][gameStatus.game.me.x - 1] == 1:
                    gameStatus.game.d_SafeZone[0] = 2
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y + 1
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x - 1

                elif gameStatus.game.weightedMap[gameStatus.game.me.y + 1][gameStatus.game.me.x + 1] == 1:
                    gameStatus.game.d_SafeZone[0] = 2
                    gameStatus.game.d_SafeZone[1] = gameStatus.game.me.y + 1
                    gameStatus.game.d_SafeZone[2] = gameStatus.game.me.x + 1

                else:
                    gameStatus.game.d_SafeZone[0] = 3

            '''
            Use the LSTM model to predict enemy action
            '''

            if gameStatus.game.stage is not 0:
                for k in gameStatus.game.enemies.keys():
                    #print('CICLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
                    if len(gameStatus.game.enemies.get(k).actionList) > 0:
                        #print('CHIAVE ' + str(k) + ' ' + 'lista: ' + str(gameStatus.game.enemies.get(k).actionList))

                        tmp_act = []
                        tmp_pred = []
                        gameStatus.game.enemies.get(k).predictedActions = []
                        for a in gameStatus.game.enemies.get(k).actionList:
                            tmp_act.append(a)
                        # ottengo una serie di predizioni lunga 10
                        #print('ACTTTTT ' + str(tmp_act))

                        for i in range(1):
                            # preparo array di input al modello prendendo le azioni fatte finora
                            x_input = array(tmp_act)
                            x_input = to_categorical(x_input, num_classes=3)
                            x_input = x_input.reshape((1, len(x_input), 3))
                            # predizione e estrazione dell'azione
                            #with graph.as_default():
                            pred = model.predict(x_input, verbose=0)
                            max_pred = 0
                            max_pos = 0
                            for z in range(3):
                                if pred[0][z] > max_pred:
                                    max_pred = pred[0][z]
                                    max_pos = z
                            if max_pos == 0:
                                pred_dec = 0
                            elif max_pos == 1:
                                pred_dec = 1
                            else:
                                pred_dec = 2
                            tmp_pred.append(pred_dec)
                            tmp_act.append(pred_dec)
                        # aggiornamento array azioni predette in GameStatus
                        for j in tmp_pred:
                            gameStatus.game.enemies.get(k).predictedActions.append(j)

                        count_0 = 0
                        count_1 = 0
                        count_2 = 0
                        max_count = 0
                        max_i = None
                        for x in tmp_act:
                            if x == 0:
                                count_0 += 1
                                if count_0 > max_count:
                                    max_count = count_0
                                    max_i = 0
                            elif x == 1:
                                count_1 += 1
                                if count_1 > max_count:
                                    max_count = count_1
                                    max_i = 1
                            elif x == 2:
                                count_2 += 1
                                if count_2 > max_count:
                                    max_count = count_2
                                    max_i = 2
                        gameStatus.game.enemies.get(k).classificatedAs = max_i
                        #print('CLASSE: ' +  str(gameStatus.game.enemies.get(k).classificatedAs))



                nearFlagRunnerList = []
                otherRunnerList = []
                for k in gameStatus.game.enemies.keys():
                    if gameStatus.game.enemies.get(k).classificatedAs == 1:
                        if gameStatus.game.enemies.get(k).flagEuclideanDistance < gameStatus.game.wantedFlagEuclideanDistance:
                            nearFlagRunnerList.append(k)
                        else:
                            otherRunnerList.append(k)

                if len(nearFlagRunnerList) > 0:
                    fireLineX, fireLineY = findFireLineCoordinateForKilling(nearFlagRunnerList)
                    print("ATTENZIONE! Il nemico è piu vicino alla bandiera di me, dovrei andare ad ucciderlo.")
                    gameStatus.game.runner = [2, fireLineX, fireLineY]

                elif len(otherRunnerList) > 0:
                    fireLineX, fireLineY = findFireLineCoordinateForKilling(otherRunnerList)
                    #print("il nemico è a coordinate:" + str(gameStatus.game.enemies.get(otherRunnerList[0]).x) + " " + str(gameStatus.game.enemies.get(otherRunnerList[0]).y))
                    #print("ho runner, lo killo in coordinate; " + str(fireLineX) + " " + str(fireLineY))
                    gameStatus.game.runner = [1, fireLineX, fireLineY]
                else:
                    gameStatus.game.runner = [0, 0, 0]


            """
            if gameStatus.game.me.symbol == "A":
                print("For " + gameStatus.game.me.symbol + " at " + str(gameStatus.game.me.x) + " " + str(gameStatus.game.me.y))
                #for p in gameStatus.game.serverMap:
                #   print(p)
                print("nearestRecharge: " + str(nearestRecharge[1]) + " " + str(nearestRecharge[2]))
                print("nearestEnemy: " + str(nearestEnemy[1]) + " " + str(nearestEnemy[2]) + " enemy at: " + str(gameStatus.game.enemies.get("a").x) + " " + str(gameStatus.game.enemies.get("a").y))

                #print(time.time())

            """
            time.sleep(0.2)
