# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import incision_models 
import suture_models
import random


scale3d_skin="0.7 0.4 1"
#scale3d_skin="0.25 0.65 0.1"
scale3d_scalpel="1 1 1 "

skinVolume_fileName="mesh\skin_30201"
#skinVolume_fileName="mesh/skin_volume_403020_05"
scalpel_Instrument="mesh\scalpel.obj"
# Collision particles positions
pointPosition_onscalpel1="8 -7.4 -17" 


# Choose in your script to activate or not the GUI
USE_GUI = True

# Define the variables
geomagic=True
carving=False

stiffness_springSkins=2000
skin_youngModulus=4000
thread_youngModulus=3000
skin_poissonRatio=0.1
thread_poissonRatio=0.8


stiffness_springNeedle=40
stiffness_springSkins=100

geomagic=True
carving=False



z_epi=3 #thickness=0.1mm youngModulus=1MPa
z_derma=z_epi*2 #thickness=1mm youngModulus=88-300kPa
z_hypo=z_epi*3 #thickness=1.2mm youngModulus=34kPa


scale3d_skin="0.25 0.65 0.1"
scale3d_needle="3 3 3"
scale3d_thread="0.5 0.5 0.5"

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

## This function creates the graph node.

def createScene(root):

    Config=open('C:/sofa/src/Chiara/Bats/Config.txt')
    for line in Config:
        pass
    user_name = line
    Config.close()
    fileNamePos=f"0_{user_name}_Incision1Pos"
    fileNameVel=f"0_{user_name}_Incision1Vel"
    fileNameForce=f"0_{user_name}_Incision1Force"

    # Define root properties
    root.gravity=[0, 0, -9]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")

    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="1.5", contactDistance="1", angleCone="0.1")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Add skin
    posx_left=6.5 #0<x<7
    posy=10 #10<y<22
    boxes=[10,11.5,13,14.5,16,17.5,19,20.5,22]

    skin_left=incision_models.SkinHexa(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 10.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, posy, -2, 7, posy+12, 0.1],  side=0, 
    borderBox1=[posx_left-1, boxes[0], -2, posx_left+1, boxes[1], 1],borderBox2=[posx_left-1, boxes[1], -2, posx_left+1, boxes[2], 1],borderBox3=[posx_left-1, boxes[2], -2, posx_left+1, boxes[3], 1],
    borderBox4=[posx_left-1, boxes[3], -2, posx_left+1, boxes[4], 1], borderBox5=[posx_left-1, boxes[4], -2, posx_left+1, boxes[5], 1],borderBox6=[posx_left-1, boxes[5], -2, posx_left+1, boxes[6], 1],
    borderBox7=[posx_left-1, boxes[6], -2, posx_left+1, boxes[7], 1],borderBox8=[posx_left-1, boxes[7], -2, posx_left+1, boxes[8], 1]
    )

    posx=posx_left+0.85 
    skin_right=incision_models.SkinHexa(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[posx, 10, 0], 
    scale3d=scale3d_skin, fixingBox=[posx, posy, -2, posx*2, posy+12, 0.1],  side=1, 
    borderBox1=[posx-0.5, boxes[0], -2, posx+1.5, boxes[1], 1],borderBox2=[posx-0.5, boxes[1], -2, posx+1.5, boxes[2], 1],borderBox3=[posx-0.5, boxes[2], -2, posx+1.5, boxes[3], 1],
    borderBox4=[posx-0.5, boxes[3], -2, posx+1.5, boxes[4], 1], borderBox5=[posx-0.5, boxes[4], -2, posx+1.5, boxes[5], 1],borderBox6=[posx-0.5, boxes[5], -2, posx+1.5, boxes[6], 1],
    borderBox7=[posx-0.5, boxes[6], -2, posx+1.5, boxes[7], 1],borderBox8=[posx-0.5, boxes[7], -2, posx+1.5, boxes[8], 1]
    )


    station_type="Single"
    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        if station_type=="Double\n":
            root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Right Device", scale="1", drawDeviceFrame="1", 
            drawDevice="1", positionBase="20 20 0",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@SutureNeedle/LCPFFNeedle")

            root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Left Device", scale="1", drawDeviceFrame="1", 
            drawDevice="1", positionBase="0 20 0",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@SutureNeedle/LCPFFNeedle")

            GeomagicDevice(parentNode=root, name='OmniRight', position="@GeomagicDeviceRight.positionDevice")
            GeomagicDevice(parentNode=root, name='OmniLeft', position="@GeomagicDeviceLeft.positionDevice")

        else: 
            root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", scale="1", drawDeviceFrame="1", 
            drawDevice="0", positionBase="10 13 10",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@SutureNeedle/LCPFFNeedle")
            
            GeomagicDevice(parentNode=root, name='Omni', position="@GeomagicDevice.positionDevice")

    #############################################################################################################

    # Add scalpel
    incision_models.ScalpelHexa(parentNode=root, name='Scalpel')#, monitor=True, file1=fileNamePos, file2=fileNameVel, file3=fileNameForce)

    # Add controller
    root.addObject(IncisionTaskTrainingController(root, skin_left, skin_right))
  
    
    return root



