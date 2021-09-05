# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import incision_models 
import suture_models
import random
import read_Files

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

stiffness_springSkins=1000


        
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

    [RepNumber,user_name]=read_Files.read()

    fileNamePos=f"Rep{RepNumber}_{user_name}_Incision4Pos_Double"
    fileNameVel=f"Rep{RepNumber}_{user_name}_Incision4Vel_Double"
    fileNameForce=f"Rep{RepNumber}_{user_name}_Incision4Force_Double"

    # Define root properties
    root.gravity=[0, 0, -9]
    root.dt=0.01

    root.addObject('RequiredPlugin', pluginName="Geomagic SofaBoundaryCondition SofaCarving SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")

    #root.addObject('OglLabel', label="INCISION TASK", x=20, y=20, fontsize=30, selectContrastingColor="1")
    #root.addObject('OglLabel', label="Cut the skin in correnspondence of the central line", x=20, y=70, fontsize=20, selectContrastingColor="1")
    root.addObject('ViewerSetting', fullscreen="true")
    root.addObject('BackgroundSetting', color="0.3 0.5 0.8")

    #root.addObject('OglViewport', screenSize="250 250" , screenPosition="0 0", cameraPosition="7.54243 16.2274 18.8554", cameraOrientation="0 0 0 1")
    #root.addObject('OglViewport', screenSize="250 250" , screenPosition="0 0", cameraPosition="7.41534 3.637 11.523", cameraOrientation="0.399602 0.00651676 -0.00445552 0.916655")
    #root.addObject('OglViewport', screenSize="250 250" , screenPosition="0 0", cameraPosition="7.41534 3.637 11.523", cameraOrientation="0.399602 0.00651676 -0.1 0.916655")
    #root.addObject('OglViewport', screenSize="250 250" , screenPosition="0 0", cameraPosition="0.456576 4.19955 11.9958", cameraOrientation="0.352224 -0.158983 -0.142336 0.911265")
    
    # Collision pipeline
    root.addObject('CollisionPipeline', depth="6", verbose="0", draw="0")

    # Forces
    root.addObject('BruteForceDetection', name="detection")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContact")
    root.addObject('LocalMinDistance', name="proximity", alarmDistance="0.1", contactDistance="0.01", angleCone="0.1")

    # Animation loop
    root.addObject('FreeMotionAnimationLoop')

    # Constraint solver
    root.addObject('LCPConstraintSolver', tolerance="0.001", maxIt="1000")

    # Add skin
    posx_left=6.5 #0<x<7
    posy=10 #10<y<22
    boxes=[10,11.5,13,14.5,16,17.5,19,20.5,22]

    skin_left=incision_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 10.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, posy, -2, 7, posy+12, 0.1], importFile=skinVolume_fileName,  side=0, 
    borderBox1=[posx_left-0.1, boxes[0], -2, posx_left+0.6, boxes[1], 1],borderBox2=[posx_left-0.1, boxes[1], -2, posx_left+0.6, boxes[2], 1],borderBox3=[posx_left-0.1, boxes[2], -2, posx_left+0.6, boxes[3], 1],
    borderBox4=[posx_left-0.1, boxes[3], -2, posx_left+0.6, boxes[4], 1], borderBox5=[posx_left-0.1, boxes[4], -2, posx_left+0.6, boxes[5], 1],borderBox6=[posx_left-0.1, boxes[5], -2, posx_left+0.6, boxes[6], 1],
    borderBox7=[posx_left-0.1, boxes[6], -2, posx_left+0.6, boxes[7], 1],borderBox8=[posx_left-0.1, boxes[7], -2, posx_left+0.6, boxes[8], 1]
    )
    # borderBox1=[posx_left-0.1, boxes[0], -2, posx_left+0.6, boxes[1], 1],borderBox2=[posx_left-0.1, boxes[1], -2, posx_left+0.6, boxes[2], 1],borderBox3=[posx_left-0.1, boxes[2], -2, posx_left+0.6, boxes[3], 1],
    # borderBox4=[posx_left-0.1, boxes[3], -2, posx_left+0.6, boxes[4], 1], borderBox5=[posx_left-0.1, boxes[4], -2, posx_left+0.6, boxes[5], 1],borderBox6=[posx_left-0.1, boxes[5], -2, posx_left+0.6, boxes[6], 1],
    # borderBox7=[posx_left-0.1, boxes[6], -2, posx_left+0.6, boxes[7], 1],borderBox8=[posx_left-0.1, boxes[7], -2, posx_left+0.6, boxes[8], 1]  ,borderBox9=[posx_left-0.1, boxes[8], -2, posx_left+0.6, boxes[9], 1], 
    # borderBox10=[posx_left-0.1, boxes[9], -2, posx_left+0.6, boxes[10], 1] , borderBox11=[posx_left-0.1, boxes[10], -2, posx_left+0.6, boxes[11], 1] , borderBox12=[posx_left-0.1, boxes[11], -2, posx_left+0.6, boxes[12], 1] )

    posx=posx_left+0.85 
    skin_right=incision_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[posx, 10, 0], 
    scale3d=scale3d_skin, fixingBox=[posx, posy, -2, posx*2, posy+12, 0.1], importFile=skinVolume_fileName,  side=1, 
    borderBox1=[posx-0.1, boxes[0], -2, posx+0.6, boxes[1], 1],borderBox2=[posx-0.1, boxes[1], -2, posx+0.6, boxes[2], 1],borderBox3=[posx-0.1, boxes[2], -2, posx+0.6, boxes[3], 1],
    borderBox4=[posx-0.1, boxes[3], -2, posx+0.6, boxes[4], 1], borderBox5=[posx-0.1, boxes[4], -2, posx+0.6, boxes[5], 1],borderBox6=[posx-0.1, boxes[5], -2, posx+0.6, boxes[6], 1],
    borderBox7=[posx-0.1, boxes[6], -2, posx+0.6, boxes[7], 1],borderBox8=[posx-0.1, boxes[7], -2, posx+0.6, boxes[8], 1]
    )

    # borderBox1=[posx-0.1, boxes[0], -2, posx+0.6, boxes[1], 1],borderBox2=[posx-0.1, boxes[1], -2, posx+0.6, boxes[2], 1],borderBox3=[posx-0.1, boxes[2], -2, posx+0.6, boxes[3], 1],
    # borderBox4=[posx-0.1, boxes[3], -2, posx+0.6, boxes[4], 1], borderBox5=[posx-0.1, boxes[4], -2, posx+0.6, boxes[5], 1],borderBox6=[posx-0.1, boxes[5], -2, posx+0.6, boxes[6], 1],
    # borderBox7=[posx-0.1, boxes[6], -2, posx+0.6, boxes[7], 1],borderBox8=[posx-0.1, boxes[7], -2, posx+0.6, boxes[8], 1] ,borderBox9=[posx-0.1, boxes[8], -2, posx+0.6, boxes[9], 1], 
    # borderBox10=[posx-0.1, boxes[9], -2, posx+0.6, boxes[10], 1] , borderBox11=[posx-0.1, boxes[10], -2, posx+0.6, boxes[11], 1] , borderBox12=[posx-0.1, boxes[11], -2, posx+0.6, boxes[12], 1] )

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Right Device", scale="1", drawDeviceFrame="0", 
    drawDevice="0", positionBase="7 15 0",  orientationBase="0.707 0 0 0.707")#, forceFeedBack="@SutureNeedle/LCPFFNeedle")

    GeomagicDevice(parentNode=root, name='OmniRight', position="@GeomagicDeviceRight.positionDevice")

    # Add needles
    incision_models.Scalpel(parentNode=root, name='Scalpel', monitor=True, file1=fileNamePos, file2=fileNameVel, file3=fileNameForce, position="@GeomagicDeviceRight.positionDevice", external_rest_shape='@../OmniRight/DOFs')
    #incision_models.Scalpel(parentNode=root, name='Scalpel', monitor=True, file1=fileNamePos, file2=fileNameVel, file3=fileNameForce, position="@GeomagicDeviceLeft.positionDevice", external_rest_shape='@../OmniLeft/DOFs')

    ################################################################################################################


    # Add controller
    root.addObject(IncisionTaskTrainingController(root, skin_left, skin_right))
  
    
    return root


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
    GeomagicDevice.MSC=name.GEOMSC


