# Required import for python
import Sofa
import numpy as np


# Data
poissonRatio_ALL=0.48
youngModulus_H=3400
youngModulus_D=300
youngModulus_E=1000
scale3d_std="80 50 20"
scale3d_scalpel="5 5 5"
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skinVolume2"
#skinSurface_fileName="C:\sofa\src\examples\skinSurface.stl"
scalpel_Instrument="mesh\scalpel.obj"

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
    root.gravity=[0, -9.81, 0]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping ")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.5", contactDistance="0.05", angleCone="0.1")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    #root.addObject('GenericConstraintSolver')
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Geomagic device
    root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="0 0 8",  orientationBase="0.707 0 0 0.707")
    
    # Carving
    #root.addObject('CarvingManager', active="true", carvingDistance="0.1") #CARVING

    #########################################################
    #--------------------- SKIN LAYER ----------------------#
    #########################################################
    

    #################### BEHAVIOUR ##########################

    skin = root.addChild('skin')
    
    # Solvers
    skin.addObject('EulerImplicitSolver', name="odesolver")
    skin.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    
    # Volumetric mesh loader
    skin.addObject('MeshGmshLoader', name='volumeLoader', filename=skinVolume_fileName, scale3d=scale3d_std)
    #skin.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    skin.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer',  template='Vec3d')
    skin.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    skin.addObject('TetrahedronSetTopologyModifier')

    # Mechanical object
    skin.addObject('MechanicalObject', name='SkinMechObj', template='Vec3d')#, showIndices='true')

    # Mass
    skin.addObject('UniformMass', template="Vec3d,double", name="SkinMass", totalMass="10")

    # Constraints: check to have not overconstrained the skin!
    skin.addObject('BoxROI', name='boxROI', box='-50 -50 0 50 50 10', drawBoxes='true')
    skin.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    skin.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus='300', poissonRatio='0.49')
    skin.addObject('UncoupledConstraintCorrection')


    #################### COLLISION ##########################

    skinCollis = skin.addChild('skinCollis')

    # Mapped from the tetra of behaviour model
    skinCollis.addObject('TriangleSetTopologyContainer', name="T_Container")
    skinCollis.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    skinCollis.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    skinCollis.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")

    # Types of collision
    skinCollis.addObject('TriangleCollisionModel')#, tags="CarvingSurface")
    skinCollis.addObject('LineCollisionModel')
    skinCollis.addObject('PointCollisionModel')#, tags="CarvingSurface")   


    #################### VISUALIZATION ########################

    skinVisu = skinCollis.addChild('skinVisu')
    skinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    skinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )


    
    #######################################################
    #--------------------- GEOMAGIC ----------------------#
    #######################################################

    Omni=root.addChild('Omni')
    Omni.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDevice.positionDevice")
    Omni.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")


    
    #########################################################
    #--------------------- INSTRUMENT ----------------------#
    #########################################################

    scalpelNode = root.addChild('scalpel')

    scalpelNode.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    scalpelNode.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    scalpelNode.addObject('MechanicalObject', name='mechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d_scalpel)

    scalpelNode.addObject('UniformMass', name='mass', totalMass="1")
    scalpelNode.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    scalpelNode.addObject('LCPForceFeedback', name="LCPFF1", activate="true", forceCoef="0.5")
    scalpelNode.addObject('UncoupledConstraintCorrection')

    # Visual node
    scalpelVisNode = scalpelNode.addChild('VisualModel')

    scalpelVisNode.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=scalpel_Instrument)
    
    scalpelVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@instrumentMeshLoader', ry="-180", rz="-90", dz="3.5", dx="-0.3",scale3d=scale3d_scalpel)
    scalpelVisNode.addObject('RigidMapping', name='MM-VM mapping', input='@../mechObject', output='@InstrumentVisualModel')

    # Collision node
    scalpelColNode = scalpelNode.addChild('CollisionModel')

    scalpelColNode.addObject('MeshObjLoader', filename=scalpel_Instrument, name='loader')
    scalpelColNode.addObject('MeshTopology', src='@loader', name='InstrumentCollisionModel')
    scalpelColNode.addObject('MechanicalObject', src='@InstrumentCollisionModel', name='instrumentCollisionState', ry="-180", rz="-90", dz="3.5", dx="-0.3", scale3d=scale3d_scalpel)
    scalpelColNode.addObject('RigidMapping', name='MM-CM mapping', input='@../mechObject', output='@instrumentCollisionState')

    #scalpelColNode.addObject('TriangleCollisionModel', name='instrumentTriangle', contactStiffness=10, contactFriction=10)
    scalpelColNode.addObject('LineCollisionModel', name='instrumentLine', contactStiffness=10, contactFriction=10)
    #scalpelColNode.addObject('PointCollisionModel', name='instrumentPoint', contactStiffness="10", contactFriction="10")


    return root



if __name__ == '__main__':
    main()
