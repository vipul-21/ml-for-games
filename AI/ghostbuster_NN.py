import gym
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, defaultdict
import time
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import os
from torch import optim
from env import *
from ghost_buster_dqn import *
from q_learning.QValues import *
from q_learning.ReplayMemory import *
from strategy.ghostnbuster_agent import *
# from strategy.agent import *

from strategy.epsilon_greedy import *
from utils import plot_testing
Experience = namedtuple('Experience', ('state', 'action', 'next_state', 'reward'))

############################TRAIN##########################
def train():
    '''
    Should X position be tensor or not, and how to pass action tuple + need to handle multiple modes of transport in action.
    '''

    batch_size = 10  # 256
    gamma = 0.999
    eps_start = 1
    eps_end = 0.01
    eps_decay = 0.001
    target_update = 10  # how often we update target with policy n/w
    memory_size = 100000  # check with paper
    lr = 0.001 #learning rate for adam
    num_episodes = 1000  # 1000
    # state_dim = True

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # start_state = [26, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    start_state = [100, 5, [41, 112, 198, 141, 174], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
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
            possible_moves = em.get_possible_moves()
            action_tensor, rate, choices = agent.select_action(state, policy_net, possible_moves)

            # action_tensor, rate, last_move_type = agent.select_action(state, policy_net, em.board[em.ghost_posititon])

            action = action_tensor.tolist()
            # print('Move to take for Ghost', agent.mappings[action[0]])

            reward = em.take_action(action, timestep, choices)
            # print ('Reward',reward)

            next_state, update_state = em.get_state(timestep)
            # print ('Next State in the form of feature vector',next_state)
            new_action = []
            for val in action:
                new_action.append(max(val, 0))
            new_action = torch.tensor(new_action).to("cpu")
            memory.push(
                Experience(torch.tensor(state), new_action, torch.tensor(next_state), torch.tensor([reward])))
            # memory.push(Experience(state, action_tensor, next_state, torch.tensor(reward)))
            # print ('MEMORY',memory)
            # update_UI(update_state, action, last_move_type)

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
                performance.append(busters_win - ghost_win )
                game_number.append(episode)
                break
            elif (em.is_done(timestep) == 1):
                busters_win += 1
                exploration_rate.append(rate)
                performance.append(busters_win - ghost_win )
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
    torch.save(policy_net, 'ghostbuster_1000.pth')

############################TEST##########################
def update_UI(data, last_move, last_move_type, epoch, ghost_win, busters_win): #TODO : Update firebase for the positions, tokens and round
    # sending post request and saving response as response object
    print(data)
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
    print("Round :", data[4], data[2][0],data[2][1],data[2][2],data[2][3],data[2][4], last_move, last_move_type)
    ref.update({
        'ghost': ghost_pos,
        'ghostLastMove': last_move_type,
         'a': data[2][0],
        'b': data[2][1],
        'c': data[2][2],
        'd': data[2][3],
        'e': data[2][4],
        'round': data[4],
        'epoch': epoch,
        'ghost_win': ghost_win,
        'busters_win': busters_win,
        'resources': data[3]
    })

    # print(r)
    # status = r.status
    # print("Updated:" % status)
    time.sleep(1)

def test():
    model = torch.load('ghostbuster_final.pth')
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

    # start_state = [118, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    # start_state = [154, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
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
        ghost_pos = random.randint(0,199)
        li = [val for val in range(200)]
        ghostbuster_pos = list(random.sample(li, 5))
        start_state = [ghost_pos, 5, ghostbuster_pos, [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
        # reset the environment
        em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])
        # print ('Reset',em.ghost_posititon)

        # getting initial state
        state, initial_state = em.get_state(0)
        # update_UI(initial_state)

        for timestep in range(25):
            possible_moves = em.get_possible_moves()
            action_tensor, choices = agent.select_action_testing(state, policy_net, possible_moves)

            action = action_tensor.tolist()
            # print('Move to take for Ghost', agent.mappings[action[0]])
            # print('Move to take', action)

            reward = em.take_action(action_tensor, timestep, choices)
            # print ('Reward',reward)

            next_state, update_state = em.get_state(timestep)
            # print ('Next State in the form of feature vector',next_state)
            # update_UI(update_state, action, last_move_type, episode, ghost_win, busters_win)
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

