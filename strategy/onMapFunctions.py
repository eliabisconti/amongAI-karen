from scipy.spatial import distance

from data_structure import gameStatus
from data_structure.gameStatus import *

"""
Discourage Karen to allign with enemies. If there is no other way, go and shoot.
"""


def deterministicMap(maxWeight):

    value = [int(maxWeight / 2), int(maxWeight / 4)]
    walkable = ["."]
    river = ["~"]
    trap = ["!"]
    obstacles = ["#", "@"]
    recharge = ["$"]
    barrier = ["&"]
    allies = gameStatus.game.allies.keys()
    enemies = gameStatus.game.enemies.keys()
    serverMap = gameStatus.game.serverMap
    weightedMap = [row[:] for row in serverMap]

    def recursiveMap(count, j, rec_weightedMap, weight):
        """
        Recursive map generation. Resamble Cellular Automata decision adding weight to the map consistently with the distance from enemies
        :param count: the horizontal coordinate
        :param j: the vertical coordinate
        :param rec_weightedMap: the map
        :param weight: the weight of being in [i:,:j] position
        :return: a weighted map
        """
        # da  muro a nemico
        for position in range(enemy.x, -1, -1):
            if rec_weightedMap[count][position] != '#' and rec_weightedMap[count][position] != "&" and \
                    rec_weightedMap[count][position] not in list(allies):
                if isinstance(rec_weightedMap[count][position], int) is False:
                    rec_weightedMap[count][position] = weight
            else:
                break

        # da nemico a muro
        for position in range(enemy.x, len(rec_weightedMap[count])):
            if rec_weightedMap[count][position] != '#' and rec_weightedMap[count][position] != "&" and \
                    rec_weightedMap[count][position] not in list(allies):
                if isinstance(rec_weightedMap[count][position], int) is False:
                    rec_weightedMap[count][position] = weight
            else:
                break

        # Controllo per colonne
        for position in range(enemy.y, -1, -1):
            if rec_weightedMap[position][j] != '#' and rec_weightedMap[position][j] != "&" and \
                    rec_weightedMap[position][j] not in list(allies):
                if isinstance(rec_weightedMap[position][j], int) is False:
                    rec_weightedMap[position][j] = weight
            else:
                break
        # print("POS ENEMY: " + str(enemy.x) + " " +str(enemy.y) +  "j value : " + str(j) + " max for value " + str(len(rec_weightedMap[j])))
        for position in range(enemy.y, len(rec_weightedMap)):
            if rec_weightedMap[position][j] != '#' and rec_weightedMap[position][j] != "&" and \
                    rec_weightedMap[position][j] not in list(allies):
                if isinstance(rec_weightedMap[position][j], int) is False:
                    rec_weightedMap[position][j] = weight
            else:
                break

        return rec_weightedMap

    # ---------------------------------------------------------------------------------------------------
    # For each enemy that is still alive, create a weighted map assigning value to all the position in the map around the enemy
    for enemykey in gameStatus.game.enemies.keys():
        enemy = gameStatus.game.enemies.get(enemykey)
        if enemy.state == "ACTIVE":
            # First call to assign weight to the enemy's 'x column' and 'y row' coordinate
            weightedMap = recursiveMap(enemy.y, enemy.x, weightedMap, int(maxWeight / 2))

            # Recursive calls giving the already weighted to assign weight to all the coordinate around the enemy player
            if enemy.y - 1 >= 0:
                if enemy.x - 1 >= 0:
                    weightedMap = recursiveMap(enemy.y - 1, enemy.x - 1, weightedMap, int(maxWeight / 4))
                if enemy.x + 1 < gameStatus.game.mapWidth:
                    weightedMap = recursiveMap(enemy.y - 1, enemy.x + 1, weightedMap, int(maxWeight / 4))

            if enemy.y + 1 < gameStatus.game.mapHeight:
                if enemy.x - 1 >= 0:
                    weightedMap = recursiveMap(enemy.y + 1, enemy.x - 1, weightedMap, int(maxWeight / 4))
                if enemy.x + 1 < len(weightedMap[0]):
                    weightedMap = recursiveMap(enemy.y + 1, enemy.x + 1, weightedMap, int(maxWeight / 4))

    # For each position, assign different weight considering their nature
    for i in range(0, gameStatus.game.mapHeight):
        for j in range(0, gameStatus.game.mapWidth):

            if weightedMap[i][j] in value:
                None

            elif serverMap[i][j] in walkable:
                weightedMap[i][j] = 1

            elif serverMap[i][j] in river:
                weightedMap[i][j] = int(maxWeight / 3)

            elif serverMap[i][j] in trap:
                weightedMap[i][j] = int(maxWeight)

            elif serverMap[i][j] in obstacles:
                weightedMap[i][j] = 0

            elif serverMap[i][j] in recharge:
                weightedMap[i][j] = 1

            elif serverMap[i][j] in barrier:
                weightedMap[i][j] = 0

            elif serverMap[i][j] == gameStatus.game.wantedFlagName:
                weightedMap[i][j] = 1

            elif serverMap[i][j] == gameStatus.game.toBeDefendedFlagName:
                weightedMap[i][j] = 0

            elif serverMap[i][j] in allies or serverMap[i][j] in enemies or serverMap[i][
                j] == gameStatus.game.me.symbol:
                weightedMap[i][j] = 1

    return weightedMap


