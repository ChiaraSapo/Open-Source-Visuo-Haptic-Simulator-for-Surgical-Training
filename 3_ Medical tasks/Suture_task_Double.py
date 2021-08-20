# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
#from goto import goto, label
import subprocess


# Data

scale3d_skin="0.25 0.55 0.1"
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

## This function creates the graph node
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

    root.addObject('OglLabel', label="SUTURE TASK - TRAINING", x=20, y=20, fontsize=30, selectContrastingColor="1")
    root.addObject('OglLabel', label="Pierce the skin in correnspondence of the green spheres", x=20, y=70, fontsize=20, selectContrastingColor="1")
    root.addObject('OglLabel', label="starting from the one closest to the needle", x=20, y=100, fontsize=20, selectContrastingColor="1")

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

    # Add skin
    x=[8,8,12,12]
    y=[3,11,7,15]
    z=3

    skin_left=suture_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 16.5, 0.1], 
    sphere1Box=[x[0]-2, y[0]-2, -0.1, x[0]+2, y[0]+2, 3], sphere2Box=[x[1]-2, y[1]-2, -0.1, x[1]+2, y[1]+2, 3])

    skin_right=suture_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[10.5, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[10.5, -0.1, -2, 21, 16.5, 0.1],
    sphere3Box=[x[2]-2, y[2]-2, -0.1, x[2]+2, y[2]+2, 3], sphere4Box=[x[3]-2, y[3]-2, -0.1, x[3]+2, y[3]+2, 3], side=1) 

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Right Device", scale="1", drawDeviceFrame="1", 
    drawDevice="1", positionBase="20 20 0",  orientationBase="0.707 0 0 0.707", forceFeedBack="@SutureNeedle/LCPFFNeedle")

    root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Left Device", scale="1", drawDeviceFrame="1", 
    drawDevice="1", positionBase="0 20 0",  orientationBase="0.707 0 0 0.707", forceFeedBack="@SutureNeedleLeft/LCPFFNeedle")

    GeomagicDevice(parentNode=root, name='OmniRight', position="@GeomagicDeviceRight.positionDevice")
    GeomagicDevice(parentNode=root, name='OmniLeft', position="@GeomagicDeviceLeft.positionDevice")

    # Add needles
    suture_models.SutureNeedle(parentNode=root, name='SutureNeedle', monitor=True, file1="SutureTask_pos", file2="SutureTask_vel", file3="SutureTask_force", position="@GeomagicDeviceRight.positionDevice", external_rest_shape='@../OmniRight/DOFs') # To fall on sphere: dx=12, dy=3, dz=
    suture_models.SutureNeedleLeft(parentNode=root, name='SutureNeedle_left', monitor=True, file1="SutureTask_pos", file2="SutureTask_vel", file3="SutureTask_force", position="@GeomagicDeviceLeft.positionDevice", external_rest_shape='@../OmniLeft/DOFs') # To fall on sphere: dx=12, dy=3, dz=6

    #############################################################################################################

    # # Add Suture Controller
    root.addObject(SutureTrainingContactControllerDoubleHaptic(name="MyController", rootNode=root,  skin_left=skin_left, skin_right=skin_right))

    # Add training spheres: add when necessary
    suture_models.sphere(parentNode=root, name="Sphere1", translation=[x[0], y[0], z], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", SphereModelNumber="M1")
    suture_models.sphere(parentNode=root, name="Sphere2", translation=[x[1], y[1], z], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", SphereModelNumber="M2")
    suture_models.sphere(parentNode=root, name="Sphere3", translation=[x[2], y[2], z], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", SphereModelNumber="M3")
    suture_models.sphere(parentNode=root, name="Sphere4", translation=[x[3], y[3], z], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", SphereModelNumber="M4")

    return root


## This function defines a geomagic
# @param parentNode: parent node of the skin patch
# @param name: name of the behavior node
# @param rotation: rotation 
# @param translation: translation
def GeomagicDevice(parentNode=None, name=None, position=None):
    name=parentNode.addChild(name)
    name.addObject('MechanicalObject', template="Rigid3", name="DOFs", position=position)
    name.addObject('MechanicalStateController', template="Rigid3", listening="true", mainDirection="-1.0 0.0 0.0", handleEventTriggersUpdate="true")


# Controller for suture task training
# Handles the suture procedure

class SutureTrainingContactControllerDoubleHaptic(Sofa.Core.Controller):
    ## Constructor of the class. 
    # @param name: name of the controller
    # @param rootnode: path to the root node of the simulation
    # @param skin_left: path to the left skin patch root node
    # @param skin_right: path to the right skin patch root node
    
    
    def __init__(self, name, rootNode, skin_left, skin_right):
        Sofa.Core.Controller.__init__(self, name, rootNode, skin_left, skin_right)
        

        # Pass last created springs (LeftSkin-Needle)
        self.springsCreated_left=False
        # Pass last created springs (RightSkin-Needle)
        self.springsCreated_right=False

        self.boxAttached=None
        self.finished=True
        self.root=rootNode
        self.points=0

        self.first=1
        self.skin_left=skin_left
        self.skin_right=skin_right

    ## Method called at each begin of animation step
    # @param event: animation step event
    # If a contact between the needle tip and one of the skin patches, the function retrieves the skin triangle index of contact and 
    # checks if it belongs to one of the sphere boxes. If it does and no springs already exist between the needle and that skin patch,
    # it checks if springs exist between the needle and the other skin patch. If they do, the patches get connected by springs, 
    # the former springs needle-skin are removed. Then the new needle-skin springs are created. 
    # Finally, the color of the sphere is changed from red to green adn the user points are increased.
    # At the end of the function, the last needle-skin springs are removed on button press.

    def onAnimateBeginEvent(self, event):

        if self.first==1: 
            self.initializeStuff(suture_models.SutureNeedle.COLL_FRONT, suture_models.SutureNeedle.COLL_BACK_MO)
            self.first=0

        if self.root.GeomagicDeviceRight.findData('button2').value==1:
            suture_models.SutureNeedle.VIS.findData('isEnabled').value=0
            suture_models.SutureNeedleLeft.VIS.findData('isEnabled').value=1
            self.first=1
            return

        elif self.root.GeomagicDeviceLeft.findData('button2').value==1:
            suture_models.SutureNeedleLeft.VIS.findData('isEnabled').value=0
            suture_models.SutureNeedle.VIS.findData('isEnabled').value=1
            self.first=1
            return

        newMaterial="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
        coll_indexes=self.contact_listener.getContactElements() 
        coll_indexes_right=self.contact_listener_right.getContactElements() 

        # In case of collision (SkinLeft-Needle):
        if coll_indexes!=[] and self.finished==True:
            
            print("Contact on the left")
            self.finished=False

            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]

            # Does it belong to box 1? If it does: 
            if coll_index_skin in suture_models.Skin.sphere1Box.findData('triangleIndices').value:
                print("Box 1")    

                if self.springsCreated_left==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_right==True:

                        # Attach the two boxes: the old one and the new one
                        self.contactLeft_attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere1Box.findData('indices').value) # Left then right

                        # Then remove the previous springs.
                        self.contactLeft_disattach()                    
                        
                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere1Box
                    
                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(self.boxAttached)
                    
                    # Change sphere color
                    suture_models.sphere.M1.findData('material').value=newMaterial

                    # Increase the points!
                    self.points+=1

                self.finished=True
    
            
            # Does it belong to box 2? If it does: 
            elif coll_index_skin in suture_models.Skin.sphere2Box.findData('triangleIndices').value:
                print("Box 2")

                if self.springsCreated_left==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_right==True:

                        # Attach the two boxes: the old one and the new one
                        self.contactLeft_attachBoxes(self.boxAttached.findData('indices').value,suture_models.Skin.sphere2Box.findData('indices').value) # Left then right

                        # Then remove the previous springs.
                        self.contactLeft_disattach()          

                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere2Box

                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(self.boxAttached)

                    # Change sphere color
                    suture_models.sphere.M2.findData('material').value=newMaterial

                    # Increase the points!
                    self.points+=1

                self.finished=True
            
            else:
                print("No ball detected")
                self.finished=True
        
            
        # In case of collision (SkinRight-Needle):
        if coll_indexes_right!=[] and self.finished==True:
            print("Contact on the right")
            self.finished=False

            coll_indexes2=coll_indexes_right[0]
            coll_index_skin=coll_indexes2[1]
            # print("index", coll_index_skin)

            # Does it belong to a box? If it does: 
            if coll_index_skin in suture_models.Skin.sphere3Box.findData('triangleIndices').value:
                print("Box 3")

                if self.springsCreated_right==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_left==True:
                        # Attach the two boxes: the old one and the new one
                        self.contactRight_attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere3Box.findData('indices').value) # Check
    
                        # Then remove the previous springs.
                        self.contactRight_disattach()
                        
                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere3Box

                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(self.boxAttached)
                    
                    # Change sphere color
                    suture_models.sphere.M3.findData('material').value=newMaterial
                    
                    # Increase the points!
                    self.points+=1

                self.finished=True
    
            # Does it belong to a box? If it does: 
            elif coll_index_skin in suture_models.Skin.sphere4Box.findData('triangleIndices').value:
                print("Box 4")

                if self.springsCreated_right==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_left==True:
                        # Attach the two boxes: the old one and the new one
                        self.contactRight_attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere4Box.findData('indices').value) # Check
                        
                        # Then remove the previous springs.
                        self.contactRight_disattach()
                    
                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere4Box
                    
                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(self.boxAttached)

                    # Change sphere color
                    suture_models.sphere.M4.findData('material').value=newMaterial
                    
                    # Increase the points!
                    self.points+=1

                self.finished=True
            
            else:
                print("No ball detected")
                self.finished=True


        if self.root.GeomagicDevice.findData('button2').value==1:
            if self.springsCreated_left==True:
                self.contactRight_disattach()
            if self.springsCreated_right==True:
                self.contactLeft_disattach()

        # if self.root.GeomagicDevice.findData('button1').value==1:
        #     self.root.animate = False
        #     Config=open('Config.txt')
        #     for line in Config:
        #         pass
        #     user_name = line
        #     Config.close()

        #     fileName=f"{user_name}.txt"
        #     User = open(fileName, 'a')
        #     var = f"{self.points}"
        #     User.write(var)
        #     User.close()

        #     subprocess.call(['D:\Thesis\GUI\plotSuture.bat'])
        #     self.root.quit()

            
        
        #label .ending
        #print("no collision")

    ## Method that deefines the contact listeners between spheres and the needle and creates the force fields 
    def initializeStuff(self, sutColl_FRONT, sutColl_BACK):
        
        # Define spring force fields (SkinLeft-Needle; SkinRight-Needle; SkinLeft-SkinRight)
        self.spring_force_field = self.skin_left.addObject("StiffSpringForceField", name="LeftFF", object1 = suture_models.Skin.MO,  object2=sutColl_BACK)
        self.spring_force_field_right = self.skin_right.addObject("StiffSpringForceField", name="RightFF", object1 = suture_models.Skin.MO_right,  object2=sutColl_BACK)
        self.spring_force_field_skins = self.skin_left.addObject("StiffSpringForceField", name="SkinsFF", object1 = suture_models.Skin.MO,  object2=suture_models.Skin.MO_right)
        self.spring_force_field_skins_right = self.skin_right.addObject("StiffSpringForceField", name="SkinsRightFF", object1 = suture_models.Skin.MO_right,  object2=suture_models.Skin.MO)
        
        # Define contact listeners (SkinLeft-Needle; SkinRight-Needle)
        self.contact_listener = self.root.addObject('ContactListener', name="LeftContact", collisionModel1 = suture_models.Skin.COLL, collisionModel2 = sutColl_FRONT)
        self.contact_listener_right = self.root.addObject('ContactListener', name="RightContact", collisionModel1 = suture_models.Skin.COLL_right, collisionModel2 = sutColl_FRONT)

    ## Method that creates springs between the right skin patch and the left one.
    # @param indicesBox1: indices of the right box
    # @param indicesBox2: indices of the left box

    def contactRight_attachBoxes(self, indicesBox1, indicesBox2):
        print("Attach two boxes")

        # Create springs
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=1) for i, j in zip(indicesBox1,indicesBox2)] 
        self.spring_force_field_skins.addSprings(springs)
        print("Springs added between skins")

    ## Method that creates springs between the left skin patch and the right one.
    # @param indicesBox1: indices of the left box
    # @param indicesBox2: indices of the right box

    def contactLeft_attachBoxes(self, indicesBox1, indicesBox2):
        print("Attach two boxes")

        # Create springs
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=stiffness_springSkins, dampingFactor=2, restLength=1) for i, j in zip(indicesBox1,indicesBox2)] 
        self.spring_force_field_skins_right.addSprings(springs)
        print("Springs added between skins")

    ## Method that creates springs between the left skin patch and the needle.
    # @param box: indices of the box

    def contactLeft_attach(self, box):
        print("Contact on the left box detected!")
        indicesBox = box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springNeedle, dampingFactor=1, restLength=1) for i in indicesBox] 
        self.spring_force_field.addSprings(springs)
        self.springsCreated_left=True
        print("Springs created between needle and left skin")

    ## Method that removes springs between the right skin patch and the needle

    def contactLeft_disattach(self):
        print("Eliminating springs from right side of skin")
        
        N_Indices=len(self.boxAttached.findData('indices').value)
        self.spring_force_field_right.clear()

        print("Springs removed")
        self.springsCreated_right=False

    ## Method that creates springs between the right skin patch and the needle.
    # @param box: indices of the box

    def contactRight_attach(self, box):
        print("Contact on the right box detected!")
        indicesBox=box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springNeedle, dampingFactor=1, restLength=1) for i in indicesBox] 
        self.spring_force_field_right.addSprings(springs)
        self.springsCreated_right=True
        print("Springs created between needle and right skin")

    ## Method that removes springs between the left skin patch and the needle
    def contactRight_disattach(self):
        print("Eliminating springs from left side of skin")
        
        N_Indices=len(self.boxAttached.findData('indices').value)
        self.spring_force_field.clear()

        print("Springs removed")
        self.springsCreated_left=False



if __name__ == '__main__':
    main()


