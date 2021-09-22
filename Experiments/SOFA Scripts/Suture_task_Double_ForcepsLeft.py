# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
#from goto import goto, label
import subprocess
import read_Files
import time

import time

# Data
scale3d_skin="0.25 0.55 0.1"

# Spring stiffnesses
stiffness_springNeedle=150 #100 #300 slows sim
stiffness_springSkins=200
stiffness_springPlier=300#200



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
    [RepNumber,user_name]=read_Files.read()

    fileNamePos=f"Rep{RepNumber}_{user_name}_SuturePos_Forceps_Double"
    fileNameVel=f"Rep{RepNumber}_{user_name}_SutureVel_Forceps_Double"
    fileNameForce=f"Rep{RepNumber}_{user_name}_SutureForce_Forceps_Double"
    fileNamePosLeft=f"Rep{RepNumber}_{user_name}_SuturePosLeft_Forceps_Double"
    fileNameVelLeft=f"Rep{RepNumber}_{user_name}_SutureVelLeft_Forceps_Double"
    fileNameForceLeft=f"Rep{RepNumber}_{user_name}_SutureForceLeft_Forceps_Double"

    # Define root properties
    root.gravity=[0, 0, -2]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaCarving SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")

    # root.addObject('OglLabel', label="SUTURE TASK - TRAINING", x=20, y=20, fontsize=30, selectContrastingColor="1")
    # root.addObject('OglLabel', label="Pierce the skin in correnspondence of the green spheres", x=20, y=70, fontsize=20, selectContrastingColor="1")
    # root.addObject('OglLabel', label="starting from the one closest to the needle", x=20, y=100, fontsize=20, selectContrastingColor="1")
    #root.addObject('ViewerSetting', fullscreen="true")
    root.addObject('BackgroundSetting', color="0.3 0.5 0.8")
    
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

    # Add skin
    x=[8,8,13.5,13.5]
    y=[5,10.5,4.5,10]
    z=2
    boxSize=2

    skin_left=suture_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 16.5, 0.1], 
    sphere1Box=[x[0]-boxSize, y[0]-boxSize, -0.1, x[0]+boxSize, y[0]+boxSize, 3], sphere2Box=[x[1]-boxSize, y[1]-boxSize, -0.1, x[1]+boxSize, y[1]+boxSize, 3])

    skin_right=suture_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11.5, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[10.5, -0.1, -2, 21, 16.5, 0.1],
    sphere3Box=[x[2]-boxSize, y[2]-boxSize, -0.1, x[2]+boxSize, y[2]+boxSize, 3], sphere4Box=[x[3]-boxSize, y[3]-boxSize, -0.1, x[3]+boxSize, y[3]+boxSize, 3], side=1) 

    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    root.addObject('GeomagicDriver', name="GeomagicDeviceRight", deviceName="Right Device", scale="1", drawDeviceFrame="0", 
    drawDevice="0", positionBase="20 6 10",  orientationBase="0.707 0 0 0.707", forceFeedBack="@SutureNeedleLeft/LCPFFNeedle")

    root.addObject('GeomagicDriver', name="GeomagicDeviceLeft", deviceName="Left Device", scale="1", drawDeviceFrame="0", 
    drawDevice="0", positionBase="0 6 10",  orientationBase="0.707 0 0 0.707", forceFeedBack="@Forceps/LCPFFPlier")

    GeomagicDevice(parentNode=root, name='OmniRight', position="@GeomagicDeviceRight.positionDevice")
    GeomagicDevice(parentNode=root, name='OmniLeft', position="@GeomagicDeviceLeft.positionDevice")

    # Add needles
    suture_models.SutureNeedle(parentNode=root, name='SutureNeedleLeft', monitor=True, file1=fileNamePos, file2=fileNameVel, file3=fileNameForce, position="@GeomagicDeviceLeft.positionDevice", external_rest_shape='@../OmniLeft/DOFs',rx=90, ry=180, rz=0) # To fall on sphere: dx=12, dy=3, dz=
    suture_models.Plier(parentNode=root, name='Forceps', monitor=True, file1=fileNamePosLeft, file2=fileNameVelLeft, file3=fileNameForceLeft, position="@GeomagicDeviceRight.positionDevice", external_rest_shape='@../OmniRight/DOFs', rx=0, ry=0, rz=30) # To fall on sphere: dx=12, dy=3, dz=6

    ############################################################################################################

    # Add Suture Controller
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
        
        # Last created springs (LeftSkin-Needle, LeftRight-Needle, SkinLeft-Plier, SkinRight-Plier)
        self.springsCreated_left=False
        self.springsCreated_right=False
        self.springs_created_plier=False
        self.springs_created_plier_right=False

        self.boxAttached=None
        self.finished=True
        self.root=rootNode
        self.points=0

        self.skin_left=skin_left
        self.skin_right=skin_right

        # Define spring force fields (SkinLeft-Needle; SkinRight-Needle; SkinLeft-SkinRight; SkinLeft-Plier; SkinRight-Plier)
        self.spring_force_field = self.skin_left.addObject("StiffSpringForceField", name="LeftFF", object1 = suture_models.Skin.MO,  object2=suture_models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_right = self.skin_right.addObject("StiffSpringForceField", name="RightFF", object1 = suture_models.Skin.MO_right,  object2=suture_models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_skins = self.skin_left.addObject("StiffSpringForceField", name="SkinsFF", object1 = suture_models.Skin.MO,  object2=suture_models.Skin.MO_right)
        self.spring_force_field_skins_right = self.skin_right.addObject("StiffSpringForceField", name="SkinsRightFF", object1 = suture_models.Skin.MO_right,  object2=suture_models.Skin.MO)
        self.spring_force_field_plier = self.skin_left.addObject("StiffSpringForceField", name="LeftPlier", object1 = suture_models.Skin.MO,  object2=suture_models.Plier.COLL_BACK_MO)
        self.spring_force_field_plier_right = self.skin_right.addObject("StiffSpringForceField", name="RightPlier", object1 = suture_models.Skin.MO_right,  object2=suture_models.Plier.COLL_BACK_MO)
        
        # Define contact listeners (SkinLeft-Needle; SkinRight-Needle; SkinLeft-Plier; SkinRight-Plier)
        self.contact_listener = self.root.addObject('ContactListener', name="LeftContact", collisionModel1 = suture_models.Skin.COLL, collisionModel2 = suture_models.SutureNeedle.COLL_FRONT)
        self.contact_listener_right = self.root.addObject('ContactListener', name="RightContact", collisionModel1 = suture_models.Skin.COLL_right, collisionModel2 = suture_models.SutureNeedle.COLL_FRONT)
        self.contact_listener_plier = self.root.addObject('ContactListener', name="LeftContactPlier", collisionModel1 = suture_models.Skin.COLL, collisionModel2 = suture_models.Plier.COLL_FRONT)
        self.contact_listener_plier_right = self.root.addObject('ContactListener', name="RightContactPlier", collisionModel1 = suture_models.Skin.COLL_right, collisionModel2 = suture_models.Plier.COLL_FRONT)    


    ## Method called at each begin of animation step
    # @param event: animation step event
    # If a contact between the needle tip and one of the skin patches, the function retrieves the skin triangle index of contact and 
    # checks if it belongs to one of the sphere boxes. If it does and no springs already exist between the needle and that skin patch,
    # it checks if springs exist between the needle and the other skin patch. If they do, the patches get connected by springs, 
    # the former springs needle-skin are removed. Then the new needle-skin springs are created. 
    # Finally, the color of the sphere is changed from red to green adn the user points are increased.
    # At the end of the function, the last needle-skin springs are removed on button press.

    def onAnimateBeginEvent(self, event):
        #start_time = time.time()


        # New color
        newMaterial="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"

        # Contact listener
        coll_indexes=self.contact_listener.getContactElements() 
        coll_indexes_right=self.contact_listener_right.getContactElements()
        coll_indexes_plier=self.contact_listener_plier.getContactElements() 
        coll_indexes_plier_right=self.contact_listener_plier_right.getContactElements()
        
        # In case of collision (SkinLeft-Needle):
        if coll_indexes!=[] and self.finished==True:
            
            print("Contact on the left")
            self.finished=False

            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]

            # Does it belong to box 1? If it does: 
            if (coll_index_skin in suture_models.Skin.sphere1Box.findData('triangleIndices').value):
                print("Box 1")    
                
                # Change sphere color
                suture_models.sphere.M1.findData('material').value=newMaterial 

                if self.springsCreated_left==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_right==True:

                        # Attach the two boxes: the old one and the new one
                        self.contactLeft_attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere1Box.findData('indices').value) # Left then right

                        # Then remove the previous springs.
                        self.contactLeft_disattach(self.spring_force_field_right)     

                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere1Box
                    
                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(self.boxAttached, self.spring_force_field)
                    
                    # Increase the points!
                    self.points+=1

                self.finished=True
                self.contactRight_disattach(self.spring_force_field)   # ADDED TO BREAK SPRINGS WITHOUT BUTTON!
    
            
            # Does it belong to box 2? If it does: 
            elif (coll_index_skin in suture_models.Skin.sphere2Box.findData('triangleIndices').value):
                print("Box 2")
                # Change sphere color
                suture_models.sphere.M2.findData('material').value=newMaterial

                if self.springsCreated_left==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_right==True:

                        # Attach the two boxes: the old one and the new one
                        self.contactLeft_attachBoxes(self.boxAttached.findData('indices').value,suture_models.Skin.sphere2Box.findData('indices').value) # Left then right

                        # Then remove the previous springs.
                        self.contactLeft_disattach(self.spring_force_field_right)    

                          

                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere2Box

                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(self.boxAttached, self.spring_force_field)

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
            if (coll_index_skin in suture_models.Skin.sphere3Box.findData('triangleIndices').value):
                print("Box 3")
                # Change sphere color
                suture_models.sphere.M3.findData('material').value=newMaterial

                if self.springsCreated_right==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_left==True:
                        # Attach the two boxes: the old one and the new one
                        self.contactRight_attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere3Box.findData('indices').value) # Check
    
                        # Then remove the previous springs.
                        self.contactRight_disattach(self.spring_force_field)
                    
                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere3Box

                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(self.boxAttached, self.spring_force_field_right)
                    
                    # Increase the points!
                    self.points+=1

                self.finished=True
    
            # Does it belong to a box? If it does: 
            elif (coll_index_skin in suture_models.Skin.sphere4Box.findData('triangleIndices').value):
                print("Box 4")

                # Change sphere color
                suture_models.sphere.M4.findData('material').value=newMaterial

                if self.springsCreated_right==False:

                    # Do springs on the other side exist? If they do:
                    if self.springsCreated_left==True:
                        # Attach the two boxes: the old one and the new one
                        self.contactRight_attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere4Box.findData('indices').value) # Check
                        
                        # Then remove the previous springs.
                        self.contactRight_disattach(self.spring_force_field)
                    
                    # Set this box as the last one attached
                    self.boxAttached=suture_models.Skin.sphere4Box

                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(self.boxAttached, self.spring_force_field_right)
                    
                    # Increase the points!
                    self.points+=1

                self.finished=True
            
            else:
                print("No ball detected")
                self.finished=True


        # If the left button is pressed
        if self.root.GeomagicDeviceRight.findData('button2').value!=0:
            print("Button pressed")

            # If left springs exist: break them
            if self.springs_created_plier==True:
                print("Springs exist on plier")
                self.spring_force_field_plier.clear()
                self.springs_created_plier=False
                time.sleep(0.2)

            # If right springs exist: break them
            if self.springs_created_plier_right==True:
                print("Springs exist on plier")
                self.spring_force_field_plier_right.clear()
                self.springs_created_plier_right=False
                time.sleep(0.2)

            # If there is contact: create springs
            if coll_indexes_plier!=[]:
                coll_indexes2=coll_indexes_plier[0]
                coll_index_skin=coll_indexes2[1]           
                print("Collision left plier and button")
                if coll_index_skin in suture_models.Skin.sphere1Box.findData('triangleIndices').value:
                    print("Box 1 plier")    
                    suture_models.sphere.M1.findData('material').value="Default Diffuse 1 1 0.5 1 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
                    springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springPlier, dampingFactor=1, restLength=1) for i in suture_models.Skin.sphere1Box.findData('indices').value] 
                    self.spring_force_field_plier.addSprings(springs)
                    self.springs_created_plier=True
                    
                if coll_index_skin in suture_models.Skin.sphere2Box.findData('triangleIndices').value:
                    print("Box 2 plier")      
                    suture_models.sphere.M2.findData('material').value="Default Diffuse 1 1 0.5 1 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
                    springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springPlier, dampingFactor=1, restLength=1) for i in suture_models.Skin.sphere2Box.findData('indices').value] 
                    self.spring_force_field_plier.addSprings(springs)
                    self.springs_created_plier=True
                    
                time.sleep(0.2)
                return
                
            elif coll_indexes_plier_right!=[]:
                coll_indexes2=coll_indexes_plier_right[0]
                coll_index_skin=coll_indexes2[1]           
                print("Collision left plier and button")
                if coll_index_skin in suture_models.Skin.sphere3Box.findData('triangleIndices').value:
                    print("Box 3 plier")      
                    suture_models.sphere.M3.findData('material').value="Default Diffuse 1 1 0.5 1 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
                    springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springPlier, dampingFactor=1, restLength=1) for i in suture_models.Skin.sphere3Box.findData('indices').value] 
                    self.spring_force_field_plier_right.addSprings(springs)
                    self.springs_created_plier_right=True
                    
                if coll_index_skin in suture_models.Skin.sphere4Box.findData('triangleIndices').value:
                    print("Box 4 plier")      
                    suture_models.sphere.M4.findData('material').value="Default Diffuse 1 1 0.5 1 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
                    springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springPlier, dampingFactor=1, restLength=1) for i in suture_models.Skin.sphere4Box.findData('indices').value] 
                    self.spring_force_field_plier_right.addSprings(springs)
                    self.springs_created_plier_right=True
                    
                time.sleep(0.2)
                return
        #print("--- %s seconds ---" % (time.time() - start_time))


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

    def contactLeft_attach(self, box, ff):
        print("Contact on the left box detected!")
        indicesBox = box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springNeedle, dampingFactor=1, restLength=1) for i in indicesBox] 
        ff.addSprings(springs)
        self.springsCreated_left=True
        print("Springs created between needle and left skin")

    ## Method that removes springs between the right skin patch and the needle

    def contactLeft_disattach(self, ff):
        print("Eliminating springs from right side of skin")
        
        N_Indices=len(self.boxAttached.findData('indices').value)
        ff.clear()

        print("Springs removed")
        self.springsCreated_right=False

    ## Method that creates springs between the right skin patch and the needle.
    # @param box: indices of the box

    def contactRight_attach(self, box, ff):
        print("Contact on the right box detected!")
        indicesBox=box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=stiffness_springNeedle, dampingFactor=1, restLength=1) for i in indicesBox] 
        ff.addSprings(springs)
        self.springsCreated_right=True
        print("Springs created between needle and right skin")

    ## Method that removes springs between the left skin patch and the needle
    def contactRight_disattach(self, ff):
        print("Eliminating springs from left side of skin")
        
        N_Indices=len(self.boxAttached.findData('indices').value)
        ff.clear()

        print("Springs removed")
        self.springsCreated_left=False


  



if __name__ == '__main__':
    main()


