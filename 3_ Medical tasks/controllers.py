import Sofa
import numpy as np
import models
import sys

# TRUE Controller for incision task
# class IncisionContactController(Sofa.Core.Controller):

#     def __init__(self, name, rootNode):
#         Sofa.Core.Controller.__init__(self, name, rootNode)

#         # # Define spring force field
#         self.spring_force_field = rootNode.addObject("StiffSpringForceField",  object1=models.Skin.MO,  object2=models.Skin.MO_right)
#         springs = [Sofa.SofaDeformable.LinearSpring(index1=40, index2=78, springStiffness=100, dampingFactor=5, restLength=1)] # Then set to right index
#         self.spring_force_field.addSprings(springs)
#         self.first=1
        
#         # Define contact listeners
#         self.contact_listener = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.Scalpel.COLL_FRONT)
#         self.contact_listener_right = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.Scalpel.COLL_FRONT)
#         self.indexes=[(0, 0, 0, 0)]

#     def onAnimateBeginEvent(self, event): # called at each begin of animation step
        
#         if self.first==1:
#             # IndicesLeft=models.Skin.borderBox.findData('indices').value
#             # IndicesRight=models.Skin.borderBox_right.findData('indices').value
#             # N_indices=sys.getsizeof(IndicesRight)
            
#             #print("Indices in Left Box:", models.Skin.borderBox.findData('indices').value)
#             #print("Indices in Right Box:", models.Skin.borderBox_right.findData('indices').value)
#             self.first=0
#             # Define spring force field

#             # self.spring_force_field = rootNode.addObject("StiffSpringForceField",  object1=models.Skin.MO,  object2=models.Skin.MO_right)
#             # springs = [Sofa.SofaDeformable.LinearSpring(index1=1, index2=1, springStiffness=100, dampingFactor=5, restLength=1)] # Then set to right index
#             # self.spring_force_field.addSprings(springs)

#         # If there is a contact between skin left or skin right (note: while is useless, this already loops)
#         if self.contact_listener.getNumberOfContacts()!=0 or self.contact_listener_right.getNumberOfContacts()!=0:

#             # If contact point is different from before
#             if self.indexes != self.contact_listener.getContactElements():

#                 # Remove spring
#                 self.spring_force_field.removeSpring(0)
#                 self.indexes = self.contact_listener.getContactElements() # Then set to right index






# TRIAL Controller for incision task
class IncisionContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)

        
        
        
        # Define contact listeners
        self.contact_listener = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.Scalpel.COLL_FRONT)
        self.contact_listener_right = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL_right, collisionModel2 = models.Scalpel.COLL_FRONT)

        self.spring_force_field = rootNode.addObject("StiffSpringForceField",  object1=models.Skin.MO,  object2=models.Skin.MO_right)

        self.first=True

    def onAnimateBeginEvent(self, event): # called at each begin of animation step
        
        if self.first==True:

            IndicesLeft=models.Skin.borderBox.findData('indices').value
            IndicesRight=models.Skin.borderBox_right.findData('indices').value
            N_indices=sys.getsizeof(IndicesRight)
            print(N_indices)


            self.first=False

            # Define spring force field
            # Se indicizzo: muore tutto
            springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=j, springStiffness=100, dampingFactor=5, restLength=1) for i, j in zip(IndicesLeft,IndicesRight)] # Then set to right index
            self.spring_force_field.addSprings(springs)
            
            #print("Indices in Left Box:", models.Skin.borderBox.findData('indices').value)
            #print("Indices in Right Box:", models.Skin.borderBox_right.findData('indices').value)
            
            # Define spring force field


        # If there is a contact between skin left or skin right (note: while is useless, this already loops)
        if self.contact_listener.getNumberOfContacts()!=0 or self.contact_listener_right.getNumberOfContacts()!=0:

            # If contact point is different from before
            if self.indexes != self.contact_listener.getContactElements():

                # Remove spring
                self.spring_force_field.removeSpring(0)
                self.indexes = self.contact_listener.getContactElements() # Then set to right index


# Controller for suture task
class SutureContactController(Sofa.Core.Controller):

    def __init__(self, name, rootNode):
        Sofa.Core.Controller.__init__(self, name, rootNode)
        
        
        # Define spring force field
        self.spring_force_field = rootNode.addObject("StiffSpringForceField",  object1 = models.Skin.MO,  object2=models.SutureNeedle.COLL_BACK_MO)

        # Define contact listener
        self.contact_listener = rootNode.addObject('ContactListener', collisionModel1 = models.Skin.COLL, collisionModel2 = models.SutureNeedle.COLL_FRONT)
        self.first=True

    def onAnimateBeginEvent(self, event): # called at each begin of animation step

        #print("Indices in ROI", models.Skin.aa.findData('indices').value)
        #print("Triangle indices in ROI", models.Skin.aa.findData('triangleIndices').value)
        print("Indices in ROI", models.Skin.aa.findData('indices').value)
        # If there is a contact between skin and instrument and it is the first detection
        
        if self.contact_listener.getNumberOfContacts()!=0 and self.first==True:

            #print("Triangle indices in ROI", models.Skin.aa.findData('triangleIndices').value)
            
            print("COLLISION!")

            # Retrieve the skin indexes that are in contact
            coll_indexes=self.contact_listener.getContactElements()
            coll_indexes2=coll_indexes[0]
            coll_index_skin=coll_indexes2[1]
            print("The triangle index is:", coll_index_skin)

            # Set first to False
            self.first=False

            # Create spring
            springs = [Sofa.SofaDeformable.LinearSpring(index1=i, index2=0, springStiffness=10, dampingFactor=5, restLength=1) for i in range(10)] # Then set to right index
            self.spring_force_field.addSprings(springs)
