import pygame
import random
import pygame.mixer
import os

pygame.init()
# Добавим музыку
pygame.mixer.init()
pygame.mixer.music.load('farm.mp3')
eating_sound = pygame.mixer.Sound("eat_sound.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
window_size = width, height = 700, 600
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Салат для улитки")

# загружаем изображение
background_image = pygame.image.load("grass.jpg")
background_image = pygame.transform.scale(background_image, window_size)
screen.blit(background_image, (0, 0))

walls = [pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 20), 40, 20) for _ in range(7)]
walls2 = [pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 10), 20, 50) for _ in range(5)]


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Snail(pygame.sprite.Sprite):
    image = load_image("snail.png", -1)
    image = pygame.transform.scale(image, (60, 50))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Snail.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (width // 2, height // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5


class Tomato(pygame.sprite.Sprite):
    image = load_image("tomato.jpg", -1)
    image = pygame.transform.scale(image, (40, 40))

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Tomato.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = pos


all_sprites = pygame.sprite.Group()
snail = Snail()
tomatoes = [Tomato((random.randint(0, width - 40), random.randint(0, height - 40))) for _ in range(10)]
score = 0
end_timer = 0
game_over = False

# Основной игровой цикл
running = True
show_rules = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and show_rules:
            show_rules = False

    screen.blit(background_image, (0, 0))

    if show_rules:
        font = pygame.font.Font(None, 46)
        text1 = font.render("Правила игры:", True, pygame.Color('yellow'))
        text2 = font.render("Накормить улитку всеми томатами,", True, pygame.Color('yellow'))
        text3 = font.render("не врезавшись в стенки.", True, pygame.Color('yellow'))

        screen.blit(text1, (100, 100))
        screen.blit(text2, (100, 150))
        screen.blit(text3, (100, 200))

    else:
        for tomato in tomatoes:
            screen.blit(tomato.image, tomato.rect)

        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 0), wall)
        for wall2 in walls2:
            pygame.draw.rect(screen, (0, 0, 0), wall2)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Счет: {score}", True, pygame.Color('black'))
        screen.blit(text, (10, 10))

        all_sprites.draw(screen)
        all_sprites.update()

        eaten_tomatoes = []
        for tomato in tomatoes:
            if snail.rect.colliderect(tomato.rect):
                eating_sound.play()
                score += 50
                eaten_tomatoes.append(tomato)

        for tomato in eaten_tomatoes:
            tomatoes.remove(tomato)

        for wall in walls:
            if snail.rect.colliderect(wall):
                game_over = True

        for wall2 in walls2:
            if snail.rect.colliderect(wall2):
                game_over = True
        if game_over:
            screen.blit(pygame.font.Font(None, 100).render("GAME OVER", True, pygame.Color('red')), (150, 200))
            running = False

        if not tomatoes:
            screen.blit(pygame.font.Font(None, 100).render("THE END", True, pygame.Color('red')), (200, 200))
            end_timer = pygame.time.get_ticks()

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()
