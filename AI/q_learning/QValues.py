import torch

class QValues():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    @staticmethod
    def get_current(policy_net, states, actions):
        filter_action= []
        # for val in actions:
        #     if val.item() > -1:
        #         filter_action.append(val)
        v = policy_net(states).gather(dim=1, index=actions)
        return torch.mean(v, dim=1)
        # return v.gather(dim=1, index=actions.unsqueeze(-1))
    @staticmethod
    def get_next(target_net, next_states):
        a = next_states
        b = a.max(dim=1)[0]
        final_state_locations = b.eq(0).type(torch.bool)
        non_final_state_locations = (final_state_locations == False)
        non_final_states = next_states[non_final_state_locations]
        batch_size = next_states.shape[0]
        values = torch.zeros(batch_size).to(QValues.device)
        values[non_final_state_locations] = target_net(non_final_states).max(dim=1)[0].detach()
        return values