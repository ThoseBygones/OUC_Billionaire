# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 23:47:48 2019

@author: Sherlock Holmes
"""

import pygame
from settings import Settings
from button import Button
import game_functions as gf
from dice import Dice
from messageboard import Messageboard
from game_state import GameState
from player_queue import PlayerQueue

def run_game():
    """游戏运行的主函数"""
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    
    # 导入设置文件中对窗口的设置
    ai_settings = Settings()
    screen = pygame.display.set_mode(
            (ai_settings.screen_width, ai_settings.screen_height))
    
    # 创建“开始游戏”按钮
    play_button = Button(screen, ai_settings.play_button)
    
    # 设置窗口顶部导航栏标题
    pygame.display.set_caption("OUC Billionaire")
    
    # 地点编组
    locations = []
    # 地点坐标信息编组
    location_points = []
    # 创建所有地点格子
    gf.create_all_locations(ai_settings, screen, locations, location_points)
    
    # 创建游戏玩家游戏回合顺序队列
    player_que = PlayerQueue()
    gf.create_player_queue(ai_settings, screen, locations, player_que)
    
    # 创建信息板
    messageboard = Messageboard(ai_settings, screen, locations)
    
    # 创建骰子
    dice = Dice(screen, messageboard)
    
    # 绘制骰子初始状态
    dice.draw_dice(dice.cur_dice)
    
    # 读取事件并创建事件字典
    events_dict = gf.read_events_list(ai_settings)
    # 读取事件图片并创建列表
    event_images = gf.read_event_images(ai_settings)
    
    # 游戏当前的状态
    gs = GameState(ai_settings)
    
    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, gs, play_button, locations, events_dict, 
                        event_images, messageboard, dice, player_que)
        gf.update_screen(ai_settings, screen, gs, play_button, locations, 
                         location_points, events_dict, event_images, 
                         messageboard, dice, player_que)

run_game()
