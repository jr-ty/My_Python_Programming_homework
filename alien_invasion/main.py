import sys
from time import sleep

import pygame
import random
import math

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien_bullet import Alien_Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的整体类。"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()

        # --- 新增：音频初始化 ---
        pygame.mixer.init()  # 初始化混音器模块

        # 设置游戏窗口标题
        pygame.display.set_caption("Alien Invasion")

        # --- 新增：背景音乐设置 ---
        # 加载背景音乐文件
        pygame.mixer.music.load('sounds/BGM.mp3')
        # 设置音量 (0.0 到 1.0)
        pygame.mixer.music.set_volume(0.5)
        # 播放背景音乐，-1 表示无限循环播放
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()  # 创建时钟对象，用于控制游戏帧率
        self.settings = Settings()

        # 创建游戏窗口
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 创建一个用于存储游戏统计信息的实例，以及创建记分牌。
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        # 创建精灵编组（Group），用于统一管理多个精灵
        self.bullets = pygame.sprite.Group()  # 飞船的子弹
        self.aliens = pygame.sprite.Group()  # 外星人舰队
        # --- 新增：外星人子弹编组 ---
        self.alien_bullets = pygame.sprite.Group()  # 外星人发射的子弹

        self._create_fleet()

        # 游戏启动时处于非活动状态（等待点击 Play 按钮）。
        self.game_active = False

        # 创建 Play 按钮。
        self.play_button = Button(self, "Play")

        # --- 新增：加载音效对象 ---
        self.shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')  # 射击音效
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')  # 爆炸音效

    def run_game(self):
        """开始游戏的主循环。"""
        while True:
            # 1. 检查事件（键盘、鼠标）
            self._check_events()

            if self.game_active:
                # 2. 更新飞船位置
                self.ship.update()

                # 3. 更新飞船子弹位置（包括删除消失的子弹、检测与外星人的碰撞）
                self._update_bullets()

                # 4. 更新外星人位置（包括检测是否撞到飞船或到底部）
                self._update_aliens()

                # --- 新增：外星人攻击逻辑 ---
                # 5. 外星人尝试发射子弹（基于概率）
                self._fire_alien_bullet()

                # 6. 更新外星人子弹位置（包括删除消失的子弹、检测与飞船的碰撞）
                self._update_alien_bullets()

            # 7. 重新绘制屏幕
            self._update_screen()

            # 控制帧率，确保游戏运行速度一致 (60 FPS)
            self.clock.tick(60)

    def _check_events(self):
        """响应按键和鼠标事件。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # --- 新增：退出前保存数据 ---
                self.stats.save_highscore()  # 每次退出前保存最高分到文件
                pygame.mixer.music.stop()  # 停止背景音乐
                sys.exit()  # 点击关闭按钮退出

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击 Play 按钮时开始新游戏。"""
        # 检查鼠标点击位置是否在按钮的 rect 范围内
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 重置游戏设置（如速度恢复初始值）
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计信息（分数、等级、生命）
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # 清空现有的子弹和外星人
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()  # 同时清空外星人子弹

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 游戏开始后隐藏光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键按下。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            # --- 新增：按Q退出时也保存数据 ---
            self.stats.save_highscore()  # 保存最高分
            pygame.mixer.music.stop()  # 停止音乐
            sys.exit()  # 退出游戏
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # 按空格发射子弹

    def _check_keyup_events(self, event):
        """响应按键松开。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一个新子弹并将其加入子弹编组。"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.shoot_sound.play()  # --- 新增：播放子弹发射音效 ---
            self.bullets.add(new_bullet)

    def _fire_alien_bullet(self):
        """让外星人随机发射子弹（包含随机方向计算）。"""
        # 如果外星人全部被消灭，就不发射
        if not self.aliens:
            return

        # 生成一个随机数，如果小于设定的概率，就开火
        # 这里的逻辑是：每一帧都判断一次，概率通常设得很小（例如 0.02）
        if random.random() < self.settings.alien_fire_probability:
            # 随机选择一个外星人作为发射源
            random_alien = random.choice(self.aliens.sprites())

            # --- 新增：计算随机发射轨迹 ---
            # 这里的目的是让子弹不仅仅垂直向下，而是带有一定的随机散射角度

            # 1. 随机生成一个垂直速度分量 (dy)
            # random.randint 保证 dy 至少有一定的大小，random.random 增加浮点数随机性
            dy = random.randint(0, int(self.settings.alien_bullet_speed)) + random.random()

            # 确保 dy 不超过设定的最大速度，否则下面的开根号计算可能出错
            if dy > self.settings.alien_bullet_speed:
                dy -= 1.0

            # 2. 根据勾股定理计算水平速度分量 (dx)
            # 总速度^2 = dx^2 + dy^2  =>  dx = sqrt(总速度^2 - dy^2)
            dx = math.sqrt(math.pow(self.settings.alien_bullet_speed, 2) - math.pow(dy, 2))
            dx *=random.choice([-1,1])

            # 创建外星人子弹对象，传入计算好的向量
            new_bullet = Alien_Bullet(self, random_alien, dx, dy)
            self.alien_bullets.add(new_bullet)

    def _update_bullets(self):
        """更新飞船子弹位置并删除已消失的子弹。"""
        # 更新子弹位置。
        self.bullets.update()

        # 删除已消失的子弹。
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 检测子弹与外星人的碰撞
        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        """更新外星人子弹位置，删除出界子弹，检测碰撞。"""
        self.alien_bullets.update()

        # 删除消失的子弹（飞出屏幕底部）
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        # 检测外星人子弹是否击中飞船
        # spritecollideany 返回击中飞船的第一个子弹精灵，如果没有则返回 None
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()  # 直接调用现有的飞船被撞击逻辑

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞。"""
        # 删除所有发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            # 遍历碰撞字典，如果有子弹击中了多个外星人，都计入分数
            for aliens in collisions.values():
                self.explosion_sound.play()  # --- 新增：播放爆炸音效 ---
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()  # 更新分数显示
            self.sb.check_high_score()  # 检查是否打破最高分

        if not self.aliens:
            # 如果外星人全部被消灭：删除现有的子弹，加快节奏，创建新外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """响应飞船被外星人撞击（或被子弹击中）。"""
        self.explosion_sound.play()  # --- 新增：播放爆炸音效 ---

        if self.stats.ships_left > 0:
            # 生命值减1，更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的外星人、飞船子弹和外星人子弹
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停一会儿让玩家反应
            sleep(0.5)
        else:
            # 生命值耗尽，游戏结束
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置。"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞（身体直接接触）
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端。"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break

    def _create_fleet(self):
        """创建外星人群。"""
        # 创建一个外星人，计算一行可容纳多少个外星人。
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 一行结束；重置 x 值，并递增 y 值。
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行。"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """如果有外星人到达边缘，做出相应的响应。"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向。"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。"""
        self.screen.fill(self.settings.bg_color)

        # 绘制飞船子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # --- 新增：绘制外星人子弹 ---
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 显示得分信息
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制 Play 按钮
        if not self.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()