import json, random


teams = []
with open('players.json', 'r') as f:
    players = json.load(f)
with open('names.json', 'r') as f:
    names = json.load(f)
#with open('players.json', 'r') as f:
    #teams = json.loads(f)
positions = ["GK", "LW", "RW", "LB", "RB", "CB", "ST", "CM", "LM", "RM"]

team_names = [
    'Arsenal',
    'Aston Villa',
    'Bournemouth',
    'Brentford',
    'Brighton & Hove Albion',
    'Burnley',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Fulham',
    'Liverpool',
    'Luton Town',
    'Manchester City',
    'Manchester United',
    'Newcastle United',
    'Nottingham Forest',
    'Sheffield United',
    'Tottenham Hotspur',
    'West Ham United',
    'Wolverhampton Wanderers', 'Athletic Bilbao', 'Atletico Madrid', 'Barcelona', 'Celta Vigo', 'Espanyol', 'Getafe', 'Levante', 'Mallorca', 'Osasuna', 'Rayo Vallecano', 'Real Betis', 'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
def create_team(name, players, manager):
    team = Teams()
    team['name'] = name
    team['players'] = players
    team['manager'] = manager
    teams.append(team)
used_players = []
def choose_players():
    list_of_players = []
    place = int(random.randrange(0, 150))
    for i in positions:
        no = int(random.randrange(0, 6))
        nw = 0
        for x in players[place:place+10000]:
            if x['position'] == i and x["name"] not in [v for v in used_players]:
                if nw > no:
                    break
                list_of_players.append(x)
                used_players.append(x["name"])
                nw += 1
    return list_of_players

def create_all_teams():
    for i in team_names:
        manager = random.choice(names)
        place = int(random.randrange(0, 100000))
        players_list = choose_players()
        create_team(i, players_list, manager)
    print(teams)
    with open('teams.json', 'w') as f:
        f.write(json.dumps(teams, indent=5))


def Teams():
    name = "Team name"
    players = []
    money = 25
    income = 2
    training = 1
    stadium = 1
    manager = 'The managers name'
    overallaverage = 0
    return({'name':name, 'players': players, 'money':money, 'income':income, 'training':training, 'stadium':stadium, 'manager':manager, 'overallaverage':overallaverage})


create_all_teams()