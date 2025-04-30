import pygame
from renderer_class import Renderer
from Actor.skyBox_class import SkyBox
from Actor.skyDome_class import SkyDome
from Actor.cubeActor_class import CubeActor
from Actor.Obstacles.block_class import Block
from Actor.healthbar_class import  HealthBar
from Actor.planeActor_class import PlaneActor
from Actor.Tanks.enemyTank_class import EnemyTank
from Actor.Tanks.playerTank_class import PlayerTank
from collisionManager_class import CollisionManager
from mapGenerator_class import MapGenerator
from gameMap_class import GameMap
from Lights.directionalLight_class import DirectionalLight
from enemyGenerator_class import EnemyGenerator
import glm
import Paras

class Game:
    def __init__(self):
        self.mActors = []
        self.mIsRunning = True
        self.mRenderer=Renderer(self, Paras.WINDOWWIDTH, Paras.WINDOWHEIGHT)
        self.mAmbientLight=None
        self.mDirectionalLight=None
        self.mCameras=[]
        # self.mCameraActor=RawCamera(self)
        # self.mCameraActor.mPosition.z=20
        # #only for debugging
        # self.mFreeCamera=FreeCamera(self)
        
        self.mPlayerTank=None
        
        self.mScore=0
        self.mEnemyCount=0
        self.mEnemyGenerator=EnemyGenerator(self)
        
        #self.mPlaneActor=PlaneActor(self)
        
        self.mProjectiles=[]
        self.mEnemies=[]
        self.mObstacles=[]
        
        self.mCollisionManager=CollisionManager(self)
        
        self.mGameMap=None
        
    def Initialize(self):
        
        self.mRenderer.Initialize()
        pygame.display.set_caption("TankWar")
        
        #HealthBar(self)
        
        self.FPSClock = pygame.time.Clock()
        
        self.LoadData()
        
    def LoadData(self):
    
        mp=MapGenerator.generate_map(3,3,3)
        self.mEnemyCount=5
        self.mGameMap=GameMap(mp)
        self.ConstructMap(mp)
        
        self.mSkyBox=SkyDome(self)
        self.mSkyBox.mPosition=self.mGameMap.GetCenter()
        scale=max(self.mGameMap.GetMapWidth(), self.mGameMap.GetMapHeight())
        self.mSkyBox.mScale=1.3*scale
        
        self.mAmbientLight=glm.vec3(0.01,0.01,0.01)
        
        self.mDirectionalLight=DirectionalLight(self)
        self.mDirectionalLight.mPosition=self.mGameMap.GetCenter()+glm.vec3(0,0,10000)
        self.mDirectionalLight.mDiffuseColor = glm.vec3(3.0, 1.9, 3.5)
        self.mDirectionalLight.mSpecColor   = glm.vec3(3.2, 2.0, 3.8)

        self.mDirectionalLight.mDirection = glm.vec3(0.5, -1.0, -1)

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
            
        # #only for debugging
        # if keyState[pygame.K_1]:
        #     self.DisableAllCamera()
        #     self.mCameras[0].mActive=True
        # if keyState[pygame.K_2]:
        #     self.DisableAllCamera()
        #     self.mCameras[1].mActive=True
        # if keyState[pygame.K_3]:
        #     self.DisableAllCamera()
        #     self.mCameras[2].mActive=True
        # if keyState[pygame.K_4]:
        #     self.DisableAllCamera()
        #     self.mCameras[3].mActive=True
        # if keyState[pygame.K_5]:
        #     self.DisableAllCamera()
        #     self.mCameras[4].mActive=True
    
    def DisableAllCamera(self):
        for camera in self.mCameras:
            camera.mActive=False
    
    def Update(self):
        deltatime = self.FPSClock.get_time() / 1000.0

        self.mEnemyGenerator.GenerateNewEnemy()
        
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
    def ConstructMap(self, map):
        width=len(map)
        height=len(map[0])
        
        px=500
        py=500
        for x in range(width):
            for y in range(height):
                pa=PlaneActor(self)
                pa.mPosition=glm.vec3(px, py, 0)
                
                if map[x][y]=='@':
                    from AI.StateMachine.States.enemyStates import EnemyWanderState
                    from AI.StateMachine.States.enemyStates import EnemyAttendState
                    from AI.StateMachine.States.enemyStates import EnemyDefaultState
                    ea=EnemyTank(self)
                    ea.mPosition=glm.vec3(px+100, py+100, 15)
                    ea.mStateMachine.ChangeState(EnemyDefaultState.get_instance())
                if map[x][y]=='#':
                    oe=Block(self)
                    oe.mPosition=glm.vec3(px, py, 50)
                    pass
                if map[x][y]=='$':
                    pt=PlayerTank(self)
                    pt.mPosition=glm.vec3(px, py, 15)
                    self.mPlayerTank=pt
                
                py+=1000
            px+=1000
            py=500