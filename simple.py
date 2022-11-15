from math import *
from time import *
from random import *
from os import *
import pygame as pg



import pygame
pygame.init()
clock = pygame.time.Clock()

WIDTH=1920/2
HEIGHT=1080/2

fov = 1

my_font = pygame.font.SysFont('Comic Sans MS', 50)

tft = pygame.display.set_mode([WIDTH, HEIGHT])

def fill_rect(a, b, c, d, color):
  global tft
  pygame.draw.rect(tft, color, pygame.Rect(a, b, c, d))

def color(a, b, c):
  return (a, b, c)

def fill_polygon(coords, color):
  global tft
  if(coords[0][0]>-1000 and coords[0][0]<WIDTH+1000 and coords[0][1]>-2000 and coords[0][1]<HEIGHT+1000):
    pygame.draw.polygon(tft, color, coords)

def get_pixel(x, y):
  return tft.get_at((x, y))

def draw_string(string, x, y):
  text_surface = my_font.render(string, False, (0, 0, 0))
  tft.blit(text_surface, (x,y))



px=0
py=0
pz=0

rx=0.2392526803190927
ry=radians(180)
rz=0

def distance3D(x,y,z):
  global px, py, pz

  return sqrt((px-x)**2+(y-py)**2+(pz-z)**2)

def rotate(x,y,r):
  r*=-1
  cosR=cos(r)
  sinR=sin(r)
  a2=[0,0]
  a2[0]=x*cosR-y*sinR
  a2[1]=y*cosR+x*sinR
      
  return a2


def getPoint2D(pointX, pointZ, pointY,ignore=False):
    global px, py, pz, rx, ry, rz, fov
    pp=rotate(0,20,-ry)
    camX=px-pp[0]
    camY=py-10
    camZ=pz-pp[1]
    
    camRX=rx
    camRY=ry
    camRZ=rz

    if(ignore==True):
      rr=rotate(pointX,pointZ,-ry+radians(180))
      pointX=px-rr[0]
      pointY=py-pointY
      pointZ=pz-rr[1]

    pX = pointX - camX
    pY = pointY - camY
    pZ = pointZ - camZ

    cosX = cos(camRX)
    sinX = sin(camRX)
    cosY = cos(camRY)
    sinY = sin(camRY)
    cosZ = cos(camRZ)
    sinZ = sin(camRZ)

    # rotate Y
    pX2=pX
    pX=cosY*pX2+sinY*pZ
    pZ=-sinY*pX2+cosY*pZ
    
    pY2=pY
    pX2=pX
    
    # rotate X
    pY2=pY
    pY=cosX*pY2-sinX*pZ
    pZ=sinX*pY2+cosX*pZ
    
    if pZ <= 0:
        return None

    pY2=pY
    pX2=pX
    
    # Perspective projection
    f = WIDTH*fov / pZ
    pX2 = pX * f
    pY2 = pY * f

    pX2 += WIDTH / 2
    pY2 += HEIGHT / 2
    return [int(pX2), int(pY2)]

def distance3D(x,y,z):
  global px, py, pz
  return sqrt((px-x)**2+(y-py)**2+(pz-z)**2)

map=[
[[0,8],[2,8]],
[[0,15],[2,14]],
[[1,17],[2.25,14.75]],
[[3,17],[3,15]],
[[7,17],[7,15]],
[[11,16],[10,14]],
[[14,12],[12,12]],
[[14,9],[12,9]],
[[13,6],[11,6]],
[[13,2],[11,3]],
[[10,0],[10,2]],
[[6,1],[8,2]],
[[4,3],[5,5]],
[[1,5],[3,6]],
[[0,8],[2,8]]
]

poly=[]

lsx,lsy=[0,0],[0,0]

def addRoad(p1,p2):
  global lsx,lsy
  poly.append([
  [lsx[0]*2,lsy[0]*2,0],
  [lsx[1]*2,lsy[1]*2,0],
  [p2[0]*2,p2[1]*2,0],
  [p1[0]*2,p1[1]*2,0],
  color(170,132,85)])
    
  lsx=p1[0],p2[0]
  lsy=p1[1],p2[1]

