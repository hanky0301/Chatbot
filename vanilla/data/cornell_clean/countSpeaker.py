fileList = ['train.speaker', 'train.addressee', 'valid.speaker', 'valid.addressee']


speakers = []
for fin in fileList:
	with open(fin) as file:
		content = file.read()
	curSpeaker = content.splitlines()
	for curS in curSpeaker:
		if curS not in speakers:
			speakers.append(curS)
print len(speakers)
	



