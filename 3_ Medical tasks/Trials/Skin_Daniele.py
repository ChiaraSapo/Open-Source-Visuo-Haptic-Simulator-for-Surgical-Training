# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models
import controllers


# Data
#scale3d_skin="0.2 0.3 1" #thin
#scale3d_skin="1 0.6 1"
scale3d_skin="0.25 0.5 0.1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="mesh\skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="mesh\suture_needle.obj"
threadVolume_fileName="mesh/threadCh2"

# Data
skin_youngModulus=1000#300
thread_youngModulus=2000
skin_poissonRatio=0.49
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
    root.gravity=[0, 0, -10]
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


    # Define the variables
    geomagic=True
    carving=False

    skin=root.addChild("skin")
    skin.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    skin.addObject('SparseLDLSolver')
    skin.addObject('MechanicalObject', template="Vec3d", name="Hexa", scale3d="2 1 0.2", position="-19 0 -8", showVectors="true", drawMode="2")
    skin.addObject('RegularGridTopology', name="grid", n="8 8 2", min="-5 -4 -10", max="3 4 10", p0="-4 -4 -10" )
    skin.addObject('HexahedronSetGeometryAlgorithms')
    skin.addObject('DiagonalMass', template="Vec3d", name="Mass", massDensity="1.0")
    skin.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM" ,poissonRatio="0.47" ,youngModulus="2000")
    skin.addObject('LinearSolverConstraintCorrection')
    #skin.addObject('FixedConstraint' ,template="Vec3d" ,name="Fixed Dofs", indices="0 4 20 24 30 34 40 44 50 54 1 2 3  5 6 7 8 9 10 11 12 13 14 15 16 17 18 19  21 22 23" ,drawSize="0" )
    skin.addObject('BoxROI', name='boxROI', box=[-20, -20, -3, 20, 20, 0], drawBoxes='true', computeTriangles='true')
    skin.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')
    skin.addObject('FixedPlaneConstraint', template="Vec3d" ,name="defaultPlane" ,direction="0 0 1" ,dmin="-8")
    
    SkinQ=skin.addChild("SkinQ")
    SkinQ.addObject('QuadSetTopologyContainer', name="Container")
    SkinQ.addObject('QuadSetTopologyModifier', name="Container")
    SkinQ.addObject('QuadSetGeometryAlgorithms' ,template="Vec3d" ,name="GeomAlgo")
    SkinQ.addObject('Hexa2QuadTopologicalMapping' ,name="default6", input="@../grid", output="@Container")
    
    SkinT=SkinQ.addChild("SkinT")
    SkinT.gravity=[0, 0, -15]
    SkinT.addObject('TriangleSetTopologyContainer', name="Container")
    SkinT.addObject('TriangleSetTopologyModifier' ,name="Modifier")
    SkinT.addObject('TriangleSetGeometryAlgorithms' ,template="Vec3d", name="GeomAlgo")
    SkinT.addObject('Quad2TriangleTopologicalMapping' ,name="default8" ,input="@../Container" ,output="@Container")
    SkinT.addObject('TriangleCollisionModel', name="SkinCollisionT" ,contactStiffness="0.01")
    
    Visu=SkinT.addChild("Visu")
    Visu.addObject('OglModel', template="ExtVec3f", name="Visual" ,color="1 0.75 0.796" ,material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    Visu.addObject('OglViewport' ,screenPosition="0 0" ,screenSize="250 250" ,cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946")
    Visu.addObject('IdentityMapping' ,template="Vec3d,ExtVec3f", name="default12" ,input="@.." ,output="@Visual")
    


    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="0", positionBase="7 2 10",  orientationBase="0.707 0 0 0.707")
        
        models.GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################



    instrument=root.addChild("instrument")
    instrument.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01" ,rayleighMass="0.02")
    instrument.addObject('SparseLDLSolver')
    instrument.addObject('MechanicalObject', name="instrumentState" ,template="Rigid3")
    instrument.addObject('UniformMass', name="mass", totalMass="0.2")
    instrument.addObject('RestShapeSpringsForceField' ,stiffness='1000' ,angularStiffness='1000' ,external_rest_shape='@../Omni/DOFs' ,points='0' ,external_points='0')
    instrument.addObject('LCPForceFeedback' ,name="LCPFF1" ,activate="true" ,forceCoef="0.05")
    instrument.addObject('LinearSolverConstraintCorrection')
    
    VisuTool=instrument.addChild("VisuTool")
    VisuTool.addObject('MeshObjLoader', name="meshLoader_1", filename="mesh\suture_needle.obj", handleSeams="1")
    VisuTool.addObject('OglModel' ,name="InstrumentVisualModel", src="@meshLoader_1", color="1.0 0.2 0.2 1.0", ry="-180", rz="-90", dz="3.5", dx="-0.3")
    VisuTool.addObject('RigidMapping', name="MM->VM mapping" ,input="@instrumentState" ,output="@InstrumentVisualModel")
    
    CollMod=instrument.addChild("CollMod")
    CollMod.addObject('MeshObjLoader', filename="mesh\suture_needle.obj" , name="loader")
    CollMod.addObject('MeshTopology' ,src="@loader", name="InstrumentCollisionModel")
    CollMod.addObject('MechanicalObject' ,src="@loader", name="instrumentCollisionState"  ,ry="-180", rz="-90" ,dz="3.5", dx="-0.3" )
    CollMod.addObject('LineCollisionModel' ,contactStiffness="0.001")
    CollMod.addObject('PointCollisionModel' ,contactStiffness="0.001" ,name="Instrument")
    CollMod.addObject('RigidMapping', name="MM->CM mapping", input="@instrumentState" ,output="@instrumentCollisionState")
    
    InstrumentColl_Front = instrument.addChild('InstrumentColl_Front')
    
    InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="0 0 0", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('RigidMapping', template="Rigid3d,Vec3d" , name="MM->CM mapping",  input="@../instrumentState",  output="@Particle")
 
    return root



if __name__ == '__main__':
    main()
