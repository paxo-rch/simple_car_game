from math import *
from kandinsky import *
from ion import *
from time import *
from random import *
from os import *

px=0
py=0
pz=0

rx=0
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
    global px, py, pz, rx, ry, rz
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
    f = 320 / pZ
    pX2 = pX * f
    pY2 = pY * f

    pX2 += 320 / 2
    pY2 += 240 / 2
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

class auto_gen:
  def __init__(self):
    self.x=0
    self.y=0
    self.r=180
  
  def update(self):
    global poly
    print("update")
    
    leng=10
    larg=6
    
    self.r+=randint(-20,20)
    
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

    rx,ry=randint(-30,30),randint(-30,30)
    rfx,rfy=(p1[0]+p2[0])/2,(p1[1]+p2[1])/2
    poly.append([
    [rfx*2-0.5+rx, rfy*2+ry, 0],
    [rfx*2+rx, rfy*2-0.5+ry, 0],
    [rfx*2+0.5+rx, rfy*2+ry, 0],
    [rfx*2+rx, rfy*2+ry, -3],
    color(randint(0,10),randint(200,255),randint(0,10))])

    addRoad(p1,p2)
    
gen=auto_gen()

carPoly=[
[[-0.5,1,2],[0.5,1,2],[1,-1,2],[-1,-1,2]],
[[-1,-1,2],[1,-1,2],[0.5,-1,0.5],[-0.5,-1,0.5]]]

derape=False

def render():
  global poly,px,py,pz,ry,derape
  
  h_s=getPoint2D(rotate(0,100000000,-ry)[0],rotate(0,100000000,-ry)[1],0)[1]
  fill_rect(0,0,320,h_s,color(200,200,255))
  fill_rect(0,h_s,320,240-h_s,color(88,41,0))
  
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
  
  if(co0!=None and get_pixel(co0[0],co0[1])!=(168, 132, 80)):
    derape=True
  else:
    derape=False

  for t in carPoly:
    co1=getPoint2D(t[0][0],t[0][1],t[0][2],True)
    co2=getPoint2D(t[1][0],t[1][1],t[1][2],True)
    co3=getPoint2D(t[2][0],t[2][1],t[2][2],True)
    co4=getPoint2D(t[3][0],t[3][1],t[3][2],True)
    try:
      fill_polygon([(co1),(co2),(co3),(co4)],color(200,50,50))
    except:
      pass
      
reload=1

speed=0
mspeed=0

generate_len=50
ch=0

while(1):
  ch=monotonic()
  if(speed>mspeed):
    mspeed=speed
  print(len(poly))
  while(len(poly)==0 or distance3D(poly[len(poly)-1][0][0],poly[len(poly)-1][0][2],poly[len(poly)-1][0][1])<generate_len-10):
    gen.update()
  while(len(poly)!=0 and distance3D(poly[0][0][0],poly[0][0][2],poly[0][0][1])>generate_len):
    del poly[0]
  
  speed-=0.02
    
  if(derape):
    if(speed*20>20):
      speed/=1.1
  
  if(speed<0.03 and speed>-0.03):
    speed=0
  if(keydown(KEY_UP)):
    speed+=0.05
    """mvt=rotate(0.3, 0, ry)
    pz+=mvt[0]
    px+=mvt[1]
    reload=1"""
  if(keydown(KEY_DOWN)):
    speed/=1.1
    """mvt=rotate(-0.1, 0, ry)
    pz+=mvt[0]
    px+=mvt[1]
    reload=1"""
  if(keydown(KEY_RIGHT)):
    mvt=rotate(0, 0.1, ry)
    pz+=mvt[0]
    px+=mvt[1]
    reload=1
    speed/=1.03
  if(keydown(KEY_LEFT)):
    mvt=rotate(0, -0.1, ry)
    pz+=mvt[0]
    px+=mvt[1]
    reload=1
    speed/=1.03
  if(keydown(KEY_PLUS)):
    py-=0.5
    reload=1
  if(keydown(KEY_MINUS)):
    py+=0.5
    reload=1
  if(keydown(KEY_SIX)):
    ry-=radians(0.8*speed)
    speed/=1.01
    reload=1
  if(keydown(KEY_FOUR)):
    ry+=radians(0.8*speed)
    speed/=1.01
    reload=1
  if(keydown(KEY_EIGHT)):
      rx-=radians(2)
      reload=1
  if(keydown(KEY_TWO)):
      rx+=radians(2)
      reload=1
  if(speed!=0):
    mvt=rotate(speed, 0, ry)
    pz+=mvt[0]
    px+=mvt[1]
    reload=1
  if(reload==1):
    render()
    draw_string(str(speed*20)[:4],0,0)
    draw_string(str(mspeed*20)[:4],0,30)
    reload=0
  print(1/(monotonic()-ch))
