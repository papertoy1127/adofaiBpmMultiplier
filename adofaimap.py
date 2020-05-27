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
pathData = 'R' + pathData
pathList = []
for i in range(len(pathData) - 1):
    try:
        pre = angle[pathData[i]]
        lat = angle[pathData[i+1]]
        pathList.append(getAngle(pre, lat))
        
    except KeyError as e:
        print('죄송합니다, 지원하지 않는 각도이거나 잘못된 타일로 보입니다.({})'.format(e))
actions = []
tmp = 0
for i in pathList:
    actions.append({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp]/pathList[tmp-1] },)
    tmp += 1
print(actions)

settings = {
    "version": 2, 
    "artist": "아티스트", 
    "song": "제목", 
    "author": "만든이", 
    "separateCountdownTime": "Enabled",
    "songFilename": "", 
    "bpm": 320, 
    "volume": 100, 
    "offset": 0, 
    "pitch": 100, 
    "hitsound": "Kick", 
    "hitsoundVolume": 100,
    "trackColorType": "Single", 
    "trackColor": "debb7b", 
    "secondaryTrackColor": "ffffff", 
    "trackColorAnimDuration": 2, 
    "trackColorPulse": "None", 
    "trackPulseLength": 10, 
    "trackStyle": "Standard", 
    "trackAnimation": "None", 
    "beatsAhead": 3, 
    "trackDisappearAnimation": "None", 
    "beatsBehind": 4,
    "backgroundColor": "000000", 
    "bgImage": "", 
    "bgImageColor": "ffffff", 
    "parallax": [100, 100], 
    "bgDisplayMode": "FitToScreen", 
    "lockRot": "Disabled", 
    "loopBG": "Disabled", 
    "unscaledSize": 100,
    "relativeTo": "Player", 
    "position": [0, 0], 
    "rotation": 0, 
    "zoom": 100,
    "bgVideo": "", 
    "loopVideo": "Disabled", 
    "vidOffset": 0, 
    "floorIconOutlines": "Disabled", 
    "stickToFloors": "Enabled", 
    "planetEase": "Linear", 
    "planetEaseParts": 1,
    "madewith": "AHS Free by PAPER_PPT_"
}

filedata = {}
filedata['pathData'] = pathData
filedata['settings'] = settings
filedata['actions'] = actions

print(json.dumps(filedata))
file = open('multiplied.adofai', mode='w')
file.write(json.dumps(filedata, indent=4))