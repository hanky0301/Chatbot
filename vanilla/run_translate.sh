#! /bin/bash

cp -f $1 data/translation/test.en

python src/translate.py --decode --data_dir data/translation --train_dir model/translation --output_file $2 --size=256 
