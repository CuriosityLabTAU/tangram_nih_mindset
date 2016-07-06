from tangrams import *
import json


class Agent:
    def __init__(self):
        self.solver = Solver()

    def solve_task(self, json_str_task):
        task = Task()
        task.create_from_json(json_str_task)
        self.solver.set_available_pieces(task)
        seq = self.solver.run_task(task, stop=True)
        # TODO convert seq to json str, for now just return the moves of the task
        return json_str_task



