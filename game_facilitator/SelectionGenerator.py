from tangrams import *
import json
import numpy as np
import matplotlib.pyplot as plt


class SelectionGenerator:

    def __init__(self):
        self.N_dif_levels = 5
        self.dif_level = []
        self.dif_indexes = np.zeros([self.N_dif_levels], dtype=np.int)
        self.current_level = 1
        for n in range(self.N_dif_levels):
            self.dif_level.append([])

    def load_dif_levels(self):
        # read tangrams for each difficulty from tangram_levels.txt
        # file format is:
        #  dif 0
        # {"pieces": [["square", "90", "1 1"], ["small triangle2", "180", "0 1"]], "size": "5 5"}
        # {"pieces": [["square", "180", "0 0"], ["small triangle2", "180", "0 1"]], "size": "5 5"}
        # dif 1
        # {"pieces": [["square", "180", "0 0"], ["small triangle2", "180", "0 1"]], "size": "5 5"}
        # ...
        #
        dif_i = -1
        self.dif_level = []
        with open('./game_facilitator/tangram_levels.txt','r') as fp:
            for line in fp:
                if 'dif' in line:
                    dif_i += 1
                    self.dif_level.append([])
                else:
                    self.dif_level[dif_i].append(line.strip('\n'))
        self.N_dif_levels = dif_i + 1
        self.dif_indexes = np.zeros([self.N_dif_levels], dtype=np.int)



    def get_current_selection(self):
        # return three json_strings
        T1 = self.dif_level[self.current_level-1][self.dif_indexes[self.current_level-1]]
        T2 = self.dif_level[self.current_level][self.dif_indexes[self.current_level]]
        T3 = self.dif_level[self.current_level + 1][self.dif_indexes[self.current_level + 1]]
        return [T1, T2, T3]

    def update_game_result(self, user_selection, game_result):
        # update the selection generator according to user selection and game result
        # user_selection is 0/1/2
        # game_result is 'S' or 'F'

        self.dif_indexes[self.current_level - 1] += 1
        self.dif_indexes[self.current_level] += 1
        self.dif_indexes[self.current_level + 1] += 1

        if game_result == 'F':
            if user_selection == 0:
                self.current_level -= 1
        elif game_result == 'S':
            self.current_level += 1

    def display(self):
        plt.figure()
        task = Task()
        for n in range(self.N_dif_levels):
            for k in range(len(self.dif_level[n])):
                plt.subplot(6,self.N_dif_levels, n+1+k*self.N_dif_levels)
                task.create_from_json(self.dif_level[n][k])
                if k < self.dif_indexes[n]:
                    plt.imshow(task.x*-1, interpolation='none')
                else:
                    plt.imshow(task.x, interpolation='none')
        plt.subplot(6,self.N_dif_levels,
                    self.current_level-1+1+(self.dif_indexes[self.current_level - 1])*self.N_dif_levels)
        task.create_from_json(self.dif_level[self.current_level-1][self.dif_indexes[self.current_level - 1]])
        plt.imshow(np.sin(task.x), interpolation='none')
        plt.subplot(6, self.N_dif_levels,
                    self.current_level  + 1 + (self.dif_indexes[self.current_level]) * self.N_dif_levels)
        task.create_from_json(self.dif_level[self.current_level ][self.dif_indexes[self.current_level ]])
        plt.imshow(np.sin(task.x), interpolation='none')
        plt.subplot(6, self.N_dif_levels,
                    self.current_level + 1 + 1 + (self.dif_indexes[self.current_level + 1]) * self.N_dif_levels)
        task.create_from_json(self.dif_level[self.current_level + 1][self.dif_indexes[self.current_level + 1]])
        plt.imshow(np.sin(task.x), interpolation='none')

                # T1 = self.dif_level[self.current_level - 1][self.dif_indexes[self.current_level - 1]]
                # T2 = self.dif_level[self.current_level][self.dif_indexes[self.current_level]]
                # T3 = self.dif_level[self.current_level + 1][self.dif_indexes[self.current_level + 1]]



# task_dic =  {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
# json_str = json.dumps(task_dic)
# dif_level[0].append(json_str)
#
# task_dic =  {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
# json_str = json.dumps(task_dic)
# dif_level[0].append(json_str)



#
# task = Task()
# task.create_from_json(json_str)
#
#
# task_dic =  {'size': '5 5', 'pieces': [('square', '0', '1 1'), ('small triangle2', '0', '0 1')]}
# json_str = json.dumps(task_dic)
# task = Task()
# task.create_from_json(json_str)
