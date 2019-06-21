# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 22:05:22 2019

@author: Sherlock Holmes
"""

import sys
import pygame
from location import Location
import json
import random
from player import Player
import os

def update_screen(ai_settings, screen, gs, locations, location_points, 
                  event, event_imgs, messageboard, dice, pq):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    
    #`绘制背景图片
    screen.blit(ai_settings.map, (0, 0))
    
    # 绘制所有地点
    for location in locations:
        location.draw_location()
        
    # 绘制地点之间的连线
    pygame.draw.lines(screen, ai_settings.line_color, True, location_points, 3)
        
    # 绘制所有的玩家
    pq.reverse_draw()
    
    # 绘制信息板
    messageboard.draw_messageboard(gs, event_imgs, pq)
    
    # 绘制骰子
    dice.draw_dice(dice.cur_dice)
    
    # 显示最新绘制的屏幕
    pygame.display.flip()

def check_events(ai_settings, gs, events_dict, events_imgs, messageboard, dice, 
                 pq):
    """监视并相应鼠标和键盘事件"""
    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 定位鼠标点击位置
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #print(mouse_x, mouse_y)
            # 检测点击位置是否在骰子图片区域内
            #print(dice.rect.left, dice.rect.right)
            # 获得当前回合游戏的玩家
            cur_player = pq.get_first()
            if (gs.game_state == ai_settings.ROLL_DICE and 
                dice.rect.collidepoint(mouse_x, mouse_y)):
                step = dice.roll_dice()
                cur_player.move(step)
                gs.game_state = ai_settings.CHOOSE
                gs.cur_event_index = trigger_location_event(ai_settings, 
                                                            events_dict)
                gs.cur_event_imgs = events_imgs[gs.cur_event_index]
                #messageboard.draw_messageboard(gs, player1)
                #pygame.display.update()
            elif gs.game_state == ai_settings.CHOOSE:
                if messageboard.event_msg_rect[1].collidepoint(mouse_x, 
                                              mouse_y):
                    gs.cur_event_imgs = gs.cur_event_imgs['A']
                    cur_player.invest(events_dict[gs.cur_event_index]['A']['change'])
                elif messageboard.event_msg_rect[2].collidepoint(mouse_x, mouse_y):
                    gs.cur_event_imgs = gs.cur_event_imgs['B']
                    cur_player.invest(events_dict[gs.cur_event_index]['B']['change'])
                elif messageboard.event_msg_rect[3].collidepoint(mouse_x, mouse_y):
                    gs.cur_event_imgs = gs.cur_event_imgs['C']
                    cur_player.invest(events_dict[gs.cur_event_index]['C']['change'])
                else:
                    break
                gs.game_state = ai_settings.END_ROUND
                #messageboard.draw_messageboard(gs, player1)
                #pygame.display.update()
            elif gs.game_state == ai_settings.END_ROUND:
                if messageboard.button_rect.collidepoint(mouse_x, mouse_y):
                    gs.cur_event = None
                    pq.next_round()
                    gs.game_state = ai_settings.ROLL_DICE
                    #messageboard.draw_messageboard(gs, player1)
                    #pygame.display.update()

def create_location(ai_settings, screen, locations, index, x, y, name):
    """创建一个地点"""
    location = Location(ai_settings, screen, index, x, y, name)
    locations.append(location)

def create_all_locations(ai_settings, screen, locations, location_points):
    """创建所有的地点圆点"""
    data = read_locations_list(ai_settings)
    ai_settings.location_cnt = len(data)
    for i in range(0, ai_settings.location_cnt):
        create_location(ai_settings, screen, locations, i, int(data[i][0]), 
                        int(data[i][1]), data[i][2])
        location_points.append([int(data[i][0]), int(data[i][1])])
        #print(int(data[i][0]), int(data[i][1]), data[i][2])
        
def read_locations_list(ai_settings):
    """从txt文件中读取地点信息"""
    data = []
    with open(ai_settings.locations_data_path, encoding = ('utf-8')) as file_data:
        for line in file_data:
            line = line.rstrip()
            x, y, name = line.split(' ')
            data.append([x, y, name])
            #print(x, y, name)
    #print(data)
    return data

def read_events_list(ai_settings):
    """从json文件中读取事件信息"""
    with open(ai_settings.events_path, encoding = ('utf-8')) as file:
        events_dict = json.load(file)
        #print(events_dict)
        return events_dict['events']

def read_event_images(ai_settings):
    """从event_images目录下读取所有的事件图片并存入一个列表"""
    event_images = []
    dir_path = ai_settings.event_images_dir
    dir_cnt = 0
    # 获得文件夹数量
    for lists in os.listdir(dir_path):
        sub_path = os.path.join(dir_path, lists)
        if os.path.isdir(sub_path):
            dir_cnt += 1
    #print("dir_cnt: " + str(dir_cnt))
    # 遍历所有文件夹
    for i in range(0, dir_cnt):
        event_dir_path = dir_path + "/event_" + str(i).zfill(3)
        #print(event_dir_path)
        img_content = pygame.image.load((event_dir_path + "/content.png"))
        img_choice_a = pygame.image.load((event_dir_path + "/choice_A.png"))
        img_choice_b = pygame.image.load((event_dir_path + "/choice_B.png"))
        img_choice_c = pygame.image.load((event_dir_path + "/choice_C.png"))
        img_result_a = pygame.image.load((event_dir_path + "/result_A.png"))
        img_result_b = pygame.image.load((event_dir_path + "/result_B.png"))
        img_result_c = pygame.image.load((event_dir_path + "/result_C.png"))
        event_dict = dict({
                'content': img_content, 
                'A': {'choice': img_choice_a, 'result': img_result_a},
                'B': {'choice': img_choice_b, 'result': img_result_b},
                'C': {'choice': img_choice_c, 'result': img_result_c}
                })
        event_images.append(event_dict)
    #print(len(event_images))
    return event_images

def trigger_location_event(ai_settings, events_dict):
    """在每个地点触发事件"""
    index = random.randint(0, ai_settings.event_cnt - 1)
    return index

def create_player_queue(ai_settings, screen, locations, pq):
    # 创建所有玩家
    player1 = Player(ai_settings, screen, locations, 1, "ZZY")
    player2 = Player(ai_settings, screen, locations, 2, "SJT")
    player3 = Player(ai_settings, screen, locations, 3, "JFX")
    player4 = Player(ai_settings, screen, locations, 4, "LLN")
    player5 = Player(ai_settings, screen, locations, 5, "LYF")
    # 将所有玩家加入游戏队列
    pq.push(player1)
    pq.push(player2)
    pq.push(player3)
    pq.push(player4)
    pq.push(player5)