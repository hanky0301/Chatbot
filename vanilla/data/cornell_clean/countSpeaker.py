fileList = ['train.speaker', 'train.addressee', 'valid.speaker', 'valid.addressee']


speakers = []
for fin in fileList:
	with open(fin) as file:
		content = file.read()
	fout = fin + ".new"
	f = open(fout, "w")
	f.truncate()
	curSpeaker = content.splitlines()
	for curS in curSpeaker:
		curS = curS.replace(" ", "_")
		f.write(curS + "\n")
		if curS not in speakers:
			speakers.append(curS)
	f.close()
print len(speakers)
	