tree=[
[[0.2, 0.2, 0], [-0.2, 0.2, 0], [-0.2, 0.2, 1.5], [0.2, 0.2, 1.5]],
[[0.2, 0.2, 0], [0.2, -0.2, 0], [0.2, -0.2, 1.5], [0.2, 0.2, 1.5]],
[[-0.2, 0.2, 0], [-0.2, -0.2, 0], [-0.2, -0.2, 1.5], [-0.2, 0.2, 1.5]],
[[-0.2, -0.2, 0], [0.2, -0.2, 0], [0.2, -0.2, 1.5], [-0.2, -0.2, 1.5]],


[[0,3,1.5], [2.5,1.5,1.5], [2.5,-1.5,1.5], [0,-3,1.5]],
[[0,-3,1.5], [-2.5,-1.5,1.5], [-2.5,1.5,1.5], [0,3,1.5]],

[[2.5,1.5,1.5], [2.5,-1.5,1.5], [0.5, -0.3, 3.5], [0.5, 0.3, 3.5]],
[[2.5,-1.5,1.5], [0,-3,1.5], [0, -0.6, 3.5], [0.5, -0.3, 3.5]],
[[0,-3,1.5], [-2.5,-1.5,1.5], [-0.5, -0.3, 3.5], [0, -0.6, 3.5]],
[[-2.5,-1.5,1.5], [-2.5,1.5,1.5], [-0.5, 0.3, 3.5], [-0.5, -0.3, 3.5]],
[[-2.5,1.5,1.5], [0,3,1.5], [0, 0.6, 3.5], [-0.5, 0.3, 3.5]],
[[0,3,1.5], [2.5,1.5,1.5], [0.5, 0.3, 3.5], [0, 0.6, 3.5]],


[[0, 2, 3.5], [1.7,1,3.5], [1.7,-1,3.5], [0, -2, 3.5]],
[[0, -2, 3.5], [-1.7,-1,3.5], [-1.7,1,3.5], [0, 2, 3.5]],

[[0, 2, 3.5], [1.7,1,3.5], [0.3, 0.2, 5.5], [0, 0.4, 5.5]],
[[1.7,1,3.5], [1.7,-1,3.5], [0.3, -0.2, 5.5], [0.3, 0.2, 5.5]],
[[1.7,-1,3.5], [0, -2, 3.5], [0, -0.4, 5.5], [0.3, -0.2, 5.5]],
[[0, -2, 3.5], [-1.7,-1,3.5], [-0.3, -0.2, 5.5], [0, -0.4, 5.5]],
[[-1.7,-1,3.5], [-1.7,1,3.5], [-0.3, 0.2, 5.5], [-0.3, -0.2, 5.5]],
[[-1.7,1,3.5], [0, 2, 3.5], [0, 0.4, 5.5], [-0.3, 0.2, 5.5]],


[[0, 1.3, 5.5], [1.1,0.8 , 5.5], [1.1,-0.8 , 5.5], [0, -1.3, 5.5]],
[[0, 1.3, 5.5], [-1.1,0.8 , 5.5], [-1.1,-0.8 , 5.5], [0, -1.3, 5.5]],

[[0, 0, 8], [-1.1,-0.8 , 5.5], [0, -1.3, 5.5], [0, 0, 8]],
[[0, 0, 8], [-1.1,0.8 , 5.5], [-1.1,-0.8 , 5.5], [0, 0, 8]],
[[0, 0, 8], [0, 1.3, 5.5], [-1.1,0.8 , 5.5], [0, 0, 8]],
[[0, 0, 8], [1.1,0.8 , 5.5], [0, 1.3, 5.5], [0, 0, 8]],
[[0, 0, 8], [1.1,-0.8 , 5.5], [1.1,0.8 , 5.5], [0, 0, 8]],
[[0, 0, 8], [0, -1.3, 5.5], [1.1,-0.8 , 5.5], [0, 0, 8]]
]

