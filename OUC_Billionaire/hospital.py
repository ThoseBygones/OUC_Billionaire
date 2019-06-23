# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 22:13:14 2019

@author: Sherlock Holmes
"""

from location import Location

class Hospital(Location):
    """医院类（继承地点类）"""
    def __init__(self, ai_settings, screen, index, pos_x, pos_y, msg):
        # 继承父类的构造方法
        super().__init__(ai_settings, screen, index, pos_x, pos_y, msg)
    
    def trigger_event(self):
        """触发事件"""
        # 随机事件的编号
        index = 0
        return index