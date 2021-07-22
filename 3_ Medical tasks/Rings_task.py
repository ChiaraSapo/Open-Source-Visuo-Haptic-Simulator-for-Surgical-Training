# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
import time


# Data

scale3d_skin="0.25 0.65 0.1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.3"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="mesh/skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="mesh/suture_needle.obj"
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

    # Define root properties
    root.gravity=[0, 0, -5]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    #root.addObject('VisualStyle', displayFlags="showInteractionForceFields ")
    root.addObject('OglLabel', label="RINGS TASK - TRAINING", x=20, y=20, fontsize=30, selectContrastingColor="1")
    root.addObject('OglLabel', label="Pass through the rings without touching them,", x=20, y=70, fontsize=20, selectContrastingColor="1")
    root.addObject('OglLabel', label="starting from the one closest to the needle", x=20, y=100, fontsize=20, selectContrastingColor="1")


    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.3", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # View
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -1 -0.000108372 0.908378")

    # Add skin
    suture_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[7, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName,  task="Suture")

    suture_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[11, -0.1, -2, 22, 20, 0.1], borderBox=[11, -0.1, -2, 14, 20, 1],
    importFile=skinVolume_fileName,  side=1, task="Suture") 


    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="0", positionBase="10 11 10",  orientationBase="0.707 0 0 0.707", handleEventTriggersUpdate=True, emitButtonEvent=True, button2=True)
        
        suture_models.GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################

    # # Add training rings
    suture_models.ring(parentNode=root, name="Ring1", x=8, y=3, z=4, scale3d="1.5 1.5 1.5",  M="M1")
    suture_models.ring(parentNode=root, name="Ring2", x=8, y=13, z=4, scale3d="1.5 1.5 1.5",  M="M2")
    suture_models.ring(parentNode=root, name="Ring3", x=12, y=7, z=4, scale3d="1.5 1.5 1.5",  M="M3")
    suture_models.ring(parentNode=root, name="Ring4", x=12, y=17, z=4, scale3d="1.5 1.5 1.5", M="M4")

    suture_models.SutureNeedle(parentNode=root, name='SutureNeedle', monitor=True, file1="RingsTask_pos", file2="RingsTask_vel", file3="RingsTask_force",  geomagic=geomagic, dx=0, dy=0, dz=10) # To fall on sphere: dx=12, dy=3, dz=6

    root.addObject(ChangeColorAtContactController(name="MyController", rootNode=root))



    return root



# Controller for suture task training
class ChangeColorAtContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        self.root=rootNode
        self.contact_listener1 = rootNode.addObject('ContactListener', name="C1", collisionModel1 = suture_models.ring.C1, collisionModel2 = suture_models.SutureNeedle.COLL)
        self.contact_listener2 = rootNode.addObject('ContactListener', name="C2", collisionModel1 = suture_models.ring.C2, collisionModel2 = suture_models.SutureNeedle.COLL)
        self.contact_listener3 = rootNode.addObject('ContactListener', name="C3", collisionModel1 = suture_models.ring.C3, collisionModel2 = suture_models.SutureNeedle.COLL)
        self.contact_listener4 = rootNode.addObject('ContactListener', name="C4", collisionModel1 = suture_models.ring.C4, collisionModel2 = suture_models.SutureNeedle.COLL)
        
    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):

        newMaterial="Default Diffuse 1 1 0 0 1 Ambient 1 0.2 0 0 1 Specular 0 1 0 0 1 Emissive 0 1 0 0 1 Shininess 0 45"
        oldMaterial="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
                
        # ring.M.texcoords.value and ring.M.findData('material').value give the same result.
        if self.contact_listener4.getNumberOfContacts()!=0: #4:1
            print("contact1")
            suture_models.ring.V4.findData('material').value=newMaterial

        if self.contact_listener2.getNumberOfContacts()!=0:
            print("contact2")
            suture_models.ring.V2.findData('material').value=newMaterial
            if suture_models.ring.V4.findData('material').value!=oldMaterial:
                suture_models.ring.V4.findData('material').value=oldMaterial

        if self.contact_listener3.getNumberOfContacts()!=0: #3
            print("contact3")
            suture_models.ring.V3.findData('material').value=newMaterial
            if suture_models.ring.V2.findData('material').value!=oldMaterial:
                suture_models.ring.V2.findData('material').value=oldMaterial

        if self.contact_listener1.getNumberOfContacts()!=0:
            print("contact4")
            suture_models.ring.V1.findData('material').value=newMaterial
            if suture_models.ring.V2.findData('material').value!=oldMaterial:
                suture_models.ring.V2.findData('material').value=oldMaterial

        
        



class ButtonCheckController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        self.root=rootNode

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





if __name__ == '__main__':
    main()
