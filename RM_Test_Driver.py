from Reinforcement_Maze import Reinforcement_Maze
from State_Controller import State_Controller
from State import State
from Action import Action
import math
import sys
import time
class RM_Compare_Driver:
    def main(arguments):
        tol = 0.00001       # initialize default values for the tolerance and number of trials to generate random actions
        num_trials = 10000
        if(arguments.__len__() == 4):
            tol = arguments[2] # If we had 4 arguments (3 arguments plus name of driver), we assume argument 2 was tolerance and argument 3 was number of trials to randomly generate an action.
            if(isinstance(tol,str)):
                tol = float(tol)
            num_trials = arguments[3]
            if(isinstance(num_trials,str)):
                num_trials = int(num_trials)
        elif(arguments.__len__() != 2):
            raise IndexError
        result=RM_Compare_Driver.read_reinforcement_information(arguments[1]) # This method reads in the text file(s)
        r_maze_1 = Reinforcement_Maze(result[1], result[0]) # Creates a reinforcement_maze object.
        r_maze_2 = Reinforcement_Maze(result[1], result[0])
        r_maze_3 = Reinforcement_Maze(result[1], result[0])
        r_maze_4 = Reinforcement_Maze(result[1], result[0])
        r_maze_5 = Reinforcement_Maze(result[1], result[0])
        r_maze_6 = Reinforcement_Maze(result[1], result[0])
        r_maze_7 = Reinforcement_Maze(result[1], result[0])
        r_maze_8 = Reinforcement_Maze(result[1], result[0])
        r_maze_9 = Reinforcement_Maze(result[1], result[0])
        r_maze_10 = Reinforcement_Maze(result[1], result[0])
        r_maze_11 = Reinforcement_Maze(result[1], result[0])
        r_maze_12 = Reinforcement_Maze(result[1], result[0])
        r_maze_13 = Reinforcement_Maze(result[1], result[0])
        r_maze_14 = Reinforcement_Maze(result[1], result[0])
        r_maze_15 = Reinforcement_Maze(result[1], result[0])
        r_maze_16 = Reinforcement_Maze(result[1], result[0])
        RM_test_list_1 = list()
        RM_test_list_2 = list()
        
        r_maze_control = Reinforcement_Maze(result[1], result[0])
        averages = r_maze_control.countedAverages(num_trials)
        
        RM_test_list_1.append(r_maze_1)
        RM_test_list_1.append(r_maze_2)
        RM_test_list_1.append(r_maze_3)
        RM_test_list_1.append(r_maze_4)
        RM_test_list_1.append(r_maze_5)
        RM_test_list_1.append(r_maze_6)
        RM_test_list_1.append(r_maze_7)
        RM_test_list_1.append(r_maze_8)
        
        RM_test_list_2.append(r_maze_9)
        RM_test_list_2.append(r_maze_10)
        RM_test_list_2.append(r_maze_11)
        RM_test_list_2.append(r_maze_12)
        RM_test_list_2.append(r_maze_13)
        RM_test_list_2.append(r_maze_14)
        RM_test_list_2.append(r_maze_15)
        RM_test_list_2.append(r_maze_16)
        
        util_dict_1 = dict()
        util_dict_2 = dict()
        
        time_1_initial = time.time()
        for i in range(8):
            util_dict_1[i+1] = RM_test_list_1[i].createListUtilities(tol, averages)
        time_1_final = time.time()
        
        time_2_initial = time.time()
        for i in range(8):
            util_dict_2[i+9] = RM_test_list_2[i].createListUtilitiesAdjusted(tol, averages, 200)
        time_2_final = time.time()
        
        time_1_total = time_1_final - time_1_initial
        time_2_total = time_2_final - time_2_initial
        
        
        #print("Total Time for Alg 1: " + str(time_1_total))
        #print("Total Time for Alg 2: " + str(time_2_total))
        
        return time_1_total, time_2_total
        
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
    
time_1_totals = 0
time_2_totals = 0
if(__name__ == '__main__'):
    for i in range(30):
        for i in range(100):
            time_totals = RM_Compare_Driver.main(sys.argv)
            time_1_totals = time_1_totals + time_totals[0]
            time_2_totals = time_2_totals + time_totals[1]
        
        print(time_1_totals / 100)
        print(time_2_totals / 100)