## Controller for incision task.
# Handles the cutting of the skin
'''
class IncisionTaskTrainingController(Sofa.Core.Controller):
    
    ## Constructor of the class. 
    # @param name: name of the controller
    # @param rootnode: path to the root node of the simulation
    # @param skin_left: path to the left skin patch root node
    # @param skin_right: path to the right skin patch root node
    # Defines the contact listeners between skin and the scalpel and creates the 8 force fields between skin patches
    
    def __init__(self, root, skin_left, skin_right):
        
        Sofa.Core.Controller.__init__(self, root, skin_left, skin_right)
        self.contact_listener = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.contact_listener_right = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL_right, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.contact_listener2 = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL, collisionModel2 = incision_models.Scalpel.COLL_FRONT2)
        self.contact_listener2_right = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL_right, collisionModel2 = incision_models.Scalpel.COLL_FRONT2)
        
        self.rootNode=root

        self.spring_force_field1 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field2 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field3 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field4 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field5 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field6 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field7 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field8 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field9 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field10 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field11 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field12 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)

        self.indices1=[  4, 5, 72, 73, 74, 105, 106, 234, 235, 236, 241, 292, 464, 610, 642, 643, 955  ]
        self.indices2=[  75, 76, 77, 107, 108, 109, 233, 237, 278, 594, 627, 829  ]
        self.indices3=[  78, 79, 110, 111, 222, 238, 239, 269, 456, 537, 618, 830, 858  ]
        self.indices4=[  80, 81, 82, 112, 113, 114, 218, 223, 224, 267, 514, 589, 630, 862, 864  ]
        self.indices5=[  83, 84, 85, 115, 116, 117, 219, 229, 283, 512, 619, 869  ]
        self.indices6=[  86, 87, 118, 119, 217, 220, 221, 268, 536, 591, 617, 877, 884  ]
        self.indices7=[  88, 89, 90, 120, 121, 122, 208, 225, 230, 264, 280, 515, 613, 631, 873  ]
        self.indices8=[  91, 92, 93, 123, 124, 125, 209, 210, 284, 525, 906, 907  ]
        self.indices9=[  94, 95, 126, 127, 211, 226, 231, 272, 529, 535, 621, 629, 890  ]
        self.indices10=[  96, 97, 98, 128, 129, 130, 212, 227, 232, 266, 489, 543, 624, 840, 885  ]
        self.indices11=[  99, 100, 101, 131, 132, 133, 213, 214, 277, 476, 628, 836  ]
        self.indices12=[  6, 7, 102, 103, 104, 134, 135, 215, 216, 228, 252, 290, 294, 606, 639, 827, 957  ]

        self.indices1_right=[  0, 1, 8, 9, 10, 41, 42, 203, 204, 205, 247, 291, 482, 607, 956  ]
        self.indices2_right=[  11, 12, 13, 43, 44, 45, 201, 206  ]
        self.indices3_right=[  14, 15, 46, 47, 191, 202, 207, 939  ]
        self.indices4_right=[  16, 17, 18, 48, 49, 50, 185, 187, 192, 273  ]
        self.indices5_right=[  19, 20, 21, 51, 52, 53, 188, 197  ]
        self.indices6_right=[  22, 23, 54, 55, 186, 189, 190  ]
        self.indices7_right=[  24, 25, 26, 56, 57, 58, 176, 193, 198  ]
        self.indices8_right=[  27, 28, 29, 59, 60, 61, 177, 178  ]
        self.indices9_right=[  30, 31, 62, 63, 179, 194, 199  ]
        self.indices10_right=[  32, 33, 34, 64, 65, 66, 180, 195, 200, 959  ]
        self.indices11_right=[  35, 36, 37, 67, 68, 69, 181, 182, 625, 960  ]
        self.indices12_right=[  2, 3, 38, 39, 40, 70, 71, 183, 184, 196, 259, 289, 595, 608  ]

        self.ff1=True
        self.ff2=True
        self.ff3=True
        self.ff4=True
        self.ff5=True
        self.ff6=True
        self.ff7=True
        self.ff8=True
        self.ff9=True
        self.ff10=True
        self.ff11=True
        self.ff12=True

        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices1,self.indices1_right)] # Then set to right indices (the ones below)
        self.spring_force_field1.addSprings(springs)

        springs2 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices2,self.indices2_right)] # Then set to right indices (the ones below)
        self.spring_force_field2.addSprings(springs2)

        springs3 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices3,self.indices3_right)] # Then set to right indices (the ones below)
        self.spring_force_field3.addSprings(springs3)

        springs4 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices4,self.indices4_right)] # Then set to right indices (the ones below)
        self.spring_force_field4.addSprings(springs4)

        springs5 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices5,self.indices5_right)] # Then set to right indices (the ones below)
        self.spring_force_field5.addSprings(springs5)

        springs6 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices6,self.indices6_right)] # Then set to right indices (the ones below)
        self.spring_force_field6.addSprings(springs6)

        springs7 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices7,self.indices7_right)] # Then set to right indices (the ones below)
        self.spring_force_field7.addSprings(springs7)

        springs8 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices8,self.indices8_right)] # Then set to right indices (the ones below)
        self.spring_force_field8.addSprings(springs8)

        springs9 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices9,self.indices9_right)] # Then set to right indices (the ones below)
        self.spring_force_field5.addSprings(springs9)

        springs10 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices10,self.indices10_right)] # Then set to right indices (the ones below)
        self.spring_force_field6.addSprings(springs10)

        springs11 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices11,self.indices11_right)] # Then set to right indices (the ones below)
        self.spring_force_field7.addSprings(springs11)

        springs12 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices12,self.indices12_right)] # Then set to right indices (the ones below)
        self.spring_force_field8.addSprings(springs12)


    ## Method called at each begin of animation step
    # @param event: animation step event
    # If a contact between the scalpel and the skin, the force field in that point is deactivated

    def onAnimateBeginEvent(self, event): 

        coll_indexes=self.contact_listener.getContactElements()
        coll_indexes_right=self.contact_listener_right.getContactElements()
        coll_indexes2=self.contact_listener2.getContactElements()
        coll_indexes2_right=self.contact_listener2_right.getContactElements()
        
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
    
        # self.indices1=incision_models.Skin.borderBox1.findData('indices').value
        # self.indices2=incision_models.Skin.borderBox2.findData('indices').value        
        # self.indices3=incision_models.Skin.borderBox3.findData('indices').value
        # self.indices4=incision_models.Skin.borderBox4.findData('indices').value
        # self.indices5=incision_models.Skin.borderBox5.findData('indices').value
        # self.indices6=incision_models.Skin.borderBox6.findData('indices').value        
        # self.indices7=incision_models.Skin.borderBox7.findData('indices').value
        # self.indices8=incision_models.Skin.borderBox8.findData('indices').value
        # self.indices9=incision_models.Skin.borderBox9.findData('indices').value
        # self.indices10=incision_models.Skin.borderBox10.findData('indices').value        
        # self.indices11=incision_models.Skin.borderBox11.findData('indices').value
        # self.indices12=incision_models.Skin.borderBox12.findData('indices').value

        # self.indices1_right=incision_models.Skin.borderBox1_right.findData('indices').value
        # self.indices2_right=incision_models.Skin.borderBox2_right.findData('indices').value        
        # self.indices3_right=incision_models.Skin.borderBox3_right.findData('indices').value
        # self.indices4_right=incision_models.Skin.borderBox4_right.findData('indices').value
        # self.indices5_right=incision_models.Skin.borderBox5_right.findData('indices').value
        # self.indices6_right=incision_models.Skin.borderBox6_right.findData('indices').value        
        # self.indices7_right=incision_models.Skin.borderBox7_right.findData('indices').value
        # self.indices8_right=incision_models.Skin.borderBox8_right.findData('indices').value
        # self.indices9_right=incision_models.Skin.borderBox9_right.findData('indices').value
        # self.indices10_right=incision_models.Skin.borderBox10_right.findData('indices').value        
        # self.indices11_right=incision_models.Skin.borderBox11_right.findData('indices').value
        # self.indices12_right=incision_models.Skin.borderBox12_right.findData('indices').value

        # print("1L")
        # print("[", self.computeIndices(self.indices1), "]")
        # print("2L")
        # print("[", self.computeIndices(self.indices2), "]")
        # print("3L")
        # print("[", self.computeIndices(self.indices3), "]")
        # print("4L")
        # print("[", self.computeIndices(self.indices4), "]")
        # print("5L")
        # print("[", self.computeIndices(self.indices5), "]")
        # print("6L")
        # print("[", self.computeIndices(self.indices6), "]")
        # print("7L")
        # print("[", self.computeIndices(self.indices7), "]")
        # print("8L")
        # print("[", self.computeIndices(self.indices8), "]")
        # print("9L")
        # print("[", self.computeIndices(self.indices9), "]")
        # print("10L")
        # print("[", self.computeIndices(self.indices10), "]")
        # print("11L")
        # print("[", self.computeIndices(self.indices11), "]")
        # print("12L")
        # print("[", self.computeIndices(self.indices12), "]")
        # print("1R")
        # print("[", self.computeIndices(self.indices1_right), "]")
        # print("2R")
        # print("[", self.computeIndices(self.indices2_right), "]")
        # print("3R")
        # print("[", self.computeIndices(self.indices3_right), "]")
        # print("4R")
        # print("[", self.computeIndices(self.indices4_right), "]")
        # print("5R")
        # print("[", self.computeIndices(self.indices5_right), "]")
        # print("6R")
        # print("[", self.computeIndices(self.indices6_right), "]")
        # print("7R")
        # print("[", self.computeIndices(self.indices7_right), "]")
        # print("8R")
        # print("[", self.computeIndices(self.indices8_right), "]")
        # print("9R")
        # print("[", self.computeIndices(self.indices9_right), "]")
        # print("10R")
        # print("[", self.computeIndices(self.indices10_right), "]")
        # print("11R")
        # print("[", self.computeIndices(self.indices11_right), "]")
        # print("12R")
        # print("[", self.computeIndices(self.indices12_right), "]")




    ## Method to dectivate force fields after a contact on the left side of the skin has occurred.
    # @param: skin triangle indices and scalpel point indices on which contact happened 
    # Estracts the skin triangle index and checks if it belongs to any of the border boxes: if it does, the force field in that point is deactivated
    def left_ff(self, coll_indexes):   
        coll_indexes2=coll_indexes[0]
        coll_index_skin=coll_indexes2[1]
        if coll_index_skin in incision_models.Skin.borderBox1.findData('triangleIndices').value and self.ff1==True:
            self.spring_force_field1.clear()
            self.ff1=False
        elif coll_index_skin in incision_models.Skin.borderBox2.findData('triangleIndices').value and self.ff2==True:
            self.spring_force_field2.clear()
            self.ff2=False
        elif coll_index_skin in incision_models.Skin.borderBox3.findData('triangleIndices').value and self.ff3==True:
            self.spring_force_field3.clear()
            self.ff3=False
        elif coll_index_skin in incision_models.Skin.borderBox4.findData('triangleIndices').value and self.ff4==True:
            self.spring_force_field4.clear()
            self.ff4=False
        elif coll_index_skin in incision_models.Skin.borderBox5.findData('triangleIndices').value and self.ff5==True:
            self.spring_force_field5.clear()
            self.ff5=False
        elif coll_index_skin in incision_models.Skin.borderBox6.findData('triangleIndices').value and self.ff6==True:
            self.spring_force_field6.clear()
            self.ff6=False
        elif coll_index_skin in incision_models.Skin.borderBox7.findData('triangleIndices').value and self.ff7==True:
            self.spring_force_field7.clear()
            self.ff7=False
        elif coll_index_skin in incision_models.Skin.borderBox8.findData('triangleIndices').value and self.ff8==True:
            self.spring_force_field8.clear()
            self.ff8=False
        else:
            print(self.ff1, self.ff2, self.ff3, self.ff4, self.ff5, self.ff6, self.ff7, self.ff8)
   
   
    ## Method to dectivate force fields after a contact on the right side of the skin has occurred.
    # @param: skin triangle indices and scalpel point indices on which contact happened 
    # Estracts the skin triangle index and checks if it belongs to any of the border boxes: if it does, the force field in that point is deactivated
    def right_ff(self, coll_indexes_right):
        coll_indexes2=coll_indexes_right[0]
        coll_index_skin=coll_indexes2[1]
        if coll_index_skin in incision_models.Skin.borderBox1_right.findData('triangleIndices').value and self.ff1==True:
            self.spring_force_field1.clear()
            self.ff1=False
        elif coll_index_skin in incision_models.Skin.borderBox2_right.findData('triangleIndices').value and self.ff2==True:
            self.spring_force_field2.clear()
            self.ff2=False
        elif coll_index_skin in incision_models.Skin.borderBox3_right.findData('triangleIndices').value and self.ff3==True:
            self.spring_force_field3.clear()
            self.ff3=False
        elif coll_index_skin in incision_models.Skin.borderBox4_right.findData('triangleIndices').value and self.ff4==True:
            self.spring_force_field4.clear()
            self.ff4=False
        elif coll_index_skin in incision_models.Skin.borderBox5_right.findData('triangleIndices').value and self.ff5==True:
            self.spring_force_field5.clear()
            self.ff5=False
        elif coll_index_skin in incision_models.Skin.borderBox6_right.findData('triangleIndices').value and self.ff6==True:
            self.spring_force_field6.clear()
            self.ff6=False
        elif coll_index_skin in incision_models.Skin.borderBox7_right.findData('triangleIndices').value and self.ff7==True:
            self.spring_force_field7.clear()
            self.ff7=False
        elif coll_index_skin in incision_models.Skin.borderBox8_right.findData('triangleIndices').value and self.ff8==True:
            self.spring_force_field8.clear()
            self.ff8=False
        else:
            print("Index does not belong to a border box")


        

    ## Method to compute the string of indices given the input array of integers.
    # @param indicesBox: array of indices 

    def computeIndices(self, indicesBox):
        N_indices=len(indicesBox)
        result=' '  

        for i in range(N_indices):
            result += str(indicesBox[i]) + ", "

        return result
'''

