import gym
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, defaultdict
from itertools import count
from PIL import Image
import time
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import os
from torch import optim
import http.server
import socketserver
import requests





class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.ll1 = nn.Linear(1211, 708)  # we need to change the initial filter of size 1211 to 1012
        self.ll2 = nn.Linear(708, 708)
        self.ll3 = nn.Linear(708, 354)
        self.ll4 = nn.Linear(354, 354)
        self.oll = nn.Linear(354, 200)  # changed from 16 to 200, - too large a reduction , will reducing in steps.

    # function implements a forward pass to the network
    def forward(self, x):
        # x = x.flatten(start_dim=1) - flattening needed only for images
        x = F.relu(self.ll1(x))
        x = F.relu(self.ll2(x))
        x = F.relu(self.ll3(x))
        x = F.relu(self.ll4(x))
        x = F.softmax(self.oll(x))
        return x



Experience = namedtuple('Experience', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory():  # iNstead of using array try using doubly linked list - orderedDict
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0  # keep track of how many experiences we've added to memory

    # function to store experiences as they occur in replay memory
    def push(self, experience):
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            # if number of experiences exceeds capacity,
            # push the new experience to the front of memory, overriding the oldest experiences
            self.memory[self.push_count % self.capacity] = experience
        self.push_count += 1

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def can_provide_sample(self, batch_size):
        return len(self.memory) >= batch_size


class EpsilonGreedyStrategy():
    def __init__(self, start, end, decay):
        self.start = start
        self.end = end
        self.decay = decay

    def get_exploration_rate(self, current_step):
        return self.end + (self.start - self.end) * \
               math.exp(-1. * current_step * self.decay)


class Agent():
    def __init__(self, strategy, num_actions, device):
        self.current_step = 0
        self.strategy = strategy
        self.num_actions = num_actions
        self.device = device
        self.mappings = defaultdict(tuple)

    def select_action(self, state, policy_net, possible_moves):
        # policy network is the deep Q network that we train to get the optimal policy
        rate = self.strategy.get_exploration_rate(self.current_step)
        # print("Exploration rate: ", rate)
        self.current_step += 1

        if rate > random.random():
            # print ('Exploring')
            action = random.choice(possible_moves)  # pick a possible out of the available ones - change
            return torch.tensor(action[0]).to(self.device), rate  # TODO - model action tensor

        else:
            # turning off gradient tracking during inference, not training
            # print('Exploiting')
            with torch.no_grad():
                # print(state)
                returned_states = policy_net(state)
                max_value = float("-inf")
                max_index = 0
                # print("POSSIBLE MOVES: ", possible_moves)
                possible_moves_indexes = []
                for i in possible_moves:
                    possible_moves_indexes.append(i[0])
                for index, value in enumerate(returned_states):
                    if (index in possible_moves_indexes and value > max_value):
                        max_value = value
                        max_index = index
                max_index_tensor = torch.tensor(max_index).to(self.device)
                # result = policy_net(state).argmax(dim=-1).to(self.device)
                # print ('RESULT', max_index_tensor)
                return max_index_tensor, rate
                # return policy_net(torch.tensor(state)).argmax(dim=1).to(self.device) # exploit

    def select_action_testing(self, state, policy_net, possible_moves):
        with torch.no_grad():
            # print(policy_net(state))
            returned_states = policy_net(state)
            max_value = float("-inf")
            max_index = 0
            # print("POSSIBLE MOVES: ", possible_moves)
            possible_moves_indexes = []

            for i in possible_moves:
                possible_moves_indexes.append(i[0])

            for index, value in enumerate(returned_states):
                if (index in possible_moves_indexes and value > max_value):
                    max_value = value
                    max_index = index
            max_index_tensor = torch.tensor(max_index)

            # print ('Result',max_index_tensor)
            return max_index_tensor
            # return policy_net(torch.tensor(state)).argmax(dim=1).to(self.device) # exploit

class Environment():
    def __init__(self, ghost_posititon, ghost_resources, ghostbuster_positions, ghostbuster_resources):
        # print(ghost_posititon)
        # start_state = [165, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]

        WALK = 'WALK'
        SEWAGE = 'SEWAGE'
        TUNNEL = 'TUNNEL'
        BLACK = 'BLACK'
        self.board = (((8, (WALK,)), (9, (WALK,)), (58, (SEWAGE,)), (46, (SEWAGE, TUNNEL))),
                      # locToRoutes[0] has no value; need to access locToRoutes[1] and higher
                      ((8, (WALK,)), (9, (WALK,)), (58, (SEWAGE,)), (46, (SEWAGE, TUNNEL))),  # 001
                      ((20, (WALK,)), (10, (WALK,))),
                      ((11, (WALK,)), (12, (WALK,)), (4, (WALK,)), (22, (SEWAGE,)), (23, (SEWAGE,))),
                      ((3, (WALK,)), (13, (WALK,))),
                      ((15, (WALK,)), (16, (WALK,))),  # 005
                      ((29, (WALK,)), (7, (WALK,))),
                      ((6, (WALK,)), (17, (WALK,)), (42, (SEWAGE,))),
                      ((1, (WALK,)), (19, (WALK,)), (18, (WALK,))),
                      ((1, (WALK,)), (19, (WALK,)), (20, (WALK,))),
                      ((2, (WALK,)), (11, (WALK,)), (34, (WALK,)), (21, (WALK,))),  # 010
                      ((3, (WALK,)), (10, (WALK,)), (22, (WALK,))),
                      ((3, (WALK,)), (23, (WALK,))),
                      ((4, (WALK,)), (14, (WALK, SEWAGE)), (24, (WALK,)), (23, (WALK, SEWAGE)), (52, (SEWAGE,)),
                       (89, (TUNNEL,)), (67, (TUNNEL,)), (46, (TUNNEL,))),
                      ((13, (WALK, SEWAGE)), (15, (WALK, SEWAGE)), (25, (WALK,))),
                      ((5, (WALK,)), (16, (WALK,)), (28, (WALK,)), (26, (WALK,)), (14, (WALK, SEWAGE)),
                       (29, (SEWAGE,)), (41, (SEWAGE,))),  # 015
                      ((5, (WALK,)), (29, (WALK,)), (28, (WALK,)), (15, (WALK,))),
                      ((7, (WALK,)), (30, (WALK,)), (29, (WALK,))),
                      ((8, (WALK,)), (31, (WALK,)), (43, (WALK,))),
                      ((8, (WALK,)), (9, (WALK,)), (32, (WALK,))),
                      ((2, (WALK,)), (9, (WALK,)), (33, (WALK,))),  # 020
                      ((10, (WALK,)), (33, (WALK,))),
                      ((11, (WALK,)), (23, (WALK, SEWAGE)), (35, (WALK,)), (34, (WALK, SEWAGE)),
                       (3, (SEWAGE,)), (65, (SEWAGE,))),
                      ((12, (WALK,)), (13, (WALK, SEWAGE)), (37, (WALK,)), (22, (WALK, SEWAGE)),
                       (3, (SEWAGE,)), (67, (SEWAGE,))),
                      ((13, (WALK,)), (38, (WALK,)), (37, (WALK,))),
                      ((14, (WALK,)), (39, (WALK,)), (38, (WALK,))),  # 025
                      ((15, (WALK,)), (27, (WALK,)), (39, (WALK,))),
                      ((26, (WALK,)), (28, (WALK,)), (40, (WALK,))),
                      ((15, (WALK,)), (16, (WALK,)), (41, (WALK,)), (27, (WALK,))),
                      ((6, (WALK,)), (17, (WALK,)), (42, (WALK, SEWAGE)), (41, (WALK, SEWAGE)), (16, (WALK,)),
                       (55, (SEWAGE,)), (15, (SEWAGE,))),
                      ((17, (WALK,)), (42, (WALK,))),  # 030
                      ((18, (WALK,)), (44, (WALK,)), (43, (WALK,))),
                      ((19, (WALK,)), (33, (WALK,)), (45, (WALK,)), (44, (WALK,))),
                      ((20, (WALK,)), (21, (WALK,)), (46, (WALK,)), (32, (WALK,))),
                      ((10, (WALK,)), (22, (WALK, SEWAGE)), (48, (WALK,)), (47, (WALK,)), (63, (SEWAGE,)),
                       (46, (SEWAGE,))),
                      ((22, (WALK,)), (36, (WALK,)), (65, (WALK,)), (48, (WALK,))),  # 035
                      ((37, (WALK,)), (49, (WALK,)), (35, (WALK,))),
                      ((23, (WALK,)), (24, (WALK,)), (50, (WALK,)), (36, (WALK,))),
                      ((24, (WALK,)), (25, (WALK,)), (51, (WALK,)), (50, (WALK,))),
                      ((26, (WALK,)), (52, (WALK,)), (51, (WALK,)), (25, (WALK,))),
                      ((27, (WALK,)), (41, (WALK,)), (53, (WALK,)), (52, (WALK,))),  # 040
                      ((28, (WALK,)), (29, (WALK, SEWAGE)), (54, (WALK,)), (40, (WALK,)),
                       (15, (SEWAGE,)), (87, (SEWAGE,)), (52, (SEWAGE,))),
                      ((30, (WALK,)), (56, (WALK,)), (72, (WALK, SEWAGE)), (29, (WALK, SEWAGE)),
                       (7, (SEWAGE,))),
                      ((18, (WALK,)), (31, (WALK,)), (57, (WALK,))),
                      ((32, (WALK,)), (58, (WALK,)), (31, (WALK,))),
                      ((32, (WALK,)), (46, (WALK,)), (60, (WALK,)), (59, (WALK,)),  # 045
                       (58, (WALK,))),
                      ((33, (WALK,)), (47, (WALK,)), (61, (WALK,)), (45, (WALK,)), (34, (SEWAGE,)),
                       (78, (SEWAGE,)), (58, (SEWAGE,)), (1, (SEWAGE, TUNNEL)), (13, (TUNNEL,)),
                       (79, (TUNNEL,)), (74, (TUNNEL,))),
                      ((34, (WALK,)), (62, (WALK,)), (46, (WALK,))),
                      ((34, (WALK,)), (35, (WALK,)), (63, (WALK,)), (62, (WALK,))),
                      ((36, (WALK,)), (50, (WALK,)), (66, (WALK,))),
                      ((37, (WALK,)), (38, (WALK,)), (49, (WALK,))),  # 050
                      ((38, (WALK,)), (39, (WALK,)), (52, (WALK,)), (68, (WALK,)), (67, (WALK,))),
                      ((39, (WALK,)), (40, (WALK,)), (69, (WALK,)), (51, (WALK,)), (13, (SEWAGE,)),
                       (41, (SEWAGE,)), (86, (SEWAGE,)), (67, (SEWAGE,))),
                      ((40, (WALK,)), (54, (WALK,)), (69, (WALK,))),
                      ((41, (WALK,)), (55, (WALK,)), (70, (WALK,)), (53, (WALK,))),
                      ((71, (WALK,)), (54, (WALK,)), (29, (SEWAGE,)), (89, (SEWAGE,))),  # 055
                      ((42, (WALK,)), (91, (WALK,))),
                      ((43, (WALK,)), (58, (WALK,)), (73, (WALK,))),
                      ((45, (WALK,)), (59, (WALK,)), (75, (WALK,)), (74, (WALK, SEWAGE)), (57, (WALK,)),
                       (44, (WALK,)), (46, (SEWAGE,)), (77, (SEWAGE,)), (1, (SEWAGE,))),
                      ((45, (WALK,)), (76, (WALK,)), (75, (WALK,)), (58, (WALK,))),
                      ((45, (WALK,)), (61, (WALK,)), (76, (WALK,))),  # 060
                      ((46, (WALK,)), (62, (WALK,)), (78, (WALK,)), (76, (WALK,)), (60, (WALK,))),
                      ((47, (WALK,)), (48, (WALK,)), (79, (WALK,)), (61, (WALK,))),
                      ((48, (WALK,)), (64, (WALK,)), (80, (WALK,)), (79, (WALK, SEWAGE)),
                       (34, (SEWAGE,)), (65, (SEWAGE,)), (100, (SEWAGE,))),
                      ((65, (WALK,)), (81, (WALK,)), (63, (WALK,))),
                      ((35, (WALK,)), (66, (WALK,)), (82, (WALK, SEWAGE)), (64, (WALK,)),  # 065
                       (22, (SEWAGE,)), (67, (SEWAGE,)), (63, (SEWAGE,))),
                      ((49, (WALK,)), (67, (WALK,)), (82, (WALK,)), (65, (WALK,))),
                      ((51, (WALK,)), (68, (WALK,)), (84, (WALK,)), (66, (WALK,)), (23, (SEWAGE,)),
                       (52, (SEWAGE,)), (102, (SEWAGE,)), (82, (SEWAGE,)), (65, (SEWAGE,)),
                       (13, (TUNNEL,)), (89, (TUNNEL,)), (111, (TUNNEL,)),
                       (79, (TUNNEL,))),
                      ((51, (WALK,)), (69, (WALK,)), (85, (WALK,)), (67, (WALK,))),
                      ((52, (WALK,)), (53, (WALK,)), (86, (WALK,)), (68, (WALK,))),
                      ((54, (WALK,)), (71, (WALK,)), (87, (WALK,))),  # 070
                      ((55, (WALK,)), (72, (WALK,)), (89, (WALK,)), (70, (WALK,))),
                      ((42, (WALK, SEWAGE)), (91, (WALK,)), (90, (WALK,)), (71, (WALK,)),
                       (107, (SEWAGE,)), (105, (SEWAGE,))),
                      ((57, (WALK,)), (74, (WALK,)), (92, (WALK,))),
                      ((58, (WALK, SEWAGE)), (75, (WALK,)), (92, (WALK,)), (73, (WALK,)),
                       (94, (SEWAGE,)), (46, (TUNNEL,))),
                      ((58, (WALK,)), (59, (WALK,)), (94, (WALK,)), (74, (WALK,))),  # 075
                      ((59, (WALK,)), (60, (WALK,)), (61, (WALK,)), (77, (WALK,))),
                      ((78, (WALK, SEWAGE)), (96, (WALK,)), (95, (WALK,)), (76, (WALK,)),
                       (124, (SEWAGE,)), (94, (SEWAGE,)), (58, (SEWAGE,))),
                      ((61, (WALK,)), (79, (WALK, SEWAGE)), (97, (WALK,)), (77, (WALK, SEWAGE)),
                       (46, (SEWAGE,))),
                      ((62, (WALK,)), (63, (WALK, SEWAGE)), (98, (WALK,)), (78, (WALK, SEWAGE)),
                       (46, (TUNNEL,)), (67, (TUNNEL,)), (111, (TUNNEL,)),
                       (93, (TUNNEL,))),
                      ((63, (WALK,)), (100, (WALK,)), (99, (WALK,))),  # 080
                      ((64, (WALK,)), (82, (WALK,)), (100, (WALK,))),
                      ((65, (WALK, SEWAGE)), (66, (WALK,)), (67, (SEWAGE,)), (101, (WALK,)), (140, (SEWAGE,)),
                       (81, (WALK,)), (100, (SEWAGE,))),
                      ((102, (WALK,)), (101, (WALK,))),
                      ((67, (WALK,)), (85, (WALK,))),
                      ((68, (WALK,)), (103, (WALK,)), (84, (WALK,))),  # 085
                      ((69, (WALK,)), (52, (SEWAGE,)), (87, (SEWAGE,)), (104, (WALK,)), (116, (SEWAGE,)),
                       (103, (WALK,)), (102, (SEWAGE,))),
                      ((70, (WALK,)), (41, (SEWAGE,)), (88, (WALK,)), (105, (SEWAGE,)), (86, (SEWAGE,))),
                      ((89, (WALK,)), (117, (WALK,)), (87, (WALK,))),
                      ((71, (WALK,)), (55, (SEWAGE,)), (13, (TUNNEL,)), (105, (WALK, SEWAGE)),
                       (128, (TUNNEL,)), (88, (WALK,)), (140, (TUNNEL,)),
                       (67, (TUNNEL,))),
                      ((72, (WALK,)), (91, (WALK,)), (105, (WALK,))),  # 090
                      ((56, (WALK,)), (107, (WALK,)), (105, (WALK,)), (90, (WALK,)), (72, (WALK,))),
                      ((73, (WALK,)), (74, (WALK,)), (93, (WALK,))),
                      ((92, (WALK,)), (94, (WALK, SEWAGE)), (79, (TUNNEL,))),
                      ((74, (SEWAGE,)), (75, (WALK,)), (95, (WALK,)), (77, (SEWAGE,)), (93, (WALK, SEWAGE))),
                      ((77, (WALK,)), (122, (WALK,)), (94, (WALK,))),  # 095
                      ((77, (WALK,)), (97, (WALK,)), (109, (WALK,))),
                      ((78, (WALK,)), (98, (WALK,)), (109, (WALK,)), (96, (WALK,))),
                      ((79, (WALK,)), (99, (WALK,)), (110, (WALK,)), (97, (WALK,))),
                      ((80, (WALK,)), (112, (WALK,)), (110, (WALK,)), (98, (WALK,))),
                      ((81, (WALK,)), (82, (SEWAGE,)), (101, (WALK,)), (113, (WALK,)),  # 100
                       (112, (WALK,)), (111, (SEWAGE,)), (80, (WALK,)), (63, (SEWAGE,))),
                      ((83, (WALK,)), (114, (WALK,)), (100, (WALK,)), (82, (WALK,))),
                      ((67, (SEWAGE,)), (103, (WALK,)), (86, (SEWAGE,)), (115, (WALK,)), (127, (SEWAGE,)),
                       (83, (WALK,))),
                      ((85, (WALK,)), (86, (WALK,)), (102, (WALK,))),
                      ((86, (WALK,)), (116, (WALK,))),
                      ((90, (WALK,)), (72, (SEWAGE,)), (91, (WALK,)), (106, (WALK,)),  # 105
                       (107, (SEWAGE,)), (108, (WALK, SEWAGE)), (87, (SEWAGE,)), (89, (WALK, SEWAGE))),
                      ((107, (WALK,)), (105, (WALK,))),
                      ((91, (WALK,)), (72, (SEWAGE,)), (119, (WALK,)), (161, (SEWAGE,)),
                       (106, (WALK,)), (105, (SEWAGE,))),
                      ((105, (WALK, SEWAGE)), (119, (WALK,)), (135, (SEWAGE,)), (117, (WALK,)),
                       (116, (SEWAGE,)), (115, (BLACK,))),
                      ((97, (WALK,)), (110, (WALK,)), (124, (WALK,)), (96, (WALK,))),
                      ((99, (WALK,)), (111, (WALK,)), (109, (WALK,)), (98, (WALK,))),  # 110
                      ((112, (WALK,)), (100, (SEWAGE,)), (67, (TUNNEL,)),
                       (153, (TUNNEL,)), (124, (WALK, SEWAGE)), (163, (TUNNEL,)),
                       (110, (WALK,)), (79, (TUNNEL,))),
                      ((100, (WALK,)), (125, (WALK,)), (111, (WALK,)), (99, (WALK,))),
                      ((114, (WALK,)), (125, (WALK,)), (100, (WALK,))),
                      ((101, (WALK,)), (115, (WALK,)), (126, (WALK,)),
                       (132, (WALK,)), (131, (WALK,)), (113, (WALK,))),
                      ((102, (WALK,)), (127, (WALK,)), (126, (WALK,)), (114, (WALK,)),  # 115
                       (108, (BLACK,)), (157, (BLACK,))),
                      ((104, (WALK,)), (86, (SEWAGE,)), (117, (WALK,)), (108, (SEWAGE,)),
                       (118, (WALK,)), (142, (SEWAGE,)), (127, (WALK, SEWAGE))),
                      ((88, (WALK,)), (108, (WALK,)), (129, (WALK,)), (116, (WALK,))),
                      ((116, (WALK,)), (129, (WALK,)), (142, (WALK,)), (134, (WALK,))),
                      ((107, (WALK,)), (136, (WALK,)), (108, (WALK,))),
                      ((121, (WALK,)), (144, (WALK,))),  # 120
                      ((122, (WALK,)), (145, (WALK,)), (120, (WALK,))),
                      ((95, (WALK,)), (123, (WALK, SEWAGE)), (146, (WALK,)),
                       (121, (WALK,)), (144, (SEWAGE,))),
                      ((124, (WALK, SEWAGE)), (149, (WALK,)), (165, (SEWAGE,)), (148, (WALK,)),
                       (137, (WALK,)), (144, (SEWAGE,)), (122, (WALK, SEWAGE))),
                      ((109, (WALK,)), (111, (WALK, SEWAGE)), (130, (WALK,)), (138, (WALK,)),
                       (153, (SEWAGE,)), (123, (WALK, SEWAGE)), (77, (SEWAGE,))),
                      ((113, (WALK,)), (131, (WALK,)), (112, (WALK,))),  # 125
                      ((115, (WALK,)), (127, (WALK,)), (140, (WALK,)), (114, (WALK,))),
                      ((116, (WALK, SEWAGE)), (134, (WALK,)), (133, (WALK, SEWAGE)),
                       (126, (WALK,)), (115, (WALK,)), (102, (SEWAGE,))),
                      ((143, (WALK,)), (135, (SEWAGE,)), (89, (TUNNEL,)), (160, (WALK,)),
                       (161, (SEWAGE,)), (188, (WALK,)), (199, (SEWAGE,)), (172, (WALK,)),
                       (187, (SEWAGE,)), (185, (TUNNEL,)), (142, (WALK, SEWAGE)),
                       (140, (TUNNEL,))),
                      ((117, (WALK,)), (135, (WALK,)), (143, (WALK,)), (142, (WALK,)),
                       (118, (WALK,))),
                      ((131, (WALK,)), (139, (WALK,)), (124, (WALK,))),  # 130
                      ((114, (WALK,)), (130, (WALK,)), (125, (WALK,))),
                      ((114, (WALK,)), (140, (WALK,))),
                      ((127, (WALK, SEWAGE)), (141, (WALK,)), (157, (SEWAGE,)), (140, (WALK, SEWAGE))),
                      ((118, (WALK,)), (142, (WALK,)), (141, (WALK,)), (127, (WALK,))),
                      ((108, (SEWAGE,)), (136, (WALK,)), (161, (WALK, SEWAGE)), (143, (WALK,)),  # 135
                       (128, (SEWAGE,)), (129, (WALK,))),
                      ((119, (WALK,)), (162, (WALK,)), (135, (WALK,))),
                      ((123, (WALK,)), (147, (WALK,))),
                      ((152, (WALK,)), (150, (WALK,)), (124, (WALK,))),
                      ((130, (WALK,)), (140, (WALK,)), (154, (WALK,)), (153, (WALK,))),
                      ((132, (WALK,)), (82, (SEWAGE,)), (126, (WALK,)), (89, (TUNNEL,)),  # 140
                       (133, (WALK, SEWAGE)), (128, (TUNNEL,)), (156, (WALK, SEWAGE)),
                       (154, (WALK, SEWAGE)), (153, (TUNNEL,)), (139, (WALK,))),
                      ((134, (WALK,)), (142, (WALK,)), (158, (WALK,)), (133, (WALK,))),
                      ((118, (WALK,)), (116, (SEWAGE,)), (129, (WALK,)), (143, (WALK,)),
                       (128, (WALK, SEWAGE)), (158, (WALK,)), (157, (SEWAGE,)), (141, (WALK,)),
                       (134, (WALK,))),
                      ((135, (WALK,)), (160, (WALK,)), (128, (WALK,)), (142, (WALK,)),
                       (129, (WALK,))),
                      ((120, (WALK,)), (122, (SEWAGE,)), (145, (WALK,)), (123, (SEWAGE,)),
                       (163, (SEWAGE,)), (177, (WALK,))),
                      ((121, (WALK,)), (146, (WALK,)), (144, (WALK,))),  # 145
                      ((122, (WALK,)), (147, (WALK,)), (163, (WALK,)), (145, (WALK,))),
                      ((137, (WALK,)), (164, (WALK,)), (146, (WALK,))),
                      ((123, (WALK,)), (149, (WALK,)), (164, (WALK,))),
                      ((123, (WALK,)), (150, (WALK,)), (165, (WALK,)), (148, (WALK,))),
                      ((138, (WALK,)), (151, (WALK,)), (149, (WALK,))),  # 150
                      ((152, (WALK,)), (166, (WALK,)), (165, (WALK,)), (150, (WALK,))),
                      ((153, (WALK,)), (151, (WALK,)), (138, (WALK,))),
                      ((139, (WALK,)), (111, (TUNNEL,)), (154, (WALK, SEWAGE)),
                       (140, (TUNNEL,)), (167, (WALK,)), (184, (SEWAGE,)),
                       (185, (TUNNEL,)), (166, (WALK,)), (180, (SEWAGE,)),
                       (163, (TUNNEL,)), (152, (WALK,)), (124, (SEWAGE,))),
                      ((140, (WALK, SEWAGE)), (155, (WALK,)), (156, (SEWAGE,)), (153, (WALK, SEWAGE)),
                       (139, (WALK,))),
                      ((156, (WALK,)), (168, (WALK,)), (167, (WALK,)), (154, (WALK,))),  # 155
                      ((140, (WALK, SEWAGE)), (157, (WALK, SEWAGE)), (169, (WALK,)),
                       (184, (SEWAGE,)), (155, (WALK,)), (154, (SEWAGE,))),
                      ((133, (SEWAGE,)), (158, (WALK,)), (142, (SEWAGE,)), (170, (WALK,)),
                       (185, (SEWAGE,)), (156, (WALK, SEWAGE)), (115, (BLACK,)), (194, (BLACK,))),
                      ((141, (WALK,)), (142, (WALK,)), (159, (WALK,)), (157, (WALK,))),
                      ((158, (WALK,)), (172, (WALK,)), (198, (WALK,)), (186, (WALK,)),
                       (170, (WALK,))),
                      ((143, (WALK,)), (161, (WALK,)), (173, (WALK,)), (128, (WALK,))),  # 160
                      ((107, (SEWAGE,)), (174, (WALK,)), (199, (SEWAGE,)), (160, (WALK,)),
                       (128, (SEWAGE,)), (135, (WALK, SEWAGE))),
                      ((175, (WALK,)), (136, (WALK,))),
                      ((146, (WALK,)), (111, (TUNNEL,)), (153, (TUNNEL,)),
                       (191, (SEWAGE,)), (177, (WALK,)), (176, (SEWAGE,)), (144, (SEWAGE,))),
                      ((147, (WALK,)), (148, (WALK,)), (179, (WALK,)), (178, (WALK,))),
                      ((149, (WALK,)), (123, (SEWAGE,)), (151, (WALK,)), (180, (WALK, SEWAGE)),  # 165
                       (179, (WALK,)), (191, (SEWAGE,))),
                      ((153, (WALK,)), (183, (WALK,)), (181, (WALK,)), (151, (WALK,))),
                      ((155, (WALK,)), (168, (WALK,)), (183, (WALK,)), (153, (WALK,))),
                      ((155, (WALK,)), (184, (WALK,)), (167, (WALK,))),
                      ((156, (WALK,)), (184, (WALK,))),
                      ((157, (WALK,)), (159, (WALK,)), (185, (WALK,))),  # 170
                      ((173, (WALK,)), (175, (WALK,)), (199, (WALK,))),
                      ((128, (WALK,)), (187, (WALK,)), (159, (WALK,))),
                      ((160, (WALK,)), (174, (WALK,)), (171, (WALK,)), (188, (WALK,))),
                      ((175, (WALK,)), (173, (WALK,)), (161, (WALK,))),
                      ((162, (WALK,)), (171, (WALK,)), (174, (WALK,))),  # 175
                      ((177, (WALK,)), (163, (SEWAGE,)), (189, (WALK,)), (190, (SEWAGE,))),
                      ((144, (WALK,)), (163, (WALK,)), (176, (WALK,))),
                      ((164, (WALK,)), (191, (WALK,)), (189, (WALK,))),
                      ((165, (WALK,)), (191, (WALK,)), (164, (WALK,))),
                      ((165, (WALK, SEWAGE)), (181, (WALK,)), (153, (SEWAGE,)), (193, (WALK,)),  # 180
                       (184, (SEWAGE,)), (190, (SEWAGE,))),
                      ((166, (WALK,)), (182, (WALK,)), (193, (WALK,)), (180, (WALK,))),
                      ((183, (WALK,)), (195, (WALK,)), (181, (WALK,))),
                      ((167, (WALK,)), (196, (WALK,)), (182, (WALK,)), (166, (WALK,))),
                      ((169, (WALK,)), (156, (SEWAGE,)), (185, (WALK, SEWAGE)), (197, (WALK,)),
                       (196, (WALK,)), (180, (SEWAGE,)), (168, (WALK,)), (153, (SEWAGE,))),
                      ((170, (WALK,)), (157, (SEWAGE,)), (186, (WALK,)), (187, (SEWAGE,)),  # 185
                       (128, (TUNNEL,)), (184, (WALK, SEWAGE)), (153, (TUNNEL,))),
                      ((159, (WALK,)), (198, (WALK,)), (185, (WALK,))),
                      ((172, (WALK,)), (128, (SEWAGE,)), (188, (WALK,)), (198, (WALK,)),
                       (185, (SEWAGE,))),
                      ((128, (WALK,)), (173, (WALK,)), (199, (WALK,)), (187, (WALK,))),
                      ((178, (WALK,)), (190, (WALK,)), (176, (WALK,))),
                      ((191, (WALK, SEWAGE)), (192, (WALK,)), (180, (SEWAGE,)),  # 190
                       (189, (WALK,)), (176, (SEWAGE,))),
                      ((179, (WALK,)), (165, (SEWAGE,)), (192, (WALK,)), (190, (WALK, SEWAGE)),
                       (178, (WALK,)), (163, (SEWAGE,))),
                      ((191, (WALK,)), (194, (WALK,)), (190, (WALK,))),
                      ((181, (WALK,)), (194, (WALK,)), (180, (WALK,))),
                      ((195, (WALK,)), (192, (WALK,)), (193, (WALK,)), (157, (BLACK,))),
                      ((182, (WALK,)), (197, (WALK,)), (194, (WALK,))),  # 195
                      ((183, (WALK,)), (184, (WALK,)), (197, (WALK,))),
                      ((196, (WALK,)), (184, (WALK,)), (195, (WALK,))),
                      ((159, (WALK,)), (187, (WALK,)), (199, (WALK,)), (186, (WALK,))),
                      ((188, (WALK,)), (128, (SEWAGE,)), (171, (WALK,)), (161, (SEWAGE,)),
                       (198, (WALK,)))
                      )

        self.ghost_posititon = ghost_posititon
        self.ghostbuster_positions = ghostbuster_positions
        self.ghost_resources = ghost_resources
        # self.ghostbuster_resources = ghostbuster_resources
        self.ghostbuster_resources = [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]]
        self.done = False
        self.possible_moves = self.board[self.ghost_posititon]

    def take_action_detectives_random(self):
        d = {
            "WALK": 0,
            "SEWAGE": 1,
            "TUNNEL": 2,
            "BLACK": 3
        }
        # print(self.ghostbuster_resources)
        for index, each_detective in enumerate(self.ghostbuster_positions):
            pm = self.board[each_detective]
            new_pm = []
            for x in pm:
                for k in range(0, len(x[1])):
                    if (x[1][k] != "BLACK"):

                        if (self.ghostbuster_resources[index][d[x[1][k]]] > 0):
                            new_pm.append((x[0], x[1][k]))
            if (len(new_pm) > 0):
                random_move = random.choice(new_pm)

                # print(random_move)
                if 'WALK' == random_move[1]:
                    resource_used = 0

                elif 'SEWAGE' == random_move[1]:
                    resource_used = 1

                else:
                    resource_used = 2

                self.ghostbuster_positions[index] = random_move[0]
                self.ghostbuster_resources[index][resource_used] -= 1

    def take_action_detectives(self):
        res_state_loc = []
        res_state_resources = self.ghostbuster_resources

        for count, det in enumerate(self.ghostbuster_positions):
            moves = self.board[int(det)]
            min_dist_node = -1
            min_dist_val = float("inf")

            for move in moves:
                val = self.getdistance(self.ghost_posititon, move[0])

                if (val < min_dist_val):
                    min_dist_node = move
                    min_dist_val = val

            res_state_loc.append(min_dist_node[0])
            # print("COUNT: ", count)
            if (min_dist_node[1][0] == 'WALK'):
                res_state_resources[count][0] = max(res_state_resources[count][0] - 1, 0)

            elif (min_dist_node[1][0] == 'SEWAGE'):
                res_state_resources[count][1] = max(res_state_resources[count][1] - 1, 0)
            else:
                res_state_resources[count][2] = max(res_state_resources[count][2] - 1, 0)
        return (res_state_loc, res_state_resources)

    def get_state(self, round_number):
        in_state = [self.ghost_posititon, self.ghost_resources, self.ghostbuster_positions, self.ghostbuster_resources, round_number]
        # print("1", in_state)
        state = generate_feature_space(in_state)
        # print("2")
        return torch.tensor(state), in_state

    def getdistance(self, x, y):
        return abs(int(x) - int(y))

    def num_actions_available(self):
        return len(self.possible_moves)

    def take_action(self, action, timestep):
        # update Mr. X's position to simulate his taking an action
        self.ghost_posititon = action
        self.take_action_detectives_random()

        # detective_position_average = 0
        # for each_detective in self.ghostbuster_positions:
        #   detective_position_average += each_detective
        # detective_position_average = detective_position_average/5

        # reward = self.getdistance(self.ghost_posititon, detective_position_average)
        self.done = self.is_done(timestep)
        if self.done == 1:
            return -100
        elif (self.done == 2):
            return 100
        else:
            return 0

    def is_done(self, timestep):
        # game ends when either one detective is at the place of Mr. X
        for each_detective in self.ghostbuster_positions:
            if each_detective == self.ghost_posititon:
                return 1
        if (timestep == 24):
            return 2
        return 0

    # returns true is ghost wins
    def winner(self):

        for each_ghostbuster in self.ghostbuster_positions:
            if each_ghostbuster == self.ghost_posititon:
                return False
        return True


