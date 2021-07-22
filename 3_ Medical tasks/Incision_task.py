# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import incision_models 


scale3d_skin="1 0.6 1"
scale3d_scalpel="1 1 1 "

skinVolume_fileName="mesh\skin_30201"
scalpel_Instrument="mesh\scalpel.obj"
# Collision particles positions
pointPosition_onscalpel1="8 -7.4 -17" 


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

    # Define root properties
    root.gravity=[0, 0, -9]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    root.addObject('VisualStyle', displayFlags="showBehaviorModels")

    root.addObject('OglLabel', label="INCISION TASK", x=20, y=20, fontsize=30, selectContrastingColor="1")
    root.addObject('OglLabel', label="Cut the skin in correnspondence of the central line", x=20, y=70, fontsize=20, selectContrastingColor="1")
    #root.addObject('OglLabel', label="starting from the one closest to the needle", x=20, y=100, fontsize=20, selectContrastingColor="1")


    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.5", contactDistance="0.05", angleCone="0.1")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Define the variables
    geomagic=False
    carving=False

    # Add skin
    incision_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[9.5, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName, carving=carving, side=0, task="Incision",
    borderBox1=[7, -0.1, -2, 10, 5, 1],borderBox2=[7, 5, -2, 10, 10, 1],borderBox3=[7, 10, -2, 10, 15, 1],borderBox4=[7, 15, -2, 10, 20, 1])

    incision_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[10, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[10, -0.1, -2, 20, 20, 0.1], borderBox=[10, -0.1, -2, 10.5, 20, 1],
    importFile=skinVolume_fileName, carving=carving, side=1, task="Incision",
    borderBox1=[10, -0.1, -2, 14, 5, 1],borderBox2=[10, 5, -2, 14, 10, 1],borderBox3=[10, 10, -2, 14, 15, 1],borderBox4=[10, 15, -2, 14, 20, 1]) 

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="0", positionBase="10 20 10",  orientationBase="0.707 0 0 0.707")
        
        incision_models.GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################


    #################### CARVING #############################################
    if carving==True:
        root.addObject('CarvingManager', active="true", carvingDistance="0.1")
    ##########################################################################

    
    # Add scalpel
    Scalpel(parentNode=root, name='Scalpel',   geomagic=geomagic)

    # Add contact listener: uncomment to do stuff at animation time
    #root.addObject(IncisionContactControllerSprings(root))
    #root.addObject(IncisionContactControllerAttach(root)) # If true: set translation of skin right to 10
    

    return root
    