"""
Same as deterministic map. here the map is computed considering allies as enemies and viceversa
"""


def deterministicImpostorMap(maxWeight):

    value = [int(maxWeight / 2), int(maxWeight / 4)]
    walkable = ["."]
    river = ["~"]
    trap = ["!"]
    obstacles = ["#", "@"]
    recharge = ["$"]
    barrier = ["&"]
    enemies = gameStatus.game.allies.keys()
    allies = gameStatus.game.enemies.keys()
    serverMap = gameStatus.game.serverMap
    weightedMap = [row[:] for row in serverMap]

    def recursiveMap(count, j, rec_weightedMap, weight):
        """
        Recursive map generation. Resamble Cellular Automata decision adding weight to the map consistently with the distance from enemies
        :param count: the horizontal coordinate
        :param j: the vertical coordinate
        :param rec_weightedMap: the map
        :param weight: the weight of being in [i:,:j] position
        :return: a weighted map
        """
        # da  muro a nemico
        for position in range(enemy.x, -1, -1):
            if rec_weightedMap[count][position] != '#' and rec_weightedMap[count][position] != "&" and \
                    rec_weightedMap[count][position] not in list(allies):
                if isinstance(rec_weightedMap[count][position], int) is False:
                    rec_weightedMap[count][position] = weight
            else:
                break

        # da nemico a muro
        for position in range(enemy.x, len(rec_weightedMap[count])):
            if rec_weightedMap[count][position] != '#' and rec_weightedMap[count][position] != "&" and \
                    rec_weightedMap[count][position] not in list(allies):
                if isinstance(rec_weightedMap[count][position], int) is False:
                    rec_weightedMap[count][position] = weight
            else:
                break

        # Controllo per colonne
        for position in range(enemy.y, -1, -1):
            if rec_weightedMap[position][j] != '#' and rec_weightedMap[position][j] != "&" and \
                    rec_weightedMap[position][j] not in list(allies):
                if isinstance(rec_weightedMap[position][j], int) is False:
                    rec_weightedMap[position][j] = weight
            else:
                break
        # print("POS ENEMY: " + str(enemy.x) + " " +str(enemy.y) +  "j value : " + str(j) + " max for value " + str(len(rec_weightedMap[j])))
        for position in range(enemy.y, len(rec_weightedMap)):
            if rec_weightedMap[position][j] != '#' and rec_weightedMap[position][j] != "&" and \
                    rec_weightedMap[position][j] not in list(allies):
                if isinstance(rec_weightedMap[position][j], int) is False:
                    rec_weightedMap[position][j] = weight
            else:
                break

        return rec_weightedMap

    # ---------------------------------------------------------------------------------------------------
    # For each enemy that is still alive, create a weighted map assigning value to all the position in the map around the enemy
    for enemykey in gameStatus.game.allies.keys():
        enemy = gameStatus.game.allies.get(enemykey)
        if enemy.state == "ACTIVE":
            # First call to assign weight to the enemy's 'x column' and 'y row' coordinate
            weightedMap = recursiveMap(enemy.y, enemy.x, weightedMap, int(maxWeight / 2))

            # Recursive calls giving the already weighted to assign weight to all the coordinate around the enemy player
            if enemy.y - 1 >= 0:
                if enemy.x - 1 >= 0:
                    weightedMap = recursiveMap(enemy.y - 1, enemy.x - 1, weightedMap, int(maxWeight / 4))
                if enemy.x + 1 < gameStatus.game.mapWidth:
                    weightedMap = recursiveMap(enemy.y - 1, enemy.x + 1, weightedMap, int(maxWeight / 4))

            if enemy.y + 1 < gameStatus.game.mapHeight:
                if enemy.x - 1 >= 0:
                    weightedMap = recursiveMap(enemy.y + 1, enemy.x - 1, weightedMap, int(maxWeight / 4))
                if enemy.x + 1 < len(weightedMap[0]):
                    weightedMap = recursiveMap(enemy.y + 1, enemy.x + 1, weightedMap, int(maxWeight / 4))

    # For each position, assign different weight considering their nature
    for i in range(0, gameStatus.game.mapHeight):
        for j in range(0, gameStatus.game.mapWidth):

            if weightedMap[i][j] in value:
                None

            elif serverMap[i][j] in walkable:
                weightedMap[i][j] = 1

            elif serverMap[i][j] in river:
                weightedMap[i][j] = int(maxWeight / 3)

            elif serverMap[i][j] in trap:
                weightedMap[i][j] = int(maxWeight)

            elif serverMap[i][j] in obstacles:
                weightedMap[i][j] = 0

            elif serverMap[i][j] in recharge:
                weightedMap[i][j] = 1

            elif serverMap[i][j] in barrier:
                weightedMap[i][j] = 0

            elif serverMap[i][j] == gameStatus.game.wantedFlagName:
                weightedMap[i][j] = 1

            elif serverMap[i][j] == gameStatus.game.toBeDefendedFlagName:
                weightedMap[i][j] = 0

            elif serverMap[i][j] in allies or serverMap[i][j] in enemies or serverMap[i][
                j] == gameStatus.game.me.symbol:
                weightedMap[i][j] = 1

    return weightedMap


