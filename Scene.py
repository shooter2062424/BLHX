# coding: utf-8

import time
import random

import GraphCap as gc
import Template
import Action


class Scene:
    def __init__(self, game):
        self.game = game

    def sleep(self, min=1.0, max=2.0):
        time.sleep(random.uniform(min, max))


class MainScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.weighAnchorAct = Action.ClickAction(game, Template.Template(game, "出击", "./Main/WeighAnchor.png"))

    def enterPrecombat(self):
        self.sleep()
        self.weighAnchorAct.execute()
        self.sleep()


class PrecombatScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.backAct = Action.ClickAction(game, Template.Template(game, "返回", "./Precombat/Back.png"))
        self.exerciseAct = Action.ClickAction(game, Template.Template(game, "演习", "./Precombat/Exercise.png"))
        self.goNowAct = Action.ClickAction(game, Template.Template(game, "立刻前往", "./Precombat/GoNow.png"))
        self.goNowAct2 = Action.ClickAction(game, Template.Template(game, "立刻前往2", "./Precombat/GoNow2.png"))

        self.prevPageTarget = Template.SpecifiedTarget(game, gc.Point(40, 300), gc.Size(25, 35))
        self.nextPageTarget = Template.SpecifiedTarget(game, gc.Point(910, 300), gc.Size(25, 35))

        self.chapterTemplList = []
        self.chapterTemplList.append(Template.Template(game, "第1章", "./Precombat/C01.png"))
        self.chapterTemplList.append(Template.Template(game, "第2章", "./Precombat/C02.png"))
        self.chapterTemplList.append(Template.Template(game, "第3章", "./Precombat/C03.png"))
        self.chapterTemplList.append(Template.Template(game, "第4章", "./Precombat/C04.png"))
        self.chapterTemplList.append(Template.Template(game, "第5章", "./Precombat/C05.png"))
        self.chapterTemplList.append(Template.Template(game, "第6章", "./Precombat/C06.png"))
        self.chapterTemplList.append(Template.Template(game, "第7章", "./Precombat/C07.png"))
        self.chapterTemplList.append(Template.Template(game, "第8章", "./Precombat/C08.png"))
        self.chapterTemplList.append(Template.Template(game, "第9章", "./Precombat/C09.png"))
        self.chapterTemplList.append(Template.Template(game, "第10章", "./Precombat/C10.png"))
        self.chapterTemplList.append(Template.Template(game, "第11章", "./Precombat/C11.png"))
        self.chapterTemplList.append(Template.Template(game, "第12章", "./Precombat/C12.png"))

        self.subcapterDict = {}
        self.subcapterDict[100 * 1 + 1] = Template.SpecifiedTarget(game, gc.Point(160, 376), gc.Size(114, 24))
        self.subcapterDict[100 * 3 + 4] = Template.SpecifiedTarget(game, gc.Point(507, 306), gc.Size(137, 25))

    def back(self):
        self.sleep()
        self.backAct.execute()
        self.sleep()

    def enterExercise(self):
        self.sleep()
        self.exerciseAct.execute()
        self.sleep()

    def getChapter(self):
        while True:
            image = self.game.capture()
            subImage = image.clip(gc.Rect(30, 115, 28, 20))
            for i in range(len(self.chapterTemplList)):
                chapterTempl = self.chapterTemplList[i]
                target = chapterTempl.matchOn(subImage)
                if target.similarity > 0.99:
                    print("当前是第{0}章".format(i + 1))
                    return i + 1

    def enterSubcapter(self, capter, subcapter):
        current = self.getChapter()
        if capter < current:
            for i in range(current - capter):
                self.sleep()
                self.prevPageTarget.click()
                self.sleep()
        elif capter > current:
            for i in range(capter - current):
                self.sleep()
                self.nextPageTarget.click()
                self.sleep()
        key = 100 * capter + subcapter
        if key not in self.subcapterDict:
            print("{0}-{1}不存在。".format(capter, subcapter))
            return False
        target = self.subcapterDict[key]
        self.sleep()
        target.click()
        self.sleep()
        self.goNowAct.execute()
        self.sleep()
        self.goNowAct2.execute()
        self.sleep()
        return True


class ExerciseScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.backAct = Action.ClickAction(game, Template.Template(game, "返回", "./Exercise/Back.png"))
        self.operationAct = Action.ClickAction(game, Template.Template(game, "演习", "./Exercise/Operation.png"),
                                               specifiedTarget=Template.SpecifiedTarget(game, gc.Point(50, 128),
                                                                                        gc.Size(160, 228)))
        self.startExerciseAct = Action.ClickAction(game,
                                                   Template.Template(game, "开始演习", "./Exercise/StartExercise.png"))
        self.weighAnchorAct = Action.ClickAction(game, Template.Template(game, "出击", "./Exercise/WeighAnchor.png"))
        self.ttcAct = Action.ClickAction(game, Template.Template(game, "点击继续", "./Exercise/TTC.png"), 0.85,
                                         specifiedTarget=Template.SpecifiedTarget(game, gc.Point(50, 420),
                                                                                  gc.Size(850, 130)))
        self.ttcAct2 = Action.ClickAction(game, Template.Template(game, "点击继续2", "./Exercise/TTC2.png"),
                                          specifiedTarget=Template.SpecifiedTarget(game, gc.Point(50, 420),
                                                                                   gc.Size(850, 130)))
        self.confirmAct = Action.ClickAction(game, Template.Template(game, "确认", "./Exercise/Confirm.png"))

    def back(self):
        self.sleep()
        self.backAct.execute()
        self.sleep()

    def enterExercise(self):
        self.sleep()
        self.operationAct.execute()
        self.sleep()
        self.startExerciseAct.execute()
        self.sleep()
        self.weighAnchorAct.execute()
        self.sleep()

    def leaveExercise(self):
        self.sleep()
        self.ttcAct.execute()
        self.sleep()
        self.ttcAct2.execute()
        self.sleep()
        self.confirmAct.execute()
        self.sleep()