def Scalpel(parentNode=None, name=None, translation=[0.0, 0.0, 0.0], scale3d=[0.0, 0.0, 0.0], color=[0.0, 0.0, 0.0],
carving=False, geomagic=False): 
    # Taken from C:\sofa\src\examples\Components\collision\RuleBasedContactManager
    
    name=parentNode.addChild(name)
    name.addObject('EulerImplicitSolver',  rayleighStiffness="0.1", rayleighMass="0.1" )
    name.addObject('CGLinearSolver', iterations="25", tolerance="1e-5" ,threshold="1e-5")
    if geomagic==True:
        name.addObject('MechanicalObject',  name='InstrumentMechObject', template='Rigid3d', position="@GeomagicDevice.positionDevice", scale3d="1.0", rotation="0 0 10" ) #, src="@instrumentMeshLoader")
        name.addObject('RestShapeSpringsForceField', stiffness='1000', angularStiffness='1000', external_rest_shape='@../Omni/DOFs', points='0', external_points='0') 
        name.addObject('LCPForceFeedback', name="LCPFFNeedle",  forceCoef="0.1", activate="true")# Decide forceCoef value better
    else: 
        name.addObject('MechanicalObject', name="InstrumentMechObject", template="Rigid3d", scale="1.0" ,dx="12", dy="13", dz="16")
    name.addObject('UniformMass' , totalMass="3")
    name.addObject('UncoupledConstraintCorrection')

    Visu=name.addChild('Visu')
    Visu.addObject('MeshObjLoader' ,name="meshLoader_3", filename="mesh/Scalpel.obj", scale="1.0", handleSeams="1" )
    if geomagic==True:
        Visu.addObject('OglModel',name="Visual", src='@meshLoader_3', rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0",  color="0 0.5 0.796")
    else:
        Visu.addObject('OglModel' ,name="Visual" ,src="@meshLoader_3",  color="0 0.5 0.796")
    Visu.addObject('RigidMapping' ,input="@..", output="@Visual")
    
    Surf=name.addChild('Surf')
    Surf.addObject('MeshObjLoader' ,filename="mesh/Scalpel.obj" ,name="loader" )
    Surf.addObject('MeshTopology' ,src="@loader")
    if geomagic==True:
        Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else: 
        Surf.addObject('MechanicalObject' ,src="@loader", scale="1.0")#, dx="8", dy="3", dz="6")
    #Surf.addObject('TriangleCollisionModel', name="Torus2Triangle") # DO NOT UNCOMMENT
    #Surf.addObject('LineCollisionModel', name="Torus2Line" ) # DO NOT UNCOMMENT
    Surf.addObject('PointCollisionModel' ,name="Torus2Point")
    Surf.addObject('RigidMapping')

    collFront = name.addChild('collFront')
    if geomagic==True:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5", rx="-10", ry="160", rz="180",  dz="-4", dx="0", dy="0")
    else:
        collFront.addObject('MechanicalObject', template="Vec3d", name="Particle", position="4 -3.7 -8.5")
    collFront.addObject('SphereCollisionModel', radius="0.2", name="SphereCollisionInstrument", contactStiffness="1")
    collFront.addObject('RigidMapping', name="MM->CM mapping",  input="@../InstrumentMechObject",  output="@Particle")




class IncisionContactControllerAttach(Sofa.Core.Controller):

    def __init__(self, root):
        Sofa.Core.Controller.__init__(self, root)
        self.contact_listener = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.contact_listener_right = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL_right, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.rootNode=root

        root.addObject('AttachConstraint',
        name="Incision constraint",
        object1 = "@SkinLeft", 
        object2 = "@SkinRight", 
        indices1= "  4 5 6 7 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239  ", 
        indices2= "  0 1 2 3 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207  ") 


    # # # Uncomment to recompute indices
    # def onAnimateBeginEvent(self, event): 

    #     print(incision_models.Skin.borderBox.findData('indices').value)
    #     index1=incision_models.Skin.borderBox.findData('indices').value
    #     index2=incision_models.Skin.borderBox_right.findData('indices').value
    #     temp1=len(index1)
    #     temp2=len(index2)
    #     self.N_indices=min(temp1,temp2)
    #     in1=self.computeIndices(index1)
    #     in2=self.computeIndices(index2)

    #     print("indices1= \"", in1, "\", indices2= \"", in2, "\")")


    def computeIndices(self, indicesBox):

        result=' '  

        for i in range(self.N_indices):
            result += str(indicesBox[i]) + ", "

        return result


class IncisionContactControllerSprings(Sofa.Core.Controller):

    def __init__(self, root):
        Sofa.Core.Controller.__init__(self, root)
        self.contact_listener = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.contact_listener_right = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL_right, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.rootNode=root

        self.spring_force_field = root.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        
        index1=[  4, 5, 6, 7, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 
        103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
        133, 134, 135, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 
        235, 236, 237, 238, 239 ]

        index2=[  0, 1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 
        39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 176, 177, 
        178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207 ]
        
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=100000, dampingFactor=0.5, restLength=0.001) for i, j in zip(index1,index2)] # Then set to right indices (the ones below)
        self.spring_force_field.addSprings(springs)
        self.indexes=0

    # # Uncomment to recompute indices
    # def onAnimateBeginEvent(self, event): 

    #     index1=incision_models.Skin.borderBox.findData('indices').value
    #     index2=incision_models.Skin.borderBox_right.findData('indices').value
    #     in1=self.computeIndices(index1)
    #     in2=self.computeIndices(index2)

    #     print("[", in1, "]")
    #     print("[", in2, "]")
  

    def computeIndices(self, indicesBox):
        N_indices=len(indicesBox)
        result=' '  

        for i in range(N_indices):
            result += str(indicesBox[i]) + ", "

        return result

if __name__ == '__main__':
    main()