def extract_tensors(experiences):
    # Convert batch of Experiences to Experience of batches
    batch = Experience(*zip(*experiences))
    t1 = torch.stack(batch.state)
    t4 = torch.stack(batch.next_state)
    t3 = torch.stack(batch.reward)
    t2 = torch.stack(batch.action)
    #t3 = torch.cat(batch.reward)
    #t4 = torch.cat(batch.next_state)

    return (t1,t2,t3,t4)

def one_hot_encode(value, size, max_value):
    a = np.array(value)
    b = np.zeros((size, max_value))
    b[np.arange(size), a - 1] = 1
    return b.tolist()


def generate_feature_space(inital_st):
    # inital_st = [26, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    feature_space = []
    feature_space.extend(one_hot_encode(inital_st[0], 1, 199)[0])
    feature_space.append(inital_st[1])
    ghostbuster_loc = one_hot_encode(inital_st[2], 5, 199)
    feature_space.extend(ghostbuster_loc[0])
    feature_space.extend(ghostbuster_loc[1])
    feature_space.extend(ghostbuster_loc[2])
    feature_space.extend(ghostbuster_loc[3])
    feature_space.extend(ghostbuster_loc[4])
    ghostbuster_tic = inital_st[3]
    feature_space.extend(ghostbuster_tic[0])
    feature_space.extend(ghostbuster_tic[1])
    feature_space.extend(ghostbuster_tic[2])
    feature_space.extend(ghostbuster_tic[3])
    feature_space.extend(ghostbuster_tic[4])
    feature_space.append(inital_st[4])
    # print(feature_space)
    # print(len(feature_space))
    return feature_space


