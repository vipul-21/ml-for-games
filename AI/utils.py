import numpy as np
import torch
from collections import namedtuple, defaultdict
import matplotlib
import matplotlib.pyplot as plt
Experience = namedtuple('Experience', ('state', 'action', 'next_state', 'reward'))

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

    # feature_space.extend(inital_st[4])
    # feature_space.extend(one_hot_encode(inital_st[5], 1, 5)[0])
    # print(feature_space)
    # print(len(feature_space))
    return feature_space








def plot_training(rates, performance):
    # plotting the points
    plt.plot(rates, performance, color='green', linestyle='solid', linewidth=3)

    # naming the x axis
    plt.xlabel('Explore')
    # naming the y axis
    plt.ylabel('Ghostbuster Wins- Ghost Wins')
    plt.xlim(1, 0)
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
    plt.ylabel('Ghostbuster Wins- Ghost Wins ')

    # giving a title to my graph
    plt.title('Testing')

    # function to show the plot
    plt.show()


