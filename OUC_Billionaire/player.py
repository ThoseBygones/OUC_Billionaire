# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 23:17:52 2019

@author: Sherlock Holmes
"""

import pygame

class Player():
    """玩家信息类"""
    def __init__(self, ai_settings, screen, locations, player_id, name):
        self.ai_settings = ai_settings
        self.screen = screen
        self.locations = locations
        
        # 玩家名称
        self.player_name = name
        # 玩家拥有的金钱数量
        self.money = self.ai_settings.player_init_money
        # 玩家在地图上的初始位置
        self.pos = 0
        
        # 加载图像并获得其外接矩形
        file_path_str = "images/player" + str(player_id) + ".png"
        self.image = pygame.image.load(file_path_str)
        self.rect = self.image.get_rect()
        self.rect.center = (self.locations[0].x, self.locations[0].y)
        
    def move(self, step):
        """控制玩家每回合的移动"""
        self.pos = (self.pos + step) % self.ai_settings.location_cnt
    
    def invest(self, val):
        """控制玩家的投资的收支"""
        self.money += val
        
    def draw_player(self):
        """绘制玩家的位置"""
        self.rect = self.image.get_rect()
        self.rect.center = (self.locations[self.pos].x, self.locations[self.pos].y)
        #print(self.rect.center)
        self.screen.blit(self.image, self.rect)
        