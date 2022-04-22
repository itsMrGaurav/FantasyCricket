from mongoengine import *
from mongoengine.context_managers import switch_collection

PASSWORD = 'arik'
URL = f"mongodb+srv://kira:{PASSWORD}@cluster0.ujw7r.mongodb.net/FantasyCricket?retryWrites=true&w=majority"


class Stat(Document):
    player = StringField(required=True)
    matches = IntField(required=True)
    runs = IntField(required=True)
    hundreds = IntField(required=True)
    fifties = IntField(required=True)
    value = IntField(required=True)
    ctg = StringField(required=True)
    meta = {'db_alias': 'fc'}


class Team(Document):
    name = StringField(required=True)
    players = ListField(required=True)
    value = IntField(required=True)
    meta = {'db_alias': 'fc'}


class Match(Document):
    name = StringField(required=True)
    scored = IntField(required=True)
    faced = IntField(required=True)
    fours = IntField(required=True)
    sixes = IntField(required=True)
    bowled = IntField(required=True)
    maiden = IntField(required=True)
    given = IntField(required=True)
    wkts = IntField(required=True)
    catches = IntField(required=True)
    stumping = IntField(required=True)
    ro = IntField(required=True)
    meta = {'db_alias': 'fc'}


class GameDataModel():

    connect(host=URL, alias='fc')

    def getPlayers(self, type):
        batsmen = dict()
        with switch_collection(Stat, 'stats'):
            for stat in Stat.objects():
                if (stat.ctg == type):
                    batsmen[stat.player] = stat.value
        return batsmen

    def getTeams(self, steam=None):
        if steam:
            with switch_collection(Team, 'teams'):
                for team in Team.objects():
                    if team["name"] == steam:
                        return team
        teams = []
        with switch_collection(Team, 'teams'):
            for team in Team.objects():
                teams.append(team)
        return teams

    def getMatch(self, i):
        match = []
        with switch_collection(Match, f'match{i}'):
            for playerData in Match.objects():
                match.append(playerData)
        return match

    def addStats(self, data):
        with switch_collection(Stat, 'stats') as stat:
            print(data[0])
            stat = Stat(player=data[0],
                        matches=data[13],
                        runs=data[14],
                        hundreds=data[15],
                        fifties=data[16],
                        value=data[12],
                        ctg=data[17]
                        )
            stat.save()

    def addMatch(self, data):
        match = Match()
        with switch_collection(Match, 'match1') as match:
            match = Match(
                name=data[0],
                scored=data[1],
                faced=data[2],
                fours=data[3],
                sixes=data[4],
                bowled=data[5],
                maiden=data[6],
                given=data[7],
                wkts=data[8],
                catches=data[9],
                stumping=data[10],
                ro=data[11]
            )
            match.save()

    def addTeam(self, name, players, value):
        team = Team()
        with switch_collection(Team, 'teams') as team:
            team = Team(name=name, players=players, value=value)
            team.save()
