import os
import sys

data_dir = sys.argv[1]

def parse_test():
    slot_dicts = []
    with open(os.path.join(data_dir, 'test.txt'), 'r') as f:
        lines = f.readlines()
    
    with open(os.path.join(data_dir, 'test.en'), 'w') as f:
        for line in lines:
            x = []
            slot_value = {}
            x.append(line[:line.find('(')])
            slot_strs = line[line.find('(') + 1 : line.find(')')].split(';')
            for s in slot_strs:
                if '=' in s:
                    x.append('_' + s.split('=')[0])
                    slot_value['_' + s.split('=')[0]] = s.split('=')[1].strip('\'')
                else:
                    x.append(s)

            slot_dicts.append(slot_value)
            f.write(' '.join(x) + '\n')
    
    return slot_dicts


def fill_slots(slot_dicts):
    with open(sys.argv[5], 'r') as f:
        lines = f.readlines()

    with open(sys.argv[5], 'w') as f:
        for line, slot_value in zip(lines, slot_dicts):
            for slot in slot_value:
                line = line.replace(slot, slot_value[slot])
            f.write(line)


slot_dicts = parse_test()
if sys.argv[3] == 'True':
    fill_slots(slot_dicts)
