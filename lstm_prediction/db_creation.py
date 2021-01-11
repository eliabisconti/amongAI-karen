from scipy.spatial import distance
from lstm_prediction.parser_def import *


def create_db():
    a_file = open("dati_salvati.pickle", "rb")

    structure = pickle.load(a_file)
    print("Ci sono " + str(len(structure.playerList)))
    instances = []
    for k in structure.playerList.keys():
        sequence = []
        # (NOP, SHOOT, GOTOFLAG)
        player = structure.playerList.get(k)
        print("len: " +str(len(player.act_list)))
        previousCoord = None
        previousDist = None
        for action in player.act_list:
            if action[0] == 'SHOOT':
                sequence.append((0, 1, 0))
            elif action[0] == 'MOVE':

                if previousCoord is None:
                    try:
                        previousCoord = (int(action[4][0]), int(action[4][1]))
                        previousDist = distance.euclidean(previousCoord, player.flagToCatch)

                    except:
                        previousCoord = None
                        previousDist = None
                        continue

                else:

                    try:
                        actualCoord = (int(action[4][0]), int(action[4][1]))
                    except:
                        continue

                    actualDist = distance.euclidean(previousCoord, player.flagToCatch)

                    if actualDist < previousDist:
                        sequence.append((0, 0, 1))
                    else:
                        sequence.append((0, 0, 0))

                    previousDist = actualDist
                    previousCoord = actualCoord
            else:
                sequence.append((1, 0, 0))

        if len(sequence) > 10:
            instances.append(sequence)

 #       with open("trainingInstances.pickle", "wb") as file:
#            pickle.dump(instances, file)

create_db()

#trainingInstances = open("trainingInstances.pickle", "rb")

#structure = pickle.load(trainingInstances)
#print("Ci sono " + str(len(structure)) + " istanze di training")

#print(structure[0])
#print(structure[1])