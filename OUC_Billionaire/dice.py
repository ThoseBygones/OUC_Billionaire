# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:28:09 2019

@author: Sherlock Holmes
"""

import pygame
import random

class Dice():
    """骰子类"""
    def __init__(self, screen, messageboard):
        self.screen = screen
        self.messageboard = messageboard
        # 存储骰子每个面的图像
        self.dice_side = []
        # 导入骰子的图片
        for i in range(1, 7):
            file_name_str = "dice" + str(i)
            file_path_str = "images/" + file_name_str + ".png"
            dice_image = pygame.image.load(file_path_str)
            self.dice_side.append(dice_image)
        # 设置当前骰子的面图片以及位置参数
        self.cur_dice = self.dice_side[0]
        self.rect = self.cur_dice.get_rect()
        self.rect.center = self.messageboard.box_1.center
    
    def draw_dice(self, dice_image):
        """绘制骰子"""
        self.screen.blit(dice_image, self.rect)
    
    def roll_dice(self):
        """掷骰子"""
        #print("rolling dice...")
        # 随机骰子的值并制造出骰子随机的效果
        for i in range(1, 18):
            index = random.randint(0, 5)
            self.cur_dice = self.dice_side[index]
            self.draw_dice(self.cur_dice)
            pygame.display.update()
            pygame.time.wait(100)
        # 骰子最后停下时的值
        result = random.randint(0, 5)
        self.cur_dice = self.dice_side[result]
        return result + 1
        