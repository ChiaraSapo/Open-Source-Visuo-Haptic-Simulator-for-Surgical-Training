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
whichGeomagic="right"



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
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")


    # Add skin
    suture_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[7, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName,  task="Suture")

    suture_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[11, -0.1, -2, 22, 20, 0.1], borderBox=[11, -0.1, -2, 14, 20, 1],
    importFile=skinVolume_fileName,  side=1, task="Suture") 


    #################### GEOMAGIC TOUCH DEVICES ##################################################################

    root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Right Device", scale="1", drawDeviceFrame="1", 
    drawDevice="1", positionBase="20 20 0",  orientationBase="0.707 0 0 0.707", forceFeedBack="@SutureNeedle/LCPFFNeedle")

    root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Left Device", scale="1", drawDeviceFrame="1", 
    drawDevice="1", positionBase="0 20 0",  orientationBase="0.707 0 0 0.707", forceFeedBack="@SutureNeedle/LCPFFNeedle")

    GeomagicDevice(parentNode=root, name='OmniRight', position="@GeomagicDeviceRight.positionDevice")
    GeomagicDevice(parentNode=root, name='OmniLeft', position="@GeomagicDeviceLeft.positionDevice")
    

    #############################################################################################################


    # # Add training rings
    suture_models.ring(parentNode=root, name="Ring1", x=8, y=3, z=4, scale3d="1.5 1.5 1.5",  M="M1")
    suture_models.ring(parentNode=root, name="Ring2", x=8, y=13, z=4, scale3d="1.5 1.5 1.5",  M="M2")
    suture_models.ring(parentNode=root, name="Ring3", x=12, y=7, z=4, scale3d="1.5 1.5 1.5",  M="M3")
    suture_models.ring(parentNode=root, name="Ring4", x=12, y=17, z=4, scale3d="1.5 1.5 1.5", M="M4")
    
    SutureNeedle(parentNode=root, name='SutureNeedle', geomagic=geomagic, dx=0, dy=0, dz=10, ERS="@../OmniRight/DOFs", geomagicPosition="@GeomagicDeviceRight.positionDevice") # To fall on sphere: dx=12, dy=3, dz=6
    
    root.addObject(ButtonCheckController(name="MyController", rootNode=root))

    return root


def GeomagicDevice(parentNode=None, name=None, position=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position=position)
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")
    

def SutureNeedle(parentNode=None, name=None, dx=0, dy=0, dz=0, scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0],
geomagic=False, monitor=False, geomagicPosition=None, ERS=None): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position=geomagicPosition, scale3d="3 3 3", rotation="0 0 10" ) #, src="@instrumentMeshLoader")
        #name.addObject('RestShapeSpringsForceField', name="RestShapeSpringsFFNeedle", stiffness='1000', angularStiffness='1000', points='0', external_points='0', external_rest_shape="@../OmniRight/DOFs") 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
        #SutureNeedle.RS=name.RestShapeSpringsFFNeedle
    else: 
        name.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale="3.0" , dx=dx, dy=dy, dz=dz)
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')
    if monitor==True:
        name.addObject('Monitor', template="Vec3d", name="SutureNeedle_pos", listening="1", indices="0", shoWPositions="True", ExportPositions="True")

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/Suture_needle.obj", scale="3.0", handleSeams="1" )
    if geomagic==True:
        Visu.addObject('OglModel',name="Visual", src='@meshLoader_3', rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0",  color="0 0.5 0.796")
    else:
        Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/Suture_needle.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    if geomagic==True:
        Surf.addObject('MechanicalObject' ,src="@loader", scale="3.0", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else: 
        Surf.addObject('MechanicalObject' ,src="@loader", scale="3.0")#, dx="8", dy="3", dz="6")
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')


    collFront = name.addChild('collFront')
    if geomagic==True:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-4.2 0.02 -0.25", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-4.2 0.02 -0.25")

    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool")


    collFront.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collBack = name.addChild('collBack')
    if geomagic==True:
        collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25")
    collBack.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1")
    collBack.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    SutureNeedle.ITSELF=name
    SutureNeedle.COLL=name.Surf.Torus2Point.getLinkPath()
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.collBack.Particle2.getLinkPath()
    SutureNeedle.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedle.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    SutureNeedle.COLL_FRONT_TAG=name.collFront.SphereCollisionInstrument
    SutureNeedle.COLL_BACK=name.collBack.SphereCollisionInstrument2.getLinkPath()
    SutureNeedle.MO_TAG=name.InstrumentMechObject
    

 
# Controller for suture task training
class ChangeColorAtContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        self.root=rootNode
        self.contact_listener1 = rootNode.addObject('ContactListener', name="C1", collisionModel1 = suture_models.ring.C1, collisionModel2 = SutureNeedle.COLL)
        self.contact_listener2 = rootNode.addObject('ContactListener', name="C2", collisionModel1 = suture_models.ring.C2, collisionModel2 = SutureNeedle.COLL)
        self.contact_listener3 = rootNode.addObject('ContactListener', name="C3", collisionModel1 = suture_models.ring.C3, collisionModel2 = SutureNeedle.COLL)
        self.contact_listener4 = rootNode.addObject('ContactListener', name="C4", collisionModel1 = suture_models.ring.C4, collisionModel2 = SutureNeedle.COLL)
        
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
        if self.root.GeomagicDeviceRight.findData('button2').value==1:
            
            if whichGeomagic=="right":
                print("on the right")
                SutureNeedle.MO_TAG.findData('position').value=self.root.GeomagicDeviceleft.findData('positionDevice').value
                print("2")
                SutureNeedle.MO_TAG.reinit()
                print("3")
                #SutureNeedle.RS.findData('external_rest_shape').value='@../OmniLeft/DOFs'
            else:
                SutureNeedle.MO_TAG.findData('position').value="@GeomagicDeviceRight.positionDevice"
                #SutureNeedle.RS.findData('external_rest_shape').value='@../OmniRight/DOFs'

            SutureNeedle.MO_TAG.reinit()
            #SutureNeedle.RS.reinit()





if __name__ == '__main__':
    main()
