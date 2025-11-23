import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船发射子弹的类。"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在 (0, 0) 处创建一个子弹的矩形，然后设置正确的位置。
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        # 将子弹的顶部中央设置为飞船的顶部中央（即从飞船头部发射）
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储子弹位置为浮点数，以便进行精确控制。
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹。"""
        # 更新子弹的精确浮点数位置。
        # 坐标系原点在左上角，y值减小意味着向上移动。
        self.y -= self.settings.bullet_speed
        # 更新 rect 对象的位置。
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹。"""
        pygame.draw.rect(self.screen, self.color, self.rect)