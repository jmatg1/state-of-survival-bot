import os
import time
from datetime import datetime
from PIL import Image
from PIL import ImageOps
from tkinter import Tk, Button, Text, END

from tkinter import ttk

import threading
import multiprocessing
from subprocess import check_output, Popen, PIPE
# from com.dtmilano.android.adb.adbclient import AdbClient

tkWindow = Tk()
tkWindow.geometry('400x250')
tkWindow.title('SoS Bot By Jmatg1')


# im = Image.open("bride.jpg")
# im.rotate(45).show()

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class Bot:
    work = 1
    screenshot = 0
    t1 = 0
    fight = 1
    device = 0
    controlsUnderBuilding = [(576, 431), (1059, 768)]
    # def __init__(self):
    def shadeVariation(self, col, col2, shade = 0):
        if shade == 0:
            return col == col2
        rezult = (abs(col[0] - col2[0]), abs(col[1] - col2[1]), abs(col[2] - col2[2]))
        shadowCount = 0
        for rgb in rezult:
            if rgb <= shade:
                shadowCount += 1
        return shadowCount == 3

    def getXYByColor(self, color, isGetSCreen=True, shade = 0, startXY = (0,0), endXY=(0,0)):
        if (isGetSCreen):
            self.getScreen()
        img = self.screenshot
        coordinates = False


        if endXY[0] == 0 and endXY[1] == 0:
            endXY = (img.size[0], img.size[1])
        for x in range(img.size[0]):
            if not(startXY[0] < x < endXY[0]):
                continue

            for y in range(img.size[1]):
                if not(startXY[1] < y < endXY[1]):
                    continue
                if self.shadeVariation(img.getpixel((x, y))[:3],  color, shade):
                    coordinates = (x, y)
                    continue
        return coordinates

    def pixelSearch(self, x1, y1, color):  # x2=1600, y2=900,
        # im = ImageOps.crop(im, (x1, y1, x2, y2))
        colorPixel = self.screenshot.getpixel((x1, y1))[:3]
        if colorPixel == color:
            return True
        else:
            return False

    def getScreen(self):
        self.shell(f'/system/bin/screencap -p /sdcard/{self.device}-screenshot.png')
        # os.system('hd-adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        # Using the adb command to upload the screenshot of the mobile phone to the current directory

        os.system(f'hd-adb -s {self.device} pull /sdcard/{self.device}-screenshot.png')
        try:
            self.screenshot = Image.open(f"{self.device}-screenshot.png")
        except ValueError:
            print(ValueError)
            self.getScreen()

    def getPixelColor(self, x1, y1):
        self.getScreen()
        im = Image.open(f"{self.device}-screenshot.png")
        # im1 = ImageOps.crop(im, (0, 0, 1000, 300))
        # im1.show()
        pixelRGB = im.getpixel((x1, y1))[:3]
        return pixelRGB

    def click(self, x, y, timer=True):
        if (timer):
            time.sleep(1)
        # os.system(f'hd-adb shell input tap {x} {y}')
        self.shell(f'input tap {x} {y}')
        if (timer):
            time.sleep(1)

    # getScreen()
    # click(1550, 700)
    # pixelSearch(1550, 700)

    def isStop(self):
        return self.work == 0

    def farmBot(self):
        cicle = 0

        while self.work:
            self.getScreen()

            self.skipAds()

            if self.isMainScreen():
                self.log('Main')

                self.chechAttack()

                self.updateBuilding()

                self.trainTroops()

                self.reseach()

                self.intelligence()

                self.clanMission()


            else:
                self.log('Not Main. REstart App')
                self.shell('am force-stop com.kingsgroup.sos')
                # os.system('hd-adb shell am force-stop com.kingsgroup.sos')
                time.sleep(5)
                self.shell('monkey -p com.kingsgroup.sos -v 500')
                # os.system('hd-adb shell monkey -p com.kingsgroup.sos -v 500')
                time.sleep(30)
                continue
            self.log('Wait 1m')


            sleep = 0
            while sleep <= 60:
                self.chechAttack()
                sleep+=1
                time.sleep(1)


            cicle += 1

        self.log('STOP')

    def main(self):
        cicle = 0

        while self.work:
            self.getScreen()

            self.skipAds()

            if self.isMainScreen():
                self.log('Main')

                self.chechAttack()

                if (cicle % 5 == 0):
                    self.updateBuilding()


                if (cicle % 5 == 0):
                    self.trainTroops()


                if (cicle % 5 == 0):
                    self.reseach()


                if (cicle % 5 == 0):
                    self.intelligence()

                self.clanMission()


                # if (cicle % 120 == 0):
                #     self.raid()

                # if (cicle % 3600 == 0):
                #     self.intel()


                # if cicle % 120:
                # self.joinGroup()

            else:
                self.log('Not Main. REstart App')
                self.shell('am force-stop com.kingsgroup.sos')
                # os.system('hd-adb shell am force-stop com.kingsgroup.sos')
                time.sleep(5)
                self.shell('monkey -p com.kingsgroup.sos -v 500')
                # os.system('hd-adb shell monkey -p com.kingsgroup.sos -v 500')
                time.sleep(30)
                continue
            self.log('Wait 1m')
            # if cicle % 30:
            #     self.joinGroup()

            sleep = 0
            while sleep <= 60:
                if self.work == 0:
                    break

                self.chechAttack()
                self.joinGroup()
                sleep+=1
                time.sleep(1)

            cicle += 1

        self.log('STOP')

    def compareColor(self, cord, color, shade = 0):
        color0 = self.getPixelColor(cord[0], cord[1])
        return self.shadeVariation(color0, color, shade)


    def joinGroup(self):
        self.log('Check Can i Join Group')
        cord = self.getXYByColor((174,114,40), True, 5, (1540, 305), (1584, 348))
        if cord:
            self.log('Click Group Screen')
            self.click(cord[0] - 30, cord[1] + 30)
            time.sleep(3)
            self.log('Search available group')
            cord = self.getXYByColor((95,120,46), True, 5, (1227, 102), (1527, 882))
            if cord:
                self.log('Found')
                self.click(cord[0], cord[1])
                time.sleep(3)

                self.log('Check Stamina')
                if  self.isStaminaEnded():
                    self.log('Stamina Ended')
                    self.clickClose()
                    self.log('Return to Settlement')
                    self.clickClose()
                    return

                self.log('Check Limit MARCH')
                if self.isSmallAlert():
                    self.log('Return to Settlement')
                    self.clickClose()
                    return


                cord = self.getXYByColor((122,122,122), True, 0, (1123, 821),(1151, 838))
                if cord: # проверка на пустые войска
                    self.log(f'There are not enough troops {cord}', )
                    self.click(1445, 74)
                    self.log('Return to Settlement')
                    self.clickClose()
                    return
                self.log('Clear Troops')
                self.click(773, 789)
                self.log('Add 1 Troops')
                self.click(1289, 279)
                self.log('MARCH')
                self.click(1269, 801)
                self.log('Check message Abount enought Troops')
                cord = self.getXYByColor((96,45,45), True, 5, (410, 561), (795, 659))
                if cord:
                    self.click(611, 611)
            self.log('Return to Settlement')
            self.clickClose()

        self.log('i Can`t')

    def isSmallAlert(self):
        cord = self.getXYByColor((111,80,36), True, 1, (375, 191), (1217, 701)) #лимит марша

        if cord:
            self.log('March is Limit. Close')
            self.click(1182, 233)
            return True
        return False

    def isStaminaEnded(self):
       return self.getXYByColor((179,137,88), True, 1, (537, 233), (591, 266)) #закончилась выносливать

    def chechAttack(self):
        self.log('Check Attack')
        if self.compareColor((1525, 468), (195, 69, 69), 10):
            self.log('Attack')
            self.click(1401,850 )
            time.sleep(3)
            self.click(90, 600)
            time.sleep(3)
            cord = self.getXYByColor((77,114,43), True, 0, (182, 80), (861, 263)) # shield 2h
            cord1 = self.getXYByColor((77,114,43), True, 5, (182, 80), (861, 263)) # shield 8h

            if cord:
                self.click(cord[0], cord[1])
                self.click(1338, 825)
            elif cord1:
                self.click(cord1[0], cord1[1])
                self.click(1338, 825)

            self.clickClose()

    def skipAds(self):
        if self.isMainScreen() == False:
            if self.pixelSearch(1499, 156, (138, 136, 135)):  # Рекалма в начале запуска игры
                self.click(1499, 156)
            cord = self.getXYByColor((203,203,203), True, 5, (260, 101), (1560, 248))
            if cord:                     # Рекалма о охуительном предложении
                self.click(cord[0], cord[1])
                time.sleep(3)

    def recognizeMarkerIntel(self):
        self.log('Try Recognize Marker')
        positionMarker = [(748, 208), (841, 312)]
        purpColor = (188,71,161)

        isPurple = self.getXYByColor(purpColor, True, 5, positionMarker[0], positionMarker[1])
        if isPurple:
            self.log('Is Purple')
            self.click(isPurple[0], isPurple[1] )

    def intel(self):

        self.log('Intel Start')

        self.log('Open Wilderness')
        self.openWildernessOrSettlement()

        intelStart = 1
        while intelStart:
            def openSearch():
                time.sleep(3)
                self.log('Click Search')
                self.click(71, 704)

                time.sleep(3)
                self.log('Click Intel')
                self.click(126, 645)

            openSearch()

            time.sleep(3)
            self.log('Go Search')
            self.click(1362, 822)

            self.log('Wait 3 sec')
            time.sleep(3)

            self.log('Click on Center')
            self.click(797, 365)

            self.log('Check...')

            cord = self.getXYByColor((137, 88, 32))
            raidCord = self.getXYByColor((100,124,42))
            if cord:
                self.log('Click Successful')

                if not self.getXYByColor((82, 107, 34)):
                    self.log('Skip Dialogs')
                    self.click(1482, 90)

                self.log('Click')
                self.click(1324, 809)

                time.sleep(3)

                self.log('Check the number of marches')
                if self.compareColor((1000, 600), (111, 136, 53), 5):
                    self.log('Not enough MARCH. Close')
                    self.click(1181, 227)

                self.log('Click Level')
                self.click(918, 786)

                # self.log('Click ATTACK')
                # self.click(1308, 803)
                self.log('Click MARCH')
                self.click(1308, 803)


                self.log('Check Object of March')
                if self.getPixelColor(1184, 229) == (203, 203, 199):
                    self.log('Not Object of March. Close')
                    self.click(1181, 227)

            elif raidCord:
                self.log('Btn Raid Found. Click')
                self.click(1042, 800)
                waitEnding = 1
                while waitEnding:
                    self.log('Wait Ending')
                    time.sleep(10)
                    if self.getPixelColor(597, 202) == (255, 221, 162):
                        self.log('Win')
                        self.clickCenter()
                        self.clickCenter()
                        self.clickCenter()
                        self.clickCenter()
                        waitEnding = 0
                        break

                    color = self.getPixelColor(1186, 637)

                    if color == (76, 101, 35):
                        self.log('Lose')
                        self.clickCenter()
                        self.clickClose()
                        # self.click(1100, 663)
                        time.sleep(3)
                        waitEnding = 0
                        return
            else:
                self.log('Not Found')
                intelStart = 0

                if self.getPixelColor(146, 861) == (55, 55, 55):
                    self.log('Intel Search is Open')
                else:
                    openSearch()
                break

        self.log('Open Intel Screen')
        self.openWildernessOrSettlement()
        time.sleep(3)

        self.log('Try to collect...')

        cord = self.getXYByColor((157, 44, 31), True, 5)

        while cord:
            self.log('Found Red Marker. Click')
            self.click(cord[0] - 50, cord[1], False)
            # self.log('Check Collect Btn')
            # cord2 = self.getXYByColor((88, 112, 41))
            # if cord2:
            #     self.log('Collect Click')
            self.click(1304, 681)

            self.log('Check Window...')
            time.sleep(3)

            if self.getXYByColor((88,81,68)):
                self.click(1260,206 )
                time.sleep(3)

            cord = self.getXYByColor((157, 44, 31), True, 5)

            self.log(cord)

        self.log('Exit Intel Screen')
        self.click(1554, 54)

        self.log('Open Settlement')
        self.openWildernessOrSettlement()

        self.log('Intel End')

    def clanMission(self):
        self.log('OPen Clan')
        self.click(1140, 848)
        time.sleep(1)
        self.log('OPen Tech')
        self.click(1482, 542)  #
        self.log('Wait 3 sec')
        time.sleep(3)
        self.click(1005, 42)
        self.log('Search...')

        # coord = self.getXYByColor((35,35,35), True, 0, (257, 174), (1182, 804))

        self.log('Search Recommendations')
        coord = self.getXYByColor((114,27,27), True, 5, (257, 174), (1500, 804))
        self.log(coord)
        # coord1 = self.getXYByColor((104,22,22))
        # coord2 = self.getXYByColor((94,21,25))
        if (coord):
            self.log('Open Cart')
            self.click(coord[0], coord[1])
            self.click(coord[0], coord[1])
            self.click(coord[0], coord[1])
            self.click(coord[0], coord[1])
            self.click(coord[0], coord[1])
            self.click(coord[0], coord[1])
            self.click(coord[0], coord[1])
            count = 1
            while count < 11:
                self.log('Click')
                self.click(1149, 614, False)
                self.click(1149, 675, False)
                self.click(1149, 749, False)
                count += 1
            self.log('Close Cart')
            self.click(1333, 140)
            self.log('Return')
            self.click(46, 33)
        else:
            self.log('Return')
            self.click(46, 33)

        self.log('Shake Hand')
        self.click(890, 730)

        self.log('Click')
        self.click(848, 802)

        time.sleep(3)

        self.log('Return')
        self.click(46, 33)

        self.log('Open Screen Box')
        self.click(1495, 745)

        self.log('Click Alie`s Gift')
        self.click(1386, 347)

        self.log('Click Big Gift')
        self.click(363, 411)

        self.log('Close Ads')
        self.click(1185, 201)
        self.click(1185, 201)
        self.click(1185, 201)
        self.click(1185, 201)

        self.log('Collect Alie`s Gift...')

        search = 1
        while search:
            cord = self.getXYByColor((112, 145, 54))
            if cord:
                self.log('Found')
                self.click(cord[0], cord[1])
            else:
                search = 0
                self.log('Not Found')

        self.log('Click left tab')
        self.click(866, 213)

        self.log('Collect')
        self.click(1328, 852)

        self.log('Close Window')
        self.click(1185, 201)

        self.log('Close')
        self.click(1554, 28)

    def raid(self):
        self.log('Raid Start')
        self.log('Open Wilderness')
        self.click(77, 827)  # Wilderness
        time.sleep(5)
        self.log('Open Settlement')
        self.click(77, 827)  # Settlement
        time.sleep(5)
        self.log('Click Build Hero')
        self.click(1139, 518)  # Click Build Hero
        self.log('Open Raid')
        self.click(1401, 507)  # Open Raid
        self.log('OOpen Step')
        self.click(1112, 476)  # Open Step

        def fight():
            scan = 0
            while scan < 6:
                markerCoord = self.getXYByColor((243, 51, 68), True, 5)
                if markerCoord:
                    self.click(markerCoord[0], markerCoord[1])
                    time.sleep(2)
                    self.click(1028, 801)  # Go Fight
                    # if(self.pixelSearch()):
                    #     return
                    #
                    break
                scan += 1
            if scan == 6:
                self.log('exit. And Wait 5 sec')
                self.click(1443, 62)
                self.clickClose()
                time.sleep(5)
                self.log('Raid Stop 1')
                return

            waitEnding = 1
            while waitEnding:
                self.log('Wait Ending')
                time.sleep(10)
                if self.getPixelColor(597, 202) == (255, 221, 162):
                    self.log('Win')
                    self.clickCenter()
                    self.clickCenter()
                    self.clickCenter()
                    self.clickCenter()
                    waitEnding = 0
                    break

                color = self.getPixelColor(1186, 637)

                if color == (76, 101, 35):
                    self.log('Lose')
                    self.clickCenter()
                    self.clickClose()
                    # self.click(1100, 663)
                    time.sleep(5)
                    waitEnding = 0
                    self.log('Raid Stop 2')
                    return
            self.log('Step End. Repeat')
            fight()

        fight()
        self.log('Raid Stop')

    def isMainScreen(self):
        self.getScreen()
        if self.pixelSearch(1533, 615, (248, 248, 248)):  # 1340, 30, 1350, 40,
            return True
        elif self.pixelSearch(1533, 615, (253, 253, 253)):
            return True
        else:
            return False

    def trainTroops(self):
        self.click(22, 478)  # click left menu
        self.click(550, 182)  # click 1 troop

        def train():
            self.log('Start Train')
            self.click(806, 432)  # click on building
            self.click(806, 432)

            if self.getPixelColor(932, 645) == (94, 85, 85): # 72, 72, 72
                self.log('Found Troops Icon')
                self.click(932, 645)  # Open train screen
                time.sleep(1)
                self.log('Is Start')
                if self.getXYByColor((101,68,51), True, 2, (1188, 590), (1286, 650)):
                    self.log('Yes')
                    self.click(1553, 32)  # Click Clsoe
                else:
                    self.click(1364, 655)  # Click Train
                    self.click(1553, 32)  # Click Clsoe
            else:
                self.log('Skip Train')

        train()
        self.click(22, 478)  # click left menu
        self.click(550, 261)  # click 2 troop
        train()
        self.click(22, 478)  # click left menu
        self.click(550, 348)  # click 3 troop
        train()

    def reseach(self):
        self.log('reseach Start')
        self.clickLeftMenu()
        self.click(550, 493)  # click reseach
        self.click(987, 605)  # open reseach
        if (self.getPixelColor(489, 844) == (123, 82, 57)):  # in progress
            self.clickClose()
            self.log('reseach Finish')
            return
        if (self.fight):
            self.click(652, 835)  # open fight
        else:
            self.click(1437, 838)  # open economic
        self.click(1158, 823)  # Go
        self.clickClose()
        self.click(831, 301)  # arm
        self.log('reseach Finish')

    def intelligence(self):
        self.log('intelligence Start')
        self.clickLeftMenu()
        if (self.getPixelColor(35, 568) == (157, 94, 77)):
            self.click(551, 624)  # Open intelligence screen
            self.click(1115, 607)  # Collect
            self.click(1188, 305)  # Close
            if (self.isMainScreen() == False):
                self.click(1188, 305)  # Close
            self.log('intelligence Finish')
        else:
            self.closeLeftMenu()
            self.log('intelligence Finish Empty')

    def shakeHand(self):
        cord = self.getXYByColor((249, 200, 109))
        if (cord):
            self.click(cord[0], cord[1])

        cord = self.getXYByColor((255, 206, 115))
        if (cord):
            self.click(cord[0], cord[1])

        cord = self.getXYByColor((253, 207, 116))
        if (cord):
            self.click(cord[0], cord[1])

        cord = self.getXYByColor((241, 200, 109))
        if (cord):
            self.click(cord[0], cord[1])

        cord = self.getXYByColor((254, 205, 114))
        if (cord):
            self.click(cord[0], cord[1])

        cord = self.getXYByColor((253, 204, 113))
        if (cord):
            self.click(cord[0], cord[1])

    def searchUpdateIcon(self):
        cord = self.getXYByColor((50, 166, 50), True, 2, self.controlsUnderBuilding[0], self.controlsUnderBuilding[1])
        if (cord):
            print(0)
            return cord

        cord = self.getXYByColor((76, 191, 59))
        if (cord):
            print(1)
            return cord

        # cord = self.getXYByColor((71,186,55))
        # if(cord):
        #     print(2)
        #     return cord

        cord = self.getXYByColor((60, 175, 51))
        if (cord):
            print(3)
            return cord
        #
        # cord = self.getXYByColor((142,243,84))
        # if(cord):
        #     return cord

        return False

    def updateBuilding(self):
        self.log('update building Start 1')
        self.click(63, 240)

        def upt():
            self.clickCenter()
            self.clickCenter()
            time.sleep(3)
            cord = self.searchUpdateIcon()
            if cord:
                self.log('update building open')
                self.click(cord[0], cord[1])  # Open
                self.clickCenter()
                btnGo = self.getXYByColor((33, 33, 19))
                if (btnGo):
                    self.log('Press Update')
                    self.log('Is the button available?')
                    if self.getXYByColor((85,85,85), True, 2, (817, 769), (1099, 834)):
                        self.log('No. Close')
                        self.click(1333, 73)
                    else:
                        self.click(btnGo[0], btnGo[1])  # Go
                        # if self.getXYByColor((85, 85, 85), True, 2, (817, 769), (1099, 834)):
                        #     self.log('can`t update')
                        #     self.click(1333, 73)
                        # else:
                        self.click(1333, 73)
                        self.shakeHand()
                else:
                    self.clickClose()

        upt()
        self.log('update building Finish 1')
        self.log('update building Start 2')
        self.click(63, 350)
        upt()
        self.log('update building Finish 2')

    def clickLeftMenu(self):
        self.click(22, 478)  # click left menu

    def closeLeftMenu(self):
        self.click(668, 446)

    def clickClose(self):
        self.click(1553, 32)  # Click Clsoe

    def clickCenter(self):
        self.click(806, 432)

    def openWildernessOrSettlement(self):
        # self.log('Open Wilderness or Settlement')
        self.click(77, 827)

    def keyW(self, ms):
        self.shell(f'input swipe 250 700 250 600 {ms}')
        # os.system(f'hd-adb shell input swipe 250 700 250 600 {ms}')

    def swipeTechLeft(self, ms=500):

        self.shell(f'input swipe 767 449 255 449 {ms}')
        # os.system(f'hd-adb shell input swipe 767 449 255 449 {ms}')

    def keyBack(self):
        self.shell('input keyevent 4')
        # os.system(f'hd-adb shell ')

    def start(self):
        self.device = inputDevice.get()
        self.work = 1
        self.t1 = threading.Thread(target=self.main, args=[])
        self.t1.start()

    def farm(self):
        self.device = inputDevice.get()
        self.work = 1
        self.t1 = threading.Thread(target=self.farmBot, args=[])
        self.t1.start()

    def stop(self):
        self.work = 0
        self.log('STOP PROCESSING')

    def closeWindow(self):
        self.work = 0
        tkWindow.destroy()

    def shell(self, cmd):
        os.system(f'hd-adb -s {self.device} shell {cmd}')

    def log(self, value):
        timeVal = datetime.now().strftime("%H:%M:%S")
        text.insert(END, "%s: %s \r\n" % (timeVal, value))
        text.see("end")

    def selectedDevice(self, event):
        self.device = inputDevice.get()

bot = Bot()
buttonStart = Button(tkWindow, text='Start', command=bot.start)
buttonStart.pack()
buttonStart2 = Button(tkWindow, text='Farm', command=bot.farm)
buttonStart2.pack()
buttonStop = Button(tkWindow, text='Stop', command=bot.stop)
buttonStop.pack()

tkWindow.protocol("WM_DELETE_WINDOW", bot.closeWindow)
devList = check_output(["hd-adb", "devices"])
text = Text(tkWindow, height=10, width=50)
text.insert(END, devList)




devListArr = str(devList).replace('\\r\\n', ';').replace('\\t', ';').split(';')
rezArr = []
for x in devListArr:
    if (x.startswith('emulator-')):
        rezArr.append(x)
print(rezArr)

inputDevice = ttk.Combobox(tkWindow, width=15)
inputDevice['values'] = rezArr
inputDevice.bind("<<ComboboxSelected>>", bot.selectedDevice)

if len(rezArr) > 0:
    inputDevice.current(0)

inputDevice.pack()
text.pack()

tkWindow.mainloop()
