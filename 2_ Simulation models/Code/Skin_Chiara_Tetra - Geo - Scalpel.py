# Required import for python
import Sofa
import numpy as np


# Scales
scale3d_skin="0.5 0.3 0.5"
#scale3d_skin="50 30 5"
scale3d_scalpel="1 1 1"
# Model files
skinVolume_fileName="mesh\skinVolume7"
scalpel_Instrument="mesh\scalpel.obj"
# Collision particles positions
pointPosition_onscalpel1="4 -3.7 -8.5" 
pointPosition_onscalpel2="3.5 -3.7 -8" 
pointPosition_onscalpel3="3.25 -3.7 -7.5" 
pointPosition_onscalpel4="3 -3.7 -7" 
total="4 -3.7 -8.5   3.5 -3.7 -8   3.25 -3.7 -7.5   3 -3.7 -7" 
r=0.4
# Geomagic
GeomagicPosition="0 20 10"

vol7=" -25 -5 0"
vol2=" 0 -5 0"

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
    root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", drawDevice="1", positionBase=GeomagicPosition,  orientationBase="0.707 0 0 0.707")
    
    # Carving
    root.addObject('CarvingManager', active="true", carvingDistance="0.1") #CARVING
    
    #########################################################
    #--------------------- SKIN LAYER ----------------------#
    #########################################################
    

    #################### BEHAVIOUR ##########################
    
    skin = root.addChild('skin')
    
    # Solvers
    skin.addObject('EulerImplicitSolver', name="odesolver")
    skin.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    
    # Volumetric mesh loader
    skin.addObject('MeshGmshLoader', name='volumeLoader', filename=skinVolume_fileName, scale3d=scale3d_skin, translation=vol7)
    #skin.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    skin.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer')#,  template='Vec3d')
    skin.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    skin.addObject('TetrahedronSetTopologyModifier')

    # Mechanical object
    skin.addObject('MechanicalObject', name='SkinMechObj', template='Vec3d')#, src="@volumeLoader", position="1 1 20")#, showIndices='true')

    # Mass
    skin.addObject('DiagonalMass', name="SkinMass", template="Vec3d,double", massDensity="1.0")

    # Constraints: check to have not overconstrained the skin!
    skin.addObject('BoxROI', name='boxROI', box='-30 -30 -2 30 70 2', drawBoxes='true')
    skin.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    skin.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus='800', poissonRatio='0.49')
    skin.addObject('MeshSpringForceField', name="FEM-Bend", template="Vec3d", stiffness="100", damping="1")
    skin.addObject('UncoupledConstraintCorrection')


    #################### COLLISION ##########################

    skinCollis = skin.addChild('skinCollis')

    # Mapped from the tetra of behaviour model
    skinCollis.addObject('TriangleSetTopologyContainer', name="T_Container")
    skinCollis.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    skinCollis.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    skinCollis.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")

    # Types of collision
    skinCollis.addObject('TriangleCollisionModel', tags="CarvingSurface")
    skinCollis.addObject('LineCollisionModel')#, tags="CarvingSurface")
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
    scalpelNode.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=scalpel_Instrument)
    scalpelNode.addObject('MechanicalObject', src="@instrumentMeshLoader", name='mechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice",  scale3d=scale3d_scalpel)#, rotation="0 0 -90")
    scalpelNode.addObject('UniformMass', name='mass', totalMass="2")
    scalpelNode.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    scalpelNode.addObject('LCPForceFeedback', name="LCPFF1", activate="true", forceCoef="0.5")
    scalpelNode.addObject('UncoupledConstraintCorrection')

    # Visual node
    scalpelVisNode = scalpelNode.addChild('scalpelVisNode')

    scalpelVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d_scalpel, dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90", color="0 0.5 0.796")
    scalpelVisNode.addObject('RigidMapping', name='MM-VM mapping', input='@../mechObject', output='@InstrumentVisualModel')

    # Collision node1
    scalpelColNode1 = scalpelNode.addChild('scalpelColNode1')
    
    scalpelColNode1.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel1, dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    #scalpelColNode1.addObject('SphereCollisionModel', radius=r, name="ParticleModel1", contactStiffness="2", tags="CarvingTool")
    scalpelColNode1.addObject('PointCollisionModel', name="ParticleModel1", contactStiffness="1", tags="CarvingTool")

    scalpelColNode1.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")
    '''
    # Collision node2
    scalpelColNode2 = scalpelNode.addChild('scalpelColNode2')
    
    scalpelColNode2.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel2,rx="180", ry="180", rz="180",  dz="2", dx="-4", dy="4")
    scalpelColNode2.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2")#, tags="CarvingTool")
    scalpelColNode2.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")

    # Collision node3
    scalpelColNode3 = scalpelNode.addChild('scalpelColNode3')
    
    scalpelColNode3.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel3,rx="180", ry="180", rz="180",  dz="2", dx="-4", dy="4")
    scalpelColNode3.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2")#, tags="CarvingTool")
    scalpelColNode3.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")

    # Collision node4
    scalpelColNode4 = scalpelNode.addChild('scalpelColNode4')
    
    scalpelColNode4.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel4,rx="180", ry="180", rz="180",  dz="2", dx="-4", dy="4")
    scalpelColNode4.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2")#, tags="CarvingTool")
    scalpelColNode4.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")


    CollHexa=scalpelNode.addChild('CollHexa')
    CollHexa.addObject('MechanicalObject', template="Vec3d", name="HexaMechObj", position="0 0 0")
    CollHexa.addObject('RegularGridTopology', name="grid", nx=10, ny=10, nz=2, xmin=-10, xmax=10, ymin=-10, ymax=10, zmin=-2, zmax=2)
    Coll=CollHexa.addChild('Coll')
    Coll.addObject('MechanicalObject', template="Vec3d", position=pointPosition_onscalpel4)
    Coll.addObject('LineCollisionModel', contactStiffness="2")
    '''
    return root



if __name__ == '__main__':
    main()
