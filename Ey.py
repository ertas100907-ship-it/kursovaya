import pygame
import sys
import random
import math

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
ORANGE = (230, 126, 34)
PURPLE = (155, 89, 182)
GRAY = (149, 165, 166)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter: Advanced Adapter Architecture")
clock = pygame.time.Clock()

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 3.0)
        self.radius = random.randint(1, 3)
        self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
            self.speed = random.uniform(0.5, 3.0)

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.lifetime = random.randint(20, 50)
        self.color = color
        self.radius = random.randint(2, 6)
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.radius = max(0, self.radius - 0.1)
        if self.lifetime <= 0:
            self.active = False

    def render(self, surface):
        if self.active and self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = 60
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.active = True

    def update(self):
        self.y -= 1
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False

    def render(self, surface):
        if self.active:
            alpha = max(0, min(255, int((self.lifetime / 60) * 255)))
            text_surface = self.font.render(self.text, True, self.color)
            text_surface.set_alpha(alpha)
            surface.blit(text_surface, (self.x, self.y))

class Player:
    def __init__(self):
        self.width = 60
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 80
        self.speed = 7
        self.score = 0
        self.hp = 100
        self.max_hp = 100
        self.shoot_cooldown = 0
        self.active = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def render(self, surface):
        pygame.draw.polygon(surface, GREEN, [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])
        engine_y = self.y + self.height + random.randint(0, 10)
        pygame.draw.polygon(surface, ORANGE, [
            (self.x + self.width // 2 - 10, self.y + self.height),
            (self.x + self.width // 2 + 10, self.y + self.height),
            (self.x + self.width // 2, engine_y)
        ])
        
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, RED, (self.x, self.y - 15, self.width, 5))
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 15, self.width * hp_ratio, 5))

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Laser:
    def __init__(self, x, y, damage=1):
        self.x = x
        self.y = y
        self.speed = 12
        self.width = 4
        self.height = 15
        self.damage = damage
        self.active = True

    def update(self):
        self.y -= self.speed
        if self.y < -50:
            self.active = False

    def render(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x - self.width//2, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x - self.width//4, self.y, self.width//2, self.height))

    def get_hitbox(self):
        return pygame.Rect(self.x - self.width//2, self.y, self.width, self.height)



class StandardEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 3
        self.hp = 2
        self.max_hp = 2
        self.active = True

    def update_logic(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT + 50:
            self.active = False

    def render(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
        
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class LegacyAlienShip:
    def __init__(self, start_x, start_y):
        self.pos_x = start_x
        self.pos_y = start_y
        self.size = 50
        self.health_points = 5
        self.amplitude = 70
        self.angle = 0.0
        self.is_destroyed = False

    def shift_zig_zag(self):
        self.pos_y += 2.0
        self.angle += 0.08
        if self.health_points <= 0:
            self.is_destroyed = True

    def draw_alien_mesh(self, display_surface):
        current_x = self.pos_x + math.sin(self.angle) * self.amplitude
        points = [
            (current_x, self.pos_y),
            (current_x - self.size//2, self.pos_y + self.size//2),
            (current_x - self.size//2, self.pos_y + self.size),
            (current_x + self.size//2, self.pos_y + self.size),
            (current_x + self.size//2, self.pos_y + self.size//2)
        ]
        pygame.draw.polygon(display_surface, YELLOW, points)

    def fetch_bounds(self):
        current_x = self.pos_x + math.sin(self.angle) * self.amplitude
        return (current_x - self.size//2, self.pos_y, self.size, self.size)


class AlienAdapter:
    def __init__(self, legacy_ship: LegacyAlienShip):
        self.legacy_ship = legacy_ship
        self.max_hp = legacy_ship.health_points

    @property
    def hp(self):
        return self.legacy_ship.health_points

    @hp.setter
    def hp(self, value):
        self.legacy_ship.health_points = value

    @property
    def active(self):
        return not self.legacy_ship.is_destroyed and self.legacy_ship.pos_y < SCREEN_HEIGHT + 50

    @active.setter
    def active(self, value):
        self.legacy_ship.is_destroyed = not value

    def update_logic(self):
        self.legacy_ship.shift_zig_zag()

    def render(self, surface):
        self.legacy_ship.draw_alien_mesh(surface)

    def get_hitbox(self):
        bounds = self.legacy_ship.fetch_bounds()
        return pygame.Rect(bounds[0], bounds[1], bounds[2], bounds[3])


class LegacyAsteroidData:
    def __init__(self, cx, cy, radius):
        self.center_x = cx
        self.center_y = cy
        self.r = radius
        self.rot = 0
        self.durability = 10
        self.vec_y = random.uniform(1.0, 2.5)

    def step(self):
        self.center_y += self.vec_y
        self.rot += 2

    def display(self, scr):
        pygame.draw.circle(scr, GRAY, (int(self.center_x), int(self.center_y)), self.r)
        pygame.draw.circle(scr, BLACK, (int(self.center_x), int(self.center_y)), self.r, 2)

    def is_visible(self):
        return self.center_y - self.r < 800 and self.durability > 0

    def get_rect_tuple(self):
        return (self.center_x - self.r, self.center_y - self.r, self.r * 2, self.r * 2)


class AsteroidAdapter:
    def __init__(self, asteroid: LegacyAsteroidData):
        self.asteroid = asteroid
        self.max_hp = asteroid.durability

    @property
    def hp(self):
        return self.asteroid.durability

    @hp.setter
    def hp(self, value):
        self.asteroid.durability = value

    @property
    def active(self):
        return self.asteroid.is_visible()

    @active.setter
    def active(self, value):
        if not value:
            self.asteroid.durability = 0

    def update_logic(self):
        self.asteroid.step()

    def render(self, surface):
        self.asteroid.display(surface)

    def get_hitbox(self):
        rect_data = self.asteroid.get_rect_tuple()
        return pygame.Rect(rect_data[0], rect_data[1], rect_data[2], rect_data[3])




class GameEngine:
    def __init__(self):
        self.state = "MENU"
        self.stars = [Star() for _ in range(100)]
        self.player = Player()
        self.enemies = []
        self.lasers = []
        self.particles = []
        self.floating_texts = []
        self.spawn_timer = 0
        self.difficulty_multiplier = 1.0
        
        self.font_title = pygame.font.SysFont("Impact", 72)
        self.font_main = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)

    def spawn_enemy(self):
        self.spawn_timer += 1 * self.difficulty_multiplier
        if self.spawn_timer >= 60:
            self.spawn_timer = 0
            spawn_type = random.choices(["standard", "legacy", "asteroid"], weights=[50, 30, 20])[0]
            spawn_x = random.randint(50, SCREEN_WIDTH - 50)
            
            if spawn_type == "standard":
                self.enemies.append(StandardEnemy(spawn_x, -50))
            elif spawn_type == "legacy":
                legacy_alien = LegacyAlienShip(spawn_x, -50)
                self.enemies.append(AlienAdapter(legacy_alien))
            elif spawn_type == "asteroid":
                radius = random.randint(30, 60)
                legacy_asteroid = LegacyAsteroidData(spawn_x, -radius, radius)
                self.enemies.append(AsteroidAdapter(legacy_asteroid))

    def create_explosion(self, x, y, color, amount):
        for _ in range(amount):
            self.particles.append(Particle(x, y, color))

    def process_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.reset_game()
                    self.state = "PLAYING"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def process_playing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "PAUSED"
                if event.key == pygame.K_SPACE and self.player.shoot_cooldown == 0:
                    self.lasers.append(Laser(self.player.x + self.player.width // 2, self.player.y))
                    self.player.shoot_cooldown = 15

        self.player.handle_input()
        self.difficulty_multiplier += 0.0001
        self.spawn_enemy()

        for laser in self.lasers:
            laser.update()

        for enemy in self.enemies:
            enemy.update_logic()

        for particle in self.particles:
            particle.update()

        for f_text in self.floating_texts:
            f_text.update()

        for enemy in self.enemies:
            if not enemy.active:
                continue
            
            enemy_rect = enemy.get_hitbox()
            
            if enemy_rect.colliderect(self.player.get_hitbox()):
                self.player.hp -= 20
                enemy.active = False
                self.create_explosion(enemy_rect.centerx, enemy_rect.centery, ORANGE, 30)
                self.floating_texts.append(FloatingText(self.player.x, self.player.y - 20, "-20 HP", RED))
                if self.player.hp <= 0:
                    self.state = "GAME_OVER"

            for laser in self.lasers:
                if not laser.active:
                    continue
                if laser.get_hitbox().colliderect(enemy_rect):
                    enemy.hp -= laser.damage
                    laser.active = False
                    self.create_explosion(laser.x, laser.y, BLUE, 5)
                    self.floating_texts.append(FloatingText(enemy_rect.x, enemy_rect.y, str(laser.damage), WHITE))
                    
                    if enemy.hp <= 0:
                        enemy.active = False
                        self.player.score += enemy.max_hp * 10
                        self.create_explosion(enemy_rect.centerx, enemy_rect.centery, YELLOW, 20)

        self.lasers = [l for l in self.lasers if l.active]
        self.enemies = [e for e in self.enemies if e.active]
        self.particles = [p for p in self.particles if p.active]
        self.floating_texts = [ft for ft in self.floating_texts if ft.active]

    def process_paused(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "PLAYING"

    def process_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.state = "PLAYING"
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

    def update(self):
        for star in self.stars:
            star.update()

        if self.state == "MENU":
            self.process_menu()
        elif self.state == "PLAYING":
            self.process_playing()
        elif self.state == "PAUSED":
            self.process_paused()
        elif self.state == "GAME_OVER":
            self.process_game_over()

    def render_ui(self, surface):
        score_text = self.font_main.render(f"СКОР: {self.player.score}", True, WHITE)
        surface.blit(score_text, (20, 20))
        
        diff_text = self.font_small.render(f"Уровень угрозы: {self.difficulty_multiplier:.2f}x", True, RED)
        surface.blit(diff_text, (20, 60))

    def render_health_bars(self, surface):
        for enemy in self.enemies:
            rect = enemy.get_hitbox()
            if enemy.hp < enemy.max_hp:
                bar_width = rect.width
                fill_width = int((enemy.hp / enemy.max_hp) * bar_width)
                pygame.draw.rect(surface, RED, (rect.x, rect.y - 10, bar_width, 4))
                pygame.draw.rect(surface, GREEN, (rect.x, rect.y - 10, fill_width, 4))

    def render(self, surface):
        surface.fill((10, 10, 20))
        
        for star in self.stars:
            star.render(surface)

        if self.state == "MENU":
            title = self.font_title.render("SPACE SHOOTER ADAPTER", True, YELLOW)
            prompt = self.font_main.render("Нажми ENTER для старта", True, WHITE)
            surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
            surface.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2))

        elif self.state == "PLAYING" or self.state == "PAUSED":
            self.player.render(surface)
            for laser in self.lasers:
                laser.render(surface)
            for enemy in self.enemies:
                enemy.render(surface)
            self.render_health_bars(surface)
            for particle in self.particles:
                particle.render(surface)
            for f_text in self.floating_texts:
                f_text.render(surface)
            
            self.render_ui(surface)

            if self.state == "PAUSED":
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill(BLACK)
                surface.blit(overlay, (0, 0))
                pause_text = self.font_title.render("ПАУЗА", True, WHITE)
                surface.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - pause_text.get_height()//2))

        elif self.state == "GAME_OVER":
            go_text = self.font_title.render("СИСТЕМА УНИЧТОЖЕНА", True, RED)
            score_text = self.font_main.render(f"Итоговый счет: {self.player.score}", True, WHITE)
            restart_text = self.font_small.render("Нажми R для рестарта | ESC для меню", True, GRAY)
            
            surface.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, SCREEN_HEIGHT//3))
            surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))

    def reset_game(self):
        self.player = Player()
        self.enemies.clear()
        self.lasers.clear()
        self.particles.clear()
        self.floating_texts.clear()
        self.spawn_timer = 0
        self.difficulty_multiplier = 1.0


def main():
    engine = GameEngine()
    while True:
        engine.update()
        engine.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()