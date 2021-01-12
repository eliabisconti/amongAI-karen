import time
from threading import Thread

from scipy.spatial import distance

from data_structure import gameStatus


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

        while gameStatus.game.state == "ACTIVE":

            # update my euclidean distance from the flag
            gameStatus.game.wantedFlagEuclideanDistance = distance.euclidean(
                [gameStatus.game.me.x, gameStatus.game.me.y],
                [gameStatus.game.wantedFlagX, gameStatus.game.wantedFlagY])

            # update the number of non-dead enemies
            num_enemies = 0
            for k in gameStatus.game.enemies.keys():
                if gameStatus.game.enemies.get(k).state == "ACTIVE":
                    num_enemies += 1
            gameStatus.game.activeEnemies = num_enemies

            # update the number of non-dead allies
            num_allies = 0
            for k in gameStatus.game.allies.keys():
                if gameStatus.game.allies.get(k).state == "ACTIVE":
                    num_allies += 1
            gameStatus.game.activeAllies = num_allies


            # update the nearestEnemyLinearDistance [None, None, None]
            # number of actions (half the manhattan distance) that can be done safely and the coordinates to the nearest enemy fireline
            nearestEnemy = [11, None, None]

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

                    if gameStatus.game.weightedMap[i][j] == self.maxWeight/2:
                        manhattan = distance.cityblock([myx, myy] , [j, i])
                        if nearestEnemy[0] > manhattan:
                            nearestEnemy = [int(manhattan / 2), j, i]


                    if gameStatus.game.serverMap[i][j] == "$":
                        manhattan = distance.cityblock([myx, myy] , [j, i])
                        if nearestRecharge[0] > manhattan:
                            nearestRecharge = [int(manhattan / 2), j, i]

            gameStatus.game.nearestRecharge = nearestRecharge
            gameStatus.game.nearestEnemyLinearDistance = nearestEnemy


            """
            if gameStatus.game.me.symbol == "A":
                print("For " + gameStatus.game.me.symbol + " at " + str(gameStatus.game.me.x) + " " + str(gameStatus.game.me.y))
                for p in gameStatus.game.serverMap:
                    print(p)
                print("nearestRecharge: " + str(nearestRecharge[1]) + " " + str(nearestRecharge[2]))
                print("nearestEnemy: " + str(nearestEnemy[1]) + " " + str(nearestEnemy[2]) + " enemy at: " + str(gameStatus.game.enemies.get("a").x) + " " + str(gameStatus.game.enemies.get("a").y))

                print(time.time())
            """
