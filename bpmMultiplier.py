import paperlib
import json
import sys
import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton, QLabel, QApplication, QAction, QFileDialog, QStatusBar, QMessageBox, QTextEdit
from PyQt5.QtGui import QPalette, QColor

def getAngle(pre, lat):
    return ((pre - lat + 179) % 360 + 1)

def ifNotOneAppend(item, *target):
    print(item['bpmMultiplier'])
    if item['bpmMultiplier'] != 1:
        return paperlib.append(item, target[0])

test = []

print(ifNotOneAppend({'bpmMultiplier': 2}, []))



theAngle = {
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


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        '''btn = QPushButton('Quit', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(sys.exit())'''

        select = QLabel('파일: ')
        bpmModeLabel = QLabel('소용돌이 모드: ')

        self.fileSelected = QLineEdit()
        self.fileSelected.setReadOnly(True)
        self.fileSelected.setPlaceholderText('선택된 파일이 없습니다.')

        fileMenu = QPushButton('열기')
        fileMenu.clicked.connect(self.showDialog)

        self.dir = ''

        self.run = QPushButton('승수 넣기')
        self.run.setEnabled(False)
        self.run.clicked.connect(self.makeBpm)

        self.bpmMode = QComboBox()
        self.bpmMode.addItem('소용돌이 X')
        self.bpmMode.addItem('안으로 돌기')
        self.bpmMode.addItem('밖으로 돌기')
        #bpmMode.addItem('사용자 지정')

        statusLabel = QLabel('상태: ')
        self.status = QTextEdit()
        self.status.setReadOnly(True)

        grid.addWidget(select, 0, 0)
        grid.addWidget(self.fileSelected, 0, 1)
        grid.addWidget(fileMenu, 0, 2)

        grid.addWidget(bpmModeLabel, 1, 0)
        grid.addWidget(self.run, 1, 2)
        grid.addWidget(self.bpmMode, 1, 1)

        grid.addWidget(statusLabel, 2, 0)
        grid.addWidget(self.status, 2, 1)

        #os.system('cls')
        self.setWindowTitle('Magicshape BPM Multiplier')
        self.setGeometry(300, 300, 450, 120)
        self.setFixedSize(450, 140)
        self.show()

    def showDialog(self):
        filters = "ADOFAI Custom Files (*.adofai)"
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', filters)
        if fname[0]:
            self.fileSelected.setText(fname[0])
            self.dir = fname[0]
        if str(fname[0]).endswith('.adofai'):
            self.run.setEnabled(True)
        else:
            self.run.setEnabled(False)

    def makeBpm(self):
        global angle
        try:
            data = open(self.dir, mode='r', encoding='utf-8-sig').read()
            data = data.replace(', }', ' }')
            data = data.replace(' }\n', ' },\n')
            data = data.replace(' },\n	]',' }\n	]')
            data = json.loads(data)
            pathData = data['pathData']
            pathList = []
            for i in range(len(pathData) - 1):
                try:
                    pre = theAngle[pathData[i]]
                    lat = theAngle[pathData[i+1]]
                    pathList.append(getAngle(pre, lat))
                except KeyError as e:
                    print('Warning: Unsupported angle! ({})'.format(e))
                    pathList.append(180)
            actions = data['actions']
            tmp = 0
            twirl = 0
            direction = 0
            for i in pathList:
                if self.bpmMode.currentText() == '소용돌이 X':
                    ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp]/pathList[tmp-1] }, actions)
                elif self.bpmMode.currentText() == '안으로 돌기':
                    if direction % 2 == 0:
                        angle = pathList[tmp]
                    else:
                        angle = (((359 - pathList[tmp]) % 360) + 1)
                    if angle <= 180:
                        if direction % 2 == 0:
                            ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp]/pathList[tmp-1] }, actions) # 기본모드
                        else:
                            ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / (((359 - pathList[tmp-1]) % 360) + 1) }, actions)
                        twirl = 0
                    else:
                        actions.append({ "floor": tmp + 1, "eventType": "Twirl" })
                        if direction % 2 == 0:
                            if twirl == 0:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / pathList[tmp-1] }, actions)
                            else:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / pathList[tmp-1] }, actions)
                        else:
                            if twirl == 0:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp] / pathList[tmp-1] }, actions)
                                
                            else:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp] / (((359 - pathList[tmp-1]) % 360) + 1) }, actions)
                        direction += 1
                        twirl = 1
                elif self.bpmMode.currentText() == '밖으로 돌기':
                    if direction % 2 == 0:
                        angle = pathList[tmp]
                    else:
                        angle = (((359 - pathList[tmp]) % 360) + 1)
                    if angle >= 180:
                        if direction % 2 == 0:
                            ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp]/pathList[tmp-1] }, actions) # 기본모드
                        else:
                            ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / (((359 - pathList[tmp-1]) % 360) + 1) }, actions)
                        twirl = 0
                    else:
                        actions.append({ "floor": tmp + 1, "eventType": "Twirl" })
                        if direction % 2 == 0:
                            if twirl == 0:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / pathList[tmp-1] }, actions)
                            else:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": (((359 - pathList[tmp]) % 360) + 1) / pathList[tmp-1] }, actions)
                        else:
                            if twirl == 0:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp] / pathList[tmp-1] }, actions)
                                
                            else:
                                ifNotOneAppend({ "floor": tmp + 1, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": pathList[tmp] / (((359 - pathList[tmp-1]) % 360) + 1) }, actions)
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
            file = open(self.dir + '_multiplied.adofai', mode='w')
            file.write(json.dumps(filedata, indent=4))
            
            self.status.setText(self.dir + '_multiplied.adofai에 파일이 저장되었습니다.')
        except Exception as e:
            self.status.setText('예외 발생: {}'.format(e))
            raise e

if __name__ == '__main__':
    print('잠시만 기다리세요...')
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
