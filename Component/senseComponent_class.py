from Component.component_class import Component


#Use for AI to sense the Player
#Sensation include aural and visual
#Fire will cause an aural sense
class SenseComponent(Component):
    def __init__(self, owner, updateOrder=0):
        super().__init__(owner, updateOrder)
        self.mIsSensed=False
        
    #Must update after statemachine
    def Update(self, deltatime):
        super().Update(deltatime)
        self.mIsSensed=False
        
    #Call back function for action that may cause change in sense
    def CallVisual(self,):
        pass
    
    def CallAural(self):
        pass