# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 22:05:22 2019

@author: Sherlock Holmes
"""

import sys
import pygame
from location import Location
from location import Hospital
from location import ChemistryInstitute
from location import SouthDistrict
import json
from player import Player
import os

def update_screen(ai_settings, screen, gs, play_button, locations, 
                  location_points, event, event_imgs, messageboard, dice, pq):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    
    # 游戏被激活，则显示游戏界面
    if gs.game_active == True:
        #`绘制地图
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
    # 否则显示开始游戏界面
    else:
        screen.blit(ai_settings.bg_image, (0, 0))
        play_button.draw_button()
        
    # 显示最新绘制的屏幕
    pygame.display.flip()

def check_events(ai_settings, gs, play_button, locations, events_dict, 
                 events_imgs, messageboard, dice, pq):
    """监视并相应鼠标和键盘事件"""
    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_click_events(ai_settings, gs, play_button, locations, 
                               events_dict, events_imgs, messageboard, dice, 
                               pq)

def check_click_events(ai_settings, gs, play_button, locations, events_dict, 
                       events_imgs, messageboard, dice, pq):
    """处理鼠标点击事件的函数"""
    # 定位鼠标点击位置
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #print(mouse_x, mouse_y)
    # 检测游戏是否处于激活状态
    if gs.game_active == True:
        # 如果此时应该掷骰子
        if gs.game_state == ai_settings.ROLL_DICE:
            # 检测点击位置是否在骰子图片区域内
            if dice.rect.collidepoint(mouse_x, mouse_y):
                # 获得骰子的点数
                step = dice.roll_dice()
                # 玩家移动相应的点数
                pq.cur_player.move(step)
                # 随机得到事件的编号（列表下标）
                gs.cur_event_index = locations[pq.cur_player.pos].trigger_event(
                        pq.cur_player)
                gs.cur_event_imgs = events_imgs[gs.cur_event_index]
                # 如果随机得到的事件是多项选择事件，则进入选择阶段
                if events_dict[gs.cur_event_index]['type'] == "multiple_choice":
                    gs.game_state = ai_settings.CHOOSE
                # 否则跳过选择阶段，直接进入结束回合阶段
                else:
                    pq.cur_player.invest(events_dict[gs.cur_event_index]['change'])
                    gs.game_state = ai_settings.END_ROUND
        # 如果此时应该进行选择，则判断点击位置在哪个选项的区域内
        elif gs.game_state == ai_settings.CHOOSE:
            # 选项 A
            if messageboard.event_msg_rect[1].collidepoint(mouse_x, mouse_y):
                gs.cur_event_imgs = gs.cur_event_imgs['A']
                pq.cur_player.invest(events_dict[gs.cur_event_index]['A']['change'])
            # 选项 B
            elif messageboard.event_msg_rect[2].collidepoint(mouse_x, mouse_y):
                gs.cur_event_imgs = gs.cur_event_imgs['B']
                pq.cur_player.invest(events_dict[gs.cur_event_index]['B']['change'])
            # 选项 C
            elif messageboard.event_msg_rect[3].collidepoint(mouse_x, mouse_y):
                gs.cur_event_imgs = gs.cur_event_imgs['C']
                pq.cur_player.invest(events_dict[gs.cur_event_index]['C']['change'])
            # 不在点击范围内
            else:
                return
            gs.game_state = ai_settings.END_ROUND
        # 如果此时应该结束回合，则判断点击位置是否在结束回合按钮区域内
        elif gs.game_state == ai_settings.END_ROUND:
            if messageboard.button_rect.collidepoint(mouse_x, mouse_y):
                gs.cur_event = None
                pq.next_round()
                gs.game_state = ai_settings.ROLL_DICE
    # 游戏未激活
    else:
        # 检测是否点击开始游戏按钮
        if play_button.img_rect.collidepoint(mouse_x, mouse_y):
            gs.game_active = True

def create_location(ai_settings, screen, locations, index, x, y, name):
    """创建一个地点"""
    if name == "校医院":
        location = Hospital(ai_settings, screen, index, x, y, name)
    elif name == "化院":
        location = ChemistryInstitute(ai_settings, screen, index, x, y, name)
    elif name == "南区":
        location = SouthDistrict(ai_settings, screen, index, x, y, name)
    else:
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
        # 更新事件总数
        ai_settings.event_cnt = len(events_dict['events'])
        return events_dict['events']

def read_event_images(ai_settings):
    """从event_images目录下读取所有的事件图片并存入一个列表"""
    event_images = []
    dir_path = ai_settings.event_images_dir
    dir_cnt = 0
    # 计算文件夹数量
    for name in os.listdir(dir_path):
        sub_path = os.path.join(dir_path, name)
        if os.path.isdir(sub_path):
            dir_cnt += 1
    #print("dir_cnt: " + str(dir_cnt))
    # 遍历所有文件夹
    for i in range(0, dir_cnt):
        event_dir_path = dir_path + "/event_" + str(i).zfill(3)
        file_cnt = 0
        # 计算文件数量
        for name in os.listdir(event_dir_path):
            sub_path = os.path.join(event_dir_path, name)
            if os.path.isfile(sub_path):
                file_cnt += 1
        # 如果目录下只有一个文件，则视为固定结果事件文件夹处理
        if file_cnt == 1:
            img_result = pygame.image.load((event_dir_path + "/result.png"))
            event_dict = dict({
                'result': img_result
                })
            event_images.append(event_dict)
        # 如果目录下有三个文件，则视为随机结果事件文件夹处理
        elif file_cnt == 3:
            img_result_a = pygame.image.load((event_dir_path + "/result_A.png"))
            img_result_b = pygame.image.load((event_dir_path + "/result_B.png"))
            img_result_c = pygame.image.load((event_dir_path + "/result_C.png"))
            event_dict = dict({
                'A': {'result': img_result_a},
                'B': {'result': img_result_b},
                'C': {'result': img_result_c}
                })
            event_images.append(event_dict)
        # 如果目录下有七个文件，则视为多项选择事件文件夹处理
        elif file_cnt == 7:
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

def create_player_queue(ai_settings, screen, locations, pq):
    # 创建所有玩家
    player1 = Player(ai_settings, screen, locations, 1, "曾致元")
    player2 = Player(ai_settings, screen, locations, 2, "孙镜涛")
    player3 = Player(ai_settings, screen, locations, 3, "鞠丰禧")
    player4 = Player(ai_settings, screen, locations, 4, "罗立娜")
    player5 = Player(ai_settings, screen, locations, 5, "李亚菲")
    # 将所有玩家加入游戏队列
    pq.add_player(player1)
    pq.add_player(player2)
    pq.add_player(player3)
    pq.add_player(player4)
    pq.add_player(player5)