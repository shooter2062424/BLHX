# coding: utf-8

import time

import Window
import Task


def BLHX():
    window = Window.DesktopWindow("BlueStacks")
    task = Task.C03S04Task(window)
    print("脚本开始。")
    try:
        task.run()
    except Exception as e:
        print(e)
    print("脚本结束。")


if __name__ == "__main__":
    BLHX()
