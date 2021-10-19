# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
#from goto import goto, label
import subprocess
import ctypes
# Data





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
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaCarving SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    root.addObject('OglLabel', label="TOUCH THE CUBE", x=20, y=20, fontsize=30, selectContrastingColor="1")
    root.addObject('ViewerSetting', fullscreen="true")
    root.addObject('BackgroundSetting', color="0.3 0.5 0.8")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="1", contactDistance="0.2", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # View
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")

    root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Default Device", scale="1", drawDeviceFrame="0", 
    drawDevice="0", positionBase="2 2 10",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@StraightNeedleLeft/LCPFFNeedle")

    # Add geomagic nodes
    GeomagicDevice(parentNode=root, name='OmniLeft', position="@GeomagicDeviceLeft.positionDevice")
    
    # Add needles
    suture_models.StraightNeedleLeft(parentNode=root, name='StraightNeedleLeft', monitor=False, position="@GeomagicDeviceLeft.positionDevice", external_rest_shape='@../OmniLeft/DOFs') # To fall on sphere: dx=12, dy=3, dz=6

    cube(parentNode=root, name="cube")

    
def cube(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0]):
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")

    name.addObject('MechanicalObject', template="Vec3d", name="EpiMechObj", scale3d="0.7 0.7 0.7", position="0 0 -8", showVectors="true", drawMode="2")
    name.addObject('RegularGridTopology', name="grid", nx=3, ny=3, nz=2, xmin=-5, xmax=5, ymin=-5, ymax=5, zmin=-5, zmax=5)
    name.addObject('HexahedronSetGeometryAlgorithms')
    
    name.addObject('UniformMass', template="Vec3d,double", name="EpiMass", totalMass="5")
    name.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=10, youngModulus=100)
    name.addObject('UncoupledConstraintCorrection')
    name.addObject('BoxROI', name='boxROI', box=[-5.1, -5.1, -5.1, 5, 5, ], drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Hexa -> Quad
    quad=name.addChild('quad')
    quad.addObject('QuadSetTopologyContainer', name="Q_Container")
    quad.addObject('QuadSetTopologyModifier', name="Q_Modifier")
    quad.addObject('QuadSetGeometryAlgorithms', template="Vec3d", name="Q_GeomAlgo")
    quad.addObject('Hexa2QuadTopologicalMapping', name="default6", input="@../grid", output="@Q_Container")

    # Quad -> Tri
    tri=quad.addChild('tri')
    tri.addObject('TriangleSetTopologyContainer', name="T_Container")
    tri.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    tri.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    tri.addObject('Quad2TriangleTopologicalMapping', name="default8", input="@../Q_Container", output="@T_Container")
    
    # Triangle collision model
    tri.addObject('TriangleCollisionModel', name="TriangleCollisionSkin", contactStiffness="100")

    visu=tri.addChild('visu') 
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="0.7 0.5 0.8", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )


    
## This function defines a geomagic
# @param parentNode: parent node of the skin patch
# @param name: name of the behavior node
# @param rotation: rotation 
# @param translation: translation
def GeomagicDevice(parentNode=None, name=None, position=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position=position)
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")

def Tool(parentNode=None, name=None):
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
    name.addObject('RestShapeSpringsForceField', stiffness='100', angularStiffness='100', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFScalpel",  forceCoef="0.007", activate="true")# Decide forceCoef value better
    name.addObject('UniformMass' , totalMass="6")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="C:\sofa\src\Chiara\mesh\straight_needle.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="7", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="C:\sofa\src\Chiara\mesh\straight_needle.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle")# , contactStiffness="2")#, tags="CarvingTool")
    Surf.addObject('LineCollisionModel', name="Torus2Line" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('RigidMapping')
    