import pygame
import random
import time
import pygame.freetype
pygame.freetype.init()
score = 0

class RectangleGroup():
   # RectangleGroup class providing a means to collect rectangles of a given type and operate on them as a group
   def __init__(self):
      self.items = []
      bottoms=1
   def add(self, rectInstance):
      self.items.append(rectInstance)
      self._lastCreated = rectInstance
   def remove(self,rectInstance):
      self.items.remove(rectInstance)
   def moveAll(self,dx,dy):
      for item in self.items:
         item.move_ip(dx, dy)
   def lastCreated(self):
      if self._lastCreated:
         return self._lastCreated


class BasicPlatform(pygame.Rect):
   # Platform class extending the pygame.Rect class
   # No additional properties or methods 
   def __init__(self, height, width, xcordinate, ycordinate):
      super().__init__(height, width, xcordinate, ycordinate)
      self.colour = 0, 255, 255 
      self.hasLeftScreen = False
   
class MovingPlatform(BasicPlatform):
   
   def __init__(self, height, width, xcordinate, ycordinate):
      super().__init__(height, width, xcordinate, ycordinate)
      self.isMovingUp = False
      self.isMovingDown = True
      self.colour = "yellow"
   def movePlatform(self):
      if self.isMovingDown == True:
         self.move_ip(0,1)

      if self.isMovingUp == True:
         self.move_ip(0,-1) 
      if self.y < 10:
         self.isMovingUp = False
         self.isMovingDown = True
      if self.y > 700:
         self.isMovingDown = False
         self.isMovingUp = True
      
class BouncePad(BasicPlatform):
   def __init__(self, height, width, xcordinate, ycordinate):
      super().__init__(height, width, xcordinate, ycordinate)
      self.colour = "green"

class Coin(pygame.Rect):
   def __init__(self, height, width, xcordinate, ycordinate):
      super().__init__(height, width, xcordinate, ycordinate)
      self.colour = "yellow"
   def coinCollect(self,rectInstance):
      if  self.colliderect(rectInstance):
         return True


class Character(pygame.Rect):
   # Character class extending the pygame.Rect class and providing additionam propeties and methods
   def __init__(self, height, width, xcordinate, ycordinate):
      super().__init__(height, width, xcordinate, ycordinate)     
      self.velocity = 0
      self.accelaration = 0

   def enableGravity(self):
      self.accelaration = globalaccelaration
      
   def disableGravity(self):
      self.accelaration = 0
      self.velocity = 0  
   
   def isOnGround(self):
       return self.y >= screenHeight - playerHeight
   
   def jump(self):
      self.velocity = jumpVelocity
      self.accelaration = globalaccelaration

   def applyPhysics(self):
      self.move_ip(0,self.velocity) 
      self.velocity = self.velocity + self.accelaration

   def isInContactWithTop(self,rectInstance):
      if self.velocity > 0:
         isVertAligned = abs(self.bottom - rectInstance.top) < abs(self.velocity)
      elif self.velocity == 0:
         isVertAligned = self.bottom == rectInstance.top
      else: 
         isVertAligned = False

      isHorzAligned = rectInstance.right > self.left and rectInstance.left < self.right
      return isVertAligned and isHorzAligned

   def isInContactWithBottom(self,rectInstance):
      if self.velocity < 0:
         isVertAlignedBottom = abs(self.top - rectInstance.bottom) < abs(self.velocity)
      elif self.velocity == 0:
         isVertAlignedBottom = self.top == rectInstance.bottom
      else: 
         isVertAlignedBottom = False

      isHorzAligned = rectInstance.right > self.left and rectInstance.left < self.right
      return isVertAlignedBottom and isHorzAligned

class OriginalPlatform (BasicPlatform):
   def __init__(self, height, width, xcordinate, ycordinate):
      super().__init__(height, width, xcordinate, ycordinate)
      self.originalX = self.x
   def hardReset (self):
      self.hasLeftScreen = False   
      self.x = self.originalX

def createBackground():
   bg = RectangleGroup()
   bg.add(OriginalPlatform(0,500,200,25))
   bg.add(OriginalPlatform(300,500,200,25))
   bg.add(OriginalPlatform(600,500,200,25))
   bg.add(OriginalPlatform(900,500,200,25))
   bg.add(OriginalPlatform(1200,500,200,25))
   bg.add(OriginalPlatform(1500,500,200,25))
   return bg


pygame.init()

pygame.font.init() 
font = pygame.font.SysFont('Arial', 30)
screenHeight= 780
screenWidth = 1550
playerHeight = 50
playerWidth = 50
playerx = int(screenWidth/2)
globalaccelaration = 0.075
jumpVelocity = -8
paint_mode = False
run = True
paused = False
prevPlatformHeight = 500
endOfGame = False
# initialise screen
# screen = pygame.display.set_mode((pygame.FULLSCREEN,pygame.FULLSCREEN))
# pygame.display.set_mode(FULLSCREEN)
screen = pygame.display.set_mode((780, 1550), pygame.FULLSCREEN)
# create the player
player = Character(screenWidth/2, 450, playerHeight, playerWidth)

# create the platforms and add to group

background = createBackground()

coins = RectangleGroup()
pygame.mouse.set_visible(False)

