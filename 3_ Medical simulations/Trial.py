# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
#from goto import goto, label
import subprocess
import ctypes
# Data

scale3d_skin="0.25 0.65 0.1"
scale3d_needle="3 3 3"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="C:\sofa\src\Chiara\mesh\skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="C:\sofa\src\Chiara\mesh\suture_needle.obj"
threadVolume_fileName="C:\sofa\src\Chiara\mesh\threadCh2"

# Data
skin_youngModulus=4000#300
thread_youngModulus=2000
skin_poissonRatio=0.1
thread_poissonRatio=0.8


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
stiffness_springNeedle=40
stiffness_springSkins=100

geomagic=True
carving=False


x_vertices=10
y_vertices=10

x_offset=-10
y_offset=-10
z_offset=-20

x_length=20+x_offset
y_length=20+y_offset
n_vertices_per_layer=x_vertices*y_vertices

z_epi=3 #thickness=0.1mm youngModulus=1MPa
z_derma=z_epi*2 #thickness=1mm youngModulus=88-300kPa
z_hypo=z_epi*3 #thickness=1.2mm youngModulus=34kPa



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

    # Read user name
    Config=open('D:\Thesis\GUI\Config.txt')
    for line in Config:
        pass
    user_name = line
    Config.close()

    # Read user data (last lines of the file)
    fileName=f"D:\Thesis\GUI\{user_name}.txt"
    User=open(fileName)
    lines1=User.readlines()
    lines=lines1[-5:] #put 4 LATER
    station_type=lines[3]
    User.close()

    # Define root properties
    root.gravity=[0, 0, -2]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaCarving SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    #root.addObject('VisualStyle', displayFlags="showInteractionForceFields")

    root.addObject('OglLabel', label="SUTURE TASK - TRAINING", x=20, y=20, fontsize=30, selectContrastingColor="1")
    root.addObject('OglLabel', label="Pierce the skin in correnspondence of the green spheres", x=20, y=70, fontsize=20, selectContrastingColor="1")
    root.addObject('OglLabel', label="starting from the one closest to the needle", x=20, y=100, fontsize=20, selectContrastingColor="1")


    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="2", contactDistance="1.2", angleCone="0.0")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    LCPConstraintSolver=root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # View
    root.addObject('OglViewport', screenPosition="0 0", cameraPosition="-0.00322233 -20.3537 18.828", cameraOrientation="0.418151 -6.26277e-06 -0.000108372 0.908378")


    # Define the variables

########################################################

    # Add skin
    # Add skin
    x=[8,8,12,12]
    y=[3,11,7,15]
    z=3

    skin_left=Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 16.5, 0.1], 
    sphere1Box=[x[0]-2, y[0]-2, -0.1, x[0]+2, y[0]+2, 3], sphere2Box=[x[1]-2, y[1]-2, -0.1, x[1]+2, y[1]+2, 3])

    station_type="Single\n"
    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", 
        drawDevice="0", positionBase="10 13 10",  orientationBase="0.707 0 0 0.707", tags="Omni", forceFeedBack="@Scalpel/LCPFFScalpel")
        
        GeomagicDevice(parentNode=root, name='Omni', position="@GeomagicDevice.positionDevice")

    #############################################################################################################
    # Add needle
    #SutureNeedle(parentNode=root, name='SutureNeedle', monitor=True, file1="SutureTask_pos", file2="SutureTask_vel", file3="SutureTask_force", geomagic=geomagic, dx=0, dy=0, dz=10) # To fall on sphere: dx=12, dy=3, dz=6
    Scalpel(parentNode=root, name='Scalpel',  geomagic=geomagic)
    root.addObject(SutureTaskTrainingController(name="MyController", rootNode=root))
    print(GeomagicDevice.DOFs.findData('force').value)

def computeIndices(layer, z):
    result=' '
    indices = np.array(range(z*n_vertices_per_layer)).reshape(z,n_vertices_per_layer)

    for i in range(n_vertices_per_layer):
        if layer=="bottom":
            result += str(indices[0,i]) + " "
        elif layer=="top":
            result += str(indices[-1,i]) + " "

    return result
    
