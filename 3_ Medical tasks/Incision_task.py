# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models 
#import controllers


scale3d_skin="1 0.6 1"
scale3d_scalpel="1 1 1 "

skinVolume_fileName="mesh\skin_30201"
scalpel_Instrument="mesh\scalpel.obj"
# Collision particles positions
pointPosition_onscalpel1="8 -7.4 -17" 


# Choose in your script to activate or not the GUI
USE_GUI = True



        
def main():
    import SofaRuntime
    import Sofa.Gui
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")
    root = Sofa.Core.Node("root")
    addScene(root)
    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.addGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()


def createScene(root):

    # Define root properties
    root.gravity=[0, 0, -9]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.5", contactDistance="0.05", angleCone="0.1")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Define the variables
    geomagic=False
    carving=True

    # Add skin
    models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[9.5, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName, carving=carving, side=0, task="Incision",
    borderBox1=[7, -0.1, -2, 10, 5, 1],borderBox2=[7, 5, -2, 10, 10, 1],borderBox3=[7, 10, -2, 10, 15, 1],borderBox4=[7, 15, -2, 10, 20, 1])

    models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[10, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[10, -0.1, -2, 22, 20, 0.1], borderBox=[11, -0.1, -2, 11.5, 20, 1],
    importFile=skinVolume_fileName, carving=carving, side=1, task="Incision",
    borderBox1=[11, -0.1, -2, 14, 5, 1],borderBox2=[11, 5, -2, 14, 10, 1],borderBox3=[11, 10, -2, 14, 15, 1],borderBox4=[11, 15, -2, 14, 20, 1]) 

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="0", positionBase="10 20 10",  orientationBase="0.707 0 0 0.707")
        
        models.GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################


    #################### CARVING #############################################
    if carving==True:
        root.addObject('CarvingManager', active="true", carvingDistance="0.1")
    ##########################################################################

    
    # Add scalpel
    models.Scalpel(parentNode=root, name='Scalpel', rotation=[0.0, 0.0, 0.0], translation=[8, 8, 20], scale3d=scale3d_scalpel,  
    fixingBox=None, importFile=scalpel_Instrument, carving=carving, geomagic=geomagic)

    # Add contact listener: uncomment to do stuff at animation time
    #root.addObject(IncisionContactControllerSprings(root))
    root.addObject(IncisionContactControllerAttach(root)) # If true: set translation of skin right to 10
    

    return root
    

class IncisionContactControllerAttach(Sofa.Core.Controller):

    def __init__(self, root):
        Sofa.Core.Controller.__init__(self, root)
        self.contact_listener = root.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.Scalpel.COLL_FRONT)
        self.contact_listener_right = root.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.Scalpel.COLL_FRONT)
        self.rootNode=root

        root.addObject('AttachConstraint',
        name="Incision constraint",
        object1 = "@SkinLeft", 
        object2 = "@SkinRight", 
        indices1= "  4 5 6 7 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239  ", 
        indices2= "  0 1 2 3 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207  ") 


    # # Uncomment to recompute indices
    # def onAnimateBeginEvent(self, event): 


    #     print(models.Skin.borderBox.findData('indices').value)
    #     index1=models.Skin.borderBox.findData('indices').value
    #     index2=models.Skin.borderBox_right.findData('indices').value
    #     temp1=len(index1)
    #     temp2=len(index2)
    #     self.N_indices=min(temp1,temp2)
    #     in1=self.computeIndices(index1)
    #     in2=self.computeIndices(index2)

        #print("indices1= \"", in1, "\", indices2= \"", in2, "\")")


    def computeIndices(self, indicesBox):

        result=' '  

        for i in range(self.N_indices):
            result += str(indicesBox[i]) + " "

        return result


class IncisionContactControllerSprings(Sofa.Core.Controller):

    def __init__(self, root):
        Sofa.Core.Controller.__init__(self, root)
        self.contact_listener = root.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.Scalpel.COLL_FRONT)
        self.contact_listener_right = root.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.Scalpel.COLL_FRONT)
        self.rootNode=root

        self.spring_force_field = root.addObject("StiffSpringForceField",  object1=models.Skin.MO,  object2=models.Skin.MO_right)
        springs = [Sofa.SofaDeformable.LinearSpring(index1=40, index2=78, springStiffness=100000, dampingFactor=0.5, restLength=0.001)] # Then set to right indices (the ones below)
        self.spring_force_field.addSprings(springs)
        self.indexes=0

    # def onAnimateBeginEvent(self,event):

    #     # If there is a contact between skin left or skin right 
    #     if self.contact_listener.getNumberOfContacts()!=0 or self.contact_listener_right.getNumberOfContacts()!=0:

    #         # Retrieve index

    #         # If contact point is different from before
    #         if self.indexes != self.contact_listener.getContactElements():

    #             # Check which box it belongs to

    #             # Remove spring
    #             self.spring_force_field.removeSpring(0)
    #             self.indexes = self.contact_listener.getContactElements() # Then set to right index



if __name__ == '__main__':
    main()
