# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
import incision_models
import time
import subprocess


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


def createScene(root):

    # Read user name
    Config=open('D:\Thesis\GUI\Config.txt')
    for line in Config:
        pass
    user_name = line
    Config.close()

    # Read user data (last lines of the file)
    fileName=f"D:\Thesis\GUI\{user_name}.txt"
    User=open(fileName)
    lines1=User.readlines()
    lines=lines1[-5:] #put 4 LATER
    station_type=lines[3]
    User.close()

    # Define root properties
    root.gravity=[0, 0, -5]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    #root.addObject('VisualStyle', displayFlags="showInteractionForceFields ")
    root.addObject('OglLabel', label="RINGS TASK - TRAINING", x=20, y=20, fontsize=30, selectContrastingColor="1")
    root.addObject('OglLabel', label="Pass through the rings without touching them,", x=20, y=70, fontsize=20, selectContrastingColor="1")
    root.addObject('OglLabel', label="starting from the one closest to you", x=20, y=100, fontsize=20, selectContrastingColor="1")


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
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -1 -0.000108372 0.908378")

    # Add skin
    skin_left=suture_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1])

    skin_right=suture_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[11, -0.1, -2, 22, 20, 0.1],
    side=1) 


    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        if station_type=="Double\n":
            root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Right Device", scale="1", drawDeviceFrame="1", 
            drawDevice="1", positionBase="20 20 0",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@SutureNeedle/LCPFFNeedle")

            root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Left Device", scale="1", drawDeviceFrame="1", 
            drawDevice="1", positionBase="0 20 0",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@SutureNeedle/LCPFFNeedle")

            GeomagicDevice(parentNode=root, name='OmniRight', position="@GeomagicDeviceRight.positionDevice")
            GeomagicDevice(parentNode=root, name='OmniLeft', position="@GeomagicDeviceLeft.positionDevice")

        else: 
            root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", 
            drawDevice="0", positionBase="11 10 10",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@SutureNeedle/LCPFFNeedle")
            
            GeomagicDevice(parentNode=root, name='Omni', position="@GeomagicDevice.positionDevice")

    #############################################################################################################

    # Add training rings
    suture_models.ring(parentNode=root, name="Ring1", x=7, y=4, z=4, scale3d="1.5 1.5 1.5",  M="M1")
    suture_models.ring(parentNode=root, name="Ring2", x=7, y=12, z=4, scale3d="1.5 1.5 1.5",  M="M2")
    suture_models.ring(parentNode=root, name="Ring3", x=13, y=8, z=4, scale3d="1.5 1.5 1.5",  M="M3")
    suture_models.ring(parentNode=root, name="Ring4", x=13, y=16, z=4, scale3d="1.5 1.5 1.5", M="M4")

    suture_models.StraightNeedle(parentNode=root, name='StraightNeedle', monitor=True, file1="RingsTask_pos", file2="RingsTask_vel", file3="RingsTask_force",  geomagic=geomagic, dx=0, dy=0, dz=10) # To fall on sphere: dx=12, dy=3, dz=6
    #incision_models.Scalpel(parentNode=root, name='Scalpel',  geomagic=geomagic)

    root.addObject(ChangeColorAtContactController(name="MyController", rootNode=root))
    #root.addObject(ButtonCheckControllerModifyData(name="MyController", rootNode=root))
    #root.addObject(ButtonCheckControllerAddNeedle(name="MyController", rootNode=root))


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

