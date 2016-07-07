from tangrams import *
import numpy as np
import copy
# import matplotlib.pyplot as plt
import json


class Solver:

    n_networks = 3
    efficiency = 1.0

    def __init__(self):
        self.networks = []
        self.learned = []
        self.solutions = []
        self.errors = []
        self.solved_network_index = None

        for i in range(0, self.n_networks):
            self.networks.append(Network())
            self.solutions.append([])
            self.errors.append([])

    def set_initial_task(self, task):
        # initialize networks with the current task and efficient
        for net in self.networks:
            net.set_network(task)
            net.init_network()

    def set_blank_solver(self, task):
        # initialize networks with the size of task, and one only small triangle
        for net in self.networks:
            net.set_small_triangle_network(task)
            net.init_network()

    def set_available_pieces(self, task):
        # initialize networks with pieces in task (with all translations and rotations)
        for net in self.networks:
            net.set_available_pieces(task)
            net.init_network()

    def run_task(self, task, duration=100, stop=False, init_network=False):
        # stop  -   whether to stop when a correct solution is found
        # return-   network that solved and time it took to solve

        # initialize networks with the current task and efficient
        for net in self.networks:
            if init_network:
                net.set_network(task)
                net.init_network()
            net.init_parameters()
            net.add_task(task)

        # initialize the solutions and errors
        # these are [i,t], i.e. networks X duration
        for i in range(0, self.n_networks):
            self.solutions[i] = []
            self.errors[i] = []

        # run the task for the given duration
        for t in range(0, duration):
            # efficiency means probability of actual progressing
            if np.random.rand() < self.efficiency:
                # go over all the networks
                for i in range(0, self.n_networks):
                    # run one time-step
                    s_ti, e_ti = self.networks[i].dynamics()
                    # update the solutions and errors with the current ones
                    s_ti_copy = copy.deepcopy(s_ti) # create a copy since s_ti is a pointer to the network's activation
                    self.solutions[i].append(s_ti_copy)
                    self.errors[i].append(e_ti)

                if stop is not False:
                    for i in range(0, self.n_networks):
                        x, sol_list = self.networks[i].get_solution()
                        if task.check_solution(x, sol_list):
                            # return the networked that solved and the time it took to solve
                            self.solved_network_index = i
                            return self.networks[i], t+1
        return None, None

    def get_seq_of_moves(self):
        # return a json string such that the list of pieces, contains the moves of the robot.
        # should be called after run_task()
        seq = []
        if self.solved_network_index is not None:
            n = self.solved_network_index
            print len(self.solutions[n])
            for k in range(len(self.solutions[n])):
                for i in range(len(self.solutions[n][k])):
                    if self.solutions[n][k][i] > 0:
                        seq.append(self.networks[n].nodes[i])
        else:
            seq = []
            n = 0 # none of the networks solved so just choose the first network
            print len(self.solutions[n])
            for k in range(len(self.solutions[n])):
                for i in range(len(self.solutions[n][k])):
                    if self.solutions[n][k][i] > 0:
                        seq.append(self.networks[n].nodes[i])
        # return seq
        # convert seq to json_string
        seq_dict = {}
        (I, J) = self.networks[0].nodes[0].x.shape
        seq_dict['size'] = str((I - 1) / Piece.JUMP + 1) + ' ' + str((J - 1) / Piece.JUMP + 1)
        pieces_vec = []
        for p in seq:
            pieces_vec.append((p.name[0], p.name[1], p.name[2]))
        seq_dict['pieces'] = pieces_vec
        return json.dumps(seq_dict)


    def print_current_solutions(self):
        for i in range(0, self.n_networks):
            print(self.solutions[i][-1])
        for i in range(0, self.n_networks):
            print(self.errors[i][-1])

    def analyze_stats(self, show=False):
        # return the error statistics
        duration = len(self.errors[0])
        d = range(0, duration)
        error = np.zeros(self.n_networks)
        avg_error = np.zeros(duration)
        std_error = np.zeros(duration)
        min_error = np.zeros(duration)

        # go over all the time-steps
        for t in d:
            for i in range(0, self.n_networks):
                error[i] = self.errors[i][t]
            if t == d[-1] and t > 0:
                #print('Networks errors: ', error)
                pass
            avg_error[t] = np.average(error)
            std_error[t] = np.std(error)
            min_error[t] = np.min(error)

        if show:
            fig, ax = plt.subplots()
            ax.errorbar(d, avg_error, yerr=std_error)
            ax.plot(d, min_error, 'r')
            # plt.axis([d[0], d[-1], -5.5, 10])
            # plt.draw()
            # plt.show()

        if duration == 1:   # return numbers, not arrays
            return avg_error[0], std_error[0], min_error[0]
        else:               # return arrays
            return avg_error, std_error, min_error

    # def learn(self, task):
    #     structures = task.decompose()
    #     for net in self.networks:
    #         net.add_hebbian(structures)

    def learn(self, task):
        for net in self.networks:
            net.extend_partial_network(task)
            net.init_network()


    def evaluate_tasks(self, tasks, duration=100, stop=False):
        times = np.zeros(len(tasks))
        for t in range(0, len(tasks)):
            pass
