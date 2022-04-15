import sys
import os
import re
import json
# import win32gui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QIcon,QKeySequence,QPixmap,QGuiApplication,QPainter,QColor,QTextCharFormat,QBrush,QTextCursor,QFont)
from PyQt5.QtCore import *
# from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent,QMediaPlaylist

config = {}
workdir = os.path.dirname(os.path.abspath(sys.argv[0]))
configfile = workdir+"\\config.json"
if os.path.exists(configfile):
    with open(configfile) as f:
         config = json.loads(f.read())
else:
    config["totalgoodluck"] = 0
    config["totalbadluck"] = 0
    config["totalnormalluck"] = 0

class Static(QWidget):
    def __init__(self):
        super().__init__()
        self.goodluck = 0
        self.badluck = 0
        # self.totalgoodluck = 0
        # self.totalbadluck = 0
        # self.totalgood = config["totalgoodluck"]
        # self.totalbad = config["totalbadluck"]
        
        # self.good = MyGroupBox(self,"运气好:",self.totalgood)
        # self.bad = MyGroupBox(self,"运气差:",self.totalbad)
        # self.normal = MyGroupBox(self,"运气正常:",self.totalnormal)
        
        self.good = MyGroupBox(self,"运气好:",config["totalgoodluck"])
        self.bad = MyGroupBox(self,"运气差:",config["totalbadluck"])
        self.normal = MyGroupBox(self,"运气正常:",config["totalnormalluck"])
        self.changepersent()
        hbox = QHBoxLayout()
        hbox.addWidget(self.good)
        hbox.addWidget(self.bad)
        hbox.addWidget(self.normal)
        
        clearonebtn = QPushButton("重置本次")
        # clearbtn.setMaximumWidth(42)
        clearonebtn.clicked.connect(self.clearone)
        
        clearbtn = QPushButton("重置所有")
        # clearbtn.setMaximumWidth(42)
        clearbtn.clicked.connect(self.clear)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(clearonebtn)
        hbox2.addWidget(clearbtn)
        
        self.tips = QLabel("")
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.tips)
        
        self.setLayout(vbox)
        
        screen = QGuiApplication.primaryScreen()
        rect = screen.geometry()
        self.setGeometry(rect.center().x()-150,rect.center().y()-150, 250, 120)
        self.setWindowTitle('运气统计')  
        self.show()
        
        file = 'C:\\Users\\y\\AppData\\Roaming\\HearthstoneDeckTracker\\Logs\\hdt_log.txt'
        # file = 'hdt_log.txt'
        self.f= open(file,encoding="utf8")
        # file2 = 'D:\\Game\\Hearthstone\\Logs\\Power.log'
        # file2 = 'Power.log'
        # self.f2= open(file2,encoding="utf8")
        self.f2 = None
        s = self.f.read()
        start = s.rfind("Game ended...")
        if start == -1:
            start = 0
        print(start)
        self.f.seek(start)
        # self.fileWatcher.addPath(file)      
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.showText)
        self.timer.start()
        self.temps = ""
        self.hero = ""
        self.running = False
        self.found = False
        self.ingame = False
        self.s0 = ""
        self.s = ""
        # self.exclude_id =["BG22_HERO_004p","BG20_HERO_201e3","BG20_HERO_101pe2","BG20_HERO_301p","BG20_HERO_301pe","BG20_HERO_100p_e2","BG20_HERO_100p"]
        self.showText()
        
    def showText(self):
        # print("in showText")
        s = self.f.read()
        # print(s)
        
        # GameV2.UpdatePlayers >> SilentSword#555176 [PlayerId=1] vs 旗鼓相当的对手#524769 [PlayerId=2]
        sobj = re.search('GameV2.UpdatePlayers >> (.*) \[PlayerId=.*?\] vs (.*) \[PlayerId=.*?\]', s)
        if sobj:
            bob = sobj.group(2)
            print(f"op:{bob}")
            if bob == "调酒师鲍勃":
                self.ingame = True
        if self.ingame:
            if self.hero == "":
                sobj = re.search('Player.Play .*cardId=(.*HERO.*), cardName=(.*), zonePos=', s) #正常是这个
                if sobj:
                    if "Buddy" not in sobj.group(1):
                        self.hero_id = sobj.group(1)
                        self.hero = sobj.group(2)
                        print(f'---------------your hero id:{self.hero_id}---------------------')
                        print(f'---------------your hero:{self.hero}---------------------')
                        self.tips.setText(f'你的英雄:{self.hero}')
                        return
                sobj = re.search('GameEventHandler.SetPlayerHero >> Player=(.*)', s) #中断重连的时候是这个
                if sobj:
                    hero = sobj.group(1)
                    if hero != "BaconPHhero":
                        self.hero = hero
                        print(f'----------------your hero:{self.hero}---------------------')
                        self.tips.setText(f'你的英雄:{self.hero}')
                        # return
            sobj = re.search('(\d+:\d\d:\d\d)\|.*Player.PlayToGraveyard >> \[Player\] id=\d+, cardId=TB_BaconShop_3ofKindChecke, cardName=3ofKindCheckPlayerEnchant, zonePos=0,Info={turn=\d+, mark=Created, created=true, originalZone=',s)
            if sobj:
                self.begintime = sobj.group(1)
                print(f'---------------begin time:{self.begintime}---------------------------------------------------')
                self.tips.setText(f'团战开始...')
                self.player_dead = False
                self.oppo_dead = False
                self.found = False
                self.normal_res = False
                # self.player_damge = 0
                # self.oppo_damge = 0
                self.running = True
            sobj_arr = re.finditer('(\d+:\d\d:\d\d)\|.*Player.CreateInPlay .*cardId=(.*HERO.*), cardName=(.*), zonePos=', s) 
            # print(sobj_arr)
            # if sobj:
            for sobj in sobj_arr:
                if "Buddy" not in sobj.group(2) and "p" not in sobj.group(2).replace("BaconShop","") and "e" not in sobj.group(2).replace("KelThuzad","") and "t" not in sobj.group(2):
                    # self.begintime = sobj.group(1)
                    self.oppo_id = sobj.group(2)
                    self.oppo = sobj.group(3)
                    print(f'opponent id:{self.oppo_id}')
                    print(f'opponent:{self.oppo}')
                    self.tips.setText(f'团战开始,你的对手:{self.oppo}')
            sobj = re.search('WinRate=(.*)% \(Lethal=(.*)%\), TieRate=(.*)%, LossRate=(.*)% \(Lethal=(.*)%\)', s)
            if self.running and sobj:
                self.wr = float(sobj.group(1))
                self.br = float(sobj.group(2))
                self.tr = float(sobj.group(3))
                self.lr = float(sobj.group(4))
                self.dr = float(sobj.group(5))
                print(f'winrate:{self.wr},beatrate:{self.br},tierate:{self.tr},lostrate:{self.lr},deadrate:{self.dr}')
                # self.tips.setText(f'团战开始...')
                # self.running = True
            if self.running and (s.find("Player.DeckToPlay") != -1 or s.find("Game ended...") != -1):
                if s.find("Game ended...") != -1:
                    self.hero = ""
                    self.ingame = False
                self.temps += s
                self.running = False
                sobj = re.search('Updating entities with attacker=(.*), defender=(.*)', self.temps)
                if sobj:
                    winner = sobj.group(1)
                    loser = sobj.group(2)
                else:
                    winner = "tie"
                    loser = ""
                print(f'winner:{winner},loser:{loser}')
                self.temps = ""
                if self.wr == self.tr and self.lr == self.wr: #三者相等，哪种结果都正常
                    # print("normal luck!")
                    # self.tips.setText(f'本次团战运气正常')
                    # self.normal.add()
                    self.add_normal()
                else:
                    maxrate = max([self.wr,self.tr,self.lr])
                    if maxrate == self.wr:
                        if self.wr == self.lr: #输赢概率相等，结果应该是平，赢了是运气好，输了是运气不好
                            if winner == self.hero:
                                # print("good luck!")
                                # self.tips.setText(f'本次团战运气好')
                                # self.good.add()
                                self.add_good()
                            elif winner != self.hero and winner != "tie":
                                # print("bad luck!")
                                # self.tips.setText(f'本次团战运气不好')
                                # self.bad.add()
                                self.add_bad()
                            else:
                                # print("normal luck!")
                                # self.tips.setText(f'本次团战运气正常')
                                # self.normal.add()
                                self.add_normal()
                        elif self.wr == self.tr: #赢平概率相等，结果应该是赢平，输了是运气不好
                            if winner != self.hero and winner != "tie":
                                # print("bad luck!")
                                # self.tips.setText(f'本次团战运气不好')
                                # self.bad.add()
                                self.add_bad()
                            else:
                                # print("normal luck!")
                                # self.tips.setText(f'本次团战运气正常')
                                # self.normal.add()
                                self.add_normal()
                        else:   #概率都不等，结果应该是赢，输平都是运气不好
                            if winner != self.hero or winner == "tie":
                                # print("bad luck!")
                                # self.tips.setText(f'本次团战运气不好')
                                # self.bad.add()
                                self.add_bad()
                            else:
                                # print("normal luck!")
                                # self.tips.setText(f'本次团战运气正常')
                                # self.normal.add()
                                self.add_normal()
                    if maxrate == self.lr:
                        if self.lr == self.tr: #输平概率相等，结果应该是输平，赢了是运气好
                            if winner == self.hero:
                                # print("good luck!")
                                # self.tips.setText(f'本次团战运气好')
                                # self.good.add()
                                self.add_good()
                            else:
                                # print("normal luck!")
                                # self.tips.setText(f'本次团战运气正常')
                                # self.normal.add()
                                self.add_normal()
                        else:   #概率都不等，结果应该是输，赢平都是运气好
                            if winner == self.hero or winner == "tie":
                                # print("good luck!")
                                # self.tips.setText(f'本次团战运气好')
                                # self.good.add()
                                self.add_good()
                            else:
                                # print("normal luck!")
                                # self.tips.setText(f'本次团战运气正常')
                                # self.normal.add()
                                self.add_normal()
                    if maxrate == self.tr: #概率都不等，结果应该是平，赢了是运气好，输了是运气不好
                        if winner == self.hero:
                            # print("good luck!")
                            # self.tips.setText(f'本次团战运气好')
                            # self.good.add()
                            self.add_good()
                        elif winner != self.hero and winner != "tie":
                            # print("bad luck!")
                            # self.tips.setText(f'本次团战运气不好')
                            # self.bad.add()
                            self.add_bad()
                        else:
                            # print("normal luck!")
                            # self.tips.setText(f'本次团战运气正常')
                            # self.normal.add()
                            self.add_normal()
                #判断死亡
                if self.found and self.normal_res: #有找到伤害信息并且通过胜率判断是普通时才判断死亡
                    if not self.oppo_dead and self.br > 50:
                        self.add_bad()
                        self.normal.delete() #normal减1
                    elif self.oppo_dead and self.br <= 50:
                        # print("good luck!")
                        # self.tips.setText(f'本次团战运气好')
                        # self.good.add()
                        self.add_good()
                        self.normal.delete() #normal减1
                    elif self.player_dead and self.dr <= 50:
                        # print("bad luck!")
                        # self.tips.setText(f'本次团战运气不好')
                        # self.bad.add()
                        self.add_bad()
                        self.normal.delete() #normal减1
                    elif not self.player_dead and self.dr > 50:
                        self.add_good()
                        self.normal.delete() #normal减1
            if self.running:
                self.temps += s
                
        self.showText2()
        
        
    def add_good(self):
        print("good luck!")
        self.tips.setText(f'本次团战运气好')
        self.good.add()
        
    def add_bad(self):
        print("bad luck!")
        self.tips.setText(f'本次团战运气不好')
        self.bad.add()
        
    def add_normal(self):
        print("normal luck!")
        self.tips.setText(f'本次团战运气正常')
        self.normal.add()
        self.normal_res = True
        
    def showText2(self):
        if not self.f2:
            file2 = 'D:\\Game\\Hearthstone\\Logs\\Power.log'
            # file2 = 'Power.log'
            if os.path.exists(file2):
                self.f2= open(file2,encoding="utf8")
            else:
                return
        self.s0 = self.s  #这个结果出的太快，用上一个5s的数据
        self.s = self.f2.read()
        if not self.running or self.found: #没在对战或在这次对战中已经找到了就不找了
            return
            
        # print('================begin==================')
        '''#模拟日志没显示伤害数，暂时做不了
        sobj = re.finditer('GameState.DebugPrintPower\(\) - +TAG_CHANGE Entity=\[entityName=(.*) id=\d+ zone=PLAY zonePos=0 cardId=(.*HERO.*) player=\d+\] tag=PREDAMAGE value=(\d+)', self.s0)
        for i in sobj:
            if "Buddy" in i.group(2) or int(i.group(3))==0:
                continue
            print(f'name:{i.group(1)},id:{i.group(2)},predamage:{i.group(3)}')
            if i.group(2) == self.hero_id:
                self.player_damge = i.group(3)
            elif i.group(2) == self.oppo_id:
                self.oppo_damge = i.group(3)
            else:
                print("something wrong")
        '''
        #查找伤害信息，判断是否死亡
        sobj = re.finditer('GameState.DebugPrintPower\(\) - +TAG_CHANGE Entity=\[entityName=(.*) id=\d+ zone=PLAY zonePos=0 cardId=(.*HERO.*) player=\d+\] tag=DAMAGE value=(\d+)', self.s0)
        for i in sobj:
            self.found = True
            print(f'name:{i.group(1)},damage:{i.group(3)},id:{i.group(2)}')
            if i.group(2) == "TB_BaconShop_HERO_34": #胖子
                health = 55
            else:
                health = 40
            if int(i.group(3))>=health:
                if i.group(2) == self.oppo_id:
                    print("opponent dead")
                    self.oppo_dead = True
                elif i.group(2) == self.hero_id:
                    print("player dead")
                    self.player_dead = True
        # print('===============end===================')
        
    def clear(self):
        ret = QMessageBox.warning(self,"警告","所有数据将会删除且无法恢复，是否继续？",QMessageBox.Ok|QMessageBox.Cancel)
        print(ret)
        if ret == QMessageBox.Ok:
            config["totalgoodluck"] = 0
            config["totalbadluck"] = 0
            config["totalnormalluck"] = 0
            self.good.luck = self.bad.luck = self.normal.luck = 0
            self.good.total = self.bad.total = self.normal.total = 0
            self.good.lucklabel.setText("0")
            self.bad.lucklabel.setText("0")
            self.normal.lucklabel.setText("0")
            self.good.totalluck.setText("0")
            self.bad.totalluck.setText("0")
            self.normal.totalluck.setText("0")
            self.changepersent()
            
    def clearone(self):
        self.good.luck = self.bad.luck = self.normal.luck = 0
        self.good.lucklabel.setText("0")
        self.bad.lucklabel.setText("0")
        self.normal.lucklabel.setText("0")
        self.changepersent()
            
    def changepersent(self):
        if self.good.luck+self.bad.luck+self.normal.luck == 0:
            self.good.persent.setText("0%")
            self.bad.persent.setText("0%")
            self.normal.persent.setText("0%")
        else:
            self.good.persent.setText(str(round(self.good.luck/(self.good.luck+self.bad.luck+self.normal.luck)*100,1))+"%")
            self.bad.persent.setText(str(round(self.bad.luck/(self.good.luck+self.bad.luck+self.normal.luck)*100,1))+"%")
            self.normal.persent.setText(str(round(self.normal.luck/(self.good.luck+self.bad.luck+self.normal.luck)*100,1))+"%")
            
        if self.good.total+self.bad.total+self.normal.total == 0:
            self.good.totalpersent.setText("0%")
            self.bad.totalpersent.setText("0%")
            self.normal.totalpersent.setText("0%")
        else:
            self.good.totalpersent.setText(str(round(self.good.total/(self.good.total+self.bad.total+self.normal.total)*100,1))+"%")
            self.bad.totalpersent.setText(str(round(self.bad.total/(self.good.total+self.bad.total+self.normal.total)*100,1))+"%")
            self.normal.totalpersent.setText(str(round(self.normal.total/(self.good.total+self.bad.total+self.normal.total)*100,1))+"%")
        self.saveconfig()

    def closeEvent(self,e):
        # config["totalgoodluck"] = self.good.total
        # config["totalbadluck"] = self.bad.total
        # config["totalnormalluck"] = self.normal.total
        # with open(configfile,"w") as f:
            # f.write(json.dumps(config,indent=4))
        print("exit")
        self.saveconfig()
        self.timer.stop()
        self.f.close()
        if self.f2:
            self.f2.close()
        
    def saveconfig(self):
        config["totalgoodluck"] = self.good.total
        config["totalbadluck"] = self.bad.total
        config["totalnormalluck"] = self.normal.total
        with open(configfile,"w") as f:
            f.write(json.dumps(config,indent=4))
        