def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0],
side=0, sphere1Box=[0.0, 0.0, 0.0], sphere2Box=[0.0, 0.0, 0.0],sphere3Box=[0.0, 0.0, 0.0],sphere4Box=[0.0, 0.0, 0.0]):

    epi=parentNode.addChild('epi')
    epi.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="0.01")
    epi.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    #epi.addObject('SparseLDLSolver')

    epi.addObject('MechanicalObject', template="Vec3d", name="EpiMechObj", scale3d="2 1 0.2", position="0 0 -8", showVectors="true", drawMode="2")
    #epi.addObject('MechanicalObject', template="Vec3d", name="EpiMechObj", scale3d="1 1 1", position="0 0 -2", showVectors="true", drawMode="2")

    epi.addObject('RegularGridTopology', name="grid", nx=x_vertices, ny=y_vertices, nz=z_epi, xmin=x_offset, xmax=x_length, ymin=y_offset, ymax=y_length, zmin=z_derma+z_hypo+z_offset, zmax=(z_hypo+z_derma+z_epi+z_offset+1))
    epi.addObject('HexahedronSetGeometryAlgorithms')
    
    #epi.addObject('DiagonalMass', template="Vec3d,double", name="Mass", massDensity="1.0")
    epi.addObject('UniformMass', template="Vec3d,double", name="EpiMass", totalMass="10")
    epi.addObject('HexahedronFEMForceField', template="Vec3d", name="FEM", poissonRatio=skin_poissonRatio, youngModulus=skin_youngModulus )
    #epi.addObject('GenericConstraintCorrection')
    #epi.addObject('LinearSolverConstraintCorrection')
    epi.addObject('UncoupledConstraintCorrection')

    # WORKING WITH ONE LAYER ONLY
    epi.addObject('FixedConstraint', template="Vec3d", name="Fixed Dofs", indices=computeIndices("bottom", z_epi))
    epi.addObject('FixedPlaneConstraint', template="Vec3d", name="defaultPlane", direction="0 0 1", dmin="0")

    # Hexa -> Quad
    quad=epi.addChild('quad')
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
    tri.addObject('TriangleCollisionModel', name="EpiCollision", contactStiffness="0.01")
    #tri.addObject('TriangleCollisionModel', name="EpiCollision", contactStiffness="0.01", tags="CarvingSurface") #CARVING

    visu=tri.addChild('visu') 
    visu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    visu.addObject('OglViewport', screenPosition="0 0", screenSize="250 250", cameraPosition="-0.285199 -15.2745 16.7859", cameraOrientation="0.394169 0.0120415 0.00490558 0.918946" )
    visu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )


    return name



def GeomagicDevice(parentNode=None, name=None, position=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position=position)
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="0.0 0.0 -1.0", handleEventTriggersUpdate="true")
    # ReferenceModel=name.addChild("ReferenceModel")
    # ReferenceModel.addObject("MeshObjLoader", filename=needleVolume_fileName,  name="loader")
    # ReferenceModel.addObject("MeshTopology", src="@loader" )
    # ReferenceModel.addObject("MechanicalObject", src="@loader", name="instrumentRefState1",  rx="-10", ry="160", rz=120,  dz="0", dx="0", dy="0")
    # ReferenceModel.addObject("RigidMapping")
    GeomagicDevice.DOFs=name.DOFs
    #GeomagicDevice.instrumentRefState1=name.ReferenceModel.instrumentRefState1


