# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 10:45:31 2019

@author: Sherlock Holmes
"""

"""记录游戏统计信息的类"""
class GameState():
    """初始化统计信息"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        # 游戏刚启动时处于非活动状态
        self.game_active = False
        # 游戏的当前状态
        self.game_state = self.ai_settings.ROLL_DICE
        # 游戏当前事件
        self.cur_event_imgs = None
        self.cur_event_index = 0
        