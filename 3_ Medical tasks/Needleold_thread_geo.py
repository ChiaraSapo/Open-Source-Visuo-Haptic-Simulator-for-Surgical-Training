# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models

thread_youngModulus=2000
thread_poissonRatio=0.8


# Choose in your script to activate or not the GUI
USE_GUI = True
geomagic=True


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
    root.gravity=[0, 0, -6]
    root.dt=0.01

    # Required plugins
    #root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")
    root.addObject('VisualStyle', displayFlags="showInteractionForceFields")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.3", contactDistance="0.05", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")
    
    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="0 9 10",  orientationBase="0.707 0 0 0.707")
        
        suture_models.GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################

    # Add needle
    Needle_Thread(parentNode=root, name='SutureNeedle', rotation=[0.0, 0.0, 0.0], translation=[0,0,0],     
    scale3d="5 5 5", importFile="mesh\suture_needle.obj")

    #Thread(parentNode=root, name="Thread", rotation=[90, 0, 0], translation=[0,10,0], importFile="mesh/threadCh2", scale3d=[0.3, 0.3, 0.1])

    root.addObject('BilateralInteractionConstraint', template="Vec3d", object1=Needle_Thread.COLL_BACK_MO, object2=Needle_Thread.thread_MO,  first_point="0", second_point="0")


    return root


def Needle_Thread(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0], importFile=None):

    #################### BEHAVIOUR ##########################
    name=parentNode.addChild(name)

    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighMass="1.0", rayleighStiffness="0.01")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7") 
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)
    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d="3", rotation="0 0 10" ) #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', name="InstrumentRestShape", stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
    else: 
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d)
    name.addObject('UniformMass', name='mass', totalMass="10") 
    name.addObject('UncoupledConstraintCorrection') 

    #################### COLLISION ##########################
    InstrumentColl_Back = name.addChild('InstrumentColl_Back')
    
    InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05")
    InstrumentColl_Back.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1")
    InstrumentColl_Back.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/Suture_needle.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="3.0")#, dx="8", dy="3", dz="6")
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    #Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')

    #################### VISUALIZATION ########################
    InstrumentVisu = name.addChild('InstrumentVisu')

    InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d,  color="0 0.5 0.796")
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    Needle_Thread.MO=name.InstrumentMechObject.getLinkPath()
    Needle_Thread.COLL_BACK_MO=name.InstrumentColl_Back.Particle2.getLinkPath()
    Needle_Thread.POS=name.InstrumentMechObject.findData('position')


    Thread=parentNode.addChild("Thread")

    #################### BEHAVIOUR ##########################
    
    # Solvers
    Thread.addObject('EulerImplicitSolver', name="odesolver")
    Thread.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    Thread.addObject('MeshGmshLoader', name='name_volumeLoader', filename="mesh/threadCh2", scale3d=[0.3, 0.3, 0.1], rotation=[-90, 90, 90], translation=[10,18,4])
    #name.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    Thread.addObject('TriangleSetTopologyContainer', src='@name_volumeLoader')
    Thread.addObject('TriangleSetGeometryAlgorithms', template='Vec3d')
    Thread.addObject('TriangleSetTopologyModifier')

    # Mechanical object and mass
    Thread.addObject('MechanicalObject', name='ThreadMechObject', template='Vec3d', position="@../SutureNeedle.position")
    
    Thread.addObject('UniformMass', name="nameMass", template="Vec3d,double", totalMass="1.0")

    Thread.addObject('TriangleFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=thread_youngModulus, poissonRatio=thread_poissonRatio)
    #name.addObject('MeshSpringForceField', name="FEM-Bend", template="Vec3d", stiffness="1000", damping="0.1")
    Thread.addObject('UncoupledConstraintCorrection')

    #################### COLLISION ##########################

    ThreadColl = Thread.addChild('ThreadColl')

    ThreadColl.addObject('PointCollisionModel', name="ThreadPointCollisionModel", selfCollision="True")
    ThreadColl.addObject('TriangleCollisionModel', name="ThreadTriangleCollisionModel", selfCollision="True") 

    #################### VISUALIZATION ########################

    ThreadVisu = ThreadColl.addChild('ThreadVisu')
    ThreadVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    ThreadVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    Needle_Thread.thread_MO=Thread.ThreadMechObject.getLinkPath()


if __name__ == '__main__':
    main()
