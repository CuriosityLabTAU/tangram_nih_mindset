from tangrams import *
import json


class Agent:
    def __init__(self):
        self.solver = Solver()
        # self.mindset = Mindset()
        # self.curiosity = Curiosity()
        self.condition = 'Mindset' # value can be 'Mindset' or 'Neutral'
        self.current_round = 0
        self.child_selected_index = None #  indicates the selection of the child. possible values are 1/2/3
        self.child_result = None  #  indicates the child result. possible values are 'S' (Success) or 'F' (Fail)

    def solve_task(self, json_str_task):
        task = Task()
        task.create_from_json(json_str_task)
        self.solver.set_available_pieces(task)
        self.solver.run_task(task, duration=10, stop=True)
        seq = self.solver.get_seq_of_moves()
        return seq

    def record_child_selection(self, selected_index):
        self.child_selected_index = selected_index

    def record_child_result(self, result):
        self.child_result = result

    def set_selection(self):
        if self.condition == 'Mindset':
            if self.child_result == None:
                select = 2  # First round, select demo task
            elif self.child_result == 'S':
                select = min(self.child_selected_index+1,3)
            elif self.child_result == 'F':
                select = self.child_selected_index
            else:
                select = 2  # in case of a bug, select 2
        else:  # ==> self.condition == 'Neutral'
            if self.child_result == None:
                select = 2 # First round, select demo task
            elif self.child_result == 'S':
                select = self.child_selected_index
            elif self.child_result == 'F':
                select = max(self.child_selected_index - 1, 1)
            else:
                select = 2 # in case of a bug, select 2
        return select





