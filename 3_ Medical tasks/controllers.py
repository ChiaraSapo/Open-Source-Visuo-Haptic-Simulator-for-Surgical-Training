import Sofa
import numpy as np
import models
import sys


# Controller for incision task
class IncisionContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)

        # Define contact listeners for right and left skins
        self.contact_listener = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.Scalpel.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.Scalpel.COLL_FRONT)

        self.spring_force_field = rootNode.addObject("StiffSpringForceField",  object1=models.Skin.MO,  object2=models.Skin.MO_right)

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
            N_indices=sys.getsizeof(IndicesRight)

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



# Controller for suture task
#ToDo: set to right indices
class SutureContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        # Define spring force field

        self.spring_force_field = rootNode.addObject("StiffSpringForceField",  object1 = models.Skin.MO,  object2=models.SutureNeedle.COLL_BACK_MO)

        # Define contact listener
        self.contact_listener = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.SutureNeedle.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.SutureNeedle.COLL_FRONT)
        self.first=True


    def onAnimateBeginEvent(self, event): # called at each begin of animation step

        # If there is a contact between skin and instrument and it is the first detection
        
        if (self.contact_listener.getNumberOfContacts()!=0 or self.contact_listener_right.getNumberOfContacts()!=0) and self.first==True:
            
            print("COLLISION!")

            # Retrieve the skin indexes that are in contact
            coll_indexes=self.contact_listener.getContactElements() # then set to one of the 2 contact listeners
            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]
            print("The triangle index is:", coll_index_skin)

            # Set first to False
            self.first=False

            # Create spring
            springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=5, restLength=1) for i in range(10)] 
            self.spring_force_field.addSprings(springs)



# Controller for suture task training
class SutureTrainingContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        # Define spring force field

        self.spring_force_field = rootNode.addObject("StiffSpringForceField",  object1 = models.Skin.MO,  object2=models.SutureNeedle.COLL_BACK_MO)

        # Define contact listener
        self.contact_listener = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.SutureNeedle.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.SutureNeedle.COLL_FRONT)

        self.first=True
        self.root=rootNode
        self.side=None

    def onAnimateBeginEvent(self, event): # called at each begin of animation step
        # print(sys.getsizeof(models.Skin.sphere4Box.findData('indices').value))

        # If there is a contact between skin and instrument and the skin patch is different from before or it is the first detection

        if self.contact_listener.getNumberOfContacts()!=0 and (self.side=="Right" or self.first==True):
            self.contactLeft_attach()
            self.first=False
            
        if self.contact_listener_right.getNumberOfContacts()!=0 and (self.side=="Left" or self.first==True):
            self.contactRight_attach()
            self.first=False

        if self.contact_listener.getNumberOfContacts()!=0 and (self.side=="Right" or self.first==True):
            self.contactLeft_disattach()
            self.first=False
            
        if self.contact_listener_right.getNumberOfContacts()!=0 and (self.side=="Left" or self.first==True):
            self.contactRight_disattach()
            self.first=False


    def attachSprings(self, sphereName, indices, translation): 

        # Create sphere: it is created but not visualized. To see it click on view then again on graph so that it is updated
        models.sphere(parentNode=self.root, name=sphereName, translation=translation, scale3d="1.6 1.6 1.6", color="1.0 0.5 0.0")
        
        # Create spring
        springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=50, dampingFactor=5, restLength=1) for i in indices] 
        self.spring_force_field.addSprings(springs)
    
    def contactLeft_attach(self):
        print("COLLISION Left!")
        self.side="Left"

        # Retrieve the skin indexes that are in contact
        coll_indexes=self.contact_listener.getContactElements() 
        coll_indexes2=coll_indexes[0]
        coll_index_skin=coll_indexes2[1]
        #print("The triangle index is:", coll_index_skin)

        if coll_index_skin in models.Skin.sphere1Box.findData('triangleIndices').value:
            self.attachSprings(sphereName="Sphere12", indices=models.Skin.sphere1Box.findData('indices').value, translation=[49, 10.0, 0.0])

        elif coll_index_skin in models.Skin.sphere2Box.findData('triangleIndices').value:
            self.attachSprings(sphereName="Sphere22", indices=models.Skin.sphere2Box.findData('indices').value, translation=[49, 30.0, 0.0])
            
        else:
            print("Ball not encountered")

    def contactRight_attach(self):
        print("COLLISION Right!")
        self.side="Right"

        # Retrieve the skin indexes that are in contact
        coll_indexes=self.contact_listener_right.getContactElements() 
        coll_indexes2=coll_indexes[0]
        coll_index_skin=coll_indexes2[1]
        #print("The triangle index is:", coll_index_skin)
        
        if coll_index_skin in models.Skin.sphere3Box.findData('triangleIndices').value:
            self.attachSprings(sphereName="Sphere32", indices=models.Skin.sphere3Box.findData('indices').value, translation=[52, 20.0, 0.0])

        elif coll_index_skin in models.Skin.sphere4Box.findData('triangleIndices').value:
            self.attachSprings(sphereName="Sphere42", indices=models.Skin.sphere4Box.findData('indices').value, translation=[52, 40.0, 0.0])
            
        else:
            print("Ball not encountered")
    
    def contactLeft_disattach(self):
        self.side="Left"
        for i in range(4):
            self.spring_force_field.removeSpring(i)
        self.contactRight_attach()

    def contactRight_disattach(self):
        self.side="Right"
        for i in range(4):
            self.spring_force_field.removeSpring(i)
        self.contactLeft_attach()




