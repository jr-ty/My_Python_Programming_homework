import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类。"""

    def __init__(self, ai_game):
        """初始化飞船并设置其起始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其 rect 属性。
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部的中央。
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性 x 中存储小数值（因为 rect 只能存储整数，而我们需要更精确的速度控制）。
        self.x = float(self.rect.x)

        # 移动标志；飞船一开始不移动。
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """让飞船在屏幕上居中。"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """根据移动标志调整飞船的位置。"""
        # 更新飞船的 x 值，而不是 rect。
        # 检查是否移动且未触碰屏幕边缘
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据 self.x 更新 rect 对象。
        self.rect.x = self.x

    def blitme(self):
        """在当前位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)