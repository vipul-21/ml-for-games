from collections import defaultdict
import random
import torch

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
            action = []
            choices = []
            for val in possible_moves:
                if len(val) > 0:
                    curr= random.choice(val)
                    action.append(curr[0])
                    choices.append(curr[1])
                else:
                    action.append(-1)
                    choices.append("")

            # action = random.choice(possible_moves)  # pick a possible out of the available ones - change
            return torch.tensor(action).to(self.device), rate, choices  # TODO - model action tensor

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
                possible_moves_type = []
                chosen_mode = []
                for first in possible_moves:
                    possible_moves_indexes.append([])
                    possible_moves_type.append([])
                    for val in first:
                        possible_moves_indexes[-1].append(val[0])
                        possible_moves_type[-1].append(val[1])
                all_actions = []
                choices = []
                for i, gb in enumerate(possible_moves):
                    if gb != -1:
                        max_value = float('-inf')
                        max_index = -1
                        for index, value in enumerate(returned_states):
                            if (index in possible_moves_indexes[i] and value > max_value):
                        # chosen_mode = possible_moves_type[possible_moves_indexes.index(index)]
                                max_value = value
                                max_index = index
                        all_actions.append(max_index)
                        if max_index > -1:
                            choices.append(possible_moves_type[i][possible_moves_indexes[i].index(max_index)])
                        else:
                            choices.append("")

                    else:
                        all_actions.append(-1)
                        choices.append("")
                # result = policy_net(state).argmax(dim=-1).to(self.device)
                # print ('RESULT', max_index_tensor)
            return torch.tensor(all_actions).to(self.device), rate, choices
                # return policy_net(torch.tensor(state)).argmax(dim=1).to(self.device) # exploit


    def select_action_testing(self, state, policy_net, possible_moves):
        action = []
        choices = []
        with torch.no_grad():
            # print(policy_net(state))
            returned_states = policy_net(state)
            max_value = float("-inf")
            max_index = 0
            # print("POSSIBLE MOVES: ", possible_moves)
            possible_moves_indexes = []
            possible_moves_type = []
            chosen_mode = []
            for first in possible_moves:
                possible_moves_indexes.append([])
                possible_moves_type.append([])
                for val in first:
                    possible_moves_indexes[-1].append(val[0])
                    possible_moves_type[-1].append(val[1])
            all_actions = []
            # for index, value in enumerate(returned_states):
            #     if (index in possible_moves_indexes and value > max_value):
            #         chosen_mode = possible_moves_type[possible_moves_indexes.index(index)]
            #         max_value = value
            #         max_index = index
            # max_index_tensor = torch.tensor(max_index)
            for i, gb in enumerate(possible_moves):
                if gb != -1:
                    max_value = float('-inf')
                    max_index = -1
                    for index, value in enumerate(returned_states):
                        if (index in possible_moves_indexes[i] and value > max_value):
                            # chosen_mode = possible_moves_type[possible_moves_indexes.index(index)]
                            max_value = value
                            max_index = index
                    all_actions.append(max_index)
                    if max_index > -1:
                        choices.append(possible_moves_type[i][possible_moves_indexes[i].index(max_index)])
                    else:
                        choices.append("")

                else:
                    all_actions.append(-1)
                    choices.append("")
            return torch.tensor(all_actions).to(self.device), choices
                # return policy_net(torch.tensor(state)).argmax(dim=1).to(self.device) # exploit



