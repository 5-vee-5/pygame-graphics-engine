import pygame
import math as m
def rotate(x,y,z,rotX,rotY,rotZ):
    #x
    y,z=y*m.cos(m.radians(rotX))-z*m.sin(m.radians(rotX)),y*m.sin(m.radians(rotX))+z*m.cos(m.radians(rotX))
    #y
    x,z=x*m.cos(m.radians(rotY))+z*m.sin(m.radians(rotY)),z*m.cos(m.radians(rotY))-x*m.sin(m.radians(rotY))
    #z
    x,y=x*m.cos(m.radians(rotZ))-y*m.sin(m.radians(rotZ)),x*m.sin(m.radians(rotZ))+y*m.cos(m.radians(rotZ))
    return Point(x,y,z)
class Point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
class Triangle:
    def __init__(self,p1,p2,p3,rotX,rotY,rotZ,colour):
        self.p1=p1
        self.p2=p2
        self.p3=p3
        self.rotX=rotX
        self.rotY=rotY
        self.rotZ=rotZ
        self.colour=colour
    def zavg(self):
        return self.p1.z+self.p2.z+self.p3.z/3
class Object:
    def __init__(self,triangles,x,y,z,rotX,rotY,rotZ):
        self.triangles=triangles
        self.x=x
        self.y=y
        self.z=z
        self.rotX=rotX
        self.rotY=rotY
        self.rotZ=rotZ
class Renderer:
    def __init__(self,objectList:list[Object],screenX,screenY,camera,focalLen=1000):
        self.screenX=screenX
        self.screenY=screenY
        self.screen = pygame.Surface((self.screenX,self.screenY))
        self.running = True
        self.camera=camera
        self.focalLen=focalLen
        self.objectList=objectList
    def frame(self):
        self.screen.fill((0,0,0))
        for i in self.objectList:
            finalTriangles=[]
            for j in i.triangles:
                rotatedP1=Point(i.x+j.p1.x,i.y+j.p1.y,i.z+j.p1.z)
                rotatedP2=Point(i.x+j.p2.x,i.y+j.p2.y,i.z+j.p2.z)
                rotatedP3=Point(i.x+j.p3.x,i.y+j.p3.y,i.z+j.p3.z)
                rotatedP1=rotate(rotatedP1.x,rotatedP1.y,rotatedP1.z,i.rotX,i.rotY,i.rotZ)
                rotatedP2=rotate(rotatedP2.x,rotatedP2.y,rotatedP2.z,i.rotX,i.rotY,i.rotZ)
                rotatedP3=rotate(rotatedP3.x,rotatedP3.y,rotatedP3.z,i.rotX,i.rotY,i.rotZ)
                
                rotatedP1=Point(rotatedP1.x-self.camera.x,rotatedP1.y-self.camera.y,rotatedP1.z-self.camera.z)
                rotatedP2=Point(rotatedP2.x-self.camera.x,rotatedP2.y-self.camera.y,rotatedP2.z-self.camera.z)
                rotatedP3=Point(rotatedP3.x-self.camera.x,rotatedP3.y-self.camera.y,rotatedP3.z-self.camera.z)
                rotatedP1=rotate(rotatedP1.x,rotatedP1.y,rotatedP1.z,-self.camera.rotX,-self.camera.rotY,-self.camera.rotZ)
                rotatedP2=rotate(rotatedP2.x,rotatedP2.y,rotatedP2.z,-self.camera.rotX,-self.camera.rotY,-self.camera.rotZ)
                rotatedP3=rotate(rotatedP3.x,rotatedP3.y,rotatedP3.z,-self.camera.rotX,-self.camera.rotY,-self.camera.rotZ)
                if rotatedP1.z<0 and rotatedP2.z<0 and rotatedP3.z<0:
                    continue
                finalTriangles.append(Triangle(rotatedP1,rotatedP2,rotatedP3,0,0,0,j.colour))
                # This is close to Painter's algorithm
            for j in sorted(finalTriangles,key=Triangle.zavg,reverse=True):
                pygame.draw.polygon(self.screen,j.colour,[self.rasterise(j.p1),self.rasterise(j.p2),self.rasterise(j.p3)])
                pygame.draw.aalines(self.screen,(0,0,0),True,[self.rasterise(j.p1),self.rasterise(j.p2),self.rasterise(j.p3)])
        return self.screen
    def rasterise(self,point:Point)->tuple[float,float]:
        x=point.x
        y=point.y
        z=point.z
        if z<=1:
            z=1
        rx=(x/z)*self.focalLen+(self.screenX/2)
        ry=(y/z)*self.focalLen+(self.screenY/2)
        return (rx,ry)
