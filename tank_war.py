import pygame
import os
import random
import sys
import copy
from functools import partial
from pygame.locals import *

class Tank:
    def __init__(self,left_image,up_image,right_image,down_image,pos,speed,direction):
        self.direction=direction
        self.left_image=left_image
        self.up_image=up_image
        self.down_image=down_image
        self.right_image=right_image
        if self.direction=='left':
            self.image=left_image
        if self.direction=='up':
            self.image=up_image
        if self.direction=='right':
            self.image=right_image
        if self.direction=='down':
            self.image=down_image 
        self.pos = pos
        self.speed = speed 
        self.is_alive = True 
        self.life=int(10)

    def draw(self,screen):
        screen.blit(self.image,(self.pos[0],self.pos[1]))

    def move_up(self):
        self.direction='up'
        self.image=self.up_image
        self.pos[1]=self.pos[1]-self.speed
        return
    
    def move_left(self):
        self.direction='left'
        self.image=self.left_image
        self.pos[0]=self.pos[0]-self.speed
        return

    def move_right(self):
        self.direction='right'
        self.image=self.right_image
        self.pos[0]=self.pos[0]+self.speed
        return

    def move_down(self):
        self.direction='down'
        self.image=self.down_image
        self.pos[1]=self.pos[1]+self.speed
        return

class Bullet():
    def __init__(self,left_image,up_image,right_image,down_image,pos,speed,direction):
        self.direction=direction
        self.left_image=left_image
        self.up_image=up_image
        self.down_image=down_image
        self.right_image=right_image
        if self.direction=='left':
            self.image=left_image
        if self.direction=='up':
            self.image=up_image
        if self.direction=='right':
            self.image=right_image
        if self.direction=='down':
            self.image=down_image 
        self.pos = pos
        self.speed = speed 
        self.exist = False 

    def shoot_up(self):
            self.direction='up'
            self.image=self.up_image
            self.pos[1]=self.pos[1]-self.speed

    def shoot_down(self):
            self.direction='down'
            self.image=self.down_image
            self.pos[1]=self.pos[1]+self.speed

    def shoot_left(self):
            self.direction='left'
            self.image=self.left_image
            self.pos[0]=self.pos[0]-self.speed

    def shoot_right(self):
            self.direction='right'
            self.image=self.right_image
            self.pos[0]=self.pos[0]+self.speed
        
    def draw(self,screen):
            screen.blit(self.image,(self.pos[0],self.pos[1]))

def parse_txt_file(file_path):
    result = []
    with open(file_path, 'r',encoding='utf-8') as file:
        for line in file:
            for i in line.strip().split('，'):
                if i == '':
                    break
                else:
                    num=int(i)
                    result.append(num)
        return result

def random_move(enemy_self,player_self,map_data,grids_size,height):
    directions = ["up", "down", "left", "right"]
    if not tank_collide(map_data,enemy_self,grids_size,height):
        enemy_self.direction = random.choice(directions)
    if enemy_self.direction=='up' and tank_collide(map_data,enemy_self,grids_size,height):
        if not tanks_mutual_collide(enemy_self,player_self,grids_size):
            enemy_self.move_up()
        else:
            enemy_self.direction = random.choice(directions)
    if enemy_self.direction=='down' and tank_collide(map_data,enemy_self,grids_size,height):
        if not tanks_mutual_collide(enemy_self,player_self,grids_size):
            enemy_self.move_down()
        else:
            enemy_self.direction = random.choice(directions)
    if enemy_self.direction=='left' and tank_collide(map_data,enemy_self,grids_size,height):
        if not tanks_mutual_collide(enemy_self,player_self,grids_size):
            enemy_self.move_left()
        else:
            enemy_self.direction = random.choice(directions)
    if enemy_self.direction=='right' and tank_collide(map_data,enemy_self,grids_size,height):
        if not tanks_mutual_collide(enemy_self,player_self,grids_size):
            enemy_self.move_right()
        else:
            enemy_self.direction = random.choice(directions)
    
