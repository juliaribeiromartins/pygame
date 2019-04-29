# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import random
import time

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#classe jogador que representa a nave
class Player(pygame.sprite.Sprite):
    #construtor da classe
    def __init__(self):
        
        #construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        #carregando a imagem de fundo
        player_img = pygame.image.load(path.join(img_dir,"playerShip1_orange.png")).convert()
        self.image = player_img
        
        #diminuindo o tamanho da imagem .
        self.image = pygame.transform.scale(player_img, (50,38))
        
        #deixando transparente
        self.image.set_colorkey(BLACK)
        
        #detalhes sobre o posicionamento
        self.rect = self.image.get_rect()
        
        #centraliza embaixo da tela
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        #velocidade da nave
        self.speedx = 0
        self.radius = 25
    def update(self):
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
           
class Mob(pygame.sprite.Sprite):#classe é com letra maiúscula
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        mob_img = pygame.image.load(path.join(img_dir,"meteorBrown_med1.png")).convert()
        self.image = pygame.transform.scale(mob_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0,WIDTH)
        self.rect.bottom = random.randrange(-100,-40)
        self.speedx =random.randrange(-3,3)
        self.speedy =random.randrange(2,9)
        self.radius= int(self.rect.width*.85/2)


    def update(self):
       self.rect.y+= self.speedy
       self.rect.x+= self.speedx
       if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
           self.rect.centerx = random.randrange(0,WIDTH)
           self.rect.bottom = random.randrange(-100,-40)
           self.speedx =random.randrange(-3,3)
           self.speedy =random.randrange(2,9)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bullet_img = pygame.image.load(path.join(img_dir,"laserRed16.png")).convert()
        self.image=bullet_img
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10
        
    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.bottom<0 :
            self.kill()
            

            
        
     
# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))



# Nome do jogo
pygame.display.set_caption("Asteroids")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
snd_dir=path.join(path.dirname(__file__), 'snd')
pygame.mixer.music.load(path.join(snd_dir,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)
boom_sound=pygame.mixer.Sound(path.join(snd_dir, "expl3.wav"))
destroy_sound=pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
pew_sound=pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))






player= Player()

all_sprites=pygame.sprite.Group()   #add no grupo
all_sprites.add(player)

bullets = pygame.sprite.Group()

mobs = pygame.sprite.Group()
for i in range(0,8):
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)


# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #verifica se apertou alguma tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                    
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    pew_sound.play()

                
            
            
            
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                    
        #depois de processar os eventos 
        #atualiza a acao de cada sprite
        all_sprites.update()
       
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits: 
            destroy_sound.play()
            m = Mob() 
            all_sprites.add(m)
            mobs.add(m)
        
        
        
        #verifica se houve colisão entre a nave e meteoro
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            #toca o som da colisão
            boom_sound.play()
            time.sleep(1)#precisa esperar senão fecha
            running = False
        
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()


  









