import pygame
from renderer_class import Renderer
from Actor.Camera.cameraActor_class import CameraActor
from Actor.Camera.rawCamera_class import RawCamera
from Actor.Camera.freeCamera_class import FreeCamera
from Actor.cubeActor_class import CubeActor
from Actor.healthbar_class import  HealthBar
from Actor.planeActor_class import PlaneActor
from Actor.Tanks.tank_class import Tank
from Actor.Tanks.playerTank_class import PlayerTank
from collisionManager_class import CollisionManager
import Paras

class Game:
    def __init__(self):
        self.mActors = []
        self.mIsRunning = True
        self.mRenderer=Renderer(self, Paras.WINDOWWIDTH, Paras.WINDOWHEIGHT)
        self.mCameras=[]
        self.mCameraActor=RawCamera(self)
        self.mCameraActor.mPosition.z=20
        #only for debugging
        self.mFreeCamera=FreeCamera(self)
        
        self.mPlayerTank=None
        
        #self.mPlaneActor=PlaneActor(self)
        
        self.mProjectiles=[]
        self.mEnemies=[]
        
        self.mCollisionManager=CollisionManager(self)
        
    def Initialize(self):
        self.mRenderer.Initialize()
        pygame.display.set_caption("TankWar")
        
        #HealthBar(self)
        
        self.FPSClock = pygame.time.Clock()
        
        self.LoadData()
        
    def LoadData(self):
        self.mPlayerTank=PlayerTank(self)
        #CubeActor(self)
        Tank(self)
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
            self.DisableAllCamera()
            self.mCameras[0].mActive=True
        if keyState[pygame.K_2]:
            self.DisableAllCamera()
            self.mCameras[1].mActive=True
        if keyState[pygame.K_3]:
            self.DisableAllCamera()
            self.mCameras[2].mActive=True
        if keyState[pygame.K_4]:
            self.DisableAllCamera()
            self.mCameras[3].mActive=True
        if keyState[pygame.K_5]:
            self.DisableAllCamera()
            self.mCameras[4].mActive=True
    
    def DisableAllCamera(self):
        for camera in self.mCameras:
            camera.mActive=False
    
    def Update(self):
        deltatime = self.FPSClock.get_time() / 1000.0
        for actor in self.mActors:
            if actor.mActive:
                actor.Update(deltatime)
                
        self.mCollisionManager.CheckCollision()
            
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
