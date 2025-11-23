import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息的类。"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性。"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置。
        self.text_color = (30, 30, 30)  # 字体颜色（深灰）
        self.font = pygame.font.SysFont(None, 48)  # 使用默认字体，字号48

        # 准备初始得分图像。
        # 这些方法将文本转换为图像，因为 Pygame 不直接绘制文本字符串
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像。"""
        # round 函数让分数显示为 10 的整数倍
        rounded_score = round(self.stats.score, -1)
        # 使用字符串格式化添加千位分隔符（例如 1,000,000）
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分。
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像。"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # 将最高得分放在屏幕顶部中央。
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像。"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # 将等级放在得分下方。
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船。"""
        self.ships = Group()  # 创建一个空编组来存放飞船图标
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            # 计算每艘飞船的位置，使它们在左上角排列
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """检查是否诞生了新的最高得分。"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()  # 如果破纪录，重新渲染最高分图像

    def show_score(self):
        """在屏幕上绘制得分、等级和飞船余量。"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船编组
        self.ships.draw(self.screen)