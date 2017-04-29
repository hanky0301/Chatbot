import sys
import os
import pickle

# ] file is reverse
# ] every movie end conversation is gone

def readFile(fin):
	with open(fin) as file:
		content = file.read()
	lines = content.splitlines()	
	return lines

def writeFile(fout, data):
	f = open(fout, 'w')
	f.truncate()
	for line in data:
		f.write(line + '\n')
	f.close()
	print ('create : ' + fout)
	return

def readPickle(fin):
	with open(fin, 'rb') as file:
		data = pickle.load(file)
	return data

def writePickle(fout, data):
	with open(fout, 'wb') as file:
		pickle.dump(data, file)
	return

def divideValid(conversationPairs, cur_path):
	trainX = [] 
	trainY = []
	validX = []
	validY = []
	fout_train_X = os.path.join(cur_path, 'train.en')
	fout_train_Y = os.path.join(cur_path, 'train.es')
	fout_valid_X = os.path.join(cur_path, 'valid.en')
	fout_valid_Y = os.path.join(cur_path, 'valid.es')
	
	train_size = len(conversationPairs) * 9  / 10

	# training data
	for pair in conversationPairs[:train_size]:
		trainX.append(pair[0])
		trainY.append(pair[1])
	# validation data
	for pair in conversationPairs[train_size:]:
		validX.append(pair[0])
		validY.append(pair[1])

	writeFile(fout_train_X, trainX)
	writeFile(fout_train_Y, trainY)
	writeFile(fout_valid_X, validX)
	writeFile(fout_valid_Y, validY)	
	return

def parseField(datas):
	fieldData = [0] * len(datas)
	for i, data in enumerate(datas):
		tmps = data.split('+++$+++')
		# print("a + " + str(i))
			
		for idx in range(len(tmps)):
			if idx == 0 or idx == 1 or idx == 2:
				# print('a : ' + data)
				tmps[idx] = int(tmps[idx].strip()[1:])
			else:
				tmps[idx] = tmps[idx].strip();
		fieldData[i] = tmps
		
	return fieldData

def seperateMovie(fieldData):

	dicts = {}
	# cnt = 0
	start_idx = 0
	chunk_len = 0
	for idx in range(len(fieldData) - 1):
		chunk_len += 1
		if idx == len(fieldData) - 2:
			if fieldData[ idx ][2] != fieldData[ idx + 1 ][2]:
				dicts[fieldData[ idx ][2]] = fieldData[start_idx : start_idx + chunk_len]
				dicts[fieldData[ idx + 1][2]] = fieldData[idx + 1 :]
			else:
				dicts[fieldData[ idx ][2]] = fieldData[start_idx :]
			continue
		if fieldData[ idx ][2] != fieldData[ idx + 1 ][2]:
			# print start_idx, chunk_len, cnt
			dicts[fieldData[ idx ][2]] = fieldData[start_idx : start_idx + chunk_len]
			start_idx = idx + 1 	
			chunk_len = 0
			# cnt += 1
	for idx in dicts:
		dicts[idx].reverse()

	return dicts

def chunkConversation(fieldDataMovies):
	conversationsPair = []
	speakerPair = []
	for movieIdx in fieldDataMovies:
		MovieDict = {}
		conversation_cnt = 0
		start_idx = 0
		chunk_len = 0
		# print (fieldDataMovies[movieIdx])
		for lineIdx in range(len(fieldDataMovies[movieIdx]) - 1):
			chunk_len += 1
			if lineIdx == len(fieldDataMovies[movieIdx]) - 2:
				if fieldDataMovies[movieIdx][lineIdx][0] != fieldDataMovies[movieIdx][lineIdx + 1][0] - 1:
					MovieDict[conversation_cnt] = fieldDataMovies[movieIdx][start_idx : start_idx + chunk_len]
					MovieDict[conversation_cnt + 1] = fieldDataMovies[movieIdx][lineIdx + 1 :]
				else:
					MovieDict[conversation_cnt] = fieldDataMovies[movieIdx][start_idx :]
				continue
			if fieldDataMovies[movieIdx][lineIdx][0] != fieldDataMovies[movieIdx][lineIdx + 1][0] - 1:
				# cut
				MovieDict[conversation_cnt] = fieldDataMovies[movieIdx][start_idx : start_idx + chunk_len]
				start_idx = lineIdx + 1
				chunk_len = 0
				conversation_cnt += 1
				
		for conversationIdx in MovieDict:
			# list of one conversation
			sentences = []
			speaker = []
			sent = ''
			for lineIdx in range(len(MovieDict[conversationIdx]) - 1):
				sent += MovieDict[conversationIdx][lineIdx][4] + ' '
				if lineIdx == len(MovieDict[conversationIdx]) - 2:
					if MovieDict[conversationIdx][lineIdx][3] != MovieDict[conversationIdx][lineIdx + 1][3]:
						sentences.append(sent)
						speaker.append(MovieDict[conversationIdx][lineIdx][3])
						sentences.append(MovieDict[conversationIdx][lineIdx + 1][4])
						speaker.append(MovieDict[conversationIdx][lineIdx + 1][3])
					
					else:
						sent += MovieDict[conversationIdx][lineIdx + 1][4] + ' '
						sentences.append(sent)
						speaker.append(MovieDict[conversationIdx][lineIdx][3])
					continue	

				if MovieDict[conversationIdx][lineIdx][3] != MovieDict[conversationIdx][lineIdx + 1][3]:
					sentences.append(sent)	
					speaker.append(MovieDict[conversationIdx][lineIdx][3])
					sent = ''
				# ] the last line missing
			for idx in range(len(sentences) - 1):
				conversationsPair.append([sentences[idx], sentences[idx + 1]])
				speakerPair.append([speaker[idx], speaker[idx + 1]])
	return conversationsPair, speakerPair

def preprocess(lines):
	fieldData = parseField(lines)
	fieldDataMovies = seperateMovie(fieldData)
	conversationPairs, speakerPairs = chunkConversation(fieldDataMovies)
	return conversationPairs, speakerPairs

def main(fin, fout, cur_path):
	
	fin = os.path.join(cur_path, fin)
	fout = os.path.join(cur_path, fout)

	lines = readFile(fin)
	if not os.path.exists(fout):
		conversationPairs = preprocess(lines)
		writePickle(fout, conversationPairs)
	conversationPairs = readPickle(fout)
	
	divideValid(conversationPairs, cur_path)

	# print(len(conversationPairs))
	return

if __name__ == "__main__":

	cur_path = sys.argv[1]
	fin = 'movie_lines.txt'
	fout = 'dialoguePair.pkl'

	main(fin, fout, cur_path)