"""
Given a list of players, find the coordinates needed to go to kill them
"""


def findFireLineCoordinateForKilling(playerList):

    walkable = ["."]
    river = ["~"]
    trap = ["!"]
    obstacles = ["#", "@"]
    recharge = ["$"]
    barrier = ["&"]
    allies = gameStatus.game.allies.keys()
    enemies = playerList
    serverMap = gameStatus.game.serverMap
    weightedMap = [row[:] for row in serverMap]
    maxWeight = 32
    value = [int(maxWeight / 2), int(maxWeight / 4)]

    def recursiveMap(count, j, rec_weightedMap, weight):
        """
        Recursive map generation. Resamble Cellular Automata decision adding weight to the map consistently with the distance from enemies
        :param count: the horizontal coordinate
        :param j: the vertical coordinate
        :param rec_weightedMap: the map
        :param weight: the weight of being in [i:,:j] position
        :return: a weighted map
        """
        # da  muro a nemico
        for position in range(enemy.x, -1, -1):
            if rec_weightedMap[count][position] != '#' and rec_weightedMap[count][position] != "&" and \
                    rec_weightedMap[count][position] not in list(allies):
                if isinstance(rec_weightedMap[count][position], int) is False:
                    rec_weightedMap[count][position] = weight
            else:
                break

        # da nemico a muro
        for position in range(enemy.x, len(rec_weightedMap[count])):
            if rec_weightedMap[count][position] != '#' and rec_weightedMap[count][position] != "&" and \
                    rec_weightedMap[count][position] not in list(allies):
                if isinstance(rec_weightedMap[count][position], int) is False:
                    rec_weightedMap[count][position] = weight
            else:
                break

        # Controllo per colonne
        for position in range(enemy.y, -1, -1):
            if rec_weightedMap[position][j] != '#' and rec_weightedMap[position][j] != "&" and \
                    rec_weightedMap[position][j] not in list(allies):
                if isinstance(rec_weightedMap[position][j], int) is False:
                    rec_weightedMap[position][j] = weight
            else:
                break
        # print("POS ENEMY: " + str(enemy.x) + " " +str(enemy.y) +  "j value : " + str(j) + " max for value " + str(len(rec_weightedMap[j])))
        for position in range(enemy.y, len(rec_weightedMap)):
            if rec_weightedMap[position][j] != '#' and rec_weightedMap[position][j] != "&" and \
                    rec_weightedMap[position][j] not in list(allies):
                if isinstance(rec_weightedMap[position][j], int) is False:
                    rec_weightedMap[position][j] = weight
            else:
                break

        return rec_weightedMap

    # ---------------------------------------------------------------------------------------------------
    # For each enemy that is still alive, create a weighted map assigning value to all the position in the map around the enemy
    for enemykey in enemies:
        enemy = gameStatus.game.enemies.get(enemykey)
        if enemy.state == "ACTIVE":
            # First call to assign weight to the enemy's 'x column' and 'y row' coordinate
            weightedMap = recursiveMap(enemy.y, enemy.x, weightedMap, int(maxWeight / 2))


    # For each position, assign different weight considering their nature
    for i in range(0, gameStatus.game.mapHeight):
        for j in range(0, gameStatus.game.mapWidth):

            if weightedMap[i][j] in value:
                None

            elif serverMap[i][j] in walkable:
                weightedMap[i][j] = 1

            elif serverMap[i][j] in river:
                weightedMap[i][j] = int(maxWeight / 3)

            elif serverMap[i][j] in trap:
                weightedMap[i][j] = int(maxWeight)

            elif serverMap[i][j] in obstacles:
                weightedMap[i][j] = 0

            elif serverMap[i][j] in recharge:
                weightedMap[i][j] = 1

            elif serverMap[i][j] in barrier:
                weightedMap[i][j] = 0

            elif serverMap[i][j] == gameStatus.game.wantedFlagName:
                weightedMap[i][j] = 1

            elif serverMap[i][j] == gameStatus.game.toBeDefendedFlagName:
                weightedMap[i][j] = 0

            elif serverMap[i][j] in allies or serverMap[i][j] in enemies or serverMap[i][
                j] == gameStatus.game.me.symbol:
                weightedMap[i][j] = 1

    coordinateForKilling = [gameStatus.game.mapWidth, 0, 0]
    for i in range(0, gameStatus.game.mapHeight):
       for j in range(0, gameStatus.game.mapWidth):

        if gameStatus.game.weightedMap[i][j] == maxWeight / 2:
            manhattan = distance.cityblock([gameStatus.game.toBeDefendedFlagX, gameStatus.game.toBeDefendedFlagY], [j, i])
            if  coordinateForKilling[0] > int(manhattan):
                coordinateForKilling = [int(manhattan), j, i]

    return coordinateForKilling[1], coordinateForKilling[2]


"""
Make inference to determine player's movement
"""


def whereItMoved(prevX, prevY, newX, newY):


    # print(str(prevX) + " " + str(prevY) + " " + str(newX) + " " + str(newY) )

    previousDistance = distance.euclidean([prevX, prevY],
                                          [gameStatus.game.toBeDefendedFlagX, gameStatus.game.toBeDefendedFlagY])
    actualDistance = distance.euclidean([newX, newY],
                                        [gameStatus.game.toBeDefendedFlagX, gameStatus.game.toBeDefendedFlagY])

    numberOfMovement = 0
    numberOfMovement = distance.cityblock([prevX, prevY], [newX, newY])

    if numberOfMovement == 0:
        return [2]
    else:
        sequence = []
        for step in range(0, numberOfMovement):
            if previousDistance > actualDistance:

                # va verso la bandiera
                sequence.append(1)
            else:

                # non va verso la bandiera
                sequence.append(2)

        return sequence
