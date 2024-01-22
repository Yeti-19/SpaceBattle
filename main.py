import pygame
import sys
import random



pygame.init()




class Spaceship(pygame.sprite.Sprite):
        
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('space_battle\graphics\spaceship.gif').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (400,570))
        self.canshoot = True



    def spaceship_input(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rect.x -= 10
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rect.x +=10

    def shoot(self):
            
        if event.type == pygame.MOUSEBUTTONDOWN and self.canshoot:
            b1 = Bullets(self.rect.x + self.rect.width/2 ,self.rect.y )
            b.add(b1)
            self.canshoot = False



    def update(self):

        self.spaceship_input()
        self.shoot()


class Minion(pygame.sprite.Sprite):
    def __init__(self,x):
        super().__init__()

        self.image = pygame.image.load('space_battle/graphics/monster1.png')
        self.rect = self.image.get_rect(midbottom = (x,100))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed


class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((10,20))
        self.image.fill("white")
        self.rect = self.image.get_rect(midbottom = (x,y))

    def update(self):
        self.rect.y -= 15
        if self.rect.y < -10:
            self.kill()
            for i in spaceship:
                i.canshoot = True


class HP():
    def __init__(self,x,y,w,h,hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max = 100
        self.hp = hp

    def draw(self,surface):
        r = self.hp/self.max
        pygame.draw.rect(surface, "red", (self.x,self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x,self.y, self.w*r, self.h))



def shooting():
    for i in b:
        if pygame.sprite.spritecollide(i, monsters, True):
            b.remove(i)
            return True


def player_enemy_collision():

    if pygame.sprite.spritecollide(spaceship.sprite,monsters,True):
        return True
    else:
        return False


    





### Screen ###


screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption('Space Battle')
clock = pygame.time.Clock()
game_active = True


### Spaceship ###
spaceship = pygame.sprite.GroupSingle()
spaceship.add(Spaceship())


### Space invaders ###
monsters = pygame.sprite.Group()



    # Bullets
b = pygame.sprite.Group()

# Health Bar
health = HP(50,50, 200, 20, 100)



kills = 0
score_multiplier = 1
score = 0




timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,1000)


font = pygame.font.SysFont("Italics",100)
font2 = pygame.font.SysFont("Italics",50)



## MAINLOOP ##


while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                health.hp = 100

        if event.type == pygame.MOUSEBUTTONDOWN:
            b.add()
        if event.type == timer:
            monsters.add(Minion(random.randint(100,900)))



    if game_active:

        score = kills * score_multiplier
        s_surface = font2.render("Score: " + str(score), False, "white")
        s_rect = s_surface.get_rect(center = (800,100))

        screen.fill("Black")
        screen.blit(s_surface,s_rect)

        if shooting():
            for i in spaceship:
                i.canshoot = True
            kills += 1

        if player_enemy_collision():
            health.hp -= 20

        if health.hp <= 0:
            game_active = False


        ### Stimulating Difficulty ###

        if kills >= 20:
            for i in monsters:
                i.speed = 2
            score_multiplier += 1 

        elif kills >= 40:
            for i in monsters:
                i.speed = 3
            score_multiplier += 1

        elif kills >= 60:
            for i in monsters:
                i.speed = 4
            score_multiplier += 1

        elif kills >= 100:
            for i in monsters:
                i.speed = 5
            score_multiplier += 2


            ### Spaceship Sprite ###
        spaceship.draw(screen)
        spaceship.update()

            ### Enemies Sprites ###
        monsters.draw(screen)
        monsters.update()

            ### Bullets ###
        b.draw(screen)
        b.update()

            ### HP ###
        health.draw(screen)





    else:
        text1 = font.render("GAME OVER", False, ("red"))
        t1_rec = text1.get_rect(center = (500,200))

        text2 = font.render("PRESS SPACE TO RESTART", False, ("red"))
        t2_rec = text2.get_rect(center = (500,400))

        screen.blit(text1, t1_rec)
        screen.blit(text2, t2_rec)
        monsters.empty()
        score = 0
        score_multiplier = 1
        kills = 0


    pygame.display.update()
    clock.tick(60)
  
