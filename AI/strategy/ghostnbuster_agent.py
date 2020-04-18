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
                for i in possible_moves:
                    possible_moves_indexes.append(i[0])
                    possible_moves_type.append(i[1])

                for index, value in enumerate(returned_states):
                    if (index in possible_moves_indexes and value > max_value):
                        # chosen_mode = possible_moves_type[possible_moves_indexes.index(index)]
                        max_value = value
                        max_index = index
                max_index_tensor = torch.tensor(max_index).to(self.device)
                # result = policy_net(state).argmax(dim=-1).to(self.device)
                # print ('RESULT', max_index_tensor)
                return max_index_tensor, rate, chosen_mode
                # return policy_net(torch.tensor(state)).argmax(dim=1).to(self.device) # exploit

    def select(self):
        res_state_loc = []
        res_state_resources = self.ghostbuster_resources

        for count, det in enumerate(self.ghostbuster_positions):
            moves = self.board[int(det)]
            min_dist_node = -1
            min_dist_val = float("inf")

            for move in moves:
                val = self.getdistance(self.ghost_posititon_avail, move[0])

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



