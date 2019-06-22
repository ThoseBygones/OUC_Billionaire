# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 16:39:04 2019

@author: Sherlock Holmes
"""

class Button():
    """按钮类"""
    def __init__(self, screen, img):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.img = img
        self.img_rect = self.img.get_rect()
        self.img_rect.centerx = self.screen_rect.centerx
        self.img_rect.centery = self.screen_rect.centery + 150
        
    def draw_button(self):
        """绘制一个按钮"""
        self.screen.blit(self.img, self.img_rect)