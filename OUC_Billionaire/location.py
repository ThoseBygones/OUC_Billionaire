# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 23:43:40 2019

@author: Sherlock Holmes
"""

import pygame

class Location():
    """地点类"""
    def __init__(self, ai_settings, screen, index, pos_x, pos_y, msg):
        self.ai_settings = ai_settings
        self.screen = screen
        
        # 设置地点参数
        self.index = index
        self.x = pos_x
        self.y = pos_y
        self.radius = ai_settings.circle_radius
        self.name = msg
        
        # 设置地点信息的字体颜色和大小
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('SimHei', 20)
        
        # 设置点的颜色
        self.color = self.ai_settings.circle_color
        
        # 准备说明文字图像
        self.create_location_name()
        
    def create_location_name(self):
        """将说明文字转换为渲染的图像"""
        name_str = self.name
        self.name_image = self.font.render(name_str, True, self.text_color, 
                                           self.ai_settings.bg_color)
        
        # 将说明文字放在地点圆点下方居中
        self.name_rect = self.name_image.get_rect()
        self.name_rect.centerx = self.x
        self.name_rect.top = self.y + self.radius + 10
        
    def draw_location(self):
        """在屏幕上绘制地点圆点并且显示说明文字"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 
                           self.radius, 0)
        self.screen.blit(self.name_image, self.name_rect)
    