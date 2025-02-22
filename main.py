import pygame
from game_settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sausage.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 50
        self.speed_y = 0
        self.is_jumping = False

    def update(self):
        self.speed_y += GRAVITY
        self.rect.y += self.speed_y

        if self.rect.bottom > SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.speed_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.speed_y = JUMP_SPEED
            self.is_jumping = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sausage Man - Rainbow Temple")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        # Define rainbow colors
        rainbow_colors = [RED, (255, 165, 0), YELLOW, GREEN, BLUE, (75, 0, 130), (238, 130, 238)]

        # Create platforms
        platform1 = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, rainbow_colors[0])
        platform2 = Platform(100, SCREEN_HEIGHT - 200, 150, 20, rainbow_colors[1])
        platform3 = Platform(300, SCREEN_HEIGHT - 350, 150, 20, rainbow_colors[2])
        platform4 = Platform(500, SCREEN_HEIGHT - 200, 150, 20, rainbow_colors[3])
        platform5 = Platform(700, SCREEN_HEIGHT - 350, 150, 20, rainbow_colors[4])
        self.platforms.add(platform1, platform2, platform3, platform4, platform5)
        self.all_sprites.add(platform1, platform2, platform3, platform4, platform5)

        # Create obstacles
        obstacle1 = Obstacle(250, SCREEN_HEIGHT - 100, 50, 50, rainbow_colors[5])
        obstacle2 = Obstacle(600, SCREEN_HEIGHT - 250, 50, 50, rainbow_colors[6])
        self.obstacles.add(obstacle1, obstacle2)
        self.all_sprites.add(obstacle1, obstacle2)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    print(f"Key pressed: {event.key}")
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            # Check key states for continuous movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += PLAYER_SPEED

            self.update()
            self.draw()

        pygame.quit()

    def update(self):
        self.player.update()
        # Check for collisions with platforms
        collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if collisions:
            for platform in collisions:
                if self.player.speed_y > 0 and self.player.rect.bottom <= platform.rect.top + 10:
                    self.player.rect.bottom = platform.rect.top
                    self.player.speed_y = 0
                    self.player.is_jumping = False
        # Check for collisions with obstacles
        obstacle_collisions = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        if obstacle_collisions:
            print("Game Over!")
            pygame.quit()
            exit()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