test()

def against():
    model_ghostbuster = torch.load('ghostbuster_final.pth')
    model_ghostbuster.eval()
    model_ghost = torch.load('ghost_final.pth')
    model_ghost.eval()


    eps_start = 1
    eps_end = 0.01
    eps_decay = 0.001
    memory_size = 100000  # check with paper
    num_episodes = 10  # 1000

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # start_state = [118, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    # start_state = [154, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]


    policy_net_ghost = model_ghost
    policy_net_ghostbuster = model_ghostbuster
    ghost_win = 0
    busters_win = 0
    performance = []
    game_number = []
    for episode in range(num_episodes):
        # reset the environment
        ghost_pos = random.randint(0,199)
        li = [val for val in range(200)]
        ghostbuster_pos = list(random.sample(li, 5))
        start_state = [ghost_pos, 5, ghostbuster_pos, [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
        start_feature = generate_feature_space(start_state)

        em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])

        # Ghost_Buster
        strategy_ghostbuster = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)
        agent_ghostbuster = Agent(strategy_ghostbuster, em.num_actions_available(), device)

        # Ghost
        strategy_ghost = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)
        agent_ghost = Agent_ghost(strategy_ghost, em.num_actions_available(), device)

        # print ('Reset',em.ghost_posititon)

        # getting initial state
        state, initial_state = em.get_state(0)
        # update_UI(initial_state)

        for timestep in range(25):
            possible_moves = em.get_possible_moves()
            action_tensor_ghostbuster, choices_ghostbuster = agent_ghostbuster.select_action_testing(state, policy_net_ghostbuster, possible_moves)

            action_tensor_ghost, choices_ghost = agent_ghost.select_action_testing(state, policy_net_ghost, em.board[em.ghost_posititon])

            action_ghost = action_tensor_ghost.tolist()
            action_ghostbuster = action_tensor_ghostbuster.tolist()

            # print('Move to take for Ghost', agent.mappings[action[0]])
            print('Move to take', action_ghost, action_ghostbuster)

            reward = em.take_action_against(action_ghost, choices_ghost,action_ghostbuster, choices_ghostbuster, timestep)
            # print ('Reward',reward)

            next_state, update_state = em.get_state(timestep)
            # print ('Next State in the form of feature vector',next_state)
            update_UI(update_state, action_ghost, choices_ghost, episode, ghost_win, busters_win)
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


# from http.server import BaseHTTPRequestHandler, HTTPServer
# from json import dumps
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
#
# """ The HTTP request handler """
#
# cred = credentials.Certificate('firebase-adminsdk.json')
# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://hackathon-b4e45.firebaseio.com/'
# })
# ref = db.reference('/ghostbuster')
#
#
# class RequestHandler(BaseHTTPRequestHandler):
#
#   def _send_cors_headers(self):
#       """ Sets headers required for CORS """
#       self.send_header("Access-Control-Allow-Origin", "*")
#       self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
#       self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")
#
#   def send_dict_response(self, d):
#       """ Sends a dictionary (JSON) back to the client """
#       self.wfile.write(bytes(dumps(d), "utf8"))
#
#   def do_OPTIONS(self):
#       self.send_response(200)
#       self._send_cors_headers()
#       self.end_headers()
#
#   def do_GET(self):
#       # if(self.path):
#       print(self.path)
#       if self.path == "/start":
#         # test()
#         print("")
#         # train()
#       elif self.path == "/train":
#           train()
#       elif self.path == "/test":
#           against()
#
#       self.send_response(200)
#       self._send_cors_headers()
#       self.end_headers()
#
#       response = {}
#       response["status"] = "OK"
#       self.send_dict_response(response)
#
#
#   def do_POST(self):
#       # print(self.path)
#       self.send_response(200)
#       self._send_cors_headers()
#       self.send_header("Content-Type", "application/json")
#       self.end_headers()
#
#       dataLength = int(self.headers["Content-Length"])
#       data = self.rfile.read(dataLength)
#
#       # print(data)
#
#       response = {}
#       response["status"] = "OK"
#       self.send_dict_response(response)
#
#
# print("Starting server")
#
#
# httpd = HTTPServer(("127.0.0.1", 8000), RequestHandler)
# print("Hosting server on port 8000")
# httpd.serve_forever()

# against()