while run == True:   
   key = pygame.key.get_pressed()
   if key[pygame.K_ESCAPE] == True:
      paused = False
      # time.sleep(0.1)
      pygame.display.quit()
      pygame.quit
   
   if paused:
      key = pygame.key.get_pressed()
      if key[pygame.K_LSHIFT] and paused == True: 
         paused = False
         score = 0
         
         for item in coins.items:
            coins.remove(item)
         background = createBackground()
         player.y = 0
      
        
   else:

      if paint_mode == False:
         screen.fill((0, 0, 0))

      # draw the player
      pygame.draw.rect(screen, (255, 0, 255), player)
      pygame.draw.rect
      # IMPORTANT - enable gravity on each loop and let alogithm decide whether to turn it off again
      player.enableGravity()

      # draw the background and check for character contact
      for platform in background.items:
         pygame.draw.rect(screen, platform.colour, platform) 
         if isinstance(platform,MovingPlatform):
               platform.movePlatform()
         if player.isInContactWithTop(platform):
            if isinstance(platform,BouncePad):
               player.bottom = platform.top
               player.velocity = -10
            elif isinstance(platform,MovingPlatform):
               player.bottom = platform.top
               player.disableGravity()
               if platform.isMovingUp:
                  player.move_ip(0,-1)
               if platform.isMovingDown:
                  player.move_ip(0,1)
            else: 
               player.bottom = platform.top
               player.disableGravity()
         
         elif player.isInContactWithBottom(platform):
            if isinstance(platform,BouncePad):
               player.top = platform.bottom
               player.velocity = 0
            
            elif isinstance(platform,MovingPlatform):
               player.velocity = 0
               player.top = platform.bottom
            else:
               player.top = platform.bottom
               player.velocity = 0
         
      # check for ground contact
      
      
      
      
      if player.isOnGround():   
         player.disableGravity()
         player.move_ip(0, screenHeight - player.height - player.y)
         text_surface = pygame.font.SysFont('Arial', 300).render('GAME OVER!!!', False, (255, 0, 0))
         screen.blit(text_surface, (0,0))
         text_surface = pygame.font.SysFont('Arial', 70).render("Press shift to restart", False, (255, 0, 0))
         screen.blit(text_surface, (500,400))
         # text_surface = font.render("(P.S: these terms and conditions are legaly binding)", False, (255, 0, 0))
         # screen.blit(text_surface, (0,600))
         paused = True
         
         
      
      
      for platform in background.items:
         if platform.right == 0 and platform.hasLeftScreen == False:
            lastY = background.lastCreated().y
            newPlatformY = random.randint(lastY - 200, lastY + 200)
            if newPlatformY < 0:
               newPlatformY = newPlatformY + 300
            if newPlatformY > screenHeight:
               newPlatformY = newPlatformY - 300
            platformVariety = random.randint(1,10)
            if platformVariety == 10 or platformVariety == 9:
               background.add(BouncePad(screenWidth,newPlatformY,200,25))
            elif platformVariety == 8 or platformVariety == 7 or platformVariety == 6:
               background.add(BasicPlatform(screenWidth,newPlatformY,200,25))
               coins.add(Coin(screenWidth+100, newPlatformY - 30,20,20))
            elif platformVariety == 5 or platformVariety == 4:
               background.add(MovingPlatform(screenWidth,newPlatformY,200,25))  
            else:
               background.add(BasicPlatform(screenWidth,newPlatformY,200,25))
            platform.hasLeftScreen = True
            
      for coin in coins.items:
         pygame.draw.rect(screen, coin.colour, coin)
         if coin.coinCollect(player):
            score = score + 10
            coin.y = -20
            coins.remove(coin)
             
      # font = pygame.font.SysFont('Arial', 30, bold=True)       
      # font.render(screen, (40, 350), "Black", (0, 255, 255))
      
      text_surface = font.render('score:'+ str(score), False, (0, 255, 255))
      screen.blit(text_surface, (10,0))

      
      # Check for keypress
      key = pygame.key.get_pressed()
      if key[pygame.K_SPACE] and player.accelaration==0 :
         player.jump()
      if key[pygame.K_p] == True:
         paint_mode=True
      if key[pygame.K_c]:
         paint_mode=False
      if key[pygame.K_a] == True:
         background.moveAll(1,0)
         coins.moveAll(1,0)
      if key[pygame.K_d] == True:
         background.moveAll(-1,0)
         coins.moveAll(-1,0)
      if key[pygame.K_LSHIFT] and paused == True: 
         background = createBackground()
      
      # Update physics
      # time.sleep(0.005)
      player.applyPhysics() 
      pygame.display.update()

   
      
      #update the display
   # for platform in background.items:
   #    key = pygame.key.get_pressed()
   #    if key[pygame.K_SPACE] and paused == True: 
   #       if isinstance(platform,OriginalPlatform):
   #          paused = False
   #          platform.hardReset()  
   #          player.y = 0   
   #       else: 
   #          background.remove(platform)
   for event in pygame.event.get():
      
      # if event.type == pygame.MOUSEBUTTONDOWN and 1==1:
      #          if pygame.mouse.get_pressed()[0]: 
      #             paused = True
      #          elif pygame.mouse.get_pressed()[2]: 
      #            paused = False
      
         
         print("bums")
   

#stop the code when the loop is broken
