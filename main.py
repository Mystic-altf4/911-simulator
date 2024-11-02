import pygame
import random

# Pygame ayarları
pygame.init()
width, height = 500, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Renkler
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Oyun değişkenleri
gravity = 0.1  # Yerçekimi
bird_movement = 0
game_active = False
score = 0
high_score = 0

# Kuş özellikleri
bird_image = pygame.image.load("bird.png").convert_alpha()  # Kuş görselini yükle
bird_rect = bird_image.get_rect(center=(50, height // 3))  # Kuşun dikdörtgenini ayarla

# Boru görsellerini yükle
top_pipe_image = pygame.image.load("top_pipe.png").convert_alpha()
bottom_pipe_image = pygame.image.load("bottom_pipe.png").convert_alpha()

# Patlama görseli ve sesi yükle
explosion_image = pygame.image.load("explosion.png").convert_alpha()
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Engel özellikleri
pipe_height = [200, 300, 400]
pipes = []
pipe_velocity = 3
pipe_gap = 150  # Borular arasındaki boşluk
pipe_timer = 120  # Boru oluşturma sıklığı

# Font ayarları
font = pygame.font.Font(None, 36)

# Zorluk ayarları
difficulty = 'Easy'
jump_force = -5  # Varsayılan zıplama kuvveti

def draw_bird():
    screen.blit(bird_image, bird_rect)  # Kuşu görsel olarak çiz

def create_pipe():
    height = random.choice(pipe_height)
    top_pipe = top_pipe_image.get_rect(midbottom=(width, height - 200))  # Üst boru
    bottom_pipe = bottom_pipe_image.get_rect(midtop=(width, height + pipe_gap))  # Alt boru
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_velocity
    return [pipe for pipe in pipes if pipe.right > 0]  # Ekrandan çıkan boruları kaldır

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom < height:  # Üst boru
            screen.blit(top_pipe_image, pipe)
        else:  # Alt boru
            screen.blit(bottom_pipe_image, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= height:
        return False
    return True

def update_score(pipes):
    global score
    for pipe in pipes:
        if pipe.centerx == bird_rect.centerx:
            score += 1

def reset_game():
    global game_active, bird_movement, bird_rect, pipes, score
    game_active = True
    bird_movement = 0
    bird_rect.center = (50, height // 3)  # Başlangıç konumu
    pipes.clear()
    score = 0

def show_menu():
    global difficulty, jump_force, game_active
    menu_active = True
    while menu_active:
        screen.fill(WHITE)
        title_surface = font.render("Zorluk Seçin", True, BLACK)
        easy_surface = font.render("Kolay (1): -5", True, BLACK)
        medium_surface = font.render("Orta (2): -7", True, BLACK)
        hard_surface = font.render("Zor (3): -10", True, BLACK)

        screen.blit(title_surface, (width // 4, height // 4))
        screen.blit(easy_surface, (width // 4, height // 3))
        screen.blit(medium_surface, (width // 4, height // 2.5))
        screen.blit(hard_surface, (width // 4, height // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 'Easy'
                    jump_force = -5
                    menu_active = False
                elif event.key == pygame.K_2:
                    difficulty = 'Medium'
                    jump_force = -7
                    menu_active = False
                elif event.key == pygame.K_3:
                    difficulty = 'Hard'
                    jump_force = -10
                    menu_active = False
        
        pygame.display.flip()

def show_explosion():
    # Patlama görselini ekranda ortalayarak göster
    explosion_rect = explosion_image.get_rect(center=(width // 2, height // 2))
    screen.blit(explosion_image, explosion_rect)
    explosion_sound.play()  # Patlama sesini çal

# Ana oyun döngüsü
clock = pygame.time.Clock()
show_menu()  # Zorluk seçim menüsünü göster
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0  # Yukarı zıpla
                bird_movement += jump_force  # Seçilen zorluk seviyesine göre zıpla
            if event.key == pygame.K_SPACE and not game_active:
                reset_game()  # Oyunu sıfırla

    # Oyun güncellemesi
    if game_active:
        bird_movement += gravity  # Yerçekimi etkisi
        bird_rect.centery += bird_movement  # Kuşun düşmesini sağla
        if pipe_timer <= 0:
            pipes.extend(create_pipe())  # Yeni boru oluştur
            pipe_timer = 120  # Yeniden başlat
        else: 
            pipe_timer -= 1  # Sayacı azalt
        pipes = move_pipes(pipes)  # Boruları hareket ettir
        game_active = check_collision(pipes)  # Çarpışma kontrolü
        update_score(pipes)  # Skor güncelle

    # Ekranı temizle
    screen.fill(WHITE)
    draw_bird()  # Kuşu çiz
    draw_pipes(pipes)  # Boruları çiz

    # Skor gösterimi
    score_surface = font.render(f'Skor: {score}', True, BLACK)
    screen.blit(score_surface, (10, 10))

    # Eğer oyun aktif değilse patlama görselini göster
    if not game_active:
        show_explosion()

    pygame.display.flip()  # Ekranı güncelle
    clock.tick(120)  # FPS sınırı
