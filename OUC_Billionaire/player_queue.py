# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 20:22:52 2019

@author: Sherlock Holmes
"""

class PlayerQueue():
    """玩家队列类，用于管理玩家的轮流游戏"""
    def __init__(self):
        # 列表模拟玩家队列
        self.queue = []
        # 队列的长度
        self.size = 0
        # 当前轮到哪个玩家游戏
        self.cur_player = None
        # 当前游戏回合玩家的下标
        self.cur_player_index = -1
    
    def empty(self):
        """判断队列是否为空"""
        if self.size == 0:
            return True
        else:
            return False
    
    def add_player(self, player):
        """向队列中添加玩家"""
        self.queue.append(player)
        self.size += 1
        # 同时更新当前游戏玩家和当前游戏玩家下标
        self.cur_player_index = 0
        self.cur_player = self.queue[self.cur_player_index]
    
    def next_round(self):
        """实现游戏中玩家回合的更替"""
        # 获得下一轮游戏的玩家的下标
        self.cur_player_index = (self.cur_player_index + 1) % self.size
        self.cur_player = self.queue[self.cur_player_index]
    
    def reverse_draw(self):
        """逆序绘制队列中的玩家（图片位置）"""
        for index in range(self.size - 1, -1, -1):
            self.queue[index].draw_player()
