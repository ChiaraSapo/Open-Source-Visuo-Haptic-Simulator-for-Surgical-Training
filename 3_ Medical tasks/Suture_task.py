# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import models
import controllers


# Data
#scale3d_skin="0.2 0.3 1" #thin
#scale3d_skin="1 0.6 1"
scale3d_skin="0.25 0.65 0.1"
scale3d_needle="5 5 5"
scale3d_thread="0.5 0.5 0.5"

pointPosition_onNeedle="-6.98 0.02 0.05" #N: 5,5,5

GeomagicPosition="0 20 15"
skinVolume_fileName="mesh\skin_volume_403020_05" #03 troppo lento
needleVolume_fileName="mesh\suture_needle.obj"
threadVolume_fileName="mesh\threadCh2"

# Data
skin_youngModulus=1500#300
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
    root.gravity=[0, 0, -5]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")

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
    geomagic=False
    carving=False

    #################### CARVING ########s#####################################
    if carving==True:
        root.addObject('CarvingManager', active="true", carvingDistance="0.1")
    ##########################################################################

    # Add skin
    Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[7, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName, carving=carving, task="Suture")

    Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[11, -0.1, -2, 22, 20, 0.1], borderBox=[11, -0.1, -2, 14, 20, 1],
    importFile=skinVolume_fileName, carving=carving, side=1, task="Suture") 



    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="0", positionBase="10 9 10",  orientationBase="0.707 0 0 0.707")
        
        GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################


    # Add needle
    SutureNeedle(parentNode=root, name='SutureNeedle', rotation=[0.0, 0.0, 0.0], translation=[14, 2, 5],     
    scale3d=scale3d_needle, fixingBox=None, importFile=needleVolume_fileName, carving=carving, geomagic=geomagic)

    # # # Add thread: not added to Geo yet
    # # Thread(parentNode=root, name='SutureThread', rotation=[-90, 90, 0], translation=[10, 10, 5], 
    # # scale3d=[0.5, 0.5, 0.6],  fixingBox=None, importFile=threadVolume_fileName, geomagic=geomagic)

    # # Add contact listener
    root.addObject(SutureTrainingContactController(name="MyController", rootNode=root))

    # # Add training spheres: add when necessary
    sphere(parentNode=root, name="Sphere1", translation=[8, 3.0, 3.0], scale3d="1.5 1.5 1.5", color=[0.0, 0.5, 0.0])
    sphere(parentNode=root, name="Sphere2", translation=[8, 13.0, 3.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    sphere(parentNode=root, name="Sphere3", translation=[12, 7.0, 3.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")
    sphere(parentNode=root, name="Sphere4", translation=[12, 17.0, 3.0], scale3d="1.5 1.5 1.5", color="0.0 0.5 0.0")


    return root



# Training sphere
def sphere(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    name.addObject('MeshObjLoader', name='sphere', filename="C:\sofa\src\Chiara\mesh\sphere.obj") 
    name.addObject('OglModel', name='sphereVis', src='@sphere', scale3d="0.8 0.8 0.8", translation=translation, color=color)
    sphere.M=name.sphereVis.getLinkPath()
    sphere.color=name.sphereVis.findData('scale3d').value
   
  
def Skin(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], indicesBox=[0.0, 0.0, 0.0], borderBox=[0.0, 0.0, 0.0], importFile=None, 
carving=False, side=0, task=None, borderBox1=[0.0, 0.0, 0.0],borderBox2=[0.0, 0.0, 0.0],borderBox3=[0.0, 0.0, 0.0],borderBox4=[0.0, 0.0, 0.0]):

    name=parentNode.addChild(name)
    
    #################### BEHAVIOUR ##########################
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver", rayleighStiffness="0.01", rayleighMass="0.01") #added  2 params
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    #name.addObject('SparseLDLSolver')

    # Volumetric mesh loader
    name.addObject('MeshGmshLoader', name='volumeLoader', filename=importFile, scale3d=scale3d)

    # Tetrahedra container
    name.addObject('TetrahedronSetTopologyContainer', src='@volumeLoader', name='TetraContainer')
    name.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TetrahedronSetTopologyModifier') # Leave it there for the carving plugin!

    # Mechanical object and mass
    name.addObject('MechanicalObject', name='SkinMechObj', src='@volumeLoader', template='Vec3d', translation=translation) #added src for trial
    name.addObject('DiagonalMass', name="SkinMass", massDensity="2.0")#, template="Vec3d,double"

    # Forces
    name.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=skin_youngModulus, poissonRatio=skin_poissonRatio)
    name.addObject('UncoupledConstraintCorrection', compliance=0.001)
    #name.addObject('LinearSolverConstraintCorrection')

    # Fixed box for constraints
    boxROI=name.addObject('BoxROI', name='boxROI', box=fixingBox, drawBoxes='true', computeTriangles='true')
    name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    # Border box
    name.addObject('BoxROI', name='borderBox', box=borderBox, drawBoxes='true')
    
    if task=="Incision":
        name.addObject('BoxROI', name='borderBox1', box=borderBox1, drawBoxes='true')
        name.addObject('BoxROI', name='borderBox2', box=borderBox2, drawBoxes='true')
        name.addObject('BoxROI', name='borderBox3', box=borderBox3, drawBoxes='true')
        name.addObject('BoxROI', name='borderBox4', box=borderBox4, drawBoxes='true')

    if task=="Suture":
        name.addObject('BoxROI', name='sphere1Box', box=[8-2, 3-2, -0.1, 8+2, 3+2, 3], drawBoxes='true', computeTriangles='true')
        name.addObject('BoxROI', name='sphere2Box', box=[8-2, 13-2, -0.1, 8+2, 13+2, 3], drawBoxes='true', computeTriangles='true')
        name.addObject('BoxROI', name='sphere3Box', box=[12-2, 7-2, -0.1, 12+2, 7+2, 3], drawBoxes='true', computeTriangles='true')
        name.addObject('BoxROI', name='sphere4Box', box=[12-2, 17-2, -0.1, 12+2, 17+2, 3], drawBoxes='true', computeTriangles='true')  



    #################### COLLISION ##########################

    SkinColl = name.addChild('SkinColl')

    # Mapped from the tetra of behaviour model
    SkinColl.addObject('TriangleSetTopologyContainer', name="T_Container")
    SkinColl.addObject('TriangleSetTopologyModifier', name="T_Modifier")
    SkinColl.addObject('TriangleSetGeometryAlgorithms', template="Vec3d", name="T_GeomAlgo")
    SkinColl.addObject('Tetra2TriangleTopologicalMapping', name="default8", input="@../TetraContainer", output="@T_Container")
    #SkinColl.addObject('MechanicalObject', template="Vec3d")

    # Types of collision
    if carving==True:
        SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin", tags="CarvingSurface")
    else: 
        SkinColl.addObject('TriangleCollisionModel', name="TriangleCollisionSkin")

    #SkinColl.addObject('LineCollisionModel', name="LineCollisionSkin")
    #SkinColl.addObject('PointCollisionModel', name="PointCollisionSkin") 
    #SkinColl.addObject('IdentityMapping')

    #################### VISUALIZATION ########################
    
    SkinVisu = SkinColl.addChild('SkinVisu')
    SkinVisu.addObject('MechanicalObject', name="VisuMO")
    SkinVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", 
    material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    #SkinVisu.addObject('BarycentricMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" ) # For grids
    SkinVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )

    # Data
    if side==0: # left
        Skin.itself=name.getLinkPath()
        Skin.MO=name.SkinMechObj.getLinkPath()
        Skin.COLL=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.borderBox= name.borderBox
        if task=="Suture":
            Skin.sphere1Box=name.sphere1Box
            Skin.sphere2Box=name.sphere2Box
        if task=="Incision":
            Skin.borderBox1=name.borderBox1
            Skin.borderBox2=name.borderBox2
            Skin.borderBox3=name.borderBox3
            Skin.borderBox4=name.borderBox4

    if side==1: # right
        Skin.itself_right=name.getLinkPath()
        Skin.MO_right=name.SkinMechObj.getLinkPath()
        Skin.COLL_right=name.SkinColl.TriangleCollisionSkin.getLinkPath()
        Skin.borderBox_right = name.borderBox
        if task=="Suture":
            Skin.sphere3Box=name.sphere3Box
            Skin.sphere4Box=name.sphere4Box
        if task=="Incision":
            Skin.borderBox1_right=name.borderBox1
            Skin.borderBox2_right=name.borderBox2
            Skin.borderBox3_right=name.borderBox3
            Skin.borderBox4_right=name.borderBox4
    Skin.CONTAINER=name.TetraContainer.getLinkPath()





def Thread(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
scale3d=[0.0, 0.0, 0.0], fixingBox=[0.0, 0.0, 0.0], importFile=None, geomagic=False):

    name=parentNode.addChild(name)

    #################### BEHAVIOUR ##########################
    
    # Solvers
    name.addObject('EulerImplicitSolver', name="odesolver")
    name.addObject('CGLinearSolver', iterations="25", name="EpiLinearsolver", tolerance="1.0e-9", threshold="1.0e-9")
    name.addObject('MeshGmshLoader', name='name_volumeLoader', filename=importFile, scale3d=scale3d, rotation=rotation, translation=translation)
    #name.addObject('MeshTopology', src='@volumeLoader')

    # Tetrahedra container
    name.addObject('TriangleSetTopologyContainer', src='@name_volumeLoader')
    name.addObject('TriangleSetGeometryAlgorithms', template='Vec3d')
    name.addObject('TriangleSetTopologyModifier')

    # Mechanical object and mass
    if geomagic==True:
        name.addObject('MechanicalObject', name='ThreadMechObject', template='Vec3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d, rotation="0 0 0" )
        #name.addObject('RestShapeSpringsForceField', name="ThreadRest", stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        #name.addObject('LCPForceFeedback', name="LCPFFThread", activate="true", forceCoef="0.5")
    else:
        name.addObject('MechanicalObject', name='ThreadMechObject', template='Vec3d')
    
    name.addObject('UniformMass', name="nameMass", template="Vec3d,double", totalMass="1.0")

    name.addObject('TriangleFEMForceField', template='Vec3d', name='FEM', method='large', youngModulus=thread_youngModulus, poissonRatio=thread_poissonRatio)
    #name.addObject('MeshSpringForceField', name="FEM-Bend", template="Vec3d", stiffness="1000", damping="0.1")
    name.addObject('UncoupledConstraintCorrection')
    #name.addObject('BoxROI', name='boxROI', box=[-1, -1, -1, 1, 1, 1], drawBoxes='true')
    #name.addObject('RestShapeSpringsForceField', name='rest', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')


    #################### COLLISION ##########################

    ThreadColl = name.addChild('ThreadColl')

    ThreadColl.addObject('PointCollisionModel', name="ThreadPointCollisionModel", selfCollision="True")
    ThreadColl.addObject('TriangleCollisionModel', name="ThreadTriangleCollisionModel", selfCollision="True") 

    #################### VISUALIZATION ########################

    ThreadVisu = ThreadColl.addChild('ThreadVisu')
    ThreadVisu.addObject('OglModel', template="Vec3d", name="Visual", color="1 0.75 0.796", material="Default Diffuse 1 0 0 1 1 Ambient 1 0 0 0.2 1 Specular 0 0 0 1 1 Emissive 0 0 0 1 1 Shininess 0 45 ")
    ThreadVisu.addObject('IdentityMapping', template="Vec3d,Vec3d", name="default12", input="@..", output="@Visual" )


def GeomagicDevice(parentNode=None, name=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position="@GeomagicDevice.positionDevice")
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0")

    

def SutureNeedle(parentNode=None, name=None, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
scale3d=[0.0, 0.0, 0.0],  fixingBox=[0.0, 0.0, 0.0], importFile=None,  carving=False, geomagic=False):

    #################### BEHAVIOUR ##########################
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver', name='ODE solver', rayleighMass="1.0", rayleighStiffness="0.01")
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7") #SparseLDLSolver
    name.addObject('CGLinearSolver', name='linear solver', iterations="25", tolerance="1e-7", threshold="1e-7")
    name.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=importFile)

    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d=scale3d, rotation="0 0 10" ) #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
    else: 
        name.addObject('MechanicalObject', src="@instrumentMeshLoader", name='InstrumentMechObject', template='Rigid3d', translation=translation, scale3d=scale3d)

    name.addObject('UniformMass', name='mass', totalMass="3") # With mass=1: [WARNING] 
    # [CGLinearSolver(linear solver)] denominator threshold reached at first iteration of CG. 
    # Check the 'threshold' data field, you might decrease it
    name.addObject('UncoupledConstraintCorrection') # LinearSolverConstraintCorrection


    #################### COLLISION ##########################
    
    InstrumentColl_Front = name.addChild('InstrumentColl_Front')
    if geomagic==True:
        InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-6.98 0.02 0.05", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        InstrumentColl_Front.addObject('MechanicalObject', template="Vec3d", name="Particle", position="-6.98 0.02 0.05")

    if carving==True:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1", tags="CarvingTool") # Reduced contact stiffness
    else:
        InstrumentColl_Front.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1")
    InstrumentColl_Front.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")

    InstrumentColl_Back = name.addChild('InstrumentColl_Back')
    InstrumentColl_Back.addObject("Monitor", name="SutureNeedle_pos", indices="0", listening="1", showPositions="1", PositionsColor="1 1 0 1", TrajectoriesPrecision="0.1", TrajectoriesColor="1 1 0 1", ExportPositions="true")


    if geomagic==True:
        InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        InstrumentColl_Back.addObject('MechanicalObject', template="Vec3d", name="Particle2", position="0 0.02 0.05")

    InstrumentColl_Back.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument2", contactStiffness="1")
    InstrumentColl_Back.addObject('RigidMapping', template="Rigid3d,Vec3d", name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle2")

    #################### VISUALIZATION ########################
    
    InstrumentVisu = name.addChild('InstrumentVisu')
    if geomagic==True:
        InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d, rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0",  color="0 0.5 0.796")
    else:
        InstrumentVisu.addObject('OglModel', name='InstrumentVisualModel', src='@../instrumentMeshLoader', scale3d=scale3d,  color="0 0.5 0.796")
    
    InstrumentVisu.addObject('RigidMapping', template="Rigid3d,Vec3d", name='MM-VM mapping', input='@../InstrumentMechObject', output='@InstrumentVisualModel')
    #InstrumentVisu.addObject('IdentityMapping',  input='@../InstrumentMechObject', output='@InstrumentVisualModel')

    # Data
    SutureNeedle.MO=name.InstrumentMechObject.getLinkPath()
    SutureNeedle.COLL_BACK_MO=name.InstrumentColl_Back.Particle2.getLinkPath()
    SutureNeedle.POS=name.InstrumentMechObject.findData('position').value
    SutureNeedle.COLL_FRONT=name.InstrumentColl_Front.SphereCollisionInstrument.getLinkPath()
    SutureNeedle.COLL_BACK=name.InstrumentColl_Back.SphereCollisionInstrument2.getLinkPath()
    

 
# Controller for suture task training
class SutureTrainingContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        # Define spring force fields (SkinLeft-Needle; SkinRight-Needle; SkinLeft-SkinRight)
        self.spring_force_field = rootNode.addObject("StiffSpringForceField", name="LeftFF", object1 = Skin.MO,  object2=SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_right = rootNode.addObject("StiffSpringForceField", name="RightFF", object1 = Skin.MO_right,  object2=SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_skins = rootNode.addObject("StiffSpringForceField", name="SkinsFF", object1 = Skin.MO,  object2=Skin.MO_right)

        # Define contact listeners (SkinLeft-Needle; SkinRight-Needle)
        self.contact_listener = rootNode.addObject('ContactListener', name="LeftContact", collisionModel1 = Skin.COLL, collisionModel2 = SutureNeedle.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', name="RightContact", collisionModel1 = Skin.COLL_right, collisionModel2 = SutureNeedle.COLL_FRONT)

        # Pass last created springs (LeftSkin-Needle)
        self.springsCreated_left=False
        # Pass last created springs (RightSkin-Needle)
        self.springsCreated_right=False

        # Pass last attached box
        self.boxAttached=None

        # rootNode.addObject('AttachConstraint', name="lowerConstraint", object1 = Skin.MO,  object2=SutureNeedle.COLL_BACK_MO, 
        # indices1="555",  indices2=0)

        
    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):

        
        # In case of collision (SkinLeft-Needle):
        if self.contact_listener.getNumberOfContacts()!=0:
            print("Contact on the left")
                  
            # Save collision element
            coll_indexes=self.contact_listener.getContactElements() 
            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]
            print("The triangle index is:", coll_index_skin)


            # Does it belong to box 1? If it does: 
            if coll_index_skin in Skin.sphere1Box.findData('triangleIndices').value:
                print("Box 1")    
                
                if self.boxAttached == None:
                    self.boxAttached = Skin.sphere1Box

                # Do springs on the other side exist? If they do:
                if self.springsCreated_right==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(Skin.sphere1Box.findData('indices').value, self.boxAttached.findData('indices').value) # Left then right
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactLeft_disattach()
                # Set this box as the last one attached
                self.boxAttached=Skin.sphere1Box

                if self.springsCreated_left==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(coll_indexes, self.boxAttached)
            
            # Does it belong to box 2? If it does: 
            elif coll_index_skin in Skin.sphere2Box.findData('triangleIndices').value:
                print("Box 2")

                if self.boxAttached == None:
                    self.boxAttached = Skin.sphere2Box
                
                # Do springs on the other side exist? If they do:
                if self.springsCreated_right==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(Skin.sphere2Box.findData('indices').value, self.boxAttached.findData('indices').value) # Left then right
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactLeft_disattach()
                # Set this box as the last one attached
                self.boxAttached=Skin.sphere2Box

                if self.springsCreated_left==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(coll_indexes, self.boxAttached)
            
            else:
                print("No ball detected")
                
        # In case of collision (SkinRight-Needle):
        elif self.contact_listener_right.getNumberOfContacts()!=0:
            print("Contact on the right")
            # Save collision element
            coll_indexes=self.contact_listener_right.getContactElements() 
            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]
            print("The triangle index is:", coll_index_skin)

            # Does it belong to a box? If it does: 
            if coll_index_skin in Skin.sphere3Box.findData('triangleIndices').value:
                print("Box 3")

                if self.boxAttached == None:
                    self.boxAttached = Skin.sphere3Box
                
                # Do springs on the other side exist? If they do:
                if self.springsCreated_left==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(self.boxAttached.findData('indices').value, Skin.sphere3Box.findData('indices').value) # Check
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactRight_disattach()
                # Set this box as the last one attached
                self.boxAttached=Skin.sphere3Box

                if self.springsCreated_right==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(coll_indexes, self.boxAttached)
            
            # Does it belong to a box? If it does: 
            elif coll_index_skin in Skin.sphere4Box.findData('triangleIndices').value:
                print("Box 4")

                if self.boxAttached == None:
                    self.boxAttached = Skin.sphere4Box
                
                # Do springs on the other side exist? If they do:
                if self.springsCreated_left==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(self.boxAttached.findData('indices').value, Skin.sphere4Box.findData('indices').value) # Check
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactRight_disattach()
                # Set this box as the last one attached
                self.boxAttached=Skin.sphere4Box

                if self.springsCreated_right==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(coll_indexes, self.boxAttached)

            else:
                print("No ball detected")

    def attachBoxes(self, indicesBox1, indicesBox2):
        print("Attach two boxes")

        # Create springs
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=50, dampingFactor=0.5, restLength=1) for i, j in zip(indicesBox1,indicesBox2)] 
        self.spring_force_field_skins.addSprings(springs)
        print("Springs added")
        attached=True
        return attached

    def contactLeft_attach(self, coll_indexes, box):
        print("Contact on the left box detected!")

        # Retrieve the skin triangle indexes that are in contact
        coll_indexes2=coll_indexes[0]
        coll_index_skin=coll_indexes2[1]
        print("The triangle index is:", coll_index_skin)

        indicesBox = box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=0.5, restLength=1) for i in indicesBox] 
        self.spring_force_field.addSprings(springs)
        self.springsCreated_left=True
        print("Springs created between needle and left skin")

    def contactLeft_disattach(self):
        print("Eliminating springs from right side of skin")
        N_Indices=len(self.boxAttached.findData('indices').value)

        print("The old box has", N_Indices, "indices")
        for i in range(N_indices):
            self.spring_force_field_right.removeSpring(i)
        self.springsCreated_right=False

    def contactRight_attach(self, coll_indexes, box):
        print("Contact on the right box detected!")

        # Retrieve the skin triangle indexes that are in contact
        coll_indexes2=coll_indexes[0]
        coll_index_skin=coll_indexes2[1]
        print("The triangle index is:", coll_index_skin)

        indicesBox=box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=5, restLength=1) for i in indicesBox] 
        self.spring_force_field_right.addSprings(springs)
        self.springsCreated_right=True
        print("Springs created between needle and left skin")

    def contactRight_disattach(self):
        print("Eliminating springs from left side of skin")
        N_Indices=len(self.boxAttached.findData('indices').value)
        print("The old box has", N_Indices, "indices")
        for i in range(N_indices):
            self.spring_force_field.removeSpring(i)
        self.springsCreated_left=False




if __name__ == '__main__':
    main()
