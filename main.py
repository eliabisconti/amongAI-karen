from multiprocessing import Process
from random import randint

from karen import *

"""
Nuovo main per creare karen multi processo e non multithreading
"""


def creator(name, gameName, parameters):
    k = Karen(name, 'fuzzyStrategy')

    if k.createGame(gameName, parameters):
        k.joinGame(gameName, "AI", "AI", "AI-02")
        while True:
            time.sleep(2)
            k.startGame()


def gamer(name, gameName):
    k = Karen(name, 'fuzzyStrategy')
    time.sleep(2)

    if k.joinGame(gameName, "AI", "AI", "AI-02") is True:
        result = k.waitToStart()
    else:
        print("Errore, non ho potuto fare join.")
        return False


# POST <Tournament-name> <join

def gamerRegistration(name, tournamentName):
    k = Karen(name, 'fuzzyStrategy')
    k.chatSocket.sendInChat(tournamentName, "JOIN")
    return


if __name__ == '__main__':
    process = []
    response = 1
    print("What do you want to do?")
    print("1 - Let some Karens join a match.")
    print("2 - Let some Karens start and join a match.")
    print("3 - Let some Karens register to a tournament.")
    print("0 - Exit")
    response = input("Insert your choice: ")

    if int(response) == 1:

        number = input("How many karen do you want? ")
        if number.isdigit():
            room = input("Insert the room name: ")
            for i in range(0, int(number)):
                p = Process(target=gamer, args=('Karen' + str(i), room))
                p.start()
                process.append(p)
        else:
            print("ERROR.")

    elif int(response) == 2:
        number = input("How many karen do you want? ")
        if number.isdigit() and int(number) > 1:
            print("\nB = balanced team (optional parameter)")
            print("Q = squared map, W = wide map")
            print("0 = small map")
            print("1 = average map")
            print("2 = huge map")
            parameters = "BQ1"
            parameters = input("Insert the parameters (default BQ1): ")
            if parameters == "":
                parameters = "BQ1"

            roomname = str(randint(300000, 9000000))
            p = (Process(target=creator, args=('KarenA', roomname, parameters)))
            p.start()
            process.append(p)
            for i in range(0, int(number)-1):
                p = Process(target=gamer, args=('Karen' + str(i), roomname))
                p.start()
                process.append(p)
        else:
            print("ERROR.")

    elif int(response) == 3:
        number = input("How many karen do you want to play the tournament? ")
        if number.isdigit():
            tournament = input("Insert the tournament name: ")
            for i in range(0, int(number)):
                p = Process(target=gamerRegistration, args=('Karen' + str(i), tournament))
                p.start()
                process.append(p)


    for p in process:
        p.join()
