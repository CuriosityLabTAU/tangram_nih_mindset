from tangrams import *
import json


class Agent:
    def __init__(self):
        self.solver = Solver()

    def solve_task(self, json_str_task):
        task = Task()
        task.create_from_json(json_str_task)
        self.solver.set_available_pieces(task)
        self.solver.run_task(task, stop=True)
        seq = self.solver.get_seq_of_moves()
        return seq



