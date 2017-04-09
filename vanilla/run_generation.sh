#! /bin/bash

cp -f $1 data/nlg/test.txt

python src/parse_nlg.py data/nlg --fill_slots False

python src/translate.py --decode --data_dir data/nlg --train_dir model/nlg --output_file $2 --num_layers=2 --size=256 

python src/parse_nlg.py data/nlg --fill_slots True --output_file $2
