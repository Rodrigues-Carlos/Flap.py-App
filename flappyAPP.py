import pygame
import random
import sys

def desenho_chao():  # criar o chao
    screen.blit(superficie_chao, (chao_x_pos, 900))
    screen.blit(superficie_chao, (chao_x_pos + 576, 1024))


def gerar_cano():  # gerar canos(obstaculos) aleatorios
    gerar_cano_aleatorio = random.choice(altura_cano)
    cano_baixo = superficie_cano.get_rect(midtop=(700, gerar_cano_aleatorio))
    cano_cima = superficie_cano.get_rect(midbottom=(700, gerar_cano_aleatorio - 300))
    return cano_baixo, cano_cima


def mover_cano(canos):  # fazer a movimentação dos obstaculos
    for cano in canos:
        cano.centerx -= 5
    return canos

def criar_cano(canos):  # criar obstaculos
    for cano in canos:
        if cano.bottom >= 1024:
            screen.blit(superficie_cano, cano)
        else:
            flip_cano = pygame.transform.flip(superficie_cano, False, True)
            screen.blit(flip_cano, cano)

def remover_canos(canos):  # remover canos quando morrer
    for cano in canos:
        if cano.centerx == -600:
            canos.remove(cano)
    return canos

def conferir_colisao(canos):  # detectar colisão
    global can_score
    for cano in canos:
        if ghost.colliderect(cano):
            death_sound.play()
            can_score = True
            return False

    if ghost.top <= -100 or ghost.bottom >= 900:
        can_score = True
        return False

    return True

def animpulo_ghost(ghost):
    new_ghost = pygame.transform.rotozoom(ghost, -movimento_ghost * 3, 1)
    return new_ghost

def anim_ghost():  # animação do personagem
    new_ghost1 = ghost_partes[ghost_index]
    new_ghost = new_ghost1.get_rect(center=(100, ghost.centery))
    return new_ghost1, new_ghost

def score_display(game_state):  # iniciar score ou parar quando morrer
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'Record: {int(pontuacao_maxima)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(250, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, pontuacao_maxima):  # fazer atualização do score
    if score > pontuacao_maxima:
        pontuacao_maxima = score
    return pontuacao_maxima


def cano_score_check():
    global score, can_score

    if lista_cano:
        for cano in lista_cano:
            if 95 < cano.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if cano.centerx < 0:
                can_score = True

# Area de variaveis e e constantes

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

gravidade = 0.25
movimento_ghost = 0
game_active = True
score = 0
pontuacao_maxima = 0
can_score = True
bg_surface = pygame.image.load('assets/fundo.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

superficie_chao = pygame.image.load('assets/base.png').convert()
superficie_chao = pygame.transform.scale2x(superficie_chao)
chao_x_pos = 0

Ghost_downflap = pygame.transform.scale2x(pygame.image.load('assets/Ghost.png').convert_alpha())
Ghost_midflap = pygame.transform.scale2x(pygame.image.load('assets/Ghost.png').convert_alpha())
Ghost_upflap = pygame.transform.scale2x(pygame.image.load('assets/Ghost.png').convert_alpha())
ghost_partes = [Ghost_downflap, Ghost_midflap, Ghost_upflap]
ghost_index = 0
ghost_surface = ghost_partes[ghost_index]
ghost = ghost_surface.get_rect(center=(100, 512))

GHOSTFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(GHOSTFLAP, 200)

superficie_cano = pygame.image.load('assets/pipe-red.png')
superficie_cano = pygame.transform.scale2x(superficie_cano)
lista_cano = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
altura_cano = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(250, 576))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)


# Programa Principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                movimento_ghost = 0
                movimento_ghost -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                lista_cano.clear()
                ghost.center = (100, 512)
                movimento_ghost = 0
                score = 0

        if event.type == SPAWNPIPE:
            lista_cano.extend(gerar_cano())

        if event.type == GHOSTFLAP:
            if ghost_index < 2:
                ghost_index += 1
            else:
                ghost_index = 0

            ghost_surface, ghost = anim_ghost()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # GHOST
        movimento_ghost += gravidade
        girar_boneco = animpulo_ghost(ghost_surface)
        ghost.centery += movimento_ghost
        screen.blit(girar_boneco, ghost)
        game_active = conferir_colisao(lista_cano)

        # Canos
        lista_cano = mover_cano(lista_cano)
        lista_cano = remover_canos(lista_cano)
        criar_cano(lista_cano)

        # Pontuação
        cano_score_check()
        score += 0.001
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        pontuacao_maxima = update_score(score, pontuacao_maxima)
        score_display('game_over')

    # chao
    chao_x_pos -= 1
    desenho_chao()
    if chao_x_pos <= -576:
        chao_x_pos = 0

    pygame.display.update()
    clock.tick(120)