class MyGroupBox(QGroupBox):
    def __init__(self,par,label,total):
        super().__init__(label)
        self.luck = 0
        self.par = par
        self.total = total
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("本次:"))
        self.lucklabel = QLabel("0")
        hbox1.addWidget(self.lucklabel)
        self.persent = QLabel("0%")
        hbox1.addWidget(self.persent)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("累计:"))
        self.totalluck = QLabel(str(self.total))
        hbox2.addWidget(self.totalluck)
        self.totalpersent = QLabel("0%")
        hbox2.addWidget(self.totalpersent)
        
        # addbtn = QPushButton("加1")
        # addbtn.setMaximumWidth(42)
        # addbtn.clicked.connect(self.add)
        # delbtn = QPushButton("减1")
        # delbtn.setMaximumWidth(42)
        # delbtn.clicked.connect(self.delete)
        # btnhbox = QHBoxLayout()
        # btnhbox.addWidget(addbtn)
        # btnhbox.addWidget(delbtn)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        # vbox.addLayout(btnhbox)
        self.setLayout(vbox)
        
    def add(self):
        self.luck += 1
        self.total += 1
        self.lucklabel.setText(str(self.luck))
        self.totalluck.setText(str(self.total))
        self.par.changepersent()
        
    def delete(self):
        self.luck -= 1
        if self.luck < 0:
            self.luck = 0
        self.total -= 1
        if self.total < 0:
            self.total = 0
        self.lucklabel.setText(str(self.luck))
        self.totalluck.setText(str(self.total))
        self.par.changepersent()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Static()
    sys.exit(app.exec_())