class QValues():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    @staticmethod
    def get_current(policy_net, states, actions):
        return policy_net(states).gather(dim=1, index=actions.unsqueeze(-1))
    @staticmethod
    def get_next(target_net, next_states):
        final_state_locations = next_states.flatten(start_dim=1).max(dim=1)[0].eq(0).type(torch.bool)
        non_final_state_locations = (final_state_locations == False)
        non_final_states = next_states[non_final_state_locations]
        batch_size = next_states.shape[0]
        values = torch.zeros(batch_size).to(QValues.device)
        values[non_final_state_locations] = target_net(non_final_states).max(dim=1)[0].detach()
        return values


def plot_training(rates, performance):
    # plotting the points
    plt.plot(rates, performance, color='green', linestyle='solid', linewidth=3)

    # naming the x axis
    plt.xlabel('Explore')
    # naming the y axis
    plt.ylabel('Ghost Wins - Ghostbuster Wins')

    # giving a title to the graph
    plt.title('Training')

    # invert the x-axis on the graph
    # plt.gca().invert_xaxis()

    # function to show the plot
    plt.show()


def plot_testing(performance, games):
    # plotting the points
    plt.plot(games, performance, color='green', linestyle='solid', linewidth=3)

    # naming the x axis
    plt.xlabel('Game Number')

    # naming the y axis
    plt.ylabel('Ghost Wins - Ghostbuster Wins')

    # giving a title to my graph
    plt.title('Testing')

    # function to show the plot
    plt.show()



