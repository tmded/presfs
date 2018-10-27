#1
import pygame
from pygame.locals import *
import math as maths
import math
import random
import time as time1

#2
pygame.init()
width, height = (640, 480)#(3200, 1800)#(640, 480)
keys = [False, False, False, False]
playerpos=[100,100]
win = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
acc=[0,0]
arrows=[]
badtimer=100
badtimer1=0
badguys=[[1920,100]]
healthvalue=194
ticks_to_ignore = 0 
pygame.mixer.init()

#3
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
player_sprite = pygame.image.load("resources/images/hampster.png")
arrow = pygame.image.load("resources/images/poop.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg = badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/bensound-buddy.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
#4
running=1
exitcode=0
while 1:
	while running:
		if ticks_to_ignore > 0: 
			ticks_to_ignore -= 1
		badtimer-=1
		#5
		win.fill(1)
		#6
		for x in range (100+1):
			for y in range (100+1):
				win.blit(grass,(x*100,y*100))
		win.blit(castle,(0,30))
		win.blit(castle,(0,135))
		win.blit(castle,(0,240))
		win.blit(castle,(0,345))
		position=pygame.mouse.get_pos()
		angle=maths.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
		playerrot = pygame.transform.rotate(player_sprite, 360-angle*57.29)
		playerpos1=(playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
		for bullet in arrows:
			index=0
			velx=maths.cos(bullet[0])*20
			vely=maths.sin(bullet[0])*20
			bullet[1]+=velx
			bullet[2]+=vely
			if bullet[1]<-64 or bullet[1]>width or bullet[2]<-64 or bullet[2]>height:
				arrows.pop(index1)
			index+=1
			for projectile in arrows:
				arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
				win.blit(arrow1, (projectile[1],projectile[2]))
		if badtimer==0:
			badguys.append([1920, random.randint(50,310)])
			badtimer=50-(badtimer1*1)
			if badtimer1>=15:
				badtimer1=10
			else:
				badtimer1+=3
		index=0
		for badguy in badguys:
			if badguy[0]<-64:
				badguys.pop(index)
			badguy[0]-=7
			badrect=pygame.Rect(badguyimg.get_rect())
			badrect.top=badguy[1]
			badrect.left=badguy[0]
			if badrect.left<64:
				hit.play()
				healthvalue -= random.randint(5,20)
				badguys.pop(index1)
			index1=0
			for bullet in arrows:
				bullrect=pygame.Rect(arrow.get_rect())
				bullrect.left=bullet[1]
				bullrect.top=bullet[2]
				if badrect.colliderect(bullrect):
					enemy.play()
					acc[0]+=1
					badguys.pop(index1)
					arrows.pop(index1)
				index+=1
		win.blit(healthbar,(5,5))
		for health1 in range (healthvalue):
			win.blit(health, (health1+8,8))
		for badguy in badguys:
			win.blit(badguyimg, badguy)
			
		win.blit(playerrot,playerpos1)
		font = pygame.font.Font(None, 24)
		survivedtext = font.render(str(maths.floor((90000-pygame.time.get_ticks())/60000))+":"+str(maths.floor((90000-pygame.time.get_ticks())/1000%60)).zfill(2), True, (0,0,0))
		textRect = survivedtext.get_rect()
		textRect.topright=[635,5]
		win.blit(survivedtext, textRect)
		#7
		pygame.display.flip()
		#8
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key==K_w:
					keys[0]=True
				if event.key==K_a:
					keys[1]=True
				if event.key==K_s:
					keys[2]=True
				if event.key==K_d:
					keys[3]=True
			if event.type == pygame.KEYUP:
				if event.key==pygame.K_w:
					keys[0]=False
				if event.key==pygame.K_a:
					keys[1]=False
				if event.key==pygame.K_s:
					keys[2]=False
				if event.key==pygame.K_d:
					keys[3]=False
			if event.type == pygame.MOUSEBUTTONDOWN and ticks_to_ignore == 0: 
				shoot.play()
				ticks_to_ignore = 15
				position=pygame.mouse.get_pos()
				acc[1]+=1
				arrows.append([maths.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32]) 
			if event.type == pygame.QUIT:
				break
				pygame.quit()
				exit(0)
		if keys[0]:
			playerpos[1]-=10
		elif keys[2]:
			playerpos[1]+=10
		if keys[1]:
			playerpos[0]-=10
		elif keys[3]:
			playerpos[0]+=10
		if pygame.time.get_ticks()>=90000:
			running=0
			exitcode=1
		if healthvalue<=0:
			running=0
			exitcode=0
		if acc[1]!=0:
			accuracy=acc[0]*1.0/acc[1]*100
		else:
			accuracy=0
	if exitcode==0:
		pygame.font.init()
		font =pygame.font.Font(None,24)
		text=font.render("Accuracy: "+str(maths.floor(accuracy))+"%", True, (0,255,0))
		textRect = text.get_rect()
		textRect.centerx = win.get_rect().centerx
		textRect.centery = win.get_rect().centery
		win.blit(gameover, (0,0))
		win.blit(text, textRect)
	else:
		pygame.font.init()
		font = pygame.font.Font(None, 24)
		text = font.render("Accuracy: "+str(maths.floor(accuracy))+"%", True, (0,255,0))
		textRect = text.get_rect()
		textRect.centerx = win.get_rect().centerx
		textRect.centery = win.get_rect().centery+24
		win.blit(youwin, (0,0))
		win.blit(text, textRect)
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
		pygame.display.flip()

	break