class auto_gen:
  def __init__(self):
    self.x=0
    self.y=0
    self.r=180
  
  def update(self):
    global poly, tree
    print("update")
    
    leng=6/2
    larg=6
    
    self.r+=randint(-20,20)/2
    
    p1=rotate(0,larg/2,radians(-90))
    p2=rotate(0,larg/2,radians(+90))
    
    p1=rotate(p1[0]+leng,p1[1],radians(self.r))
    p2=rotate(p2[0]+leng,p2[1],radians(self.r))
        
    p1[0]+=self.x
    p2[0]+=self.x
    p1[1]+=self.y
    p2[1]+=self.y
    
    self.x+=rotate(0,leng,radians(self.r))[0]
    self.y+=rotate(0,leng,radians(self.r))[1]

    for n in range(1):
      rx,ry=randint(-300,300),randint(-300,300)
      rfx,rfy=(p1[0]+p2[0])/2,(p1[1]+p2[1])/2


      for i in tree:
        poly.append([
        [rfx*2+rx+i[0][0], rfy*2+ry+i[0][1], -i[0][2]],
        [rfx*2+rx+i[1][0], rfy*2+ry+i[1][1], -i[1][2]],
        [rfx*2+rx+i[2][0], rfy*2+ry+i[2][1], -i[2][2]],
        [rfx*2+rx+i[3][0], rfy*2+ry+i[3][1], -i[3][2]],
        color(randint(0,10),randint(200,255),randint(0,10))])

    addRoad(p1,p2)
    
gen=auto_gen()

carPoly=[
# front bottom
[[0.999343, 4.15361, -0.827138], [1.82491 , 3.37785, -0.827138], [1.71353, 3.38017, 0.067278], [0.859144, 4.15361, 0.039826]],
[[0.859144, 4.15361, 0.039826], [0.999343, 4.15361, -0.827138], [-0.009457, 4.15361, -0.827138], [-0.009457, 4.15361, 0.039826]],
[[-0.009457, 4.15361, 0.039826], [-0.009457, 4.15361, -0.827138], [-1.01825, 4.15361, -0.827138], [-0.878057, 4.15361, 0.039826]],
[[-0.878057, 4.15361, 0.039826], [-1.01825, 4.15361, -0.827138], [-1.84382, 3.37785, -0.827138], [-1.73244, 3.38017, 0.067278]],

# left bottom
[[-1.73244, 3.38017, 0.067278], [-1.84382, 3.37785, -0.827138], [-1.99238, 0.405449, 0.172862], [-1.99238, 0.405449, -0.827138]],
[[-1.99238, 0.405449, -0.827138], [-1.99238, 0.405449, 0.172862], [-1.99238, -3.34271, 0.172862], [-1.99238, -3.34271, -0.827138]],

# back bottom
[[-1.99238, -3.34271, -0.827138], [-1.99238, -3.34271, 0.172862], [1.97347, -3.34271, 0.172862], [1.97347, -3.34271, -0.827138]],

# right bottom
[[1.97347, -3.34271, -0.827138], [1.97347, -3.34271, 0.172862], [1.97347, 0.405449, 0.172862], [1.97347, 0.405449, -0.827138]],
[[1.97347, 0.405449, -0.827138], [1.97347, 0.405449, 0.172862], [1.71353, 3.38017, 0.067278], [1.82491, 3.37785, -0.827138]],

# bottom
[[1.97347, -3.34271, -0.827138], [-1.99238, -3.34271, -0.827138], [-1.84382, 3.37785, -0.827138], [1.82491, 3.37785, -0.827138]],
[[1.82491, 3.37785, -0.827138], [-1.84382, 3.37785, -0.827138], [-1.01825, 4.15361, -0.827138], [0.999343, 4.15361, -0.827138]]
]

for i in carPoly:
  i.append((200+randint(-30, 30),50+randint(-30, 30),50+randint(-30, 30)))

derape=False

calcfps=11
factorfps=4
pcfps=calcfps*factorfps