############################TRAIN##########################
def train():
    '''
    Should X position be tensor or not, and how to pass action tuple + need to handle multiple modes of transport in action.
    '''

    batch_size = 55  # 256
    gamma = 0.999
    eps_start = 1
    eps_end = 0.01
    eps_decay = 0.001
    target_update = 10  # how often we update target with policy n/w
    memory_size = 100000  # check with paper
    lr = 0.001 #learning rate for adam
    num_episodes = 200  # 1000
    # state_dim = True

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # start_state = [26, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    start_state = [165, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    start_feature = generate_feature_space(start_state)
    # print ('Length',len(start_feature))
    # print ('Without tensor',start_feature)
    # print ('With tensor',torch.tensor(start_feature).size())

    em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])
    strategy = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)

    agent = Agent(strategy, em.num_actions_available(), device)
    # print ('No. of available actions: ', em.num_actions_available())
    memory = ReplayMemory(memory_size)

    policy_net = DQN().to(device)
    target_net = DQN().to(device)

    # Set weights and biases in target_net to be same as that in policy_net
    target_net.load_state_dict(policy_net.state_dict())

    # eval mode, which tells PyTorch that this network is not in training mode. In other words, this network will only be used for inference
    target_net.eval()

    optimizer = optim.Adam(params=policy_net.parameters(), lr=lr)

    # store results of each episode in a list and use while plotting
    episode_durations = []

    ghost_win = 0
    busters_win = 0
    exploration_rate = []
    performance = []
    game_number = []
    for episode in range(num_episodes):
        # reset the environmet
        em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])
        # print ('Reset',em.ghost_posititon)

        # getting initial state
        state, _ = em.get_state(0)

        for timestep in range(25):
            # print ('Timestep-->', timestep, ' x position', em.ghost_posititon)
            # print ('ghostbuster Position', em.ghostbuster_positions)
            action_tensor, rate = agent.select_action(state, policy_net, em.board[em.ghost_posititon])

            action = action_tensor.tolist()
            # print('Move to take for Ghost', agent.mappings[action[0]])

            reward = em.take_action(action, timestep)
            # print ('Reward',reward)

            next_state, update_state = em.get_state(timestep)
            # print ('Next State in the form of feature vector',next_state)

            memory.push(
                Experience(torch.tensor(state), action_tensor, torch.tensor(next_state), torch.tensor([reward])))
            # memory.push(Experience(state, action_tensor, next_state, torch.tensor(reward)))
            # print ('MEMORY',memory)
            update_UI(update_state)

            state = next_state

            if memory.can_provide_sample(batch_size):
                # print ('in training')
                experiences = memory.sample(batch_size)
                states, actions, rewards, next_states = extract_tensors(experiences)

                current_q_values = QValues.get_current(policy_net, states, actions)
                # print ('Current Q values',current_q_values)

                next_q_values = QValues.get_next(target_net, next_states)
                # print ('Next Q values', next_q_values)

                target_q_values = (next_q_values * gamma) + rewards
                # print ('Target', target_q_values)

                loss = F.mse_loss(current_q_values, target_q_values.unsqueeze(1))
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if em.is_done(timestep) == 2:
                ghost_win += 1
                exploration_rate.append(rate)
                performance.append(busters_win - ghost_win)
                game_number.append(episode)
                break
            elif (em.is_done(timestep) == 1):
                busters_win += 1
                exploration_rate.append(rate)
                performance.append(busters_win - ghost_win)
                game_number.append(episode)
                # plot(episode_durations, 100)
                break

            if episode % target_update == 0:
                target_net.load_state_dict(policy_net.state_dict())

        print("Episode number: ", episode)
    print("Total number of episodes: ", num_episodes)
    print("Ghost wins: ", ghost_win)
    print("Detectives wins: ", busters_win)

    print(performance)
    print(exploration_rate)
    plot_training(exploration_rate, performance)
    torch.save(policy_net, 'ghost.pth')

