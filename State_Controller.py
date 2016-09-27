from State import State
from Action import Action
class State_Controller:
    def __init__(self, curr_state = None, state_list = None):
        '''
        Preconditions:
            curr_state - State or None
                Possible initial state for the controller to be in.
            state_list - list or None
                List of all states that this controller should have
                access to.
        Postconditions:
            Initializes a State_Controller object
        '''
        if(state_list is None):
            self.state_list = list()
        elif(isinstance(state_list, list)):
            self.state_list = state_list
        else:
            raise TypeError
        if(curr_state is None):
            self.curr_state = None
        elif(isinstance(curr_state, State)):
            self.curr_state = curr_state
            self.state_list.append(curr_state)
        else:
            raise TypeError
        self.state_list_size = self.state_list.__len__()
    
    def addState(self, state):
        '''
        Preconditions:
            state - State
                Adds a state Object to this controller's state
                list.
        Postconditions:
            Returns True if the state was successfully added to
            the list.
        Errors:
            TypeError - If parameter state is not of type State,
            this error is raised.
            NameError - If this state already exists in the list.
            This prevents duplicates.
        '''
        if(isinstance(state, State)):
            sKey = state.getKey()
            for i in self.state_list:
                iKey = i.getKey()
                if(iKey == sKey):
                    raise NameError
            self.state_list.append(state)
            if(self.state_list_size == 0):
                self.curr_state = state
            self.state_list_size = self.state_list_size + 1
            return True
        raise TypeError
    
    def addAction(self, action):
        '''
        Preconditions:
            actions - Action
                This passes a new action to be added to the current
                state's action list.
        Postconditions:
            Returns the result of adding the current action to the
            current state's action list.
        '''
        sKey = self.curr_state.getKey()
        aKey = action.getKey()
        return self.curr_state.addAction(action)
    
    def switchState(self, sKey):
        '''
        Preconditions:
            sKey - Comparable Object
                To switch states, this parameter is used to see if the
                state is part of this controller's list.
        Postconditions:
            Returns True if the curr_state was switched successfully
            to the new state.
            False if the state does not exist.
        '''
        for i in self.state_list:
            iKey = i.getKey()
            if(iKey == sKey):
                self.curr_state = i
                return True
        return False
    
    def tryAction(self, aKey):
        '''
        Preconditions:
        Postconditions:
        '''
        return self.curr_state.tryAction(aKey)
    
    def getState(self):
        '''
        Preconditions:
        Postconditions:
        '''
        return self.curr_state
    
    def getNumStates(self):
        '''
        Preconditions:
        Postconditions:
        '''
        return self.state_list_size
    
    def returnCount(self):
        '''
        Preconditions:
        Postconditions:
        '''
        return self.curr_state.getCount()
    
    def isTerminal(self):
        '''
        Preconditions:
        Postconditions:
        '''
        return self.curr_state.isTerminal()
    
    def getReward(self):
        '''
        Preconditions:
        Postconditions:
        '''
        return self.curr_state.getReward()
    
    