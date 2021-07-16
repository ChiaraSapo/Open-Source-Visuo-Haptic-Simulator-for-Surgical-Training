# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models
import controllers


# Data
#scale3d_skin="0.2 0.3 1" #thin
#scale3d_skin="1 0.6 1"
scale3d_skin="0.2 0.5 0.1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="mesh\skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="mesh\suture_needle.obj"
threadVolume_fileName="mesh/threadCh2"

# Data
skin_youngModulus=300#300
thread_youngModulus=2000
skin_poissonRatio=0.1#0.49
thread_poissonRatio=0.8


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
    root.gravity=[0, 0, 0]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

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

    # Geomagic devices
    root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Right Device", scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="12 0 0",  orientationBase="0.707 0 0 0.707", forceFeedBack="@instrumentRight/LCPFF_Right")
    root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Left Device", scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="-12 0 0",  orientationBase="0.707 0 0 0.707", forceFeedBack="@instrumentLeft/LCPFF_Left")



    ################################################################


  
    #############################################################
    #--------------------- GEOMAGIC RIGHT ----------------------#
    #############################################################

    
    OmniRight=root.addChild('OmniRight')
    OmniRight.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDeviceRight.positionDevice")
    OmniRight.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")

    
    #########################################################
    #--------------------- INSTRUMENT ----------------------#
    #########################################################

    instrumentRight=root.addChild('instrumentRight')
    instrumentRight.addObject('EulerImplicitSolver',  name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.02")
    instrumentRight.addObject('SparseLDLSolver') #'CGLinearSolver')
    instrumentRight.addObject('MechanicalObject', template="Rigid3d", name="instrumentRightState", position= "@GeomagicDeviceRight.positionDevice")
    instrumentRight.addObject('UniformMass', name="mass", totalMass="1" )
    #instrumentRight.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') #DANI
    instrumentRight.addObject('LCPForceFeedback', name="LCPFF_Right", activate="true", forceCoef="0.5")
    instrumentRight.addObject('UncoupledConstraintCorrection')
    

    #################### COLLISION ##########################
    CollisionModel=instrumentRight.addChild('CollisionModel')
    CollisionModel.addObject('MeshObjLoader', filename="Demos/Dentistry/data/mesh/dental_instrument_centerline.obj",  name="loader")
    CollisionModel.addObject('MeshTopology',src="@loader", name="instrumentRightCollisionModel" )
    CollisionModel.addObject('MechanicalObject', src="@loader", name="instrumentRightCollisionState",  ry="-180", rz="-90", dz="3.5", dx="-0.3")
    CollisionModel.addObject('LineCollisionModel')#, contactStiffness="0.001")
    CollisionModel.addObject('PointCollisionModel', contactStiffness="1", name="instrumentRight")#, tags="CarvingTool")
    CollisionModel.addObject('RigidMapping', name="CollisionMapping",  input="@instrumentRightState",  output="@instrumentRightCollisionState")
   

    #################### VISUALIZATION ##########################    
    VisualModel=instrumentRight.addChild('VisualModel')
    VisualModel.addObject('MeshObjLoader', name="meshLoaderGeo", filename="Demos/Dentistry/data/mesh/dental_instrument.obj", handleSeams="1")
    VisualModel.addObject('OglModel',  name="instrumentRightVisualModel", src="@meshLoaderGeo", color="1.0 0.2 0.2 1.0", ry="-180", rz="-90", dz="3.5", dx="-0.3")
    VisualModel.addObject('RigidMapping', name="MM->VM mapping",  input="@instrumentRightState",  output="@instrumentRightVisualModel")
    
    


    
    #############################################################
    #--------------------- GEOMAGIC LEFT ----------------------#
    #############################################################

    
    OmniLeft=root.addChild('OmniLeft')
    OmniLeft.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDeviceLeft.positionDevice")
    OmniLeft.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")

    
    #########################################################
    #--------------------- INSTRUMENT ----------------------#
    #########################################################

    instrumentLeft=root.addChild('instrumentLeft')
    instrumentLeft.addObject('EulerImplicitSolver',  name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.02")
    instrumentLeft.addObject('SparseLDLSolver') #'CGLinearSolver')
    instrumentLeft.addObject('MechanicalObject', template="Rigid3d", name="instrumentLeftState", position="@GeomagicDeviceLeft.positionDevice")
    instrumentLeft.addObject('UniformMass', name="mass", totalMass="1" )
    #instrumentLeft.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') #DANI
    instrumentLeft.addObject('LCPForceFeedback', name="LCPFF_Left", activate="true", forceCoef="0.5")
    instrumentLeft.addObject('UncoupledConstraintCorrection')
    

    #################### COLLISION ##########################
    CollisionModel=instrumentLeft.addChild('CollisionModel')
    CollisionModel.addObject('MeshObjLoader', filename="Demos/Dentistry/data/mesh/dental_instrument_centerline.obj",  name="loader")
    CollisionModel.addObject('MeshTopology',src="@loader", name="instrumentLeftCollisionModel" )
    CollisionModel.addObject('MechanicalObject', src="@loader", name="instrumentLeftCollisionState",  ry="-180", rz="-90", dz="3.5", dx="-0.3")
    CollisionModel.addObject('LineCollisionModel')#, contactStiffness="0.001")
    CollisionModel.addObject('PointCollisionModel', contactStiffness="1", name="instrumentLeft")#, tags="CarvingTool")
    CollisionModel.addObject('RigidMapping', name="CollisionMapping",  input="@instrumentLeftState",  output="@instrumentLeftCollisionState")
   

    #################### VISUALIZATION ##########################    
    VisualModel=instrumentLeft.addChild('VisualModel')
    VisualModel.addObject('MeshObjLoader', name="meshLoaderGeo", filename="Demos/Dentistry/data/mesh/dental_instrument.obj", handleSeams="1")
    VisualModel.addObject('OglModel',  name="instrumentLeftVisualModel", src="@meshLoaderGeo", color="1.0 0.2 0.2 1.0", ry="-180", rz="-90", dz="3.5", dx="-0.3")
    VisualModel.addObject('RigidMapping', name="MM->VM mapping",  input="@instrumentLeftState",  output="@instrumentLeftVisualModel")
    