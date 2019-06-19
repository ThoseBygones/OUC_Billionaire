# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 20:22:52 2019

@author: Sherlock Holmes
"""

"""
class Player():
    def __init__(self, name):
        self.name = name
    
    def say(self):
        print(self.name)
        """

class PlayerQueue():
    """玩家队列类，用于管理玩家的轮流游戏"""
    def __init__(self):
        self.queue = []
        # 队列的长度
        self.__size = 0
    
    # 判断队列是否为空
    def empty(self):
        if self.__size == 0:
            return True
        else:
            return False
    
    # 清空队列
    def clear(self):
        self.__size = 0
        self.queue.clear()
    
    # 获得队列的长度    
    def get_size(self):
        return len(self.queue)
    
    # 获得队列头部的元素（不删除）
    def get_first(self):
        return self.queue[0]
    
    # 向队列尾部添加一个元素
    def push(self, player):
        self.__size += 1
        self.queue.append(player)
        
    # 从队列首部弹出一个元素，并且返回这个元素
    def pop(self):
        self.__size -= 1
        return self.queue.pop(0)
    
    # 实现游戏中玩家回合的更替
    def next_round(self):
        cur_player = self.pop()
        self.push(cur_player)
        return cur_player
    
    # 逆序绘制队列中的玩家（图片位置）
    def reverse_draw(self):
        for index in range(self.__size - 1, -1, -1):
            self.queue[index].draw_player()
