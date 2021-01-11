from strategy.pathFinder import findPath, findPath4Fuzzy
from data_structure import gameStatus
from data_structure.gameStatus import *
from karen import *
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def fuzzyValues(maxWeight):
    close_to_enemy = gameStatus.game.nearestEnemyLinearDistance[0] # quanto sono vicino alla linea di fuoco del nemico
    d_SafeZone = [maxWeight, maxWeight, maxWeight]
    nearestRecharge = gameStatus.game.nearestRecharge
    myenergy = gameStatus.game.me.energy
    d_flag = gameStatus.game.wantedFlagEuclideanDistance
    stage = gameStatus.game.stage

    '''Useful values for impostor strategy'''
    alive_allies = gameStatus.game.activeAllies / len(gameStatus.game.allies) # alive / total
    close_to_ally = gameStatus.game.nearestAllyLinearDistance[0]  # quanto sono vicino alla linea di fuoco dell'alleato

    '''Computing safe zone'''
    # d_SafeZone = 0 means that I'm in a safeZone
    # d_SafeZone = 1 or 2 means that i need to do 1 or 2 movement to be in a safeZone
    if gameStatus.game.weightedMap[gameStatus.game.me.y][gameStatus.game.me.x] == 1:
        d_SafeZone[0] = 0
        d_SafeZone[1] = gameStatus.game.me.y
        d_SafeZone[2] = gameStatus.game.me.x
    else:
        if gameStatus.game.weightedMap[gameStatus.game.me.y - 1][gameStatus.game.me.x] == 1:
            d_SafeZone[0] = 1
            d_SafeZone[1] = gameStatus.game.me.y - 1
            d_SafeZone[2] = gameStatus.game.me.x

        elif gameStatus.game.weightedMap[gameStatus.game.me.y][gameStatus.game.me.x - 1] == 1:
            d_SafeZone[0] = 1
            d_SafeZone[1] = gameStatus.game.me.y
            d_SafeZone[2] = gameStatus.game.me.x - 1

        elif gameStatus.game.weightedMap[gameStatus.game.me.y][gameStatus.game.me.x + 1] == 1:
            d_SafeZone[0] = 1
            d_SafeZone[1] = gameStatus.game.me.y
            d_SafeZone[2] = gameStatus.game.me.x + 1

        elif gameStatus.game.weightedMap[gameStatus.game.me.y + 1][gameStatus.game.me.x] == 1:
            d_SafeZone[0] = 1
            d_SafeZone[1] = gameStatus.game.me.y + 1
            d_SafeZone[2] = gameStatus.game.me.x

        elif gameStatus.game.weightedMap[gameStatus.game.me.y - 1][gameStatus.game.me.x - 1] == 1:
            d_SafeZone[0] = 2
            d_SafeZone[1] = gameStatus.game.me.y - 1
            d_SafeZone[2] = gameStatus.game.me.x - 1

        elif gameStatus.game.weightedMap[gameStatus.game.me.y - 1][gameStatus.game.me.x + 1] == 1:
            d_SafeZone[0] = 2
            d_SafeZone[1] = gameStatus.game.me.y - 1
            d_SafeZone[2] = gameStatus.game.me.x + 1

        elif gameStatus.game.weightedMap[gameStatus.game.me.y + 1][gameStatus.game.me.x - 1] == 1:
            d_SafeZone[0] = 2
            d_SafeZone[1] = gameStatus.game.me.y + 1
            d_SafeZone[2] = gameStatus.game.me.x - 1

        elif gameStatus.game.weightedMap[gameStatus.game.me.y + 1][gameStatus.game.me.x + 1] == 1:
            d_SafeZone[0] = 2
            d_SafeZone[1] = gameStatus.game.me.y + 1
            d_SafeZone[2] = gameStatus.game.me.x + 1

        else:
            d_SafeZone[0] = 3

    return d_flag, nearestRecharge, myenergy, d_SafeZone, close_to_enemy, alive_allies, stage, close_to_ally