# Controller for suture task training
class ChangeColorAtContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        self.root=rootNode
        self.contact_listener1 = rootNode.addObject('ContactListener', name="C1", collisionModel1 = suture_models.ring.C1, collisionModel2 = suture_models.StraightNeedle.COLL)
        self.contact_listener2 = rootNode.addObject('ContactListener', name="C2", collisionModel1 = suture_models.ring.C2, collisionModel2 = suture_models.StraightNeedle.COLL)
        self.contact_listener3 = rootNode.addObject('ContactListener', name="C3", collisionModel1 = suture_models.ring.C3, collisionModel2 = suture_models.StraightNeedle.COLL)
        self.contact_listener4 = rootNode.addObject('ContactListener', name="C4", collisionModel1 = suture_models.ring.C4, collisionModel2 = suture_models.StraightNeedle.COLL)

    
    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):

        newMaterial="Default Diffuse 1 1 0 0 1 Ambient 1 0.2 0 0 1 Specular 0 1 0 0 1 Emissive 0 1 0 0 1 Shininess 0 45"
        oldMaterial="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
        
        # Button1 == Black button; Button2 == Grey button
        if self.root.GeomagicDevice.findData('button2').value!=0: # If button is toggled
            if suture_models.StraightNeedle.Monitor.findData('showTrajectories').value==1:
                suture_models.StraightNeedle.Monitor.findData('showTrajectories').value=0
            elif suture_models.StraightNeedle.Monitor.findData('showTrajectories').value==0:
                suture_models.StraightNeedle.Monitor.findData('showTrajectories').value=1
        
        if self.root.GeomagicDevice.findData('button1').value==1:
            # self.root.animate = False
            # self.root.init()
            # self.root.animate = True
            self.root.animate = False
            subprocess.call(['D:\Thesis\GUI\plotRings.bat'])
            self.root.quit()
        
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

        if self.contact_listener2.getNumberOfContacts()!=0:
            #print("contact2")
            suture_models.ring.V2.findData('material').value=newMaterial
            if suture_models.ring.V3.findData('material').value!=oldMaterial:
                suture_models.ring.V3.findData('material').value=oldMaterial
            if suture_models.ring.V4.findData('material').value!=oldMaterial:
                suture_models.ring.V4.findData('material').value=oldMaterial
            if suture_models.ring.V1.findData('material').value!=oldMaterial:
                suture_models.ring.V1.findData('material').value=oldMaterial

        if self.contact_listener3.getNumberOfContacts()!=0: #3
            #print("contact3")
            suture_models.ring.V3.findData('material').value=newMaterial
            if suture_models.ring.V4.findData('material').value!=oldMaterial:
                suture_models.ring.V4.findData('material').value=oldMaterial
            if suture_models.ring.V2.findData('material').value!=oldMaterial:
                suture_models.ring.V2.findData('material').value=oldMaterial
            if suture_models.ring.V1.findData('material').value!=oldMaterial:
                suture_models.ring.V1.findData('material').value=oldMaterial

        if self.contact_listener1.getNumberOfContacts()!=0:
            #print("contact4")
            suture_models.ring.V1.findData('material').value=newMaterial
            if suture_models.ring.V3.findData('material').value!=oldMaterial:
                suture_models.ring.V3.findData('material').value=oldMaterial
            if suture_models.ring.V2.findData('material').value!=oldMaterial:
                suture_models.ring.V2.findData('material').value=oldMaterial
            if suture_models.ring.V4.findData('material').value!=oldMaterial:
                suture_models.ring.V4.findData('material').value=oldMaterial
        


class ButtonCheckControllerModifyData(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        self.root=rootNode
        self.first=1

    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):

        # Button1 == Black button; Button2 == Grey button
        if self.root.GeomagicDevice.findData('button2').value==1:
            
            if suture_models.SutureNeedle.MO_TAG.findData('position').value=="@GeomagicDeviceRight.positionDevice":
                suture_models.SutureNeedle.MO_TAG.findData('position').value="@GeomagicDeviceLeft.positionDevice"
                suture_models.SutureNeedle.RS.findData('external_rest_shape').value='@../OmniLeft/DOFs'
            else:
                suture_models.SutureNeedle.MO_TAG.findData('position').value="@GeomagicDeviceRight.positionDevice"
                suture_models.SutureNeedle.RS.findData('external_rest_shape').value='@../OmniRight/DOFs'

            suture_models.SutureNeedle.MO_TAG.reinit()
            suture_models.SutureNeedle.RS.reinit()



class ButtonCheckControllerAddNeedle(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        self.root=rootNode
        self.first=1

    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):

        #if self.root.GeomagicDevice.findData('button2').value!=0: # If button is toggled
        if self.first==1:
            
            self.root.removeChild("StraightNeedle")

            self.StraightNeedle()
            self.first=0

    def StraightNeedle(self): 
        # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

        StraightNeedle2=self.root.addChild('StraightNeedle2')
        StraightNeedle2.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
        StraightNeedle2.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
        StraightNeedle2.addObject('MechanicalObject', name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d=[0.1, 0.4, 0.4])
        StraightNeedle2.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        StraightNeedle2.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
        #StraightNeedle2.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale3d=[0.1, 0.4, 0.4] ,dx=0, dy=5, dz=10)
        # Mass gives problems: keep at 1
        StraightNeedle2.addObject('UniformMass', totalMass=1)
        StraightNeedle2.addObject('UncoupledConstraintCorrection')
        StraightNeedle2.init()


        Visu=StraightNeedle2.addChild('Visu')
        Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="C:\sofa\src\Chiara\mesh\straight_needle.obj", scale3d=[0.1, 0.4, 0.4],  translation=[0, 0, 10] , rotation=[0, 90, 0])
        Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796")
        Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
        #Visu.init()
        Sofa.Simulation.initVisual(Visu)
        
        Surf=StraightNeedle2.addChild('Surf')
        Surf.addObject('MeshObjLoader' ,filename="C:\sofa\src\Chiara\mesh\straight_needle.obj" ,scale3d=[0.1, 0.4, 0.4], name="loader", translation=[0, 0, 10] , rotation=[0, 90, 0])
        Surf.addObject('MeshTopology' ,src="@loader")
        Surf.addObject('MechanicalObject',  name="SurfMO", src="@loader", translation=[0,0,-11])#, rotation=[90, 0, 0])
        Surf.addObject('PointCollisionModel')
        Surf.addObject('RigidMapping')
        Surf.init()






if __name__ == '__main__':
    main()