def SutureNeedle(parentNode=None, name=None, dx=0, dy=0, dz=0, scale3d=[0.0, 0.0, 0.0], 
geomagic=False, position="@GeomagicDevice.positionDevice", external_rest_shape='@../Omni/DOFs', # position and external_rest_shape are set by default for the single station case 
monitor=False, file1=None, file2=None, file3=None): # If plots are desired: save results in three different files
    rz=120
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position=position, scale3d="2", rotation="0 0 10", tags="Omni" ) #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', name="InstrumentRestShape", stiffness='100', angularStiffness='100', external_rest_shape=external_rest_shape, points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.007", activate="true")# Decide forceCoef value better
        SutureNeedle.RS=name.InstrumentRestShape
        #sname.addObject('TriangleFEMForceField', name='FEM', method='large', youngModulus=1, poissonRatio=0.5)
    else: 
        name.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale="2.0" ,dx=dx, dy=dy, dz=dz)
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/Suture_needle.obj", scale="2.0", handleSeams="1" )
    if geomagic==True:
        Visu.addObject('OglModel',name="Visual", src='@meshLoader_3', rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0",  color="0 0.5 0.796")
    else:
        Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/Suture_needle.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    if geomagic==True:
        Surf.addObject('MechanicalObject' ,name="InstrumentMechObject", src="@loader", scale="2.0", rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0") #rz=180
    else: 
        Surf.addObject('MechanicalObject' ,src="@loader", scale="2.0")#, dx="8", dy="3", dz="6")
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point", contactStiffness="10")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront') #"-4.2 0.02 -0.25" for scale5
    if geomagic==True:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-2.9 0.02 -0.25", rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0")
    else:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-4.2 0.02 -0.25")

    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument")#, contactStiffness="2", tags="CarvingTool")


    collFront.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    collBack = name.addChild('collBack') #"0 0.007 -0.25" for scale5
    if geomagic==True:
        collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25", rx="-10", ry="160", rz=rz,  dz="0", dx="0", dy="0")
    else:
        collBack.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.007 -0.25")
    collBack.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2")#, contactStiffness="2")
    collBack.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")


    name.addObject("VectorSpringForceField",   object1="@Omni/ReferenceModel/instrumentRefState1", object2="@SutureNeedle/Surf/InstrumentMechObject", stiffness="50", viscosity="0" )


def Scalpel(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0],
geomagic=False): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager

    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")

    name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale="1.0", rotation="0 0 10",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90") #, src="@instrumentMeshLoader")
    #name.addObject("Monitor", input="@InstrumentMechObject", name="ooooooooooooo", indices="0", listening="1", showForces="1", ExportForces="true")
    name.addObject('RestShapeSpringsForceField', stiffness='100', angularStiffness='100', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
    name.addObject('LCPForceFeedback', name="LCPFFScalpel",  forceCoef="0.007", activate="true")# Decide forceCoef value better

    name.addObject('UniformMass' , totalMass="6")
    name.addObject('UncoupledConstraintCorrection')
    

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/scalpel.obj", scale="1.0", handleSeams="1" )
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    Surf.addObject('TriangleCollisionModel', name="Torus2Triangle")# , contactStiffness="2")#, tags="CarvingTool")
    Surf.addObject('LineCollisionModel', name="Torus2Line" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('PointCollisionModel' ,name="Torus2Point" , contactStiffness="1000")#, tags="CarvingTool")
    Surf.addObject('RigidMapping')
    

    collFront = name.addChild('collFront')
    collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="2", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
    #collFront.addObject('UniformMass', totalMass="0.01")
    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", tags="CarvingTool")
    collFront.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    # collFront2 = name.addChild('collFront2')
    # collFront2.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="4", dx="-4", dy="-4",  rx="0", ry="0", rz="90")
    # collFront2.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1", tags="CarvingTool")
    # collFront2.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    Scalpel.MO=name.InstrumentMechObject
    # Scalpel.POS=name.InstrumentMechObject.findData('position').value
    # Scalpel.COLL_FRONT=name.Surf.Torus2Triangle.getLinkPath()
    # #Scalpel.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    # Scalpel.COLL_FRONT2=name.collFront2.SphereCollisionInstrument2.getLinkPath()

class SutureTaskTrainingController(Sofa.Core.Controller):
    
    ## Constructor of the class. 
    # @param name: name of the controller
    # @param rootnode: path to the root node of the simulation
    # @param skin_left: path to the left skin patch root node
    # @param skin_right: path to the right skin patch root node
    # Defines the contact listeners between spheres and the needle and creates the 4 force fields 
    
    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)

        self.root=rootNode
    ## Method called at each begin of animation step
    # @param event: animation step event
    # If a contact between the needle tip and one of the skin patches, the function retrieves the skin triangle index of contact and 
    # checks if it belongs to one of the sphere boxes. If it does and no springs already exist between the needle and that skin patch,
    # it checks if springs exist between the needle and the other skin patch. If they do, the patches get connected by springs, 
    # the former springs needle-skin are removed. Then the new needle-skin springs are created. 
    # Finally, the color of the sphere is changed from red to green adn the user points are increased.
    # At the end of the function, the last needle-skin springs are removed on button press.

    #def onAnimateBeginEvent(self, event):
        #print("1")
        #print(self.root.GeomagicDevice.findData('forceFeedBack').value)
        #print("2")
        #print(self.root.GeomagicDevice.forceFeedBack.get())
        #print("3")
        #print(self.root.GeomagicDevice.forceFeedBack.getValue())
        #print(GeomagicDevice.DOFs.findData('force').value)
        
        #print(Scalpel.MO.findData('force').value)
        #print(GeomagicDevice.instrumentRefState1.findData('force').value)