# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 23:29:50 2019

@author: Sherlock Holmes
"""

import pygame

class Messageboard():
    """显示游戏相关信息的类"""
    def __init__(self, ai_settings, screen, locations):
        self.screen = screen
        self.ai_settings = ai_settings
        self.locations = locations
        
        # 设置面板字体颜色和大小
        self.text_color_1 = (0, 0, 139)
        self.text_color_2 = (0, 0, 0)
        self.font = pygame.font.SysFont('SimHei', 18)
        
        # 设置各个面板块的颜色
        self.box_color_1 = self.ai_settings.board_color_1
        self.box_color_2 = self.ai_settings.board_color_2
        self.box_color_3 = self.ai_settings.board_color_3
        
        # 设置面板块位置并创建
        self.box_1 = pygame.Rect(977, 0, (1320 - 977), 140)
        self.box_2 = pygame.Rect(977, 140, (1320 - 977), 260)
        self.box_3 = pygame.Rect(977, 400, (1320 - 977), 260)
        
        # 设置结束回合图片路径
        image_path_str = "images/end_round_button.png"
        self.end_round_button = pygame.image.load(image_path_str)
        
    def update_players_message(self, pq):
        """将玩家信息转换为渲染的图像"""
        self.player_msg = []
        self.player_msg_rect = []
        # 顺序遍历玩家队列里的所有玩家
        player_cnt = pq.size
        for i in range(0, player_cnt):
            player = pq.queue[i]
            player_msg_str_1 = player.player_name + "："
            player_msg_str_2 = ("拥有金钱：$" + str(player.money) + "  当前位置：" 
                                + str(self.locations[player.pos].name))
            self.player_msg_1 = self.font.render(player_msg_str_1, True, 
                                                 self.text_color_1)
            self.player_msg_2 = self.font.render(player_msg_str_2, True, 
                                                 self.text_color_1)
            self.player_msg.append([self.player_msg_1, self.player_msg_2])
        
        # 将所有玩家信息放在第二个信息块上
        rect_1 = self.player_msg[0][0].get_rect()
        rect_2 = self.player_msg[0][1].get_rect()
        self.player_msg_rect.append([rect_1, rect_2])
        self.player_msg_rect[0][0].top = self.box_2.top + 10
        self.player_msg_rect[0][0].left = self.box_2.left + 10
        self.player_msg_rect[0][1].top = self.player_msg_rect[0][0].bottom + 5
        self.player_msg_rect[0][1].left = self.box_2.left + 10
        
        for i in range(1, player_cnt):
            rect_1 = self.player_msg[i][0].get_rect()
            rect_2 = self.player_msg[i][1].get_rect()
            self.player_msg_rect.append([rect_1, rect_2])
            self.player_msg_rect[i][0].top = (
                    self.player_msg_rect[i - 1][1].bottom + 5)
            self.player_msg_rect[i][0].left = self.box_2.left + 10
            self.player_msg_rect[i][1].top = (self.player_msg_rect[i][0].bottom
                                + 5)
            self.player_msg_rect[i][1].left = self.box_2.left + 10
    
    def update_event_message(self, gs, player):
        """更新事件信息"""
        event_msg_str = []
        self.event_msg = []
        self.event_msg_rect = []
        
        if gs.game_state == self.ai_settings.ROLL_DICE:
            # 创建初始化信息相关文字
            event_msg_str.append((player.player_name + "的游戏回合!"))
            event_msg_str.append(("请" + player.player_name + "掷骰子~"))
            for msg_str in event_msg_str:
                msg_img = self.font.render(msg_str, True, self.text_color_2)    
                self.event_msg.append(msg_img)
        elif gs.game_state == self.ai_settings.CHOOSE:
            # 创建触发事件的信息
            self.event_msg.append(gs.cur_event_imgs['content'])
            self.event_msg.append(gs.cur_event_imgs['A']['choice'])
            self.event_msg.append(gs.cur_event_imgs['B']['choice'])
            self.event_msg.append(gs.cur_event_imgs['C']['choice'])
        elif gs.game_state == self.ai_settings.END_ROUND:
            # 创建选择结果的信息
            self.event_msg.append(gs.cur_event_imgs['result'])
            # 创建结束回合按钮信息
            self.button_rect = self.end_round_button.get_rect()
            self.button_rect.bottom = self.box_3.bottom - 10
            self.button_rect.right = self.box_3.right - 10

        #print(len(self.event_msg))
        # 将事件信息放到第三个信息块上
        msg_rect = self.event_msg[0].get_rect()
        self.event_msg_rect.append(msg_rect)
        self.event_msg_rect[0].top = self.box_3.top + 10
        self.event_msg_rect[0].left = self.box_3.left + 10
        
        for i in range(1, len(self.event_msg)):
            msg_rect = self.event_msg[i].get_rect()
            self.event_msg_rect.append(msg_rect) 
            self.event_msg_rect[i].top = self.event_msg_rect[i - 1].bottom + 5
            self.event_msg_rect[i].left = self.box_3.left + 10
    
    def draw_messageboard(self, gs, event_imgs, pq):
        """在屏幕上绘制信息板"""
        pygame.draw.rect(self.screen, self.box_color_1, self.box_1)
        pygame.draw.rect(self.screen, self.box_color_2, self.box_2)
        pygame.draw.rect(self.screen, self.box_color_3, self.box_3)
        
        # 显示玩家信息并在屏幕上绘制
        self.update_players_message(pq)
        for i in range(0, pq.size):
            self.screen.blit(self.player_msg[i][0], self.player_msg_rect[i][0])
            self.screen.blit(self.player_msg[i][1], self.player_msg_rect[i][1])
        
        # 显示当前回合对应玩家随机到的事件信息并在屏幕上绘制
        self.update_event_message(gs, pq.cur_player)
        #print(len(self.event_msg_rect))
        for i in range(0, len(self.event_msg_rect)):
            self.screen.blit(self.event_msg[i], self.event_msg_rect[i])
            
        if gs.game_state == self.ai_settings.END_ROUND:
            self.screen.blit(self.end_round_button, self.button_rect)
        