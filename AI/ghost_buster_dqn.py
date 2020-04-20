import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class DQN(nn.Module): ## Different
    def __init__(self):
        super().__init__()
        self.ll1 = nn.Linear(1211, 708)
        self.ll2 = nn.Linear(708, 708)
        self.ll3 = nn.Linear(708, 354)
        self.ll4 = nn.Linear(354, 354)
        self.oll = nn.Linear(354, 200)  #
        # self.ll1 = nn.Linear(1210, 716)
        # self.ll2 = nn.Linear(716, 716)
        # self.ll3 = nn.Linear(716, 358)
        # self.ll4 = nn.Linear(358, 358)
        # self.oll = nn.Linear(358, 275)  # changed from 16 to 200, - too large a reduction , will reducing in steps.

    # function implements a forward pass to the network
    def forward(self, x):
        # x = x.flatten(start_dim=1) - flattening needed only for images
        x = F.relu(self.ll1(x))
        x = F.relu(self.ll2(x))
        x = F.relu(self.ll3(x))
        x = F.relu(self.ll4(x))
        x = F.softmax(self.oll(x))
        return x