def create_map(data,width,height,map_black_image,map_wall_image,map_stone_image,map_ice_image,map_river_image,map_forest_image,camp_alive_image):
    grids_data=[]
    cur=0
    for i in data:
        if i==0:
            j={'grids_pos':[cur%width,cur//width],'image':map_black_image,'can_pass':True,'bullet_pass':True,'life':int(0)}
        if i==1:
            j={'grids_pos':[cur%width,cur//width],'image':map_wall_image,'can_pass':False,'bullet_pass':False,'life':int(10)}
        if i==2:
            j={'grids_pos':[cur%width,cur//width],'image':map_stone_image,'can_pass':False,'bullet_pass':False,'life':int(999999)}
        if i==3:
            j={'grids_pos':[cur%width,cur//width],'image':map_ice_image,'can_pass':True,'bullet_pass':True,'life':int(999999)}
        if i==4:
            j={'grids_pos':[cur%width,cur//width],'image':map_river_image,'can_pass':False,'bullet_pass':True,'life':int(999999)}
        if i==5:
            j={'grids_pos':[cur%width,cur//width],'image':map_forest_image,'can_pass':True,'bullet_pass':True,'life':int(999999)}
        if i==6:
            j={'grids_pos':[cur%width,cur//width],'image':camp_alive_image,'can_pass':True,'bullet_pass':False,'life':int(5)}
        grids_data.append(j)
        cur+=1
    return grids_data

def draw_map(map_data,screen):
    for i in map_data:
        screen.blit(i['image'],(i['grids_pos'][0]*grids_size,i['grids_pos'][1]*grids_size))

def pos_translate(x,y,grids_size,width):
    n=(y//grids_size)*width+(x//grids_size)
    return n

def tank_collide(map_data,tank_self,grids_size,height):
    if tank_self.direction=='up':
        if tank_self.pos[0]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]-tank_self.speed,grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]-tank_self.speed,grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]+grids_size,tank_self.pos[1]-tank_self.speed,grids_size,width)]['can_pass']:
                return True
            else:
                return False    
    if tank_self.direction=='down':
        if tank_self.pos[0]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]+tank_self.speed+(grids_size//2),grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]+tank_self.speed+(grids_size//2),grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]+grids_size,tank_self.pos[1]+tank_self.speed+(grids_size//2),grids_size,width)]['can_pass']:
                return True
            else:
                return False
    if tank_self.direction=='left':
        if tank_self.pos[1]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0]-tank_self.speed,tank_self.pos[1],grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0]-tank_self.speed,tank_self.pos[1],grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]-tank_self.speed,tank_self.pos[1]+grids_size,grids_size,width)]['can_pass']:
                return True
            else:
                return False
    if tank_self.direction=='right':
        if tank_self.pos[1]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0]+tank_self.speed+(grids_size//2),tank_self.pos[1],grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0]+tank_self.speed+(grids_size//2),tank_self.pos[1],grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]+tank_self.speed+(grids_size//2),tank_self.pos[1]+grids_size,grids_size,width)]['can_pass']:
                return True
            else:
                return False

def tanks_mutual_collide(tank_self,another_tank_self,grids_size):
    if tank_self.direction=='up':
        if (-grids_size)<(tank_self.pos[0]-another_tank_self.pos[0])<grids_size:
            if (tank_self.pos[1]-another_tank_self.pos[1])<=grids_size:
                return True
            else:
                return False
    if tank_self.direction=='down':
        if (-grids_size)<(tank_self.pos[0]-another_tank_self.pos[0])<grids_size:
            if (another_tank_self.pos[1]-tank_self.pos[1])<=grids_size:
                return True
            else:
                return False
    if tank_self.direction=='left':
        if (-grids_size)<(tank_self.pos[1]-another_tank_self.pos[1])<grids_size:
            if (tank_self.pos[0]-another_tank_self.pos[0])<=grids_size:
                return True
            else:
                return False
    if tank_self.direction=='right':
        if (-grids_size)<(tank_self.pos[1]-another_tank_self.pos[1])<grids_size:
            if (another_tank_self.pos[0]-tank_self.pos[0])<=grids_size:
                return True
            else:
                return False

def bullet_collide(map_data,bullet_self,grids_size,height):
    if bullet_self.direction=='up':
        if (grids_size/12)<=bullet_self.pos[0]%grids_size<=((grids_size-grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['life']-=5
                return False , map_data 
        elif bullet_self.pos[0]%grids_size<(grids_size/12):
            if map_data[pos_translate(bullet_self.pos[0]-grids_size,bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]-grids_size,bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['life']-=5 
                map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['life']-=5
                return False , map_data
        elif bullet_self.pos[0]%grids_size>(grids_size-(grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0]+grids_size,bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['life']-=5
                map_data[pos_translate(bullet_self.pos[0]+grids_size,bullet_self.pos[1]-bullet_self.speed,grids_size,width)]['life']-=5
                return False , map_data 
    if bullet_self.direction=='down':
        if (grids_size/12)<=bullet_self.pos[0]%grids_size<=((grids_size-grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['life']-=5
                return False , map_data
        elif bullet_self.pos[0]%grids_size<(grids_size/12):
            if map_data[pos_translate(bullet_self.pos[0]-grids_size,bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]-grids_size,bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['life']-=5
                map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['life']-=5
                return False , map_data
        elif bullet_self.pos[0]%grids_size>(grids_size-(grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0]+grids_size,bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0],bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['life']-=5
                map_data[pos_translate(bullet_self.pos[0]+grids_size,bullet_self.pos[1]+bullet_self.speed+(grids_size//12),grids_size,width)]['life']-=5
                return False , map_data
    if bullet_self.direction=='left':
        if (grids_size/12)<=bullet_self.pos[1]%grids_size<=((grids_size-grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1],grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1],grids_size,width)]['life']-=5
                return False , map_data
        elif bullet_self.pos[1]%grids_size<(grids_size/12):
            if map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1]-grids_size,grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1],grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1]-grids_size,grids_size,width)]['life']-=5
                map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1],grids_size,width)]['life']-=5
                return False , map_data
        elif bullet_self.pos[1]%grids_size>(grids_size-(grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1],grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1]+grids_size,grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1],grids_size,width)]['life']-=5
                map_data[pos_translate(bullet_self.pos[0]-bullet_self.speed,bullet_self.pos[1]+grids_size,grids_size,width)]['life']-=5
                return False , map_data 
    if bullet_self.direction=='right':
        if (grids_size/12)<=bullet_self.pos[1]%grids_size<=((grids_size-grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1],grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1],grids_size,width)]['life']-=5
                return False , map_data
        elif bullet_self.pos[1]%grids_size<(grids_size/12):
            if map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1]-grids_size,grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1],grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1]-grids_size,grids_size,width)]['life']-=5
                map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1],grids_size,width)]['life']-=5
                return False , map_data
        elif bullet_self.pos[1]%grids_size>(grids_size-(grids_size/12)):
            if map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1],grids_size,width)]['bullet_pass'] and map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1]+grids_size,grids_size,width)]['bullet_pass']:
                return True , map_data
            else:
                map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1],grids_size,width)]['life']-=5
                map_data[pos_translate(bullet_self.pos[0]+bullet_self.speed+(grids_size//12),bullet_self.pos[1]+grids_size,grids_size,width)]['life']-=5
                return False , map_data 

def map_amend(map_data,map_black_image,camp_dead_image):
    for i in range(0,width*(height-1)):
        if map_data[i]['image']==camp_alive_image:
            if map_data[i]['life']<=0:
                map_data[i]['image']=camp_dead_image
                return map_data
        if map_data[i]['image']==map_wall_image:
            if map_data[i]['life']<=0:
                print(map_data[i])
                map_data[i]['image']=map_black_image
                map_data[i]['can_pass']=True
                map_data[i]['bullet_pass']=True
                return map_data
    return map_data

def ResPath(file_path):
    return os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\tank_picture', file_path)


pygame.init()
grids_size=60
width,height=20,15
screen = pygame.display.set_mode((width*grids_size,height*grids_size))
pygame.display.set_caption("坦克大战测试版")
player_tank_image_left =pygame.transform.scale(pygame.image.load(ResPath('player_tank.png')),(grids_size,grids_size))
player_tank_image_up=pygame.transform.rotate(player_tank_image_left,-90)
player_tank_image_right=pygame.transform.rotate(player_tank_image_left,-180)
player_tank_image_down=pygame.transform.rotate(player_tank_image_left,-270)
enemy_tank_image_left =pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\tank_picture', 'enemy_tank.png')),(grids_size,grids_size))
enemy_tank_image_up=pygame.transform.rotate(enemy_tank_image_left,-90)
enemy_tank_image_right=pygame.transform.rotate(enemy_tank_image_left,-180)
enemy_tank_image_down=pygame.transform.rotate(enemy_tank_image_left,-270)
camp_alive_image =pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'camp0.png')),(grids_size,grids_size))
camp_dead_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'camp1.png')),(grids_size,grids_size))
map_forest_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'forest.png')),(grids_size,grids_size))
map_ice_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'ice.png')),(grids_size,grids_size))
map_river_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'river.png')),(grids_size,grids_size))
map_stone_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'stone.png')),(grids_size,grids_size))
map_wall_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'wall.png')),(grids_size,grids_size))
map_black_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_picture', 'black.jpg')),(grids_size,grids_size))
bullet_up_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\bullet_picture', 'bullet_up.png')),(grids_size//12,grids_size//12))
bullet_down_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\bullet_picture', 'bullet_down.png')),(grids_size//12,grids_size//12))
bullet_left_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\bullet_picture', 'bullet_left.png')),(grids_size//12,grids_size//12))
bullet_right_image=pygame.transform.scale(pygame.image.load(os.path.join('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\bullet_picture', 'bullet_right.png')),(grids_size//12,grids_size//12))

#图片进行旋转 player_tank_image=pygame.transform.rotate(player_tank_image,-90)
#player_tank_image = pygame.transform.scale(player_tank_image, (30, 30))#对图片进行缩放
#screen.blit(player_tank_image_down,(640,360))
#screen.blit(map_wall_image,(60,50))
player_tank=Tank(player_tank_image_left,player_tank_image_up,player_tank_image_right,player_tank_image_down,[grids_size*(width-2),grids_size*(height-2)],grids_size//2,'up')
player_bullet=Bullet(bullet_left_image,bullet_up_image,bullet_right_image,bullet_down_image,[player_tank.pos[0],player_tank.pos[1]],grids_size//2,'up')
enemy_tank_1=Tank(enemy_tank_image_left,enemy_tank_image_up,enemy_tank_image_right,enemy_tank_image_down,[grids_size*(width-10),grids_size*(height-5)],grids_size//6,'up')

running = True
clock = pygame.time.Clock()
is_dead=False
data=parse_txt_file('C:\\Users\\hp\\Desktop\\my_program\\tank_war\\map_data.txt')
map_data=create_map(data,width,height,map_black_image,map_wall_image,map_stone_image,map_ice_image,map_river_image,map_forest_image,camp_alive_image)
#print(map_data)
moving=False
while running:
    screen.fill('black')
    draw_map(map_data,screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_tank.direction='up'
        if tank_collide(map_data,player_tank,grids_size,height):
            if not tanks_mutual_collide(player_tank,enemy_tank_1,grids_size):
                player_tank.move_up()
    elif keys[pygame.K_a]:
        player_tank.direction='left'
        if tank_collide(map_data,player_tank,grids_size,height):
            if not tanks_mutual_collide(player_tank,enemy_tank_1,grids_size):
                player_tank.move_left()
    elif keys[pygame.K_s]:
        player_tank.direction='down'
        if tank_collide(map_data,player_tank,grids_size,height):
            if not tanks_mutual_collide(player_tank,enemy_tank_1,grids_size):
                player_tank.move_down()
    elif keys[pygame.K_d]:
        player_tank.direction='right'
        if tank_collide(map_data,player_tank,grids_size,height):
            if not tanks_mutual_collide(player_tank,enemy_tank_1,grids_size):
                player_tank.move_right()
    elif keys[pygame.K_j]:
        player_bullet.direction=player_tank.direction
        if player_bullet.direction=='up':
            player_bullet.pos=[player_tank.pos[0]+((grids_size//2)-(grids_size//12)),player_tank.pos[1]]
            player_bullet.exist=True
        if player_bullet.direction=='down':
            player_bullet.pos=[player_tank.pos[0]+(grids_size//2),player_tank.pos[1]+grids_size]
            player_bullet.exist=True
        if player_bullet.direction=='left':
            player_bullet.pos=[player_tank.pos[0],player_tank.pos[1]+(grids_size//2)]
            player_bullet.exist=True
        if player_bullet.direction=='right':
            player_bullet.pos=[player_tank.pos[0]+grids_size,player_tank.pos[1]+grids_size-(grids_size//2)-(grids_size//12)]
            player_bullet.exist=True
    
    player_tank.draw(screen)
    enemy_tank_1.draw(screen)
    random_move(enemy_tank_1,player_tank,map_data,grids_size,height)
    if player_bullet.exist:
        bullet_pass,map_data=bullet_collide(map_data,player_bullet,grids_size,height)
        if bullet_pass:
            if player_bullet.direction=='up':
                player_bullet.draw(screen)
                player_bullet.shoot_up()
            if player_bullet.direction=='down':
                player_bullet.draw(screen)
                player_bullet.shoot_down()
            if player_bullet.direction=='left':
                player_bullet.draw(screen)
                player_bullet.shoot_left()
            if player_bullet.direction=='right':
                player_bullet.draw(screen)
                player_bullet.shoot_right()
        else:
            player_bullet.exist=False
    map_data=map_amend(map_data,map_black_image,camp_dead_image)
    pygame.display.flip()
    clock.tick(20)
pygame.quit()