from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F
import numpy as np
import json
import matplotlib

#___________________Libraries for the progress bar_____________________
import time
from progressbar import ProgressBar

#_________________initialize the device______________________________
