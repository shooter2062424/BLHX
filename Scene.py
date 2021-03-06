# coding: utf-8

import sys
import time
import random

import Template


def match(game, template, timeout=sys.float_info.max):
    beginTime = time.time()
    while time.time() - beginTime < timeout:
        scene = game.capture()
        target = template.matchOn(scene)
        if target is not None:
            print("匹配[{0}]成功。".format(template.name))
            return target
        else:
            print("匹配[{0}]失败。".format(template.name))
    print("匹配[{0}]超时。".format(template.name))
    return None


def matchList(game, templates):
    scene = game.capture()
    for i in range(len(templates)):
        template = templates[i]
        target = template.matchOn(scene)
        if target is not None:
            print("匹配[{0}]成功。".format(template.name))
            return target, i
        else:
            print("匹配[{0}]失败。".format(template.name))
    return None, -1


def click(game, template, timeout=sys.float_info.max):
    target = match(game, template, timeout)
    if target is not None:
        target.click()
        return True
    else:
        return False


class Scene:
    def __init__(self, game):
        self.game = game

    def sleep(self, min=1.0, max=2.0):
        time.sleep(random.uniform(min, max))


class MainScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.weighAnchor = Template.Template(game, "出击", "./Main/WeighAnchor.png")

        self.maid = Template.Template(game, "演习作战", "./Events/Maid.png")

    def enterPrecombat(self):
        click(self.game, self.weighAnchor)

    def enterMaid(self):
        return click(self.game, self.maid, 5.0)


class PrecombatScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.back1 = Template.Template(game, "返回", "./Precombat/Back.png")
        self.exercise = Template.Template(game, "演习", "./Precombat/Exercise.png")
        self.goNow = Template.Template(game, "立刻前往", "./Precombat/GoNow.png")
        self.goNow2 = Template.Template(game, "立刻前往2", "./Precombat/GoNow2.png")

        self.chapters = []
        self.chapters.append(Template.Template(game, "第1章", "./Precombat/Chapter01.png"))
        self.chapters.append(Template.Template(game, "第2章", "./Precombat/Chapter02.png"))
        self.chapters.append(Template.Template(game, "第3章", "./Precombat/Chapter03.png"))
        self.chapters.append(Template.Template(game, "第4章", "./Precombat/Chapter04.png"))
        self.chapters.append(Template.Template(game, "第5章", "./Precombat/Chapter05.png"))
        self.chapters.append(Template.Template(game, "第6章", "./Precombat/Chapter06.png"))
        self.chapters.append(Template.Template(game, "第7章", "./Precombat/Chapter07.png"))
        self.chapters.append(Template.Template(game, "第8章", "./Precombat/Chapter08.png"))
        self.chapters.append(Template.Template(game, "第9章", "./Precombat/Chapter09.png"))
        self.chapters.append(Template.Template(game, "第10章", "./Precombat/Chapter10.png"))
        self.chapters.append(Template.Template(game, "第11章", "./Precombat/Chapter11.png"))
        self.chapters.append(Template.Template(game, "第12章", "./Precombat/Chapter12.png"))

        self.subcapters = {}
        self.subcapters[100 * 1 + 1] = Template.Target(game, (160, 376), (114, 24))
        self.subcapters[100 * 3 + 4] = Template.Target(game, (507, 306), (137, 25))

        self.prevPageTarget = Template.Target(game, (40, 300), (25, 35))
        self.nextPageTarget = Template.Target(game, (910, 300), (25, 35))

    def back(self):
        click(self.game, self.back1)

    def enterExercise(self):
        click(self.game, self.exercise)

    def enterSubcapter(self, c, sc):
        time.sleep(5.0)
        curTarget, curChapter = matchList(self.game, self.chapters)
        if curTarget is None:
            print("获取海图章数失败。")
            return False
        curChapter += 1
        if c < curChapter:
            for i in range(curChapter - c):
                self.prevPageTarget.click()
                time.sleep(3.0)
        if c > curChapter:
            for i in range(c - curChapter):
                self.nextPageTarget.click()
                time.sleep(3.0)

        key = 100 * c + sc
        if key not in self.subcapters:
            print("{0}-{1}模板图片不存在。".format(c, sc))
            return False
        subcapterTarget = self.subcapters[key]
        subcapterTarget.click()
        click(self.game, self.goNow)
        time.sleep(1.0)
        click(self.game, self.goNow2)
        return True


class ExerciseScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.back1 = Template.Template(game, "返回", "./Exercise/Back.png")
        self.operation = Template.Template(game, "演习", "./Exercise/Operation.png")
        self.firstOne = Template.Target(game, (50, 128), (160, 228))
        self.startExercise = Template.Template(game, "开始演习", "./Exercise/StartExercise.png")
        self.weighAnchor = Template.Template(game, "出击", "./Exercise/WeighAnchor.png")

    def back(self):
        click(self.game, self.back1)

    def enterExercise(self):
        target = match(self.game, self.operation)
        if target is not None:
            self.firstOne.click()
        click(self.game, self.startExercise)
        click(self.game, self.weighAnchor)
        # 演习次数不足
        time.sleep(5.0)
        target = match(self.game, self.weighAnchor, 3.0)
        if target is not None:
            self.back()
            return False
        else:
            return True


class MaidScene(ExerciseScene):
    def __init__(self, game):
        super().__init__(game)
        self.advanced = Template.Template(game, "高级演习", "./Events/Advanced.png")

    def enterExercise(self):
        click(self.game, self.advanced)
        click(self.game, self.weighAnchor)


class C01S01Scene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.enterAmbushTarget = Template.Target(game, (330, 252), (87, 64))
        self.leaveAmbushTarget = Template.Target(game, (238, 252), (83, 64))
        self.meet = Template.Template(game, "迎击", "./Subchapter/Meet.png")
        self.weighAnchor = Template.Template(game, "出击", "./Subchapter/WeighAnchor.png")

    def enterAmbush(self):
        time.sleep(5.0)
        self.enterAmbushTarget.click()
        time.sleep(5.0)
        click(self.game, self.meet)
        click(self.game, self.weighAnchor)

    def leaveAmbush(self):
        time.sleep(5.0)
        self.leaveAmbushTarget.click()
        time.sleep(5.0)


class C03S04Scene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.enemies = []
        self.enemies.append(Template.Template(game, "BOSS舰队", "./Subchapter/BossFleet.png"))
        self.enemies.append(Template.Template(game, "侦查舰队", "./Subchapter/RecFleet.png"))
        self.enemies.append(Template.Template(game, "航空舰队", "./Subchapter/AirFleet.png"))
        self.enemies.append(Template.Template(game, "主力舰队", "./Subchapter/MainFleet.png"))

        self.weighAnchor1 = Template.Template(game, "出击", "./Subchapter/WeighAnchor.png")

        self.bossExist = True

    def weighAnchor(self):
        time.sleep(5.0)
        target, i = matchList(self.game, self.enemies)
        if target is None:
            print("匹配敌人失败。")
            return False
        target.click()
        click(self.game, self.weighAnchor1)
        if i == 0:
            self.bossExist = False
        return True


class BattleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.auto = Template.Template(game, "自律战斗", "./Battle/Auto.png")
        self.gotIt = Template.Template(game, "知道了", "./Battle/GotIt.png")
        self.ttc = Template.Template(game, "点击继续", "./Battle/TTC.png")
        self.ttc2 = Template.Template(game, "点击继续2", "./Battle/TTC2.png")
        self.performance = Template.Template(game, "性能", "./Battle/Performance.png")
        self.ok = Template.Template(game, "确定", "./Battle/OK.png")
        self.victory = Template.Template(game, "大获全胜", "./Battle/Victory.png")
        self.confirm = Template.Template(game, "确认", "./Battle/Confirm.png")
        self.autoFlag = False

    def enterBattle(self):
        if not self.autoFlag:
            if click(self.game, self.auto, 20.0):
                click(self.game, self.gotIt, 3.0)
            self.autoFlag = True

    def leaveBattle(self, drops=True):
        click(self.game, self.ttc)
        click(self.game, self.ttc2)
        if drops:
            if click(self.game, self.performance, 5.0):
                click(self.game, self.ok)
        click(self.game, self.confirm)
