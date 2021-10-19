# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
import incision_models
import time
import subprocess
import read_Files

# Data
scale3d_skin="0.25 0.65 0.1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.3"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="mesh/skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="mesh/straight_needle.obj"
threadVolume_fileName="mesh/threadCh2"

# Data
skin_youngModulus=1700#300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8

# Define the variables
geomagic=True
carving=False

# Choose in your script to activate or not the GUI
USE_GUI = True


def main():
    import SofaRuntime
    import Sofa.Gui
    import Sofa.Core
    SofaRuntime.importPlugin("SofaComponentAll")
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")

    root = Sofa.Core.Node("root")
    createScene(root)

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


## This function creates the graph node

def createScene(root):

    [RepNumber,user_name]=read_Files.read()

    fileNamePos=f"Rep{RepNumber}_{user_name}_RingsPos_Double"
    fileNameVel=f"Rep{RepNumber}_{user_name}_RingsVel_Double"
    fileNameForce=f"Rep{RepNumber}_{user_name}_RingsForce_Double"
    

    # Define root properties
    root.gravity=[0, 0, -5]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    
    # root.addObject('OglLabel', label="RINGS TASK - TRAINING", x=20, y=20, fontsize=30, selectContrastingColor="1")
    # root.addObject('OglLabel', label="Pass through the rings without touching them,", x=20, y=70, fontsize=20, selectContrastingColor="1")
    # root.addObject('OglLabel', label="starting from the one closest to you", x=20, y=100, fontsize=20, selectContrastingColor="1")
    root.addObject('BackgroundSetting', color="0.3 0.5 0.8")
    root.addObject('ViewerSetting', fullscreen="true")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.1", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # View
    #root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -1 -0.000108372 0.908378")

    # Add skin
    skin_left=suture_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1])

    skin_right=suture_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[11, -0.1, -2, 22, 20, 0.1], side=1) 



    #################### GEOMAGIC TOUCH DEVICE ##################################################################

    # Add geomagic drivers
    root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Default Device", scale="1", drawDeviceFrame="0", 
    drawDevice="0", positionBase="10 10 10",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@StraightNeedle/LCPFFNeedle")

    # Add geomagic nodes
    GeomagicDevice(parentNode=root, name='OmniRight', position="@GeomagicDeviceRight.positionDevice")
    
    # Add needles
    suture_models.StraightNeedle(parentNode=root, name='StraightNeedle', monitor=True, file1=fileNamePos, file2=fileNameVel, file3=fileNameForce, position="@GeomagicDeviceRight.positionDevice", external_rest_shape='@../OmniRight/DOFs') # To fall on sphere: dx=12, dy=3, dz=6

    #############################################################################################################

    # Add training rings
    suture_models.ring(parentNode=root, name="Ring1", translation=[7, 5, 4], scale3d="1.5 1.5 1.5",  RingModelNumber="M1")
    suture_models.ring(parentNode=root, name="Ring2", translation=[7, 12, 4], scale3d="1.5 1.5 1.5",  RingModelNumber="M2")
    suture_models.ring(parentNode=root, name="Ring3", translation=[13, 8.5, 4], scale3d="1.5 1.5 1.5",  RingModelNumber="M3")
    suture_models.ring(parentNode=root, name="Ring4", translation=[13, 15.5, 4], scale3d="1.5 1.5 1.5", RingModelNumber="M4")

    # Add Rings controller    
    root.addObject(RingsTaskController(name="MyController", rootNode=root))

    return root


## This function defines a geomagic
# @param parentNode: parent node of the skin patch
# @param name: name of the behavior node
# @param rotation: rotation 
# @param translation: translation
def GeomagicDevice(parentNode=None, name=None, position=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position=position)
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")


