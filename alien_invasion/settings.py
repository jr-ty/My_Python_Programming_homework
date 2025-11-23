class Settings:
    """存储《外星人入侵》所有设置的类。"""

    def __init__(self):
        """初始化游戏的静态设置。"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # 浅灰色背景

        # 飞船设置
        self.ship_limit = 3  # 飞船生命数（玩家有3条命）

        # 飞船子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)  # 深灰色子弹
        self.bullets_allowed = 10  # 屏幕上同时允许存在的最大子弹数（限制玩家射速）

        # --- 新增：外星人子弹设置 ---
        self.alien_bullet_width = 2
        self.alien_bullet_height = 10
        self.alien_bullet_color = (255, 0, 0)  # 红色子弹，区分敌我

        # 外星人设置
        self.fleet_drop_speed = 10  # 外星人撞到边缘后下落的速度

        # 游戏节奏加快的比例
        self.speedup_scale = 1.2
        # 外星人分数提高的比例
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置。"""
        self.ship_speed = 4.0  # 飞船移动速度
        self.bullet_speed = 3.0  # 飞船子弹速度
        self.alien_speed = 1.0  # 外星人水平移动速度
        # 外星人开火概率：每一帧有 5% 的概率（基于所有外星人）
        # 注意：这个值如果太大，屏幕上会瞬间布满子弹，建议 0.001 到 0.05 之间调整
        self.alien_fire_probability = 0.04

        # --- 新增：外星人子弹速度 ---
        self.alien_bullet_speed = 2.0

        # fleet_direction 为 1 表示向右移动，为 -1 表示向左移动。
        self.fleet_direction = 1

        # 计分设置
        self.alien_points = 50  # 每个外星人的基础分数

    def increase_speed(self):
        """提高速度设置和外星人分数（升级）。"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # --- 新增：同时加快外星人子弹速度 ---
        self.alien_bullet_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)