from tangrams import *
import json

class GameFacilitator(self):

    def __init__(self):
        test_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
        json_str = json.dumps(test_dict)
        self.current_task = Task()
        self.current_task.create_from_json(json_str)

    def check_solution(self, json_str_board):
        board_task = Task()
        board_task.create_from_json(json_str_board)
        return board_task.check_solution(self.current_task.x, board_task.solution)

    def generate_tangram_options(self):
        test1_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
        T1 = json.dumps(test1_dict)
        test2_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 2')]}
        T2 = json.dumps(test2_dict)
        test3_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 3')]}
        T3 = json.dumps(test3_dict)
        return T1,T2,T3

    def tangram_selected(self, json_str_selected_task):
        self.current_task.create_from_json(json_str_selected_task)


