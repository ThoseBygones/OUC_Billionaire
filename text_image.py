# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 10:54:20 2019

@author: Sherlock Holmes
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os

class TextImage:
    """文字转换为图像的类"""
    font = ImageFont.truetype("simhei.ttf", 18)
    
    def __init__(self, text):
        # 预设图片宽度
        self.width = 1320 - 980 - 10 * 2
        # 文本
        self.text = text
        # 段落, 行数, 行高
        self.paragraph, self.line_height, self.line_cnt = self.get_lines(text)
        # 设置背景图片的颜色
        self.board_color_1 = (187, 255, 255)
        self.board_color_2 = (255, 250, 205)
        self.board_color_3 = (255, 218, 185)
        self.bg_color = self.board_color_3

    def get_lines(self, text):
        """拆分段落得到每行的文字"""
        txt = Image.new('RGBA', (1000, 1000), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        paragraph = []
        # 一行文字
        line = ""
        # 行数
        line_cnt = 1
        # 宽度总和
        sum_width = 0
        # 行高
        line_height = 0
        for char in text:
            width, height = draw.textsize(char, TextImage.font)
            # 超过预设宽度就修改段落以及当前行数
            if sum_width + width > self.width:
                line_cnt += 1
                sum_width = 0
                paragraph.append(line + "\n")
                line = ""
            sum_width += width
            line += char
            line_height = max(line_height, height)
        if not line.endswith('\n'):
            line += '\n'
            paragraph.append(line + "\n")
        return paragraph, line_height, line_cnt

    def draw_text(self, save_path, bg_color):
        """绘图以及文字"""
        height = self.line_cnt * self.line_height
        bg_img = Image.new('RGBA', (self.width, height + 10), bg_color)
        draw = ImageDraw.Draw(bg_img)
        #bg_img.save("prepic.png")
        #print(self.paragraph)
        # 左上角开始
        x, y = 0, 0
        for paragraph in self.paragraph:
            draw.text((x, y), paragraph, fill=(0, 0, 0), font=TextImage.font)
            y += self.line_height
            #print(y)
        bg_img.save(save_path)

def read_events_list():
    """从json文件中读取事件信息"""
    file_path = "OUC_Billionaire/data/events_list.json"
    with open(file_path, encoding = ('utf-8')) as file:
        events_dict = json.load(file)
        #print(events_dict)
        return events_dict

if __name__ == '__main__':
    bg_color_1 = (255, 218, 185)
    bg_color_2 = (255, 255, 255)
    events_dict = read_events_list()
    events_list = events_dict['events']
    for event in events_list:
        #index = int(event['index'])
        #print(event)
        save_path = ("OUC_Billionaire/event_images/event_" + 
                     str(event['index']).zfill(3))
        # 如果该目录不存在，则创建
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # 如果是确定结果事件
        if event['type'] == "fixed_result":
            text = TextImage(event['result'])
            text.draw_text((save_path + "/result.png"), bg_color_1)
        # 如果是随机结果事件
        elif event['type'] == "random_result":
            # 读取所有结果字符串
            text_A = TextImage(event['A']['result'])
            text_B = TextImage(event['B']['result'])
            text_C = TextImage(event['C']['result'])
            text_A.draw_text((save_path + "/result_A.png"), bg_color_1)
            text_B.draw_text((save_path + "/result_B.png"), bg_color_1)
            text_C.draw_text((save_path + "/result_C.png"), bg_color_1)
        elif event['type'] == "multiple_choice":
            # 读取所有字符串
            text = TextImage(event['content'])
            text_A1 = TextImage(event['A']['choice'])
            text_A2 = TextImage(event['A']['result'])
            text_B1 = TextImage(event['B']['choice'])
            text_B2 = TextImage(event['B']['result'])
            text_C1 = TextImage(event['C']['choice'])
            text_C2 = TextImage(event['C']['result'])
            # 绘制所有的文本段落
            text.draw_text((save_path + "/content.png"), bg_color_1)
            text_A1.draw_text((save_path + "/choice_A.png"), bg_color_2)
            text_A2.draw_text((save_path + "/result_A.png"), bg_color_1)
            text_B1.draw_text((save_path + "/choice_B.png"), bg_color_2)
            text_B2.draw_text((save_path + "/result_B.png"), bg_color_1)
            text_C1.draw_text((save_path + "/choice_C.png"), bg_color_2)
            text_C2.draw_text((save_path + "/result_C.png"), bg_color_1)
    
    #n = TextImage("发生的事件为zzy去干嘛了我也不知打啊" * 5)
    #n.draw_text()