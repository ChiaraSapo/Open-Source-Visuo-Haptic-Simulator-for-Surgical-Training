# Required import for python
import Sofa
import numpy as np



poissonRatio_ALL=0.48
youngModulus_H=3400
youngModulus_D=300
youngModulus_E=1000
# Scales
scale3d_skin="80 50 20"
scale3d_scalpel="2 2 2"
# Model files
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skinVolume2"
scalpel_Instrument="mesh\scalpel.obj"
# Collision particles positions
pointPosition_onscalpel1="8 -7.4 -17" 
pointPosition_onscalpel2="7 -7.4 -16" 
pointPosition_onscalpel3="6.5 -7.4 -15" 
pointPosition_onscalpel4="6 -7.4 -14" 
r=0.4

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
    #root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", drawDevice="1", positionBase="0 0 8",  orientationBase="0.707 0 0 0.707")
    
    # Carving
    #root.addObject('CarvingManager', active="true", carvingDistance="0.1") #CARVING

    '''
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



    '''
    
    ######################################################
    #--------------------- SCALPEL ----------------------#
    ######################################################

    scalpelNode = root.addChild('scalpel')

    #scalpelNode.addObject('EulerImplicitSolver', name='ODE solver', rayleighStiffness="0.01", rayleighMass="1.0")
    #scalpelNode.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    scalpelNode.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=scalpel_Instrument)
    scalpelNode.addObject('MechanicalObject', src="@instrumentMeshLoader", name='mechObject', template='Rigid3d', translation="10 15 60 ",  scale3d=scale3d_scalpel)
    scalpelNode.addObject('UniformMass', name='mass', totalMass="2")

    # Visual node
    scalpelVisNode = scalpelNode.addChild('VisualModel')

    scalpelVisNode.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d_scalpel, color="0 0.5 0.796")
    scalpelVisNode.addObject('RigidMapping', name='MM-VM mapping', input='@../mechObject', output='@InstrumentVisualModel')

    # Collision node1
    scalpelColNode1 = scalpelNode.addChild('CollisionModel1')
    
    scalpelColNode1.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel1)
    scalpelColNode1.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode1.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")
    
    # Collision node2
    scalpelColNode2 = scalpelNode.addChild('CollisionModel2')
    
    scalpelColNode2.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel2)
    scalpelColNode2.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode2.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")

    # Collision node3
    scalpelColNode3 = scalpelNode.addChild('CollisionModel3')
    
    scalpelColNode3.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel3)
    scalpelColNode3.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode3.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")

    # Collision node4
    scalpelColNode4 = scalpelNode.addChild('CollisionModel4')
    
    scalpelColNode4.addObject('MechanicalObject', template="Vec3d", name="Particle", position=pointPosition_onscalpel4)
    scalpelColNode4.addObject('SphereCollisionModel', radius=r, name="ParticleModel", contactStiffness="2", tags="CarvingTool")
    scalpelColNode4.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../mechObject",  output="@Particle")

    return root



if __name__ == '__main__':
    main()
