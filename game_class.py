import pygame
from renderer_class import Renderer
from Actor.Camera.cameraActor_class import CameraActor
from Actor.Camera.rawCamera_class import RawCamera
from Actor.Camera.freeCamera_class import FreeCamera
from Actor.cubeActor_class import CubeActor
from Actor.healthbar_class import  HealthBar
from Actor.planeActor_class import PlaneActor
import Paras

class Game:
    def __init__(self):
        self.mActors = []
        self.mIsRunning = True
        self.mRenderer=Renderer(self, Paras.WINDOWWIDTH, Paras.WINDOWHEIGHT)
        self.mCameraActor=RawCamera(self)
        #only for debugging
        self.mFreeCamera=FreeCamera(self)
        self.mFreeCamera.mActive=False
        
        self.mCube=None
        
        #self.mPlaneActor=PlaneActor(self)
        
        self.mProjectiles=[]
        self.mEnemies=[]
        
    def Initialize(self):
        self.mRenderer.Initialize()
        pygame.display.set_caption("TankWar")
        
        #HealthBar(self)
        
        self.FPSClock = pygame.time.Clock()
        
        self.LoadData()
        
    def LoadData(self):
        self.mCube=CubeActor(self)
        PlaneActor(self)

    def Loop(self):
        while self.mIsRunning:
            self.ProcessInput()
            self.Update()
            self.Draw()
        
    def ProcessInput(self):
        keyState = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.mIsRunning = False
        
        for actor in self.mActors:
            if actor.mActive:
                actor.ProcessInput(keyState)
            
        #only for debugging
        if keyState[pygame.K_1]:
            self.mCameraActor.mActive=False
            self.mFreeCamera.mActive=True
        if keyState[pygame.K_2]:
            self.mCameraActor.mActive=True
            self.mFreeCamera.mActive=False
    
    def Update(self):
        deltatime = self.FPSClock.get_time() / 1000.0
        for actor in self.mActors:
            if actor.mActive:
                actor.Update(deltatime)
            
        # print(self.mCameraActor.mRotation)
            
        self.FPSClock.tick(Paras.FPS)
        
    def Draw(self):
       self.mRenderer.Draw()
    
    def AddActor(self, actor):
        self.mActors.append(actor)

    def RemoveActor(self, actor):
        try:
            self.mActors.remove(actor)
        except:
            pass
