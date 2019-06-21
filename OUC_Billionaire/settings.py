# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 23:35:15 2019

@author: Sherlock Holmes
"""

import pygame

class Settings():
    """初始化游戏设置"""
    def __init__(self):
        # 设置屏幕的大小和颜色
        self.screen_width = 1320
        self.screen_height = 660
        self.bg_color = (230, 230, 230)
        
        # 设置游戏统计信息
        self.ROLL_DICE = 0
        self.CHOOSE = 1
        self.END_ROUND = 2
        
        # 设置背景图片为海大地图
        self.map = pygame.image.load("images/map.png")
        
        # 设置玩家初始拥有的金钱
        self.player_init_money = 10000
        
        # 设置地点圆点半径大小和颜色
        self.circle_radius = 6
        self.circle_color = (0, 0, 0)
        
        # 设置地点之间连线的颜色
        self.line_color = (0, 0, 0)
        
        # 设置信息面板背景颜色
        self.board_color_1 = (187, 255, 255)
        self.board_color_2 = (255, 250, 205)
        self.board_color_3 = (255, 218, 185)
        
        # 设置地图上地点数量
        self.location_cnt = 0
        
        # 设置地点事件数量
        self.event_cnt = 2
        
        # 设置地点数据文件路径
        self.locations_data_path = "data/locations_list.txt"
        
        # 设置地点事件文件路径
        self.events_path = "data/events_list.json"
        
        # 设置地点事件图片路径
        self.event_images_dir = "event_images"
        