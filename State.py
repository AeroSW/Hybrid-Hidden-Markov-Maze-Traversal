from Action import Action
import random
class State:
    
    def __init__(self, reward, term, sKey, action_list=None, count_actions=False):
        '''
        Preconditions:
            Required:
                Reward - float
                    The reward recieved for bein in this step at timestep t
                Term - int value with 1 representing that this state is terminal
                    This is an integer value with 1 depicting that this state is terminal
                sKey - Any Object Type that can be used in comparisons
                    Search Key for this state, can be any value
            Optional:
                action_list - List
                    List of actions this state can perform.
                    **Objects must be of type Action**
                count_actions - Boolean
                    Default value for this optional variable is False
                    True will allow every action performed by this state to contain a counter
                    to indicate how many times the action has been performed.
        Postconditions:
            This method initializes a State Object for use.
        Errors:
            TypeError - raised if the action_list parameter is not None or a list.
        '''
        # Create instance objects to store the required variables for later use in the program
        # self keyword plus a variable name creates an instance object of the variable.
        self.reward = reward # Store the float reward passed in as the reward for this state, it cannot be changed.
        # Compare the passed in term value with 1 to determine whether or not this state is a terminal state(Goal State)
        if(term == 1):
            self.terminal = True
        else:
            self.terminal = False
        self.state_key = sKey # Store the passed in search key as the default key for this state, it cannot be changed
        # Check the type of object that was passed in for action_list.  If nothing, create an empty list instance object.
        # If a list was passed in, set the instance object to be that list, else raise a type error since it was not a list.
        if(action_list is None):
            self.__actions = list()
        elif(isinstance(action_list, list)):
            self.__actions = action_list
        else:
            raise TypeError
        self.num_actions = self.__actions.__len__() # Keep track of the number of actions this state has.
        self.counting = count_actions # Store the boolean value for whether this state is tracking how many times an action is carried out
        if(self.counting):
            if(self.num_actions != 0):
                for i in self.__actions:
                    self.action_counter[self.__actions.getKey()] = 0
            else:
                self.action_counter = dict()
        
    def tryAction(self, aKey):
        '''
        Preconditions:
            aKey
                Search key for an action that needs to be attemped
        Postconditions:
            Returns the state that the action yielded for us or -1 if the action failed.
        '''
        for i in self.__actions:
            iKey = i.getKey() # Compare the key passed in with all the action's keys that are stored in this state.
            if(iKey == aKey):
                if(self.counting):
                    self.action_counter[iKey] = self.action_counter[iKey] + 1
                return i.testAction()
        return -1
    
    def getKey(self):
        '''
        Preconditions:
            None
        Postconditions:
            returns the search key for this state.
        '''
        return self.state_key
        
    def getReward(self):
        '''
        Preconditions:
            None
        Postconditions:
            returns the reward for being in this state at timestep t
        '''
        return self.reward
        
    def isTerminal(self):
        '''
        Preconditions:
            None
        Postconditions:
            Returns True or False respectively representing if this state is terminal or not
        '''
        return self.terminal
    
    def addAction(self, action):
        '''
        Preconditions:
            action - Action
                Takes an object of type Action
        Postconditions:
            Returns True if the adding of the object was successful
        Errors:
            NameError - if the object's search key is already present in another action object stored in the list
            TypeError - if the object passed in is not of type Action
        '''
        # Ensure that the object passed in is of type Action
        if(isinstance(action,Action)):
            aKey = action.getKey() # Get its key to compare with the current actions
            for i in self.__actions:
                iKey = i.getKey()
                # Compare the parameter's key with each previously stored action's key to prevent duplicates
                if(aKey == iKey):
                    raise NameError
            self.__actions.append(action) # If key does not exist already, store this action
            if(self.counting):
                self.action_counter[aKey] = 0 # If counting is enabled, create a counter index in the table and initialize it to 0.
            self.num_actions = self.num_actions + 1 # Increase number of actions this state has stored by 1.
            return True
        raise TypeError
    
    def getNumActions(self):
        '''
        Preconditions:
            None
        Postconditions:
            Returns the number of actions this state can perform.
        '''
        return self.num_actions
    
    def getCount(self):
        '''
        Preconditions:
            None
        Postconditions:
            If counting is implemented, it returns a list with 2 values
            in it.  Value 1 is the table storing the number of times each
            action is performed.  Value2 is a dictionary storing the individual
            actions' tables that have stored the number of times each possible
            state can be reached by an action.
        Errors:
            ValueError - If counting is not enabled, this error is raised
            
        '''
        if(self.counting == False):
            raise ValueError
        action_dict = dict()
        for i in self.__actions:
            action_dict[i.getKey()] = i.getCount()
        return self.action_counter, action_dict
    