def FuzzyControlSystem(maxWeight):

    d_flag = ctrl.Antecedent(np.arange(0, gameStatus.game.wantedFlagMaxEuclideanDistance, 1), 'd_flag')
    close_to_enemy = ctrl.Antecedent(np.arange(0, 11, 1), 'close_to_enemy')
    d_safeZone = ctrl.Antecedent(np.arange(0, 3, 1), 'd_safeZone')
    myenergy = ctrl.Antecedent(np.arange(0, 256, 1), 'myenergy')
    nearestRecharge = ctrl.Antecedent(np.arange(0, 11, 1), 'nearestRecharge')
    stage = ctrl.Antecedent(np.arange(0, 2, 1), 'nearestRecharge')
    #alive_allies = ctrl.Antecedent(np.arange(0, len(gameStatus.game.allies), 1), 'alive_allies')

    output = ctrl.Consequent(np.arange(0, 30, 1), 'output')

    # goToKill, goToFlag, goToRecharge, staySafe

    output['goToKill'] = fuzz.trimf(output.universe, [0, 10, 10])
    output['goToFlag'] = fuzz.trimf(output.universe, [10, 20, 20])
    output['goToRecharge'] = fuzz.trimf(output.universe, [20, 30, 30])
    output['staySafe'] = fuzz.trimf(output.universe, [20, 30, 30])

    # Auto-membership function population is possible with .automf(3, 5, or 7)

    d_flag.automf(3)
    close_to_enemy.automf(3)
    d_safeZone.automf(3)
    myenergy.automf(3)
    nearestRecharge.automf(3)
    stage.automf(3)
    #alive_allies.automf(3)

    # poor mediocre average decent good

    kill = ctrl.Rule(
                    (stage['average'] | stage['good']) &       # I can kill only if the game stage is 1 or 2
                    (myenergy['average'] | myenergy['good']) |
                    (d_flag['good'] & d_safeZone['good'])
                    , output['goToKill'])

    flag = ctrl.Rule(
                    (d_flag['poor']) &
                    (myenergy['good'] | myenergy['average']) & (nearestRecharge['average'] | nearestRecharge['good']) &
                    (d_safeZone['average'] | d_safeZone['good'])
                     , output['goToFlag'])

    recharge = ctrl.Rule(
                        (myenergy['poor'])
                        & (d_flag['average'] | d_flag['good'])
                        & (close_to_enemy['good'] | close_to_enemy['average'])
                        & nearestRecharge['poor']
                        , output['goToRecharge'])

    safe = ctrl.Rule((close_to_enemy['average'] | close_to_enemy['good']) &  # ci sono molti nemici
                     (d_safeZone['poor']) # non sono al sicuro
                     , output['goToSafePlace'])

    system = ctrl.ControlSystem(rules=[kill, flag, recharge, safe])

    # Later we intend to run this system with a 21*21 set of inputs, so we almediocre
    # that many plus one unique runs before results are flushed.
    # Subsequent runs would return in 1/8 the time!
    sim = ctrl.ControlSystemSimulation(system)

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)

    # d_flag, nearestRecharge, myenergy, d_SafeZone, close_to_enemy, alive_allies, stage, close_to_ally
    flag, recharge, energy, safeZone, enemy, allies, stage, ally = fuzzyValues(maxWeight)

    sim.input['d_flag'] = flag
    sim.input['nearestRecharge'] = recharge
    sim.input['myenergy'] = energy
    sim.input['d_SafeZone'] = safeZone[0]
    sim.input['close_to_enemy'] = enemy
    sim.input['stage'] = stage


    '''Gestione eccezioni'''

    try:
        sim.compute()
        outputValue = sim.output.get("output")

        output.view(sim=sim)  # plot

    except:
        # crisp case: staySafe
        print("EXCEPTION FUZZY")

        outputValue = 35


    '''Outcomes'''

    if outputValue in range(0, 10): # kill

        x = gameStatus.game.nearestEnemyLinearDistance[1]
        y = gameStatus.game.nearestEnemyLinearDistance[2]

        # print(gameStatus.game.me.name + " vado ad uccidere: ")

    elif outputValue in range(10, 20):  # flag

        x = gameStatus.game.wantedFlagX
        y = gameStatus.game.wantedFlagY

        # print(gameStatus.game.me.name + " vado alla bandiera ")


    elif outputValue in range(30, 40): # safe

        x = safeZone[1]
        y = safeZone[2]

    # print(gameStatus.game.me.name + " vado in safe zone")

    else: # 20-30 recharge

        x = gameStatus.game.nearestRecharge[1]
        y = gameStatus.game.nearestRecharge[2]

    # print(gameStatus.game.me.name + " vado a ricaricarmi ")

    '''???
    if (x == maxWeight and y == maxWeight):
        x = gameStatus.game.wantedFlagX
        y = gameStatus.game.wantedFlagX
    '''
    return x, y  # return x, y, nearestEnemyDistance[0] ???





