import os
import json
import numpy as np
import argparse
from pprint import pprint

from preprocess_cornell import preprocess
# from preprocess_cornell import parseField, seperateMovie, chunkConversation, preprocess

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputCorpus', type=str, help='which corpus to parse')
args = parser.parse_args()

root_dir = '../'
data_dir = os.path.join(root_dir, 'data')
output_dir = os.path.join(data_dir, args.inputCorpus + "_clean")

train = {
	'en'		: None,
	'es'		: None,
	'speaker'	: None,
	'addressee'	: None
}

valid = {
	'en'		: None,
	'es'		: None,
	'speaker'	: None,
	'addressee'	: None
}

fout_train = {
	'en'		: os.path.join(output_dir, 'train.en'),
	'es'		: os.path.join(output_dir, 'train.es'),
	'speaker'	: os.path.join(output_dir, 'train.speaker'),
	'addressee'	: os.path.join(output_dir, 'train.addressee')
}

fout_valid = {
	'en'		: os.path.join(output_dir, 'valid.en'),
	'es'		: os.path.join(output_dir, 'valid.es'),
	'speaker'	: os.path.join(output_dir, 'valid.speaker'),
	'addressee'	: os.path.join(output_dir, 'valid.addressee')	
}

if not os.path.exists(output_dir):
	os.mkdir(output_dir)

def writeFile(datas, fout):
	f = open(fout, 'w')
	f.truncate()
	for data in datas:
		# print (data.encode('utf-8'))
		if args.inputCorpus == 'friends':
			f.write(data.encode('utf-8') + '\n')
		elif args.inputCorpus == 'cornell': 
			f.write(data + '\n')
		else:
			print 'unecpected input data'
			break
	f.close()
	return 

def divideVal(dialogues, speakers):
	# dialogues = np.array(dialogues)
	# speakers = np.array(speakers)
	en = np.array([])
	es = np.array([])
	speaker = np.array([])
	addressee = np.array([])
	# print(len(dialogues))
	for idx in range(len(dialogues)):
		# print(dialogues[idx][:-1])
		en = np.concatenate((en, dialogues[idx][:-1]), axis=0)
		es = np.concatenate((es, dialogues[idx][1:]), axis=0)
		speaker =  np.concatenate((speaker, speakers[idx][:-1]), axis=0)
		addressee = np.concatenate((addressee, speakers[idx][1:]), axis=0)
		# print (dialogues[idx])
		if idx % 100 == 99:
			print ('process dialogue: ' + str(idx + 1))

	return en, es, speaker, addressee

def divideValCornell(dialogues, speakers):
	dialogues = np.array(dialogues)
	speakers = np.array(speakers)
	en = dialogues[:, 0]
	es = dialogues[:, 1]
	speaker = speakers[:, 0]
	addressee = speakers[:, 1]

	return en, es, speaker, addressee

def getFriendsDialog(data):
	tmp_enes = []
	tmp_speaker = []
	en_es = []
	speaker = []
	# pprint(data[:20])
	# print(data[:10])
	for idx, dicts in enumerate(data):
		if 'line' in dicts and 'Previously on Friends.' in dicts['line']:
			# print( "i am here " + dicts['line'])
			continue
		if 'break' in dicts:
			if len(tmp_enes) != 0 and len(tmp_speaker) != 0:
				# print(' append : ' + tmp_enes + ' ' + tmp_speaker)
				en_es.append(tmp_enes)
				speaker.append(tmp_speaker)	
			# print (tmp_enes)
			# print('~~~~~~~~~~~')
			# print (tmp_speaker)
			tmp_enes = []
			tmp_speaker = []
			

		if 'role' in dicts and dicts['line'] != '':
			# print('in : ' + dicts['line'])
			tmp_enes.append(dicts['line'].replace('\u0092', '\''))
			tmp_speaker.append(dicts['role'].replace(':', '')) 	
			
		if idx == len(data) - 1:
			en_es.append(tmp_enes)
			speaker.append(tmp_speaker)	
	return en_es, speaker

def getCornellDialog(data):
	print('cornell size = ' + str(len(data)))
	# print(data[:20])

	conversationPairs, speakerPairs = preprocess(data)
	return conversationPairs, speakerPairs

def writeOutput(train, valid):
	print('writing data...')
	
	# pprint(train_en[:10])
	for key in train:
		if len(train[key]) != 0 and len(valid[key]) != 0:
			writeFile(train[key], fout_train[key])
			writeFile(valid[key], fout_valid[key])
		else:
			print('output file with key :' + key + ' is empty')
	return

def main():
	if args.inputCorpus == 'friends':
		source_file = os.path.join(data_dir, 'friends.json')
		with open(source_file) as file:
			data = json.load(file)
		en_es, speaker = getFriendsDialog(data)
		
		print('dividing...')
		train['en'], train['es'], train['speaker'], train['addressee'] = divideVal(en_es[:int(len(en_es) * 9 / 10)], speaker[:int(len(en_es) * 9 / 10)])
		valid['en'], valid['es'], valid['speaker'], valid['addressee'] = divideVal(en_es[int(len(en_es) * 9 / 10):], speaker[int(len(en_es) * 9 / 10):])
		
		writeOutput(train, valid)

	elif args.inputCorpus == 'cornell':
		source_file = os.path.join(data_dir, 'movie_lines.txt')
		with open(source_file) as file:
			data = file.read()
		en_es, speaker = getCornellDialog(data.splitlines())
		train['en'], train['es'], train['speaker'], train['addressee'] = divideValCornell(en_es[:int(len(en_es) * 9 / 10)], speaker[:int(len(en_es) * 9 / 10)])
		valid['en'], valid['es'], valid['speaker'], valid['addressee'] = divideValCornell(en_es[int(len(en_es) * 9 / 10):], speaker[int(len(en_es) * 9 / 10):])
		
		writeOutput(train, valid)
	else:
		print('unexpected dataset, you can try friends or cornell') 
		return
	
	
			
	
	return 

if __name__ == "__main__":
	main()