## Controller for rings task.
# Handles color changes of the rings and allows showing the trajectory of the needle on button press
class RingsTaskController(Sofa.Core.Controller):

    ## Constructor of the class. 
    # @param name: name of the controller
    # @param rootnode: path to the root node of the simulation
    # Defines the contact listeners between rings and the needle
    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        self.root=rootNode
        self.contact_listener1 = rootNode.addObject('ContactListener', name="C1", collisionModel1 = suture_models.ring.C1, collisionModel2 = suture_models.StraightNeedle.COLL)
        self.contact_listener2 = rootNode.addObject('ContactListener', name="C2", collisionModel1 = suture_models.ring.C2, collisionModel2 = suture_models.StraightNeedle.COLL)
        self.contact_listener3 = rootNode.addObject('ContactListener', name="C3", collisionModel1 = suture_models.ring.C3, collisionModel2 = suture_models.StraightNeedle.COLL)
        self.contact_listener4 = rootNode.addObject('ContactListener', name="C4", collisionModel1 = suture_models.ring.C4, collisionModel2 = suture_models.StraightNeedle.COLL)

        self.TouchedRings=0
        self.first=1
    
    ## Method called at each begin of animation step
    # @param event: animation step event
    # On button press it shows / hides the trajectory of the needle 
    # If there is a contact between ring i and the needle it changes the needle's color from green to red and, 
    # if other rings are red, it changes their color to green again
    def onAnimateBeginEvent(self, event):

        if self.first==1:
            Data = open('RingsFreq.txt', 'a')  
            var1=f"\n\n"
            Data.write(var1)
            Data.close()
            self.first=0
 
        Data = open('RingsFreq.txt', 'a')  
        var1=f"{time.time()}\n"
        Data.write(var1)
        Data.close()

        newMaterial="Default Diffuse 1 1 0 0 1 Ambient 1 0.2 0 0 1 Specular 0 1 0 0 1 Emissive 0 1 0 0 1 Shininess 0 45"
        oldMaterial="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"

        #print(suture_models.StraightNeedle.MO.findData('position').value)


        # ring.M.texcoords.value and ring.M.findData('material').value give the same result.
        if self.contact_listener4.getNumberOfContacts()!=0: #4:1
            #print("contact1")
            suture_models.ring.V4.findData('material').value=newMaterial
            if suture_models.ring.V3.findData('material').value!=oldMaterial:
                suture_models.ring.V3.findData('material').value=oldMaterial
            if suture_models.ring.V2.findData('material').value!=oldMaterial:
                suture_models.ring.V2.findData('material').value=oldMaterial
            if suture_models.ring.V1.findData('material').value!=oldMaterial:
                suture_models.ring.V1.findData('material').value=oldMaterial
            self.TouchedRings+=1

        if self.contact_listener2.getNumberOfContacts()!=0:
            #print("contact2")
            suture_models.ring.V2.findData('material').value=newMaterial
            if suture_models.ring.V3.findData('material').value!=oldMaterial:
                suture_models.ring.V3.findData('material').value=oldMaterial
            if suture_models.ring.V4.findData('material').value!=oldMaterial:
                suture_models.ring.V4.findData('material').value=oldMaterial
            if suture_models.ring.V1.findData('material').value!=oldMaterial:
                suture_models.ring.V1.findData('material').value=oldMaterial
            self.TouchedRings+=1

        if self.contact_listener3.getNumberOfContacts()!=0: #3
            #print("contact3")
            suture_models.ring.V3.findData('material').value=newMaterial
            if suture_models.ring.V4.findData('material').value!=oldMaterial:
                suture_models.ring.V4.findData('material').value=oldMaterial
            if suture_models.ring.V2.findData('material').value!=oldMaterial:
                suture_models.ring.V2.findData('material').value=oldMaterial
            if suture_models.ring.V1.findData('material').value!=oldMaterial:
                suture_models.ring.V1.findData('material').value=oldMaterial
            self.TouchedRings+=1

        if self.contact_listener1.getNumberOfContacts()!=0:
            #print("contact4")
            suture_models.ring.V1.findData('material').value=newMaterial
            if suture_models.ring.V3.findData('material').value!=oldMaterial:
                suture_models.ring.V3.findData('material').value=oldMaterial
            if suture_models.ring.V2.findData('material').value!=oldMaterial:
                suture_models.ring.V2.findData('material').value=oldMaterial
            if suture_models.ring.V4.findData('material').value!=oldMaterial:
                suture_models.ring.V4.findData('material').value=oldMaterial
            self.TouchedRings+=1
        



if __name__ == '__main__':
    main()
