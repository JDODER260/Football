import json
with open('key.json') as f:
    key = json.load(f)
mess1 = []
mess2 = []

def encode(x):
    mess1 = []
    for i in x:
        for l in key:
            if l['letter'] == i:
                mess1.append(l['codeletter'])        
    return mess1

def decode(x):
    mess2 = []
    for i in x:
        for l in key:
            if l['codeletter'] == i:
                mess2.append(l['letter'])  
    sting = ''
    for i in mess2:
        sting +=i      
    return sting
