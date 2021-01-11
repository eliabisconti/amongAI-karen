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
        self.sdScore = 0
        self.kills = []
        self.messages = []

        self.offensivePlayer = False
        # list of all the action made by a player
        self.actionList = []

        # next predicted actions
        self.predictedActions = []

        # is this player a runner, a sniper or what? TBD
        # 1 runner,
        # 2 sniper,
        # 3 boh
        self.classificatedAs = None

class Game:
    def __init__(self, gameName):
        self.name = gameName
        self.state = None

        # Valori possibili: 0, 1, 2 (fase 0 senza shoot, fase 1 no ctf, fase 2 gioco normale)
        self.stage = 0
        self.me = None

        self.allies = dict()
        self.enemies = dict()

        self.activeEnemies = None
        self.activeAllies = None

        # Map dimension, height and width
        self.mapHeight = None
        self.mapWidth = None

        # Flags coordinates, name and euclidean distance
        self.toBeDefendedFlagX = None
        self.toBeDefendedFlagY = None
        self.toBeDefendedFlagName = None
        self.wantedFlagX = None
        self.wantedFlagY = None
        self.wantedFlagName = None

        self.wantedFlagMaxEuclideanDistance = None
        self.wantedFlagEuclideanDistance =None

        # map retrieved from the server
        self.serverMap = None

        # weighted deterministic map
        self.weightedMap = None

        # Nearest recharge (manhattan distance, coordinates)
        self.nearestRecharge = [11, None, None]

        # number of actions (manhattan distance) that can be done safely and the coordinates to the nearest enemy fireline
        # if manhattan distance == 11 there is no enemy fire line
        self.nearestEnemyLinearDistance = [11, None, None]

        # come sopra ma per gli alleati (utile per impostore)
        self.nearestAlliesLinearDistance = [11, None, None]

        self.runners = 0

        # Flag che segnala emergency meeting
        self.emergencyMeeting = 0

        self.judgeList = []


global game

global sharedList
sharedList = []
