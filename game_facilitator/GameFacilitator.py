from tangrams import *
import json


class GameFacilitator():


    def __init__(self):
        self.current_task = None

    def check_solution(self, json_str_board):
        board_task = Task()
        board_task.create_from_json(json_str_board)
        return board_task.check_solution(self.current_task.x, board_task.solution)

    def generate_tangram_options(self):
        T = []
        test1_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
        T.append(json.dumps(test1_dict))
        test2_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 2')]}
        T.append(json.dumps(test2_dict))
        test3_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 3')]}
        T.append(json.dumps(test3_dict))
        return T

    def tangram_selected(self, json_str_selected_task):
        self.current_task.create_from_json(json_str_selected_task)