def ScalpelHexa(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0],
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
    Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796", dz="7", dx="-4", dy="-3",  rx="0", ry="0", rz="90")
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

    collFront2 = name.addChild('collFront2')
    collFront2.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5",  dz="4", dx="-4", dy="-4",  rx="0", ry="0", rz="90")
    collFront2.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1", tags="CarvingTool")
    collFront2.addObject('RigidMapping')#, template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    ScalpelHexa.MO=name.InstrumentMechObject
    # Scalpel.POS=name.InstrumentMechObject.findData('position').value
    #Scalpel.COLL_FRONT=name.Surf.Torus2Triangle.getLinkPath()
    ScalpelHexa.COLL_FRONT=name.collFront.SphereCollisionInstrument.getLinkPath()
    ScalpelHexa.COLL_FRONT2=name.collFront2.SphereCollisionInstrument2.getLinkPath()


## This function defines a geomagic touch device node.
# @param parentNode: parent node of the skin patch
# @param name: name of the behavior node
# @param rotation: rotation 
# @param translation: translation
def GeomagicDevice(parentNode=None, name=None, position=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position=position)
    name.addObject('MechanicalStateController', name="GEOMSC", template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")
    GeomagicDevice.MO=name.DOFs

    

def computeIndices(layer, z):
    result=' '
    indices = np.array(range(z*n_vertices_per_layer)).reshape(z,n_vertices_per_layer)

    for i in range(n_vertices_per_layer):
        if layer=="bottom":
            result += str(indices[0,i]) + " "
        elif layer=="top":
            result += str(indices[-1,i]) + " "

    return result
## Controller for incision task.

class IncisionTaskTrainingController(Sofa.Core.Controller):

    def __init__(self, root, skin_left, skin_right):
        Sofa.Core.Controller.__init__(self, root, skin_left, skin_right)
        self.contact_listener = root.addObject('ContactListener', collisionModel1 = incision_models.SkinHexa.COLL, collisionModel2 = incision_models.ScalpelHexa.COLL_FRONT)
        self.contact_listener_right = root.addObject('ContactListener', collisionModel1 = incision_models.SkinHexa.COLL_right, collisionModel2 = incision_models.ScalpelHexa.COLL_FRONT)
        self.contact_listener2 = root.addObject('ContactListener', collisionModel1 = incision_models.SkinHexa.COLL, collisionModel2 = incision_models.ScalpelHexa.COLL_FRONT2)
        self.contact_listener2_right = root.addObject('ContactListener', collisionModel1 = incision_models.SkinHexa.COLL_right, collisionModel2 = incision_models.ScalpelHexa.COLL_FRONT2)
        
        self.rootNode=root

        self.spring_force_field1 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)
        self.spring_force_field2 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)
        self.spring_force_field3 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)
        self.spring_force_field4 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)
        self.spring_force_field5 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)
        self.spring_force_field6 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)
        self.spring_force_field7 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)
        self.spring_force_field8 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.SkinHexa.MO,  object2=incision_models.SkinHexa.MO_right)


        self.ff1=True
        self.ff2=True
        self.ff3=True
        self.ff4=True
        self.ff5=True
        self.ff6=True
        self.ff7=True
        self.ff8=True
        

        self.first=1

       


    # # Uncomment to recompute indices
    def onAnimateBeginEvent(self, event): 
        if self.first==1:
            print(incision_models.SkinHexa.borderBox1_right.findData('indices').value)
            print(incision_models.SkinHexa.borderBox1.findData('indices').value)

            springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(incision_models.SkinHexa.borderBox1.findData('indices').value,incision_models.SkinHexa.borderBox1_right.findData('indices').value)] # Then set to right indices (the ones below)
            self.spring_force_field1.addSprings(springs)

            springs2 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in  zip(incision_models.SkinHexa.borderBox2.findData('indices').value,incision_models.SkinHexa.borderBox2_right.findData('indices').value)]
            self.spring_force_field2.addSprings(springs2)

            springs3 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in  zip(incision_models.SkinHexa.borderBox3.findData('indices').value,incision_models.SkinHexa.borderBox3_right.findData('indices').value)]
            self.spring_force_field3.addSprings(springs3)

            springs4 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in  zip(incision_models.SkinHexa.borderBox4.findData('indices').value,incision_models.SkinHexa.borderBox4_right.findData('indices').value)]
            self.spring_force_field4.addSprings(springs4)

            springs5 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in  zip(incision_models.SkinHexa.borderBox5.findData('indices').value,incision_models.SkinHexa.borderBox5_right.findData('indices').value)]
            self.spring_force_field5.addSprings(springs5)

            springs6 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in  zip(incision_models.SkinHexa.borderBox6.findData('indices').value,incision_models.SkinHexa.borderBox6_right.findData('indices').value)]
            self.spring_force_field6.addSprings(springs6)

            springs7 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in  zip(incision_models.SkinHexa.borderBox7.findData('indices').value,incision_models.SkinHexa.borderBox7_right.findData('indices').value)]
            self.spring_force_field7.addSprings(springs7)

            springs8 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in  zip(incision_models.SkinHexa.borderBox8.findData('indices').value,incision_models.SkinHexa.borderBox8_right.findData('indices').value)]
            self.spring_force_field8.addSprings(springs8)

            self.first=0

        #print(self.rootNode.GeomagicDevice.forceFeedBack)
        #print("1")
        #print(incision_models.SkinHexa.borderBox1.findData('triangleIndices').value)
        coll_indexes=self.contact_listener.getContactElements()
        coll_indexes_right=self.contact_listener_right.getContactElements()
        coll_indexes2=self.contact_listener2.getContactElements()
        coll_indexes2_right=self.contact_listener2_right.getContactElements()
        #print("Left top:", coll_indexes, " and right top: ", coll_indexes_right)#, "Left bottom:", coll_indexes2, " and right bottom: ", coll_indexes2_right)
        
        if coll_indexes!=[]:
            print("Contact left top")
            self.left_ff(coll_indexes)         
            
        elif coll_indexes_right!=[]:     
            print("Contact right top")
            self.right_ff(coll_indexes_right) 

        if coll_indexes2!=[] and coll_indexes==[]:
            print("Contact left bottom")
            self.left_ff(coll_indexes2)   

        elif coll_indexes2_right!=[] and coll_indexes_right==[]:     
            print("Contact right bottom")
            self.right_ff(coll_indexes2_right)  
            
    def left_ff(self, coll_indexes):   
        coll_indexes2=coll_indexes[0]
        coll_index_skin=coll_indexes2[1]
        print(coll_index_skin)
        print(incision_models.SkinHexa.borderBox1.findData('indices').value)
        if coll_index_skin in incision_models.SkinHexa.borderBox1.findData('indices').value and self.ff1==True:
            print("1")
            self.spring_force_field1.clear()
            self.ff1=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox2.findData('indices').value and self.ff2==True:
            print("2")
            self.spring_force_field2.clear()
            self.ff2=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox3.findData('indices').value and self.ff3==True:
            print("3")
            self.spring_force_field3.clear()
            self.ff3=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox4.findData('indices').value and self.ff4==True:
            print("4")
            self.spring_force_field4.clear()
            self.ff4=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox5.findData('indices').value and self.ff5==True:
            print("5")
            self.spring_force_field5.clear()
            self.ff5=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox6.findData('indices').value and self.ff6==True:
            print("6")
            self.spring_force_field6.clear()
            self.ff6=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox7.findData('indices').value and self.ff7==True:
            self.spring_force_field7.clear()
            self.ff7=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox8.findData('indices').value and self.ff8==True:
            self.spring_force_field8.clear()
            self.ff8=False
        else:
            print("Index does not belong to a border box")

    def right_ff(self, coll_indexes_right):
        coll_indexes2=coll_indexes_right[0]
        coll_index_skin=coll_indexes2[1]
        if coll_index_skin in incision_models.SkinHexa.borderBox1_right.findData('triangleIndices').value and self.ff1==True:
            self.spring_force_field1.clear()
            self.ff1=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox2_right.findData('triangleIndices').value and self.ff2==True:
            self.spring_force_field2.clear()
            self.ff2=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox3_right.findData('triangleIndices').value and self.ff3==True:
            self.spring_force_field3.clear()
            self.ff3=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox4_right.findData('triangleIndices').value and self.ff4==True:
            self.spring_force_field4.clear()
            self.ff4=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox5_right.findData('triangleIndices').value and self.ff5==True:
            self.spring_force_field5.clear()
            self.ff5=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox6_right.findData('triangleIndices').value and self.ff6==True:
            self.spring_force_field6.clear()
            self.ff6=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox7_right.findData('triangleIndices').value and self.ff7==True:
            self.spring_force_field7.clear()
            self.ff7=False
        elif coll_index_skin in incision_models.SkinHexa.borderBox8_right.findData('triangleIndices').value and self.ff8==True:
            self.spring_force_field8.clear()
            self.ff8=False
        else:
            print("Index does not belong to a border box")


    #     self.indices1=incision_models.SkinHexa.borderBox1.findData('indices').value
    #     self.indices2=incision_models.SkinHexa.borderBox2.findData('indices').value        
    #     self.indices3=incision_models.SkinHexa.borderBox3.findData('indices').value
    #     self.indices4=incision_models.SkinHexa.borderBox4.findData('indices').value
    #     self.indices5=incision_models.SkinHexa.borderBox5.findData('indices').value
    #     self.indices6=incision_models.SkinHexa.borderBox6.findData('indices').value        
    #     self.indices7=incision_models.SkinHexa.borderBox7.findData('indices').value
    #     self.indices8=incision_models.SkinHexa.borderBox8.findData('indices').value

    #     self.indices1_right=incision_models.SkinHexa.borderBox1_right.findData('indices').value
    #     self.indices2_right=incision_models.SkinHexa.borderBox2_right.findData('indices').value        
    #     self.indices3_right=incision_models.SkinHexa.borderBox3_right.findData('indices').value
    #     self.indices4_right=incision_models.SkinHexa.borderBox4_right.findData('indices').value
    #     self.indices5_right=incision_models.SkinHexa.borderBox5_right.findData('indices').value
    #     self.indices6_right=incision_models.SkinHexa.borderBox6_right.findData('indices').value        
    #     self.indices7_right=incision_models.SkinHexa.borderBox7_right.findData('indices').value
    #     self.indices8_right=incision_models.SkinHexa.borderBox8_right.findData('indices').value

    #     print("1L")
    #     print("[", self.computeIndices(self.indices1), "]")
    #     print("2L")
    #     print("[", self.computeIndices(self.indices2), "]")
    #     print("3L")
    #     print("[", self.computeIndices(self.indices3), "]")
    #     print("4L")
    #     print("[", self.computeIndices(self.indices4), "]")
    #     print("5L")
    #     print("[", self.computeIndices(self.indices5), "]")
    #     print("6L")
    #     print("[", self.computeIndices(self.indices6), "]")
    #     print("7L")
    #     print("[", self.computeIndices(self.indices7), "]")
    #     print("8L")
    #     print("[", self.computeIndices(self.indices8), "]")


        
    #     print("1R")
    #     print("[", self.computeIndices(self.indices1_right), "]")
    #     print("2R")
    #     print("[", self.computeIndices(self.indices2_right), "]")
    #     print("3R")
    #     print("[", self.computeIndices(self.indices3_right), "]")
    #     print("4R")
    #     print("[", self.computeIndices(self.indices4_right), "]")
    #     print("5R")
    #     print("[", self.computeIndices(self.indices5_right), "]")
    #     print("6R")
    #     print("[", self.computeIndices(self.indices6_right), "]")
    #     print("7R")
    #     print("[", self.computeIndices(self.indices7_right), "]")
    #     print("8R")
    #     print("[", self.computeIndices(self.indices8_right), "]")


    # def computeIndices(self, indicesBox):
    #     N_indices=len(indicesBox)
    #     result=' '  

    #     for i in range(N_indices):
    #         result += str(indicesBox[i]) + ", "

    #     return result

     


if __name__ == '__main__':
    main()
