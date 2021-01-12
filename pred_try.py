import pickle
from keras.utils import to_categorical
from numpy import array
from data_structure import gameStatus

a_file = open("lstm_prediction\LSTM_model2.pickle", "rb")
model = pickle.load(a_file)

while True:
    if gameStatus.game.stage is not 0:
        for k in gameStatus.game.enemies.keys():
            tmp_act = []
            tmp_pred = []
            gameStatus.game.enemies.get(k).predictedActions = []
            for a in gameStatus.game.enemies.get(k).actionList:
                tmp_act.append(a)
            # ottengo una serie di predizioni lunga 10
            for i in range(10):
                # preparo array di input al modello prendendo le azioni fatte finora
                x_input = array(tmp_act)
                x_input = to_categorical(x_input, num_classes=3)
                x_input = x_input.reshape((1, len(x_input), 3))
                # predizione e estrazione dell'azione
                pred = model.predict(x_input, verbose=0)
                max_pred = 0
                max_pos = 0
                for z in range(3):
                    if pred[0][z] > max_pred:
                        max_pred = pred[0][z]
                        max_pos = z
                pred_dec = None
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

            ##############################################################
            # assegno classe
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