class IncisionTaskTrainingController(Sofa.Core.Controller):

    def __init__(self, root, skin_left, skin_right):
        Sofa.Core.Controller.__init__(self, root, skin_left, skin_right)
        self.contact_listener = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.contact_listener_right = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL_right, collisionModel2 = incision_models.Scalpel.COLL_FRONT)
        self.contact_listener2 = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL, collisionModel2 = incision_models.Scalpel.COLL_FRONT2)
        self.contact_listener2_right = root.addObject('ContactListener', collisionModel1 = incision_models.Skin.COLL_right, collisionModel2 = incision_models.Scalpel.COLL_FRONT2)
        
        self.rootNode=root

        self.spring_force_field1 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field2 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field3 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field4 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field5 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field6 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field7 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)
        self.spring_force_field8 = skin_left.addObject("StiffSpringForceField",  object1=incision_models.Skin.MO,  object2=incision_models.Skin.MO_right)

        self.indices1=[  4, 5, 72, 73, 74, 75, 105, 106, 107, 233, 234, 235, 236, 241, 278, 292, 464, 610, 627, 642, 643, 955  ]
        self.indices2=[  76, 77, 78, 79, 108, 109, 110, 111, 222, 237, 238, 239, 269, 456, 537, 594, 618, 829, 830, 858  ]
        self.indices3=[  80, 81, 82, 83, 112, 113, 114, 115, 218, 219, 223, 224, 267, 283, 514, 589, 619, 630, 862, 864  ]
        self.indices4=[  84, 85, 86, 87, 116, 117, 118, 119, 217, 220, 221, 229, 268, 512, 536, 591, 617, 869, 877, 884  ]
        self.indices5=[  88, 89, 90, 91, 120, 121, 122, 123, 208, 209, 225, 230, 264, 280, 515, 525, 613, 631, 873, 907  ]
        self.indices6=[  92, 93, 94, 95, 124, 125, 126, 127, 210, 211, 226, 231, 272, 284, 529, 535, 621, 629, 890, 906  ]
        self.indices7=[  96, 97, 98, 99, 100, 128, 129, 130, 131, 132, 212, 213, 227, 232, 266, 476, 489, 543, 624, 836, 840, 885  ]
        self.indices8=[  6, 7, 100, 101, 102, 103, 104, 132, 133, 134, 135, 214, 215, 216, 228, 252, 277, 290, 294, 606, 628, 639, 827, 957  ]

        self.indices1_right=[  0, 1, 8, 9, 10, 11, 41, 42, 43, 201, 203, 204, 205, 247, 291, 482, 607, 956  ]
        self.indices2_right=[  12, 13, 14, 15, 44, 45, 46, 47, 191, 202, 206, 207, 939  ]
        self.indices3_right=[  16, 17, 18, 19, 48, 49, 50, 51, 185, 187, 188, 192, 273  ]
        self.indices4_right=[  20, 21, 22, 23, 52, 53, 54, 55, 186, 189, 190, 197  ]
        self.indices5_right=[  24, 25, 26, 27, 56, 57, 58, 59, 176, 177, 193, 198  ]
        self.indices6_right=[  28, 29, 30, 31, 60, 61, 62, 63, 178, 179, 194, 199  ]
        self.indices7_right=[  32, 33, 34, 35, 36, 64, 65, 66, 67, 68, 180, 181, 195, 200, 959, 960  ]
        self.indices8_right=[  2, 3, 36, 37, 38, 39, 40, 68, 69, 70, 71, 182, 183, 184, 196, 259, 289, 595, 608, 625  ]

        self.ff1=True
        self.ff2=True
        self.ff3=True
        self.ff4=True
        self.ff5=True
        self.ff6=True
        self.ff7=True
        self.ff8=True

        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices1,self.indices1_right)] # Then set to right indices (the ones below)
        self.spring_force_field1.addSprings(springs)

        springs2 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices2,self.indices2_right)] # Then set to right indices (the ones below)
        self.spring_force_field2.addSprings(springs2)

        springs3 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices3,self.indices3_right)] # Then set to right indices (the ones below)
        self.spring_force_field3.addSprings(springs3)

        springs4 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices4,self.indices4_right)] # Then set to right indices (the ones below)
        self.spring_force_field4.addSprings(springs4)

        springs5 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices5,self.indices5_right)] # Then set to right indices (the ones below)
        self.spring_force_field5.addSprings(springs5)

        springs6 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices6,self.indices6_right)] # Then set to right indices (the ones below)
        self.spring_force_field6.addSprings(springs6)

        springs7 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices7,self.indices7_right)] # Then set to right indices (the ones below)
        self.spring_force_field7.addSprings(springs7)

        springs8 = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=0.001) for i, j in zip(self.indices8,self.indices8_right)] # Then set to right indices (the ones below)
        self.spring_force_field8.addSprings(springs8)




    # # Uncomment to recompute indices
    def onAnimateBeginEvent(self, event): 

        #print(self.rootNode.GeomagicDevice.forceFeedBack)
        #print("1")
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
        if coll_index_skin in incision_models.Skin.borderBox1.findData('triangleIndices').value and self.ff1==True:
            self.spring_force_field1.clear()
            self.ff1=False
        elif coll_index_skin in incision_models.Skin.borderBox2.findData('triangleIndices').value and self.ff2==True:
            self.spring_force_field2.clear()
            self.ff2=False
        elif coll_index_skin in incision_models.Skin.borderBox3.findData('triangleIndices').value and self.ff3==True:
            self.spring_force_field3.clear()
            self.ff3=False
        elif coll_index_skin in incision_models.Skin.borderBox4.findData('triangleIndices').value and self.ff4==True:
            self.spring_force_field4.clear()
            self.ff4=False
        elif coll_index_skin in incision_models.Skin.borderBox5.findData('triangleIndices').value and self.ff5==True:
            self.spring_force_field5.clear()
            self.ff5=False
        elif coll_index_skin in incision_models.Skin.borderBox6.findData('triangleIndices').value and self.ff6==True:
            self.spring_force_field6.clear()
            self.ff6=False
        elif coll_index_skin in incision_models.Skin.borderBox7.findData('triangleIndices').value and self.ff7==True:
            self.spring_force_field7.clear()
            self.ff7=False
        elif coll_index_skin in incision_models.Skin.borderBox8.findData('triangleIndices').value and self.ff8==True:
            self.spring_force_field8.clear()
            self.ff8=False
        else:
            print("Index does not belong to a border box")

    def right_ff(self, coll_indexes_right):
        coll_indexes2=coll_indexes_right[0]
        coll_index_skin=coll_indexes2[1]
        if coll_index_skin in incision_models.Skin.borderBox1_right.findData('triangleIndices').value and self.ff1==True:
            self.spring_force_field1.clear()
            self.ff1=False
        elif coll_index_skin in incision_models.Skin.borderBox2_right.findData('triangleIndices').value and self.ff2==True:
            self.spring_force_field2.clear()
            self.ff2=False
        elif coll_index_skin in incision_models.Skin.borderBox3_right.findData('triangleIndices').value and self.ff3==True:
            self.spring_force_field3.clear()
            self.ff3=False
        elif coll_index_skin in incision_models.Skin.borderBox4_right.findData('triangleIndices').value and self.ff4==True:
            self.spring_force_field4.clear()
            self.ff4=False
        elif coll_index_skin in incision_models.Skin.borderBox5_right.findData('triangleIndices').value and self.ff5==True:
            self.spring_force_field5.clear()
            self.ff5=False
        elif coll_index_skin in incision_models.Skin.borderBox6_right.findData('triangleIndices').value and self.ff6==True:
            self.spring_force_field6.clear()
            self.ff6=False
        elif coll_index_skin in incision_models.Skin.borderBox7_right.findData('triangleIndices').value and self.ff7==True:
            self.spring_force_field7.clear()
            self.ff7=False
        elif coll_index_skin in incision_models.Skin.borderBox8_right.findData('triangleIndices').value and self.ff8==True:
            self.spring_force_field8.clear()
            self.ff8=False
        else:
            print("Index does not belong to a border box")


        # self.indices1=incision_models.Skin.borderBox1.findData('indices').value
        # self.indices2=incision_models.Skin.borderBox2.findData('indices').value        
        # self.indices3=incision_models.Skin.borderBox3.findData('indices').value
        # self.indices4=incision_models.Skin.borderBox4.findData('indices').value
        # self.indices5=incision_models.Skin.borderBox5.findData('indices').value
        # self.indices6=incision_models.Skin.borderBox6.findData('indices').value        
        # self.indices7=incision_models.Skin.borderBox7.findData('indices').value
        # self.indices8=incision_models.Skin.borderBox8.findData('indices').value

        # self.indices1_right=incision_models.Skin.borderBox1_right.findData('indices').value
        # self.indices2_right=incision_models.Skin.borderBox2_right.findData('indices').value        
        # self.indices3_right=incision_models.Skin.borderBox3_right.findData('indices').value
        # self.indices4_right=incision_models.Skin.borderBox4_right.findData('indices').value
        # self.indices5_right=incision_models.Skin.borderBox5_right.findData('indices').value
        # self.indices6_right=incision_models.Skin.borderBox6_right.findData('indices').value        
        # self.indices7_right=incision_models.Skin.borderBox7_right.findData('indices').value
        # self.indices8_right=incision_models.Skin.borderBox8_right.findData('indices').value

        # print("1L")
        # print("[", self.computeIndices(self.indices1), "]")
        # print("2L")
        # print("[", self.computeIndices(self.indices2), "]")
        # print("3L")
        # print("[", self.computeIndices(self.indices3), "]")
        # print("4L")
        # print("[", self.computeIndices(self.indices4), "]")
        # print("5L")
        # print("[", self.computeIndices(self.indices5), "]")
        # print("6L")
        # print("[", self.computeIndices(self.indices6), "]")
        # print("7L")
        # print("[", self.computeIndices(self.indices7), "]")
        # print("8L")
        # print("[", self.computeIndices(self.indices8), "]")


        
        # print("1R")
        # print("[", self.computeIndices(self.indices1_right), "]")
        # print("2R")
        # print("[", self.computeIndices(self.indices2_right), "]")
        # print("3R")
        # print("[", self.computeIndices(self.indices3_right), "]")
        # print("4R")
        # print("[", self.computeIndices(self.indices4_right), "]")
        # print("5R")
        # print("[", self.computeIndices(self.indices5_right), "]")
        # print("6R")
        # print("[", self.computeIndices(self.indices6_right), "]")
        # print("7R")
        # print("[", self.computeIndices(self.indices7_right), "]")
        # print("8R")
        # print("[", self.computeIndices(self.indices8_right), "]")


    # def computeIndices(self, indicesBox):
    #     N_indices=len(indicesBox)
    #     result=' '  

    #     for i in range(N_indices):
    #         result += str(indicesBox[i]) + ", "

    #     return result

     


if __name__ == '__main__':
    main()
