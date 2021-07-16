# Required import for python
import Sofa
import numpy as np

# Data
scale3d_skin="50 30 5"
GeomagicPosition="0 20 15"

skinVolume_fileName="mesh\skinVolume2"

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
    root.gravity=[0, 0, -9.81]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Collision parameters
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.5", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Geomagic device
    root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="0", drawDeviceFrame="1", drawDevice="1", positionBase=GeomagicPosition,  orientationBase="0.707 0 0 0.707", forceFeedBack="@instrument/LCPFF1")
    

    #########################################################
    #--------------------- SKIN LAYER ----------------------#
    #########################################################
    

    #################### BEHAVIOUR ##########################

    skin = root.addChild('skin')
    
    # Solvers
    skin.addObject('EulerImplicitSolver', name="odesolver")
    skin.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    
    # Volumetric mesh loader
    skin.addObject('MeshGmshLoader', name='volumeLoader', filename=skinVolume_fileName, scale3d=scale3d_skin)
    skin.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    skin.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer')
    skin.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    skin.addObject('TetrahedronSetTopologyModifier')

    # Mechanical object
    skin.addObject('MechanicalObject', name='SkinMechObj', template='Vec3d')

    # Mass
    skin.addObject('DiagonalMass', name="SkinMass", template="Vec3d,double", massDensity="1.0")

    # Constraints: check to have not overconstrained the skin!
    skin.addObject('BoxROI', name='boxROI', box='-30 -30 0 30 30 3', drawBoxes='true')
    skin.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Forces
    skin.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus='3000', poissonRatio='0.49')
    skin.addObject('UncoupledConstraintCorrection')
    


    #################### COLLISION ##########################

    skinCollis = skin.addChild('skinCollis')

    # Mapped from the tetra of behaviour model
    skinCollis.addObject('TriangleSetTopologyContainer', name="T_Container")
    skinCollis.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    skinCollis.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    skinCollis.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")

    # Types of collision
    skinCollis.addObject('TriangleCollisionModel', contactStiffness="10")
    skinCollis.addObject('LineCollisionModel', contactStiffness="10")
    skinCollis.addObject('PointCollisionModel', contactStiffness="10") 


    #################### VISUALIZATION ##########################

    skinVisu = skinCollis.addChild('skinVisu')

    skinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    skinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )


    
    ##############################################################
    #---------------------  GEOMAGIC TOUCH ----------------------#
    ##############################################################    

    Omni=root.addChild('Omni')
    Omni.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDevice.positionDevice")
    Omni.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")


    #########################################################
    #--------------------- INSTRUMENT ----------------------#
    #########################################################  
    
    #################### BEHAVIOR ##########################

    instrument=root.addChild('instrument')
    instrument.addObject('EulerImplicitSolver',  name="ODE solver")
    instrument.addObject('CGLinearSolver', iterations="25", name="GeoLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")

    instrument.addObject('MechanicalObject', template="Rigid3d", name="instrumentState", position="@GeomagicDevice.positionDevice") 
    instrument.addObject('UniformMass', name="mass", totalMass="1" )
    instrument.addObject('RestShapeSpringsForceField', stiffness='100000', angularStiffness='100000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0')
    instrument.addObject('LCPForceFeedback', name="LCPFF1", activate="true", forceCoef="0.5")
    instrument.addObject('UncoupledConstraintCorrection') 
    
    #################### VISUAL ##########################
    
    VisualModel=instrument.addChild('VisualModel')
    VisualModel.addObject('MeshObjLoader', name="meshLoaderGeo", filename="Demos/Dentistry/data/mesh/dental_instrument.obj", handleSeams="1")
    VisualModel.addObject('OglModel',  name="InstrumentVisualModel", src="@meshLoaderGeo", color="1.0 0.2 0.2 1.0", ry="-180", rz="-90", dz="3.5", dx="-0.3")
    VisualModel.addObject('RigidMapping', name="MM->VM mapping",  input="@instrumentState",  output="@InstrumentVisualModel")
    
    #################### COLLISION ##########################

    CollisionModel=instrument.addChild('CollisionModel')
    CollisionModel.addObject('MeshObjLoader', filename="Demos/Dentistry/data/mesh/dental_instrument_centerline.obj",  name="loader")
    CollisionModel.addObject('MeshTopology', src="@loader", name="InstrumentCollisionModel" )
    CollisionModel.addObject('MechanicalObject', src="@loader", name="instrumentCollisionState")
    #CollisionModel.addObject('LineCollisionModel', contactStiffness="10")
    CollisionModel.addObject('PointCollisionModel', contactStiffness="10")
    CollisionModel.addObject('RigidMapping', name="CollisionMapping",  input="@instrumentState",  output="@instrumentCollisionState")


    return root



if __name__ == '__main__':
    main()