############################TEST##########################
def update_UI(data): #TODO : Update firebase for the positions, tokens and round
    # sending post request and saving response as response object

    try:
        ghost_pos = data[0].item()
    except:
        ghost_pos = data[0]
    #ghost buster postion
    # a = data[2][0]
    # b = data[2][1]
    # c = data[2][2]
    # d = data[2][3]
    # e = data[2][4]
    #
    # round  = data[4]
    ref.update({
        'ghost': ghost_pos,
         'a': data[2][0],
        'b': data[2][1],
        'c': data[2][2],
        'd': data[2][3],
        'e': data[2][4],
        'round': data[4],
    })

    # print(r)
    # status = r.status
    # print("Updated:" % status)
    time.sleep(1)

def test():
    print("Here we are in test")
    model = torch.load('ghost.pth')
    model.eval()
    batch_size = 256  # 256
    gamma = 0.999
    eps_start = 1
    eps_end = 0.01
    eps_decay = 0.001
    target_update = 10  # how often we update target with policy n/w
    memory_size = 100000  # check with paper
    lr = 0.001
    num_episodes = 1000  # 1000
    # state_dim = True

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    start_state = [118, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    start_feature = generate_feature_space(start_state)

    em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])
    strategy = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)

    agent = Agent(strategy, em.num_actions_available(), device)
    # print ('No. of available actions: ', em.num_actions_available())
    memory = ReplayMemory(memory_size)

    policy_net = model

    ghost_win = 0
    busters_win = 0
    performance = []
    game_number = []
    for episode in range(num_episodes):
        # reset the environmet
        em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])
        # print ('Reset',em.ghost_posititon)

        # getting initial state
        state, initial_state = em.get_state(0)
        update_UI(initial_state)

        for timestep in range(25):
            action_tensor = agent.select_action_testing(state, policy_net, em.board[em.ghost_posititon])

            action = action_tensor.tolist()
            # print('Move to take for Mr. X', agent.mappings[action[0]])

            reward = em.take_action(action_tensor, timestep)
            # print ('Reward',reward)

            next_state, update_state = em.get_state(timestep)
            # print ('Next State in the form of feature vector',next_state)
            update_UI(update_state)
            state = next_state
            # print(len(state))
            if em.is_done(timestep) == 2:
                ghost_win += 1
                performance.append(busters_win - ghost_win)
                game_number.append(episode)
                break

            elif (em.is_done(timestep) == 1):
                busters_win += 1
                performance.append(busters_win - ghost_win)
                game_number.append(episode)
                # plot(episode_durations, 100)
                break

        print("Episode number: ", episode)

    print("Total number of episodes: ", num_episodes)
    print("Ghost wins: ", ghost_win)
    print("Ghost Busters wins: ", busters_win)

    print(performance)
    print(game_number)
    plot_testing(performance, game_number)


