import json
angle = {
    'R': 0,
    'J': 30,
    'E': 45,
    'T': 60,
    'U': 90,
    'G': 120,
    'Q': 135,
    'H': 150,
    'L': 180,
    'N': 210,
    'Z': 225,
    'F': 240,
    'D': 270,
    'B': 300,
    'C': 315,
    'M': 330
}

def getAngle(pre, lat):
    return ((pre - lat + 179) % 360 + 1)

data = open('magic.adofai', mode='r', encoding='utf-8-sig').read()
data = data.replace(', }', ' }')
data = data.replace(' }\n', ' },\n')
data = data.replace(' },\n	]',' }\n	]')
data = json.loads(data)
pathData = data['pathData']
pathList = []
for i in range(len(pathData) - 1):
    try:
        pre = angle[pathData[i]]
        lat = angle[pathData[i+1]]
        pathList.append(getAngle(pre, lat))
    except KeyError as e:
        print('Warning: Unsupported angle! ({})'.format(e))
        pathList.append(180)
actions = data['actions']
tmp = 0
direction = 0
for i in pathList:
    if pathList[tmp]/pathList[tmp-1] != 1:
        if direction % 2 == 0:
            angle = pathList[tmp]
        else:
            angle = (((359 - pathList[tmp]) % 360) + 1)
        if angle <= 180:
            if direction % 2 == 0:
                actions.append({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp]/pathList[tmp-1] },) # 기본모드
            else:
                actions.append({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / (((359 - pathList[tmp-1]) % 360) + 1) },)
            twirl = 0
        else:
            print(tmp)
            actions.append({ "floor": tmp + 1, "eventType": "Twirl" },)
            if direction % 2 == 0:
                if twirl == 0:
                    actions.append({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / pathList[tmp-1] },)
                    print((((359 - pathList[tmp-1]) % 360) + 1))
                    print((((359 - pathList[tmp]) % 360) + 1))
                else:
                    actions.append({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp] / (((359 - pathList[tmp-1]) % 360) + 1) },)
                    print(2)
            else:
                if twirl == 0:
                    actions.append({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp] / pathList[tmp-1] },)
                    print(3)
                    
                else:
                    actions.append({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp] / (((359 - pathList[tmp-1]) % 360) + 1) },)
                    print(4)
            print('--')
            direction += 1
            twirl = 1
    tmp += 1
#print(actions)

settings = data['settings']
settings['madewith'] = 'BPM Multiplier by PAPER_PPT_'
filedata = {}
filedata['pathData'] = pathData
filedata['settings'] = settings
filedata['actions'] = actions

#print(json.dumps(filedata))
file = open('multiplied.adofai', mode='w')
file.write(json.dumps(filedata, indent=4))
