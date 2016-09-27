# Driver
from Reinforcement_Maze import Reinforcement_Maze
from State_Controller import State_Controller
from State import State
from Action import Action
import math
import sys
import time
class RM_Driver:
    def main(arguments):
        '''
        No parameters needed.  This is the driver, this is where it starts
        1 or 3 command line arguments can be used.
        '''
        tol = 0.00001       # initialize default values for the tolerance and number of trials to generate random actions
        num_trials = 10000
        # Note, Python's command line arguments array is 0 based, but at index 0, its the file name, so I don't include it
        # when I say this driver takes 1 or 3 command line arguments.  
        if(arguments.__len__() == 4):
            tol = arguments[2] # If we had 4 arguments (3 arguments plus name of driver), we assume argument 2 was tolerance and argument 3 was number of trials to randomly generate an action.
            if(isinstance(tol,str)):
                tol = float(tol)
            num_trials = arguments[3]
            if(isinstance(num_trials,str)):
                num_trials = int(num_trials)
        elif(arguments.__len__() != 2):
            # This raises an exception since size of the command line argument list is neither 4 nor 2(3 nor 1 if you exclude driver name).
            raise IndexError
        result=RM_Driver.read_reinforcement_information(arguments[1]) # This method reads in the text file(s)
        r_maze_1 = Reinforcement_Maze(result[1], result[0]) # Creates a reinforcement_maze object.
        r_maze_2 = Reinforcement_Maze(result[1], result[0])
        c_averages = r_maze_1.countedAverages(num_trials) # Computes the averages based on the number of trials we want to randomly attempt an action in each state
        c_averages_2 = r_maze_2.countedAverages(num_trials)
        c_avg_key_list = list(c_averages.keys()) # Make a list out of all the keys in c_averages
        for i in c_avg_key_list:
            # Triple Nested Loop to print out State i Action j yielding state k and the probability of repeating this step and getting state k again
            act_averages = c_averages[i]
            act_avg_key_list = list(act_averages.keys())
            for j in act_avg_key_list:
                to_state_avg = act_averages[j]
                to_state_avg_key_list = list(to_state_avg.keys())
                for k in to_state_avg_key_list:
                    if(k < 10 or i < 10):
                        print('STATE ' + str(i) + "'S ACTION " + str(j) + '->' + str(k) + '\t\t' + str(to_state_avg[k]) + '% of the time')
                    elif(k >=10 and i >= 10):
                        print('STATE ' + str(i) + "'S ACTION " + str(j) + '->' + str(k) + '\t\t' + str(to_state_avg[k]) + '% of the time')
                    else:
                        print('STATE ' + str(i) + "'S ACTION " + str(j) + '->' + str(k) + '\t' + str(to_state_avg[k]) + '% of the time')
            print('\n')
            
        print("\n\nU\n\n")
        init_time = time.time()*1000
        t_2 = r_maze_1.createListUtilities(tol, c_averages)
        fin_time = time.time()*1000
        time_1 = fin_time - init_time
        policies = t_2[1]
        new_u_dict = t_2[0]
        for i in list(new_u_dict.keys()):
            if(i < 10):
                print('STATE 0' + str(i) + ': POLICY = ' + str(policies[i]) + ':\t UTILITY = ' + str(new_u_dict[i]))
            else:
                print('STATE ' + str(i) + ': POLICY = ' + str(policies[i]) + ':\t UTILITY = ' + str(new_u_dict[i]))
        
        print("\n\nU+\n\n")
        
        init_time = time.time()*1000
        t_2 = r_maze_2.createListUtilitiesAdjusted(tol, c_averages_2, 200)
        fin_time = time.time()*1000
        time_2 = fin_time - init_time
        policies = t_2[1]
        new_u_dict = t_2[0]
        for i in list(new_u_dict.keys()):
            if(i < 10):
                print('STATE 0' + str(i) + ': POLICY = ' + str(policies[i]) + ':\t UTILITY = ' + str(new_u_dict[i]))
            else:
                print('STATE ' + str(i) + ': POLICY = ' + str(policies[i]) + ':\t UTILITY = ' + str(new_u_dict[i]))
        print('\n\n\n\n')
        print("U's Time:  "  + str(time_1))
        print("U+'s Time: "  + str(time_2))
        
    def read_reinforcement_information(file_name=str):
        my_file = open(file_name, 'r') # Open the initial file
        num_actions=my_file.readline() # 1st Line should be the number of actions each node must be able to take
        num_actions=int(num_actions)
        num_states=my_file.readline() # 2nd Line list the number of states in our maze.
        num_states=int(num_states)
        gamma=my_file.readline() # 3rd Line contains our Gamma value
        gamma=float(gamma)
        s_controller = State_Controller(curr_state=None, state_list=None) # Initialize the controller class with a null value as the starting state
        #    The file, after the first three lines, is organized
        #    such that line1 is the value that this step adds to the total
        #    at timestep t, line2 is a boolean number with the number "1"
        #    representing true which determines whether this stae is
        #    terminal or not, and line3 is a textfile which holds this
        #    state's action matrix.
        file_list=list()
        for i in range(num_states):
            # base matrix is initialized with all 0s.  This is so terminal
            # states can have an all 0 matrix so that they can take no actions
            value=my_file.readline() # line1 is value
            value = float(value)
            terminality=my_file.readline() # line2 is terminality
            terminality=int(terminality)
            file_of_state = my_file.readline()
            file_of_state = file_of_state.rstrip()
            file_list.append(file_of_state)
            temp_state = State(value, terminality, i+1, action_list = None, count_actions=True)
            added = s_controller.addState(temp_state)
        for i in range(file_list.__len__()):
            swapped = s_controller.switchState(i+1)
            if(s_controller.isTerminal() == True):
                continue # continue on with the next iteration of this loop, skips all code below this point and starts at beginning of loop again if condition is met
            state_file = open(file_list[i], 'r')
            size = state_file.readline()
            sizes = size.split(' ')
            if(int(sizes[0]) != num_actions or int(sizes[1]) != num_states):
                state_file.close()
                raise MemoryError
            for count in range(num_actions): # Loop through the state's action matrix and store it in base_matrix
                line = state_file.readline()
                myList = line.split(' ')
                temp_dict = dict()
                if(myList.__len__() != num_states):
                    raise MemoryError
                t_list = list()
                count_i = 0
                for q in range(myList.__len__()):
                    s_controller.switchState(q+1)
                    temp_state = s_controller.getState()
                    t_list.append(s_controller.getState())
                    myList[q] = float(myList[q])
                s_controller.switchState(i+1)
                new_action = Action(count+1, t_list, result_chances=myList, create_counter_table=True)
                s_controller.addAction(new_action)
                    
            # Printing the state's matrix to check if it is being stored here.
            
            state_file.close() # close the text file to stop memory leaks and unwanted f*** ups
        my_file.close() # close the file to prevent memory and input hazards
        return s_controller, gamma
    
if(__name__ == '__main__'):
    RM_Driver.main(sys.argv)