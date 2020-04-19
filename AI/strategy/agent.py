from collections import defaultdict
import random
import torch

class Agent_ghost():
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
            return torch.tensor(action[0]).to(self.device), rate, action[1]  # TODO - model action tensor

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
                for i in possible_moves:
                    possible_moves_indexes.append(i[0])
                    possible_moves_type.append(i[1])

                for index, value in enumerate(returned_states):
                    if (index in possible_moves_indexes and value > max_value):
                        chosen_mode = possible_moves_type[possible_moves_indexes.index(index)]
                        max_value = value
                        max_index = index
                max_index_tensor = torch.tensor(max_index).to(self.device)
                # result = policy_net(state).argmax(dim=-1).to(self.device)
                # print ('RESULT', max_index_tensor)
                return max_index_tensor, rate, chosen_mode
                # return policy_net(torch.tensor(state)).argmax(dim=1).to(self.device) # exploit

    def select_action_testing(self, state, policy_net, possible_moves):
        with torch.no_grad():
            # print(policy_net(state))
            returned_states = policy_net(state)
            max_value = float("-inf")
            max_index = 0
            # print("POSSIBLE MOVES: ", possible_moves)
            possible_moves_indexes = []
            possible_moves_type = []
            chosen_mode = []
            for i in possible_moves:
                possible_moves_indexes.append(i[0])
                possible_moves_type.append(i[1])

            for index, value in enumerate(returned_states):
                if (index in possible_moves_indexes and value > max_value):
                    chosen_mode = possible_moves_type[possible_moves_indexes.index(index)]
                    max_value = value
                    max_index = index
            max_index_tensor = torch.tensor(max_index)
            # print(chosen_mode)

            # print ('Result',max_index_tensor)
            return max_index_tensor,chosen_mode
            # return policy_net(torch.tensor(state)).argmax(dim=1).to(self.device) # exploit



