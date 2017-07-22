import os
import sys
from random import shuffle

data_dir = sys.argv[1]


with open(os.path.join(data_dir, 'train.txt'), 'r') as f:
    X_train = []
    tags_train = []
    intent_train = []
    lines = f.readlines()
    shuffle(lines)

    for line in lines:
        words = line.rstrip('\n').split()
        X_train.append(' '.join(words[1 : words.index('EOS')]))
        intent_train.append(words[-1])
        tags_train.append(' '.join(words[words.index('O') + 1 : -1]))

with open(os.path.join(data_dir, 'tmp.txt'), 'r') as f:
    X_test = []
    for line in f:
        words = line.rstrip('\n').split()
        X_test.append(' '.join(words[1 : words.index('EOS')]))

with open(os.path.join(data_dir, 'train/train.seq.in'), 'w') as f:
    for line in X_train:
        f.write(line + '\n')
 
with open(os.path.join(data_dir, 'train/train.seq.out'), 'w') as f:
    for line in tags_train:
        f.write(line + '\n')

with open(os.path.join(data_dir, 'train/train.label'), 'w') as f:
    for line in intent_train:
        f.write(line + '\n')

with open(os.path.join(data_dir, 'valid/valid.seq.in'), 'w') as f:
    for line in X_train[:1000]:
        f.write(line + '\n')
 
with open(os.path.join(data_dir, 'valid/valid.seq.out'), 'w') as f:
    for line in tags_train[:1000]:
        f.write(line + '\n')

with open(os.path.join(data_dir, 'valid/valid.label'), 'w') as f:
    for line in intent_train[:1000]:
        f.write(line + '\n')

with open(os.path.join(data_dir, 'test/test.seq.in'), 'w') as f:
    for line in X_test:
        f.write(line + '\n')

with open(os.path.join(data_dir, 'test/test.seq.out'), 'w') as f:
    for line in X_test:
        Os = []
        for word in line.split():
            Os.append('O')
        f.write(' '.join(Os) + '\n')

with open(os.path.join(data_dir, 'test/test.label'), 'w') as f:
    for line in X_test:
        f.write('request_course' + '\n')
