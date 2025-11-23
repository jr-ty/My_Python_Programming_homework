import pygame.font

class Button:
    """用于为游戏创建按钮的类。"""

    def __init__(self, ai_game, msg):
        """初始化按钮属性。"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和属性。
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0) # 按钮背景色（亮绿色）
        self.text_color = (255, 255, 255) # 文本颜色（白色）
        self.font = pygame.font.SysFont(None, 48) # 使用默认字体，字号48

        # 创建按钮的 rect 对象，并使其居中。
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次。
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将 msg 渲染为图像，并使其在按钮上居中。"""
        # render 将存储在 msg 中的文本转换为图像
        # True 开启反锯齿功能，使文本边缘更平滑
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本。"""
        # 绘制按钮的背景矩形
        self.screen.fill(self.button_color, self.rect)
        # 在按钮上绘制文本图像
        self.screen.blit(self.msg_image, self.msg_image_rect)