def FuzzyControlSystemImpostor(maxWeight):

    """
    staySafe finché num_allies > 50%, nel frattempo vota.
    Poi goToKill prendendo ogni volta l'alleato più vicino
        --> lo fa una funzione a parte, controllando la distanza euclidea dalla linea di tiro in un intorno di 20 caselle.
    """

    close_to_ally = ctrl.Antecedent(np.arange(0, 11, 1), 'close_to_ally')
    d_safeZone = ctrl.Antecedent(np.arange(0, 3, 1), 'd_safeZone')
    myenergy = ctrl.Antecedent(np.arange(0, 256, 1), 'myenergy')
    nearestRecharge = ctrl.Antecedent(np.arange(0, 11, 1), 'nearestRecharge')
    stage = ctrl.Antecedent(np.arange(0, 2, 1), 'nearestRecharge')
    alive_allies = ctrl.Antecedent(np.arange(0, len(gameStatus.game.allies), 1), 'alive_allies')

    output = ctrl.Consequent(np.arange(0, 30, 1), 'output')

    """
    1. vado a ricaricarmi se:
        - ho energia bassa/media
        - la ricarica è molto vicina
        - ci sono molti nemici 
    2. resto in zona sicura se:
        - sono in vita più di metà degli allies | ho gli enemies vicini 
    3. vado ad uccidere se
        - sono vivi metà degli alleati o meno | il gioco è allo stage 2
    """

    # goToKill, goToFlag, goToRecharge, staySafe

    output['goToKill'] = fuzz.trimf(output.universe, [0, 10, 10])
    output['goToRecharge'] = fuzz.trimf(output.universe, [10, 20, 20])
    output['staySafe'] = fuzz.trimf(output.universe, [20, 30, 30])

    # Auto-membership function population is possible with .automf(3, 5, or 7)

    close_to_ally.automf(3)
    d_safeZone.automf(3)
    myenergy.automf(3)
    nearestRecharge.automf(3)
    stage.automf(3)
    alive_allies.automf(3)

    # TODO
    ''' DA AGGIORNARE
    recharge = ctrl.Rule((stage['poor'] | stage['average']) &
                           (((energy['poor'] | energy['average']) & d_recharge['poor']) |
                            (energy['poor'] | d_recharge['poor']) |
                            ((energy['poor'] | energy['average']) & d_recharge['poor'] & num_enemies['good']))
                           , output['goToRecharge'])

    safe = ctrl.Rule((allies_dist['average'] | allies_dist['good']) &
                         (stage['poor'] | stage['average']) &
                         ((num_allies['average'] | num_allies['good']) |
                          (num_enemies['average'] | num_enemies['good']))
                         , output['goToSafePlace'])

    kill = ctrl.Rule((allies_dist['poor'] & (num_allies['poor']) | (stage['good'])), output['goToKill'])
    '''

    system = ctrl.ControlSystem(rules=[kill, recharge, safe])

    sim = ctrl.ControlSystemSimulation(system)

    # d_flag, nearestRecharge, myenergy, d_SafeZone, close_to_enemy, alive_allies, stage, close_to_ally
    flag, recharge, energy, safeZone, enemy, allies, stage, ally = fuzzyValues(maxWeight)

    sim.input['nearestRecharge'] = recharge
    sim.input['myenergy'] = energy
    sim.input['d_SafeZone'] = safeZone
    sim.input['close_to_enemy'] = enemy
    sim.input['stage'] = stage
    sim.input['alive_allies'] = allies
    sim.input['close_to_ally'] = ally


    ''' Gestire eccezioni:'''
    try:
        sim.compute()
        outputValue = sim.output.get("output")
        output.view(sim=sim)

    except:
        # crisp case, stay safe
        print("EXCEPTION FUZZY")
        outputValue = 15



    '''Outcomes'''

    if outputValue in range(0, 10): # kill

        x = gameStatus.game.nearestAllyLinearDistance[1]
        y = gameStatus.game.nearestAllyLinearDistance[2]

        #print(gameStatus.game.me.name + "IMPOSTOR vado ad uccidere")

    elif outputValue in range(10, 20): #recharge

        x = gameStatus.game.nearestRecharge[1]
        y = gameStatus.game.nearestRecharge[2]

        # print(gameStatus.game.me.name + "IMPOSTOR vado a ricaricarmi")

    else: # safe

        x = safeZone[1]
        y = safeZone[2]

        # print(gameStatus.game.me.name + "IMPOSTOR vado in safe zone")


    return x, y # return x, y, nearestEnemyDistance ???
