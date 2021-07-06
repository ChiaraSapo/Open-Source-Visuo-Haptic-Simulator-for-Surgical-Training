import Sofa
import numpy as np
import models
import sys
import time

# Controller for incision task
class IncisionContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)

        # Define contact listeners for right and left skins
        self.contact_listener = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.Scalpel.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.Scalpel.COLL_FRONT)

        self.first=True
        self.first_coll=True
        self.indexes=0

    def onAnimateBeginEvent(self, event): # called at each begin of animation step
        
        if self.first==True:
            # Uncomment to recompute
            #IndicesLeft=models.Skin.borderBox.findData('indices').value
            #print(IndicesLeft)
            #IndicesRight=models.Skin.borderBox_right.findData('indices').value
            #print(IndicesRight)
            IndicesLeft=[5, 7, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]
            IndicesRight=[1, 3, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
            N_indices=len(IndicesRight)

            self.first=False

            # Define spring force field: there should be more springs though
            springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=100, dampingFactor=5, restLength=0.001) for i, j in zip(IndicesLeft,IndicesRight)] # Then set to right index
            self.spring_force_field.addSprings(springs)



        # If there is a contact between skin left or skin right (note: while is useless, this already loops)
        if (self.contact_listener.getNumberOfContacts()!=0 or self.contact_listener_right.getNumberOfContacts()!=0) and self.first_coll==True:
            
            print("COLLISION!")

            # If contact point is different from before
            if self.indexes != self.contact_listener.getContactElements():

                # Remove spring
                self.spring_force_field.removeSpring(2)

                self.indexes = self.contact_listener.getContactElements() 
                self.first_coll=False



# Controller for suture task training
class SutureTrainingContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        # Define spring force fields (SkinLeft-Needle; SkinRight-Needle; SkinLeft-SkinRight)
        self.spring_force_field = rootNode.addObject("StiffSpringForceField", name="LeftFF", object1 = models.Skin.MO,  object2=models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_right = rootNode.addObject("StiffSpringForceField", name="RightFF", object1 = models.Skin.MO_right,  object2=models.SutureNeedle.COLL_BACK_MO)
        self.spring_force_field_skins = rootNode.addObject("StiffSpringForceField", name="SkinsFF", object1 = models.Skin.MO,  object2=models.Skin.MO_right)

        # Define contact listeners (SkinLeft-Needle; SkinRight-Needle)
        self.contact_listener = rootNode.addObject('ContactListener', name="LeftContact", collisionModel1 = models.Skin.COLL, collisionModel2 = models.SutureNeedle.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', name="RightContact", collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.SutureNeedle.COLL_FRONT)

        # Pass last created springs (LeftSkin-Needle)
        self.springsCreated_left=False
        # Pass last created springs (RightSkin-Needle)
        self.springsCreated_right=False

        # Pass last attached box
        self.boxAttached=None

        
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
            if coll_index_skin in models.Skin.sphere1Box.findData('triangleIndices').value:
                print("Box 1")
                
                if self.boxAttached == None:
                    self.boxAttached = models.Skin.sphere1Box

                # Do springs on the other side exist? If they do:
                if self.springsCreated_right==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(models.Skin.sphere1Box.findData('indices').value, self.boxAttached.findData('indices').value) # Left then right
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactLeft_disattach()
                # Set this box as the last one attached
                self.boxAttached=models.Skin.sphere1Box

                if self.springsCreated_left==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactLeft_attach(coll_indexes, self.boxAttached)
            
            # Does it belong to box 2? If it does: 
            elif coll_index_skin in models.Skin.sphere2Box.findData('triangleIndices').value:
                print("Box 2")

                if self.boxAttached == None:
                    self.boxAttached = models.Skin.sphere2Box
                
                # Do springs on the other side exist? If they do:
                if self.springsCreated_right==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(models.Skin.sphere2Box.findData('indices').value, self.boxAttached.findData('indices').value) # Left then right
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactLeft_disattach()
                # Set this box as the last one attached
                self.boxAttached=models.Skin.sphere2Box

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
            if coll_index_skin in models.Skin.sphere3Box.findData('triangleIndices').value:
                print("Box 3")

                if self.boxAttached == None:
                    self.boxAttached = models.Skin.sphere3Box
                
                # Do springs on the other side exist? If they do:
                if self.springsCreated_left==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(self.boxAttached.findData('indices').value, models.Skin.sphere3Box.findData('indices').value) # Check
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactRight_disattach()
                # Set this box as the last one attached
                self.boxAttached=models.Skin.sphere3Box

                if self.springsCreated_right==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(coll_indexes, self.boxAttached)
            
            # Does it belong to a box? If it does: 
            elif coll_index_skin in models.Skin.sphere4Box.findData('triangleIndices').value:
                print("Box 4")

                if self.boxAttached == None:
                    self.boxAttached = models.Skin.sphere4Box
                
                # Do springs on the other side exist? If they do:
                if self.springsCreated_left==True:
                    # Attach the two boxes: the old one and the new one
                    attached=self.attachBoxes(self.boxAttached.findData('indices').value, models.Skin.sphere4Box.findData('indices').value) # Check
                    while attached==False:
                        time.sleep(1)
                    # Then remove the previous springs.
                    self.contactRight_disattach()
                # Set this box as the last one attached
                self.boxAttached=models.Skin.sphere4Box

                if self.springsCreated_right==False:
                    # Create springs SkinLeft-Back_Needle
                    self.contactRight_attach(coll_indexes, self.boxAttached)

            else:
                print("No ball detected")

    def attachBoxes(self, indicesBox1, indicesBox2):
        print("Attach two boxes")

        # Create springs
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=50, dampingFactor=5, restLength=1) for i, j in zip(indicesBox1,indicesBox2)] 
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
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=5, restLength=1) for i in indicesBox] 
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