# train()
# test()


#######################SERVER#########################
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

""" The HTTP request handler """

cred = credentials.Certificate('firebase-adminsdk.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hackathon-b4e45.firebaseio.com/'
})
ref = db.reference('/ghostbuster')


class RequestHandler(BaseHTTPRequestHandler):

  def _send_cors_headers(self):
      """ Sets headers required for CORS """
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

  def send_dict_response(self, d):
      """ Sends a dictionary (JSON) back to the client """
      self.wfile.write(bytes(dumps(d), "utf8"))

  def do_OPTIONS(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

  def do_GET(self):
      # if(self.path):
      print(self.path)
      if self.path == "/start":
        # test()
        train()
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

      response = {}
      response["status"] = "OK"
      self.send_dict_response(response)


  def do_POST(self):
      print(self.path)
      self.send_response(200)
      self._send_cors_headers()
      self.send_header("Content-Type", "application/json")
      self.end_headers()

      dataLength = int(self.headers["Content-Length"])
      data = self.rfile.read(dataLength)

      print(data)

      response = {}
      response["status"] = "OK"
      self.send_dict_response(response)


print("Starting server")


httpd = HTTPServer(("127.0.0.1", 8000), RequestHandler)
print("Hosting server on port 8000")
httpd.serve_forever()
