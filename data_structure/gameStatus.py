"""
Class that contains all the player's info
"""


class Player:

    def __init__(self, name):
        self.movement = None
        self.state = None
        self.name = name
        self.symbol = None
        self.team = None
        self.score = None
        self.energy = None
        self.loyalty = None
        self.x = None
        self.y = None

        self.turingScore = 0.5

        # if a player has been judged, set this parameter equal to "AI" or "H"
        self.judgedAs = ""
        # [0.0, ... ,1.0]
        self.sdScore = 0

        self.kills = []
        self.messages = []

        self.flagEuclideanDistance = 100

        self.offensivePlayer = False

        # list of all the action made by a player
        self.actionList = []

        # next predicted actions
        self.predictedActions = []

        # is this player a runner, a sniper or what? TBD
        # 1 runner,
        # 2 defender,
        # 3 boh

        self.classificatedAs = None


"""
Class that contains all the game's information
"""


class Game:
    def __init__(self, gameName):
        self.name = gameName
        self.state = None

        # Valori possibili: 0, 1, 2 (fase 0 senza shoot, fase 1 no ctf, fase 2 gioco normale)
        self.stage = 0
        self.me = None

        # list of allies player
        self.allies = dict()

        # list of enemies player
        self.enemies = dict()


        self.activeEnemies = None
        self.activeAllies = None

        # map dimension, height and width
        self.mapHeight = None
        self.mapWidth = None

        # flags coordinates, name and euclidean distance
        self.toBeDefendedFlagX = None
        self.toBeDefendedFlagY = None
        self.toBeDefendedFlagName = None
        self.wantedFlagX = None
        self.wantedFlagY = None
        self.wantedFlagName = None

        self.wantedFlagMaxEuclideanDistance = None
        self.wantedFlagEuclideanDistance = None

        # map retrieved from the server
        self.serverMap = None

        # weighted deterministic map
        self.weightedMap = None

        # weighted impostor deterministic map (create projecton for allies)
        self.weightedImpostorMap = None

        # distance and coordinate of a safezone around me
        self.d_SafeZone = [100, self.mapWidth, self.mapWidth]

        # nearest recharge (manhattan distance, coordinates)
        self.nearestRecharge = [11, None, None]

        # number of actions (manhattan distance) that can be done safely and the coordinates to the nearest enemy fireline
        # if manhattan distance == 11 there is no enemy fire line
        self.nearestEnemyLinearDistance = [11, None, None]

        # come sopra ma per gli alleati (utile per impostore)
        self.nearestAllyLinearDistance = [11, None, None]

        self.runner = [0, None, None]

        # flag che segnala emergency meeting
        self.emergencyMeeting = 0

        self.judgeList = []


global game

global sharedList
sharedList = []