class SubchapterScene(Scene):
    def __init__(self, game):
        super().__init__(game)


class C01S01Scene(SubchapterScene):
    def __init__(self, game):
        super().__init__(game)
        self.enterAmbushTarget = Template.SpecifiedTarget(game, gc.Point(330, 252), gc.Size(87, 64))
        self.leaveAmbushTarget = Template.SpecifiedTarget(game, gc.Point(238, 252), gc.Size(83, 64))
        self.meetAct = Action.ClickAction(game, Template.Template(game, "迎击", "./Subchapter/Meet.png"))
        self.weighAnchorAct = Action.ClickAction(game, Template.Template(game, "出击", "./Subchapter/WeighAnchor.png"))

    def enterAmbush(self):
        self.sleep(3.0, 5.0)
        self.enterAmbushTarget.click()
        self.sleep()
        self.meetAct.execute()
        self.sleep()
        self.weighAnchorAct.execute()
        self.sleep()

    def leaveAmbush(self):
        self.sleep()
        self.leaveAmbushTarget.click()
        self.sleep()


class C03S04Scene(SubchapterScene):
    def __init__(self, game):
        super().__init__(game)
        self.recFleetTempl = Template.Template(game, "侦查舰队", "./Subchapter/RecFleet.png",
                                               "./Subchapter/RecFleetMask.png")
        self.mainFleetTempl = Template.Template(game, "主力舰队", "./Subchapter/MainFleet.png",
                                                "./Subchapter/MainFleetMask.png")
        self.airFleetTempl = Template.Template(game, "航空舰队", "./Subchapter/AirFleet.png",
                                               "./Subchapter/AirFleetMask.png")
        self.weighAnchorTempl = Template.Template(game, "出击", "./Subchapter/WeighAnchor.png")
        self.mapX = 74
        self.mapY = 250 - (448 - 304)
        self.tileSize = 110
        self.columns = 8
        self.rows = 4
        self.pt = gc.PerspectiveTransform(gc.Size2f(890, 448), 304, 70, 81)
        self.map = [[0 for i in range(self.columns)] for i in range(self.rows)]

    def enterBattle(self):
        while True:
            image = self.game.capture()

            map = [[0 for i in range(self.columns)] for i in range(self.rows)]
            recFleetTarget = self.recFleetTempl.matchOn(image)
            for i in range(5):
                if recFleetTarget.similarity > 0.95:
                    size = recFleetTarget.getSize()
                    x = recFleetTarget.location.x - self.mapX + size.width / 2
                    y = recFleetTarget.location.y - self.mapY + size.height / 2
                    transPos = self.pt.transform(gc.Point2f(x, y))
                    col = int(transPos.x / self.tileSize)
                    row = int(transPos.y / self.tileSize)
                    if 0 <= col < self.columns and 0 <= row < self.rows:
                        map[row][col] = 1
                recFleetTarget = recFleetTarget.next()
            mainFleetTarget = self.mainFleetTempl.matchOn(image)
            for i in range(5):
                if mainFleetTarget.similarity > 0.95:
                    size = recFleetTarget.getSize()
                    x = mainFleetTarget.location.x - self.mapX + size.width / 2
                    y = mainFleetTarget.location.y - self.mapY + size.height / 2
                    transPos = self.pt.transform(gc.Point2f(x, y))
                    col = int(transPos.x / self.tileSize)
                    row = int(transPos.y / self.tileSize)
                    if 0 <= col < self.columns and 0 <= row < self.rows:
                        map[row][col] = 2
                mainFleetTarget = mainFleetTarget.next()
            airFleetTarget = self.airFleetTempl.matchOn(image)
            for i in range(5):
                if airFleetTarget.similarity > 0.95:
                    size = recFleetTarget.getSize()
                    x = airFleetTarget.location.x - self.mapX + size.width / 2
                    y = airFleetTarget.location.y - self.mapY + size.height / 2
                    transPos = self.pt.transform(gc.Point2f(x, y))
                    col = int(transPos.x / self.tileSize)
                    row = int(transPos.y / self.tileSize)
                    if 0 <= col < self.columns and 0 <= row < self.rows:
                        map[row][col] = 3
                airFleetTarget = airFleetTarget.next()
            print("--------------------------------------------")
            for row in range(4):
                line = str()
                for col in range(8):
                    id = map[row][col]
                    line += " %d " % id
                print(line)
            print("--------------------------------------------")


class BattleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.ttcAct = Action.ClickAction(game, Template.Template(game, "点击继续", "./Battle/TTC.png"), 0.85,
                                         specifiedTarget=Template.SpecifiedTarget(game, gc.Point(50, 420),
                                                                                  gc.Size(850, 130)))
        self.ttcAct2 = Action.ClickAction(game, Template.Template(game, "点击继续2", "./Battle/TTC2.png"),
                                          specifiedTarget=Template.SpecifiedTarget(game, gc.Point(50, 420),
                                                                                   gc.Size(850, 130)))
        self.performanceAct = Action.ClickAction(game, Template.Template(game, "性能", "./Battle/Performance.png"))
        self.confirmAct = Action.ClickAction(game, Template.Template(game, "确认", "./Battle/Confirm.png"))

    def leaveBattle(self):
        self.sleep()
        self.ttcAct.execute()
        self.sleep()
        self.ttcAct2.execute()
        self.sleep()
        self.confirmAct.execute()
        self.sleep()
