from tangrams import *
from SelectionGenerator import *

import json


class GameFacilitator():


    def __init__(self):
        self.selected_task_index = None  # 0/1/2 according to user selected task
        self.selection_tasks = None  # a list of 3 json strings that represent 3 tasks
        self.current_task = Task()  # The selected task as Task() object
        self.selection_gen = SelectionGenerator()
        self.selection_gen.load_dif_levels()

    def check_solution(self, json_str_board):
        board_task = Task()

        board_task.create_from_json(json_str_board)
        return board_task.check_solution(self.current_task.x, board_task.solution)

    def generate_tangram_options(self):
        self.selection_tasks = self.selection_gen.get_current_selection()
        # T = []
        # test1_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
        # T.append(json.dumps(test1_dict))
        # test2_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 2')]}
        # T.append(json.dumps(test2_dict))
        # test3_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 3')]}
        # T.append(json.dumps(test3_dict))
        return self.selection_tasks

    def tangram_selected(self, selected_task_index):
        # selected_task_index can be 0/1/2 according to user selection.
        self.selected_task_index = selected_task_index

        self.current_task.create_from_json(self.selection_tasks[self.selected_task_index])

    def update_game_result(self, game_result):
        # game_result can be 'S' (Success) or 'F' (Failure)
        self.selection_gen.update_game_result(self.selected_task_index, game_result)