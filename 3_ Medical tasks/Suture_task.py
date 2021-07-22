# Required import for python
import Sofa
import numpy as np
import Sofa.SofaDeformable
import suture_models
#from goto import goto, label


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
skin_youngModulus=1700#300
thread_youngModulus=2000
skin_poissonRatio=0.49
thread_poissonRatio=0.8

geomagic=True
carving=False



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
    root.gravity=[0, 0, -7]
    root.dt=0.01

    # Required plugins
    root.addObject('RequiredPlugin', pluginName="SofaBaseMechanics SofaBaseTopology  Geomagic SofaCarving SofaBoundaryCondition  SofaConstraint SofaDeformable SofaEngine SofaGeneralLoader SofaGeneralObjectInteraction SofaGeneralSimpleFem SofaHaptics SofaImplicitOdeSolver SofaLoader SofaMeshCollision SofaOpenglVisual SofaRigid SofaSimpleFem SofaSparseSolver SofaUserInteraction SofaTopologyMapping SofaValidation")
    root.addObject('VisualStyle', displayFlags="showInteractionForceFields")

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


    # Define the variables


    #################### CARVING ########s#####################################
    if carving==True:
        activeVal=1
    else:
        activeVal=0

    root.addObject('CarvingManager', name="MyCarvingManager", active=activeVal, carvingDistance="0.4")
    CM=root.MyCarvingManager

    ##########################################################################

    # Add skin
    suture_models.Skin(parentNode=root, name='SkinLeft', rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], 
    scale3d=scale3d_skin, fixingBox=[-0.1, -0.1, -2, 10, 20, 0.1], borderBox=[7, -0.1, -2, 10, 20, 1], 
    importFile=skinVolume_fileName,  task="Suture")

    suture_models.Skin(parentNode=root, name='SkinRight', rotation=[0.0, 0.0, 0.0], translation=[11, 0, 0], 
    scale3d=scale3d_skin, fixingBox=[11, -0.1, -2, 22, 20, 0.1], borderBox=[11, -0.1, -2, 14, 20, 1],
    importFile=skinVolume_fileName,  side=1, task="Suture") 


    #################### GEOMAGIC TOUCH DEVICE ##################################################################
    if geomagic==True:

        root.addObject('GeomagicDriver', name="GeomagicDevice", deviceName="Default Device", 
        scale="1", drawDeviceFrame="1", drawDevice="0", positionBase="10 13 10",  orientationBase="0.707 0 0 0.707")
        
        suture_models.GeomagicDevice(parentNode=root, name='Omni')

    #############################################################################################################

    # Add needle
    suture_models.SutureNeedle(parentNode=root, name='SutureNeedle', monitor=True, file1="SutureTask_pos", file2="SutureTask_vel", file3="SutureTask_force", geomagic=geomagic, dx=0, dy=0, dz=10) # To fall on sphere: dx=12, dy=3, dz=6
    # Thread(parentNode=root, name="Thread", rotation=[90, 0, 0], translation=[0,10,0], importFile="mesh/threadCh2", scale3d=[0.3, 0.3, 0.1])
    # root.addObject('BilateralInteractionConstraint', template="Vec3d", object1=suture_models.SutureNeedle.COLL_BACK_MO, object2=Thread.MO,  first_point="0", second_point="0")


    # Add thread: not added to Geo yet
    # suture_models.Thread(parentNode=root, name='SutureThread', rotation=[-90, 90, 0], translation=[4, -20, 5], 
    # scale3d=[0.5, 0.5, 0.6],  fixingBox=None, importFile=threadVolume_fileName, geomagic=geomagic)

    # # Add Suture Controller
    root.addObject(SutureTrainingContactController(name="MyController", rootNode=root, CM=CM))

    # # Add training spheres: add when necessary
    suture_models.sphere(parentNode=root, name="Sphere1", translation=[8, 3.0, 3.0], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", M="M1")
    suture_models.sphere(parentNode=root, name="Sphere2", translation=[8, 13.0, 3.0], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", M="M2")
    suture_models.sphere(parentNode=root, name="Sphere3", translation=[12, 7.0, 3.0], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", M="M3")
    suture_models.sphere(parentNode=root, name="Sphere4", translation=[12, 17.0, 3.0], scale3d="1.5 1.5 1.5", color="1.0 0 0.0", M="M4")
    
    return root





# Controller for suture task training
class AddRemoveCarving(Sofa.Core.Controller):

    def __init__(self, name, rootNode, CM):
        Sofa.Core.Controller.__init__(self, name, rootNode, CM)
        
        # Define spring force fields (SkinLeft-Needle; SkinRight-Needle; SkinLeft-SkinRight)
        self.spring_force_field = rootNode.addObject("SpringForceField", name="LeftFF", object1 = suture_models.Skin.MO,  object2=suture_models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_right = rootNode.addObject("SpringForceField", name="RightFF", object1 = suture_models.Skin.MO_right,  object2=suture_models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_skins = rootNode.addObject("SpringForceField", name="SkinsFF", object1 = suture_models.Skin.MO,  object2=suture_models.Skin.MO_right)

        # Define contact listeners (SkinLeft-Needle; SkinRight-Needle)
        self.contact_listener = rootNode.addObject('ContactListener', name="LeftContact", collisionModel1 = suture_models.Skin.COLL, collisionModel2 = suture_models.SutureNeedle.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', name="RightContact", collisionModel1 = suture_models.Skin.COLL_right, collisionModel2 = suture_models.SutureNeedle.COLL_FRONT)

        # Pass last created springs (LeftSkin-Needle)
        self.springsCreated_left=False
        # Pass last created springs (RightSkin-Needle)
        self.springsCreated_right=False

        # Pass last attached box
        self.boxAttached=None

        self.finished=True
        self.first=1

        self.root=rootNode
        self.CM=CM

        
    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):
        
        if self.first==1:

            # Carving was False
            if self.CM.findData('active').value==0:

                # Set the carving variables
                self.CM.findData('active').value=1
                suture_models.SutureNeedle.COLL_FRONT_TAG.findData('tags').value=['CarvingTool']
                suture_models.Skin.COLL_TAG.findData('tags').value=['CarvingSurface']
                self.CM.reinit()
                suture_models.SutureNeedle.COLL_FRONT_TAG.reinit() 
                suture_models.Skin.COLL_TAG.reinit()
                print("Added Carving")
                carving=True

            # Carving was True
            elif self.CM.findData('active').value==1:

                # Remove the carving variables
                self.CM.findData('active').value=0
                suture_models.SutureNeedle.COLL_FRONT_TAG.findData('tags').value=['None']
                suture_models.Skin.COLL_TAG.findData('tags').value=['None']
                self.CM.reinit()
                suture_models.SutureNeedle.COLL_FRONT_TAG.reinit() 
                suture_models.Skin.COLL_TAG.reinit()
                print("Removed Carving")
                carving=False

            else:
                print("Eh allora fanculo")

            self.first=0


   

# Controller for suture task training
class SutureTrainingContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode, CM):
        Sofa.Core.Controller.__init__(self, name, rootNode, CM)
        
        # Define spring force fields (SkinLeft-Needle; SkinRight-Needle; SkinLeft-SkinRight)
        self.spring_force_field = rootNode.addObject("SpringForceField", name="LeftFF", object1 = suture_models.Skin.MO,  object2=suture_models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_right = rootNode.addObject("SpringForceField", name="RightFF", object1 = suture_models.Skin.MO_right,  object2=suture_models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_skins = rootNode.addObject("SpringForceField", name="SkinsFF", object1 = suture_models.Skin.MO,  object2=suture_models.Skin.MO_right)

        # Define contact listeners (SkinLeft-Needle; SkinRight-Needle)
        self.contact_listener = rootNode.addObject('ContactListener', name="LeftContact", collisionModel1 = suture_models.Skin.COLL, collisionModel2 = suture_models.SutureNeedle.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', name="RightContact", collisionModel1 = suture_models.Skin.COLL_right, collisionModel2 = suture_models.SutureNeedle.COLL_FRONT)

        # Pass last created springs (LeftSkin-Needle)
        self.springsCreated_left=False
        # Pass last created springs (RightSkin-Needle)
        self.springsCreated_right=False

        # Pass last attached box
        self.boxAttached=None

        self.finished=True
        self.first=1

        self.root=rootNode
        self.CM=CM

        
    # Function called at each begin of animation step
    def onAnimateBeginEvent(self, event):


        newMaterial="Default Diffuse 1 0 0.5 0 1 Ambient 1 0 0.1 0 1 Specular 0 0 0.5 0 1 Emissive 0 0 0.5 0 1 Shininess 0 45"
        # In case of collision (SkinLeft-Needle):
        if self.contact_listener.getNumberOfContacts()!=0 and self.finished==True:
            
            self.finished=False
            print("Contact on the left")
                  
            # Save collision element
            try: 
                coll_indexes=self.contact_listener.getContactElements() 
            except:
                #goto .nextif
                exit()

            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]
            print("index", coll_index_skin)

            # Does it belong to box 1? If it does: 
            if coll_index_skin in suture_models.Skin.sphere1Box.findData('triangleIndices').value:
                print("Box 1")    

                # Do springs on the other side exist? If they do:
                if self.springsCreated_right==True:
                    # Attach the two boxes: the old one and the new one
                    self.attachBoxes(suture_models.Skin.sphere1Box.findData('indices').value, self.boxAttached.findData('indices').value) # Left then right

                    # Then remove the previous springs.
                    self.contactLeft_disattach()                    
                    
                # Set this box as the last one attached
                self.boxAttached=suture_models.Skin.sphere1Box

                if self.springsCreated_left==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(self.boxAttached)

                suture_models.sphere.M1.findData('material').value=newMaterial

                # This is the last sphere that needs to be reached: after that, clear the FF
                self.contactRight_disattach()

                self.finished=True
    
            
            # Does it belong to box 2? If it does: 
            elif coll_index_skin in suture_models.Skin.sphere2Box.findData('triangleIndices').value:
                print("Box 2")

                # Do springs on the other side exist? If they do:
                if self.springsCreated_right==True:
                    # Attach the two boxes: the old one and the new one
                    self.attachBoxes(suture_models.Skin.sphere2Box.findData('indices').value, self.boxAttached.findData('indices').value) # Left then right
                    
                    # Then remove the previous springs.
                    self.contactLeft_disattach()        
                    print("done")          

                # Set this box as the last one attached
                self.boxAttached=suture_models.Skin.sphere2Box

                if self.springsCreated_left==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(self.boxAttached)

                suture_models.sphere.M2.findData('material').value=newMaterial
                self.finished=True
            
            else:
                print("No ball detected")
                self.finished=True

            
        #label .nextif
        # In case of collision (SkinRight-Needle):
        if self.contact_listener_right.getNumberOfContacts()!=0 and self.finished==True:
            
            self.finished=False
            print("Contact on the right")
            
            # Save collision element
            try: 
                coll_indexes=self.contact_listener_right.getContactElements() 
            except:
                #goto .ending
                exit()

            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]
            print("index", coll_index_skin)

            # Does it belong to a box? If it does: 
            if coll_index_skin in suture_models.Skin.sphere3Box.findData('triangleIndices').value:
                print("Box 3")

                # Do springs on the other side exist? If they do:
                if self.springsCreated_left==True:
                    # Attach the two boxes: the old one and the new one
                    self.attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere3Box.findData('indices').value) # Check
   
                    # Then remove the previous springs.
                    self.contactRight_disattach()
                    
                # Set this box as the last one attached
                self.boxAttached=suture_models.Skin.sphere3Box

                if self.springsCreated_right==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(self.boxAttached)
                
                suture_models.sphere.M3.findData('material').value=newMaterial
 
                self.finished=True
    
            # Does it belong to a box? If it does: 
            elif coll_index_skin in suture_models.Skin.sphere4Box.findData('triangleIndices').value:
                print("Box 4")

                # Do springs on the other side exist? If they do:
                if self.springsCreated_left==True:
                    # Attach the two boxes: the old one and the new one
                    self.attachBoxes(self.boxAttached.findData('indices').value, suture_models.Skin.sphere4Box.findData('indices').value) # Check
                    
                    # Then remove the previous springs.
                    self.contactRight_disattach()
                   
                # Set this box as the last one attached
                self.boxAttached=suture_models.Skin.sphere4Box

                if self.springsCreated_right==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(self.boxAttached)

                suture_models.sphere.M4.findData('material').value=newMaterial
                self.finished=True
            
            else:
                print("No ball detected")
                self.finished=True
        
        #label .ending
        #print("no collision")



    def attachBoxes(self, indicesBox1, indicesBox2):
        print("Attach two boxes")

        # Create springs
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=50, dampingFactor=5, restLength=1) for i, j in zip(indicesBox1,indicesBox2)] 
        self.spring_force_field_skins.addSprings(springs)
        print("Springs added between skins")

    def contactLeft_attach(self, box):
        print("Contact on the left box detected!")

        indicesBox = box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=5, restLength=1) for i in indicesBox] 
        self.spring_force_field.addSprings(springs)
        self.springsCreated_left=True
        print("Springs created between needle and left skin")

    def contactLeft_disattach(self):
        print("Eliminating springs from right side of skin")
        
        N_Indices=len(self.boxAttached.findData('indices').value)
        print("The old box has", N_Indices, "indices")

        # for i in range(N_Indices):
        #     print("removing springs")
        #     self.spring_force_field_right.removeSpring(i)

        self.spring_force_field_right.clear()

        print("removed")
        self.springsCreated_right=False

    def contactRight_attach(self, box):
        print("Contact on the right box detected!")

        indicesBox=box.findData('indices').value

        # Create springs
        print("Create springs")
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=5, restLength=1) for i in indicesBox] 
        self.spring_force_field_right.addSprings(springs)
        self.springsCreated_right=True
        print("Springs created between needle and right skin")

    def contactRight_disattach(self):
        print("Eliminating springs from left side of skin")
        
        N_Indices=len(self.boxAttached.findData('indices').value)
        # print("The old box has", N_Indices, "indices")

        # for i in range(N_Indices):
        #     print("removing springs")
        #     self.spring_force_field.removeSpring(i)

        self.spring_force_field.clear()

        print("removed")
        self.springsCreated_left=False






if __name__ == '__main__':
    main()
