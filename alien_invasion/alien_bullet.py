import pygame
import random
import math
from pygame.sprite import Sprite


class Alien_Bullet(Sprite):
    """管理外星人发射子弹的类。"""

    def __init__(self, ai_game, alien, dx, dy):
        """在外星人当前位置创建一个子弹对象。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color

        # 在 (0, 0) 处创建一个子弹矩形，然后设置正确的位置。
        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width,
                                self.settings.alien_bullet_height)
        # 将子弹的顶部中央设置为外星人的底部中央（即从外星人位置发射）
        self.rect.midtop = alien.rect.midbottom

        # 存储子弹位置为浮点数，以便进行微调。
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        # --- 新增：存储子弹的运动矢量 ---
        # 保存子弹在 x 轴和 y 轴方向上的速度分量
        # 这允许子弹斜向飞行，而不仅仅是垂直向下
        self.delta_x = float(dx)
        self.delta_y = float(dy)

    def update(self):
        """移动子弹。"""
        # 更新子弹的精确浮点数位置。
        self.y += self.delta_y
        self.x += self.delta_x

        # 更新 rect 对象的位置（用于绘图和碰撞检测）。
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """在屏幕上绘制子弹。"""
        pygame.draw.rect(self.screen, self.color, self.rect)