def render():
  global poly,px,py,pz,ry,derape
  
  h_s=getPoint2D(rotate(0,100000,-ry)[0],rotate(0,100000,-ry)[1],0)[1]
  fill_rect(0,0,WIDTH,h_s,color(200,200,255))
  fill_rect(0,h_s,WIDTH,HEIGHT-h_s,color(88,41,0))
  co1, co2, co3, co4 = 0,0,0,0
  for t in reversed(poly):
    co1=getPoint2D(t[0][0],t[0][1],t[0][2])
    co2=getPoint2D(t[1][0],t[1][1],t[1][2])
    co3=getPoint2D(t[2][0],t[2][1],t[2][2])
    co4=getPoint2D(t[3][0],t[3][1],t[3][2])
    try:
      fill_polygon([(co1),(co2),(co3),(co4)],t[4])
    except:
      pass
  
  co0=getPoint2D(0,0,0,True)
  
  try:
    if(co0!=None and get_pixel(co0[0],co0[1])!=(170,132,85)):
      derape=True
    else:
      derape=False
  except:
    pass
  for t in carPoly:
    co1=getPoint2D(t[0][0],t[0][1],t[0][2],True)
    co2=getPoint2D(t[1][0],t[1][1],t[1][2],True)
    co3=getPoint2D(t[2][0],t[2][1],t[2][2],True)
    co4=getPoint2D(t[3][0],t[3][1],t[3][2],True)
    try:
      fill_polygon([(co1),(co2),(co3),(co4)],t[4])
    except:
      pass
      
reload=1

speed=0
mspeed=0

generate_len=150
#pygame.mouse.set_visible(False)

while(1):
  if(speed>mspeed):
    mspeed=speed
  print(speed*20)

  while(len(poly)==0 or distance3D(poly[len(poly)-1][0][0],poly[len(poly)-1][0][2],poly[len(poly)-1][0][1])<generate_len-10):
    gen.update()
  while(len(poly)!=0 and distance3D(poly[0][0][0],poly[0][0][2],poly[0][0][1])>generate_len):
    del poly[0]
  
  speed-=0.02/factorfps
  
  if(derape):
    if(speed*20>20):
      speed/=1+0.1/factorfps
  
  if(speed<0.03/factorfps and speed>-0.03/factorfps):
    speed=0

  keys=[]
  keys=pygame.key.get_pressed()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit(); exit();
  pygame.event.get()

  if(pygame.mouse.get_pressed()[0]):
    ry+=pygame.mouse.get_rel()[0]/1000
  else:
    pygame.mouse.set_pos([WIDTH/2, HEIGHT/2])
    pygame.mouse.get_rel()

  if(keys[pygame.K_UP]):
    fov=1.1
    speed+=0.05/factorfps
  if(keys[pygame.K_DOWN]):
    speed/=1+0.1/factorfps
  if(keys[pygame.K_RIGHT]):
    ry-=radians(0.8*speed/factorfps)
    speed/=1+0.01/factorfps
    reload=1
  if(keys[pygame.K_LEFT]):
    ry+=radians(0.8*speed/factorfps)
    speed/=1+0.01/factorfps
    reload=1
  if(keys[pygame.K_PLUS]):
    py-=0.5
    reload=1
  if(keys[pygame.K_MINUS]):
    py+=0.5
    reload=1
  if(keys[pygame.K_KP6]):
    ry-=radians(0.8*speed/factorfps)
    speed/=1+0.01/factorfps
    reload=1
  if(keys[pygame.K_KP4]):
    ry+=radians(0.8*speed/factorfps)
    speed/=1+0.01/factorfps
    reload=1
  if(keys[pygame.K_KP8]):
      rx-=radians(2)
      reload=1
  if(keys[pygame.K_KP2]):
      rx+=radians(2)
      reload=1
  if(speed!=0):
    mvt=rotate(speed, 0, ry)
    pz+=mvt[0]/factorfps
    px+=mvt[1]/factorfps
    reload=1
  if(reload==1):
    render()
    draw_string(str(speed*20)[:4]+"km/h",0,0)
    draw_string("max: "+str(mspeed*20)[:4]+"km/h",0,30)

    R=70
    w=10
    xx=WIDTH-80
    pygame.draw.circle(tft, (0,0,0), (xx, 80), R, w)
    pp=rotate(-70, 0, radians(-speed*20))
    pygame.draw.line(tft, (255,100,0), (xx, 80), (xx+pp[0], 80+pp[1]))

    pygame.display.update()
    fov=1

    reload=0
  clock.tick(pcfps)
  pygame.event.pump()
