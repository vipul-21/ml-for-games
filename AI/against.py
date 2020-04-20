
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
from strategy.epsilon_greedy import *
from utils import plot_testing
def against():
    model_ghostbuster = torch.load('ghostbuster.pth')
    model_ghostbuster.eval()
    model_ghost = torch.load('ghost.pth')
    model_ghost.eval()


    eps_start = 1
    eps_end = 0.01
    eps_decay = 0.001
    memory_size = 100000  # check with paper
    num_episodes = 200  # 1000

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # start_state = [118, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    # start_state = [154, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]
    start_state = [118, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]

    start_feature = generate_feature_space(start_state)

    em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])

    #Ghost_Buster
    strategy_ghostbuster = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)
    agent_ghostbuster = Agent(strategy_ghostbuster, em.num_actions_available(), device)


    #Ghost
    strategy_ghost = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)
    agent_ghost = Agent_ghost(strategy_ghost, em.num_actions_available(), device)


    policy_net_ghost = model_ghost
    policy_net_ghostbuster = model_ghostbuster
    ghost_win = 0
    busters_win = 0
    performance = []
    game_number = []
    for episode in range(num_episodes):
        # reset the environment
        em = Environment(start_state[0], start_state[1], start_state[2], start_state[3])
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
            # print('Move to take', action)

            reward = em.take_action_against(action_ghost, choices_ghost,action_ghostbuster, choices_ghostbuster, timestep)
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