import json, random

with open("names.json", "r") as f:
    names = json.load(f)

positions = ["GK", "LW", "RW", "LB", "RB", "CB", "ST", "CM", "LM", "RM"]


players = []

for i in names:
    rate = random.randrange(60, 120)
    price = rate/random.randrange(5, 10)
    price = int(price)
    rate = int(rate)
    dic = {
        "name": i,
        "rating": rate,
        "price": price,
        "training_rate": rate/price,
        "position": random.choice(positions),
    }
    players.append(dic)


json_object = json.dumps(players, indent=5)

with open("players.json", "w") as outfile:
    outfile.write(json_object)