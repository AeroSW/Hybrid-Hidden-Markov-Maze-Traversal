from State_Controller import State_Controller
import random
import math
class Reinforcement_Maze:
    # Instance Variables:
    #   __state_list      <- state_controller
    #   __state_list_sze  <- number_of_states_in_state_controller
    #   gamma           <- gamma
    #   utility_list    <- current utility list for this maze
    #   policy_list     <- current optimal policy based on utilities being chosen
    def __init__(self, gamma, state_controller):
        '''
        Preconditions:
            gamma - float
                This is the "cost" for not being in a terminal state.
            state_controller - State_Controller
                This object allows methods in this class to have states and
                actions.
        Postconditions:
            This method initializes a Reinforcement_Maze object for use.
        '''
        self.__state_list = state_controller
        self.__state_list_sze= self.__state_list.getNumStates()
        self.gamma = gamma
        self.utility_list = dict()  # Initialize 2 dictionaries that will store the utilities and the best policy for given utility.
        self.policy_list = dict()
        for i in range(self.__state_list_sze): # utility_list and policy_list have the same keys as the states used in this class.
            self.utility_list[i+1] = 0
        for i in range(self.__state_list_sze):
            self.policy_list[i+1] = 0
            
    def __createAdjustedUtilityList(self, val=1.0):
        '''
        Preconditions:
            val - float
                default - 1.0
                val represents a given value to add to all utilities in the original
                utility_list instance without overriding the utility_list instance.
        Postconditions:
            Returns a new utility dictionary with adjusted values in it.
        '''
        other_u_list = dict()
        keyList = list(self.utility_list.keys())
        for i in keyList:
            other_u_list[i] = self.utility_list[i] + val
        return other_u_list
    
    def __createCopyUtilityList(self):
        '''
        Preconditions:
            None
        Postconditions:
            Returns a copied utility list of the instance utility list.
        '''
        other_u_list=dict()
        keyList = list(self.utility_list.keys())
        for i in keyList:
            other_u_list[i] = self.utility_list[i]
        return other_u_list
    
    def createUtilities(self, tol, averages):
        '''
        Preconditions:
            tol - float
                tol, short for tolerance, is the minimal amount that a previous
                utility and a newly generated utility can differ by.
            averages - dictionary
                These are computed probabilities that each action has a chance of
                succeeding with.  Generally created by 'Counting the number of times
                a state is reached from another state by an action, divided by the
                number of times that action from the initial state was performed.'
        Postconditiosn:
            Returns a copy of this class's utility list after running it
            through value iteration some random number of times.
        '''
        other_u_list = self.__createAdjustedUtilityList(1)
        for i in range(self.__state_list_sze):
            last_utility_for_s = self.utility_list[i+1]
            curr_utility_for_s = other_u_list[i+1]
            util_diff = curr_utility_for_s - last_utility_for_s
            util_diff = math.fabs(util_diff)
            #count = 0
            while(util_diff > tol):
                #print(count)
                last_utility_for_s = curr_utility_for_s
                temp = self.__ValueIteration(i+1, averages, self.utility_list)
                self.utility_list[i+1] = temp[0]
                self.policy_list[i+1] = temp[1]
                curr_utility_for_s = self.utility_list[i+1]
                util_diff = curr_utility_for_s - last_utility_for_s
                util_diff = math.fabs(util_diff)
                #count += 1
        return self.utility_list.copy(), self.policy_list.copy()
    
    def __ValueIteration(self, curr_state_key, averages, u_list):
        '''
        Preconditions:
            curr_state_key - comparable Object
                Search key for the state we want to generate a utility
                for.
            averages - dictionary
                These are computed probabilities that each action has a chance of
                succeeding with.  Generally created by 'Counting the number of times
                a state is reached from another state by an action, divided by the
                number of times that action from the initial state was performed.'
            u_list - dictionary
                A utility list that contains all current utilities for all possible
                states in this class.
        Postconditions:
            Returns a new utility and policy for the curr_state
            identified by the curr_state_key parameter passed in.
        '''
        self.__state_list.switchState(curr_state_key)
        if(self.__state_list.isTerminal()):
            return self.__state_list.getReward(), 0
        policy = 0
        action_dictionaries = averages[curr_state_key]
        up_dictionaries = action_dictionaries[1]
        up_key_list = list(up_dictionaries.keys())
        left_dictionaries = action_dictionaries[2]
        left_key_list = list(left_dictionaries.keys())
        down_dictionaries = action_dictionaries[3]
        down_key_list = list(down_dictionaries.keys())
        right_dictionaries = action_dictionaries[4]
        right_key_list = list(right_dictionaries.keys())
        up_summ = 0
        for i in up_key_list:
            up_summ = up_summ + (u_list[i] * up_dictionaries[i])
        left_summ = 0
        for i in left_key_list:
            left_summ = left_summ + (u_list[i] * left_dictionaries[i])
        down_summ = 0
        for i in down_key_list:
            down_summ = down_summ + (u_list[i] * down_dictionaries[i])
        right_summ = 0
        for i in right_key_list:
            right_summ = right_summ + (u_list[i] * right_dictionaries[i])
        
        randomAU = random.randint(1,10000) #randomAU = randomActionUtility
        highest = None
        policy = None
        if(randomAU > 1500):
            highest = up_summ
            policy = 1
            if(left_summ > highest):
                highest = left_summ
                policy = 2
            if(down_summ > highest):
                highest = down_summ
                policy = 3
            if(right_summ > highest):
                highest = right_summ
                policy = 4
        else:
            if(randomAU <= 375):
                highest = up_summ
                policy = 1
            elif(randomAU > 375 and randomAU <= 750):
                highest = left_summ
                policy = 2
            elif(randomAU > 750 and randomAU <= 1125):
                highest = down_summ
                policy = 3
            else:
                highest = right_summ
                policy = 4
        cost = self.gamma * highest
        reward_s = self.__state_list.getReward()
        return reward_s + cost, policy
    
    def countedAverages(self, num_trials):
        '''
        Preconditions:
            num_trials - integer
                Number of times the user wants to randomly generate an action for
                each state.
        Postconditions:
            Returns a dictionary containing each state's key in the __state_list instance
            as a key for a reference to another dictionary with action keys as its keys
            with references to another dictionary with all possible states' keys for
            states reachable by that action with a decimal representing the probability
            that state would be reached by the action performed based on the number of
            times the action was performed in this method for the state performing the
            action.
        '''
        counted_averages = dict()
        for count in range(self.__state_list_sze):
            self.__state_list.switchState(count+1)
            t = self.__state_list.getState()
            if(t.isTerminal()):
                continue
            numActions = t.getNumActions()
            for i in range(num_trials):
                randAction = random.randint(1, numActions)
                self.__state_list.tryAction(randAction)
            countList = self.__state_list.returnCount()
            action_count = countList[0]
            actionKeys = list(action_count.keys())
            action_complete_count = countList[1]
            counted_actions=dict()
            for j in actionKeys:
                num_runs = action_count[j]
                comp_runs = action_complete_count[j]
                comp_runs_list = list(comp_runs.keys())
                counted_to_states = dict()
                for k in comp_runs_list:
                    res = comp_runs[k]
                    counted_to_states[k] = res / num_runs
                counted_actions[j] = counted_to_states
            counted_averages[count+1] = counted_actions
        return counted_averages
    
    #------------------------------------------------------------------------------
    
    def createUtilitiesAdjusted(self, tol, averages, count):
        '''
        Preconditions:
            tol - float
                tol, short for tolerance, is the minimal amount that a previous
                utility and a newly generated utility can differ by.
            averages - dictionary
                These are computed probabilities that each action has a chance of
                succeeding with.  Generally created by 'Counting the number of times
                a state is reached from another state by an action, divided by the
                number of times that action from the initial state was performed.'
            count
                When to stop visiting these utilities as much.
        Postconditiosn:
            Returns a copy of this class's utility list after running it
            through value iteration some random number of times.
        '''
        self.optimality_counter = list() # Declare a list to contain dictionaries.
        for i in range(self.__state_list_sze):
            # The dictionaries are referenced by index for {state key - 1}.  'count' key accesses the number of times we have used this action from this state, starts at 1, not zero.
            # 'isOptimal' references us still being able to use this if it is still optimal option to explore
            #self.optimality_counter.append({1:{'count':1,'isOptimal':True}, 2:{'count':1,'isOptimal':True}, 3:{'count':1,'isOptimal':True}, 4:{'count':1,'isOptimal':True}})
            self.optimality_counter.append([[1, True],[1, True],[1, True],[1, True]])
        other_u_list = self.__createAdjustedUtilityList(1)
        max_state_count = count * 4 # max number of times we can explore, keeps GLIE
        # Loop over all states once
        for i in range(self.__state_list_sze):
            curr_count = 0 # Keeps track the number of times we have explored
            last_utility_for_s = self.utility_list[i+1]
            curr_utility_for_s = other_u_list[i+1]
            # Find the magnitude of the difference in the utilities for state i+1, since i starts at 0
            util_diff = curr_utility_for_s - last_utility_for_s
            util_diff = math.fabs(util_diff)
            # While the tolerance is less than the magnitude of the difference, keep working
            while(util_diff > tol):
                # set 'prev' to hold the same value as 'curr'
                last_utility_for_s = curr_utility_for_s # last_utility_for_s is 'prev'
                # Send into the algorithm math portion
                temp = self.__ValueIterationAdjusted(i+1, averages, self.utility_list, self.optimality_counter[i], count, curr_count, max_state_count)
                curr_count = temp[2] # Grab the new current count times we have explored, its incremented in __ValueIterationAdjusted if we explored
                self.utility_list[i+1] = temp[0] # Grab the new utility for the state
                self.policy_list[i+1] = temp[1] # Grab the policy for this utility
                curr_utility_for_s = self.utility_list[i+1] # set the new utility to be the current utility.
                util_diff = curr_utility_for_s - last_utility_for_s # subtract 'prev' utility from the 'curr' utility
                util_diff = math.fabs(util_diff) # Find the magnitude of the difference.
        return self.utility_list.copy(), self.policy_list.copy() # After the loop is broken, return a copy of the utility list and the policy list.
    
    # Hybridized algorithm
    def __ValueIterationAdjusted(self, curr_state_key, averages, u_list, opt_counter, max_count, curr_count, max_state_count):
        self.__state_list.switchState(curr_state_key) # Ensure we are using the correct state for value iteration values
        # If the state is terminal, the utility is its reward.
        if(self.__state_list.isTerminal()):
            return self.__state_list.getReward(), 0, curr_count # Return the reward, the policy, and the curr_count for number of times we explored
        policy = 0 # initialize policy to be 0
        
        action_dictionaries = averages[curr_state_key] # Grab action probabilities for the current state
        
        up_dictionaries = action_dictionaries[1] # Grab probabilities for traversing 'up'
        up_key_list = list(up_dictionaries.keys()) # Grab the 'keys' for the states that this action could possibly reach
        
        left_dictionaries = action_dictionaries[2] # Grab probabilities for traversing 'left'
        left_key_list = list(left_dictionaries.keys()) # Grab the 'keys' for the states that this action could possibly reach
        
        down_dictionaries = action_dictionaries[3] # Grab probabilities for traversing 'down'
        down_key_list = list(down_dictionaries.keys()) # Grab the 'keys' for the states that this action could possibly reach
        
        right_dictionaries = action_dictionaries[4] # Grab probabilities for traversing 'right'
        right_key_list = list(right_dictionaries.keys()) # Grab the 'keys' for the states that this action could possibly reach
        
        # initialize the summation for traversing 'up'
        up_summ = 0
        for i in up_key_list:
            up_summ = up_summ + (u_list[i] * up_dictionaries[i]) # summate over all states this action could reach, multiplying their current utility by the probability of reaching them.
        # initialize the summation for traversing 'left'
        left_summ = 0
        for i in left_key_list:
            left_summ = left_summ + (u_list[i] * left_dictionaries[i])
        # initialize the summation for traversing 'down'
        down_summ = 0
        for i in down_key_list:
            down_summ = down_summ + (u_list[i] * down_dictionaries[i])
        # initialize the summation for traversing 'right'
        right_summ = 0
        for i in right_key_list:
            right_summ = right_summ + (u_list[i] * right_dictionaries[i])
        
        # Generate a number between 1 and 10000
        randomAU = random.randint(1,10000) #randomAU = randomActionUtility
        highest = 0 # highest stores the highest summation
        
        # If the random decision to explore fails, my chance is it only 'succeeds' 15% of the time, Boshart's is 10%, or if it succeeds
        # check if limit of exploration was reached, if current number of times we have explored reaches the max number of times we are
        # allowed to.
        # If either check passes, find the max of the summations
        if(randomAU > 1500 or curr_count >= max_state_count):
            highest = up_summ
            policy = 1
            if(left_summ > highest):
                highest = left_summ
                policy = 2
            if(down_summ > highest):
                highest = down_summ
                policy = 3
            if(right_summ > highest):
                highest = right_summ
                policy = 4
        else:
            # Create a dictionary to store the 'current highest (COUNTED) action', 'max count', 'weight'
            # 'current highest action' is the action key with the current highest weight.
            # 'max count' is a boolian that tracks whether or not this action has been picked the maximum number of times already.
            # 'weight' keeps track of the weight for the 'current highest action'
            #highest_util = {'current highest action' : 0, 'max count' : False, 'weight' : 1}
            highest_util = [0, False, 0]
            # It is time to explore my dear friends
            u_dict = opt_counter[0] # Grab the counters for how many times each action has been performed for this state
            l_dict = opt_counter[1]
            d_dict = opt_counter[2]
            r_dict = opt_counter[3]
            
            opt_val_list = list()
            # If the action has yet to be proved unoptimal, add it to possible actions to use for utilities.
            curr_count = curr_count + 1
            if(u_dict[1]):
                opt_val_list.append(1)
            if(l_dict[1]):
                opt_val_list.append(2)
            if(d_dict[1]):
                opt_val_list.append(3)
            if(r_dict[1]):
                opt_val_list.append(4)
            # sets default 'current highest action' to be the first key in  opt_val_list
            highest_util[0] = opt_val_list[0]
            # sets the rest of information in "highest_util" variable to the first items 'weight' and checks the number of times it was counted
            # to determine if it needs to set the 'max count' definition to True.
            # Sets the policy to the 'current highest action'
            if(opt_val_list[0] == 1):
                highest = up_summ
                highest_util[2] = (1/u_dict[0]) * up_summ
                policy = 1
                if(u_dict[0] >= max_count + 1):
                    highest_util[1] = True
            elif(opt_val_list[0] == 2):
                highest = left_summ
                highest_util[2] = (1/l_dict[0]) * left_summ
                policy = 2
                if(l_dict[0] >= max_count + 1):
                    highest_util[1] = True
            elif(opt_val_list[0] == 3):
                highest = down_summ
                highest_util[2] = (1/d_dict[0]) * down_summ
                policy = 3
                if(d_dict[0] >= max_count + 1):
                    highest_util[1] = True
            else:
                highest = right_summ
                highest_util[2] = (1/r_dict[0]) * right_summ
                policy = 4
                if(r_dict[0] >= max_count + 1):
                    highest_util[1] = True
            # These following 'if's find the highest weight.
            # If the 'up' action 'isOptimal' meaning we can still use it
            if(u_dict[1]):
                # reason why 'count' is initialized to 1 rather than 0 is for weight calculations
                u_weight = up_summ * (1 / u_dict[0])  # calculate its weight
                # Checks to see if its weight is greater than the current highest weight
                if(u_weight > highest_util[2]):
                    # If it is, set the current highest weight to its weight
                    highest_util[2] = u_weight
                    # Set highest to be the summation for this action
                    highest = up_summ
                    # set the 'current highest action' in highest_util to be the key for this action
                    highest_util[0] = 1
                    # set policy to the key for this action
                    policy = 1
            if(l_dict[1]):
                l_weight = left_summ * (1 / l_dict[0])
                if(l_weight > highest_util[2]):
                    highest_util[2] = l_weight
                    highest = left_summ
                    highest_util[0] = 2
                    policy = 2
            if(d_dict[1]):
                d_weight = down_summ * (1 / d_dict[0])
                if(d_weight > highest_util[2]):
                    highest_util[2] = d_weight
                    highest = down_summ
                    highest_util[0] = 3
                    policy = 3
            if(r_dict[1]):
                r_weight = right_summ * (1 / r_dict[0])
                if(r_weight > highest_util[2]):
                    highest_util[2] = r_weight
                    highest = right_summ
                    highest_util[0] = 4
                    policy = 4
            # increment the counter for this state's selected action
            # then check if the count has has exceeded max_count + 1(since action count is initialized to 1, need to add 1 to max_count)
            # if the count exceeds max_count + 1, then set 'isOptimal' to False so we do not check it anymore for exploration.
            selected_action = highest_util[0]
            if(selected_action == 1):
                u_dict[0] = u_dict[0] + 1
                if(u_dict[0] >= max_count+1):
                    u_dict[1] = False
            elif(selected_action == 2):
                l_dict[0] = l_dict[0] + 1
                if(l_dict[0] >= max_count+1):
                    l_dict[1] = False
            elif(selected_action == 3):
                d_dict[0] = d_dict[0] + 1
                if(d_dict[0] >= max_count+1):
                    d_dict[1] = False
            elif(selected_action == 4):
                r_dict[0] = r_dict[0] + 1
                if(r_dict[0] >= max_count+1):
                    r_dict[1] = False
        # Value Iteration math to find the new utility
        cost = self.gamma * highest
        reward_s = self.__state_list.getReward()
        return reward_s + cost, policy, curr_count # return the new utility, policy for the new utility, and the number of times we have explored
    
    #-------------------------------------------------------------------------------
    
    def createListUtilities(self, tol, c_averages):
        t_1 = self.createUtilities(tol, c_averages) # These methods create two utilities that might not be quite as tollerant as we would like.
        t_2 = self.createUtilities(tol, c_averages)
        u_dict = t_1[0]
        new_u_dict = t_2[0]
        keyList = list(u_dict.keys())
        recreate_utils = True
        # Initialize a sub-infinite loop to loop over creating better utilities until tollerance is reached.
        # Creates tolerable utility for the state list.
        while(recreate_utils):
            t_2 = self.createUtilities(tol, c_averages)
            new_u_dict = t_2[0]
            for i in keyList:
                u_diff = new_u_dict[i] - u_dict[i]
                u_diff = math.fabs(u_diff)
                # If the absolute difference in utilities is greater than 
                if(u_diff > tol):
                    recreate_utils = True
                    break
                else:
                    recreate_utils = False
            u_dict = new_u_dict
        return t_2
    
    # Hybridized algorithm call.
    def createListUtilitiesAdjusted(self, tol, c_averages, count):
        t_1 = self.createUtilitiesAdjusted(tol, c_averages, count) # These methods create two utilities that might not be quite as tollerant as we would like.
        t_2 = self.createUtilitiesAdjusted(tol, c_averages, count)
        u_dict = t_1[0]
        new_u_dict = t_2[0]
        keyList = list(u_dict.keys())
        recreate_utils = True
        # Initialize a sub-infinite loop to loop over creating better utilities until tollerance is reached.
        # Creates tolerable utility for the state list.
        while(recreate_utils):
            t_2 = self.createUtilitiesAdjusted(tol, c_averages, count)
            new_u_dict = t_2[0]
            for i in keyList:
                u_diff = new_u_dict[i] - u_dict[i]
                u_diff = math.fabs(u_diff)
                # If the absolute difference in utilities is greater than 
                if(u_diff > tol):
                    recreate_utils = True
                    break
                else:
                    recreate_utils = False
            u_dict = new_u_dict
        return t_2
    