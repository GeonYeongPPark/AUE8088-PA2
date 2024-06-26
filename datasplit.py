import os
import random
data_file = 'datasets/kaist-rgbt/train-all-04.txt'
# train_file = 'datasets/kaist-rgbt/train.txt'
# val_file = 'datasets/kaist-rgbt/val.txt'

train_file = 'datasets/kaist-rgbt/train_random.txt'
val_file = 'datasets/kaist-rgbt/val_random.txt'

with open(data_file, 'r') as f:
    lines = f.readlines()
# random.shuffle(lines) # random train/val

total_size = len(lines)
train_size = int(total_size * 0.8)
val_size = total_size - train_size

train_lines = lines[:train_size]
val_lines = lines[train_size:]

with open(train_file, 'w') as f:
    f.writelines(train_lines)

with open(val_file, 'w') as f:
    f.writelines(val_lines)