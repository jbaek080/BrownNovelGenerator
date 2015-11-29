import random

class Story:
	def __init__(self):
		#self.agent = self.get_name()
		self.tag_to_words = {}
		self.read()
		with open("output.txt", "w") as o:
			o.write(self.generate(100))
		
		
	def generate(self, d):
		n = ""
		for _ in range(d):
			sentence = [item for sublist in self.write() for item in sublist]
			for word in sentence:
				n += word + " "
			n = n.strip()
			n += ". "
		return n
			
	def read(self):
		# tags = {
		# #"DET": ("ABL", "ABN", "ABX", "AP", "AP$", "AP+AP", "AT", "CD", "CD&", "DT",\
		# #"DT$", "DT+BEZ", "DT+MD", "DTI", "DTS", "DTS+BEZ", "DTX", "OD", "PN",\
		# #"PN$", "PN+BEZ", "PN+HVD", "PN+HVZ", "PN+MD", "PP$"),
		# "DET":("AT"),
		# "V":("BE", "BED", "BED*", "BEDZ", "BEDZ*", "BEG", "BEM", "BEM*", "BEN", "BER",\
		# "BER*", "BEZ", "DO", "DO*", "DO+PPSS", "DOD", "DOD*", "DOZ", "DOZ*", "HV", \
		# "HV*", "HV+TO", "HVD", "HVD*", "HVG", "HVN", "HVZ", "HVZ*", "VB"),
		# "ADV": ("RB"),
		# "CC" :("CC"),
		# "SV" : ("CS"),
		# "EX" : ("EX", "EX+BEZ", "EX+HVD", "EX+MD"),
		# "NP" : ("NP", "NP$", "NP+BEZ", "NP+HVZ", "NP+MD", "NPS", "NPS$", "NR", \
		# "NR$", "NR+MD", "NRS"),
		# #"N": ("NN", "NN$", "NN+BEZ", "NN+HVD", "NN+HBZ", "NN+IN", "NN+MD", "NN+NN",\
		# #"NNS", "NNS$", "NNS+MD", "PP$$", "PPL", "PPLS", "PPO", "PPS", "PPS+BEZ"),
		# "N":("NN"),
		# #"P": ("IN", "IN+IN", "IN+PPO"),
		# "P":("IN"),
		# "MD": ("MD", "MD*", "MD+HV", "MD+PPSS", "MD+TO"),
		# "ADJ": ("JJ", "JJ$", "JJ+JJ", "JJR", "JJR+CS", "JJS", "JJT")
		# }
		tags = {
		"DET":("AT", "DT"), "V":("VB"), "ADV":("RB"), "SV":("CS"), "NP":("NP"), "N":("NN"), "P":("IN"), "ADJ":("JJ")
		}
		for tag_set in tags:
			self.tag_to_words[tag_set] = set()
		with open("corpus.txt") as f:
			num = 0
			for line in f:
				num += 1
				if num < 20000 or num > 21000:
					continue
				words = line.split(" ")
				for word in words:
					w = word.split("_")
					if len(word) < 2:
						continue
					raw = w[0]
					tag = w[1]
					for tag_set, tag_specific in tags.items():
						if tag in tag_specific:
							self.tag_to_words[tag_set].add(raw)
	
	def write(self):
		s = self.expand("S")
		e = 1
		while True:
			prevs = s
			# for w in s:
				# if random.random() < e:
					# i = s.index(w)
					# s[i] = self.expand(w)
			s = [self.expand(w) if random.random() < e else w for w in s ]
			s = self.flatten_to_strings(s)
			e /= 1.5
			if s == prevs:
				break
		s = self.flatten_to_strings(s)
		#print(s)
		return [random.sample(self.tag_to_words[w], 1) for w in s if w in self.tag_to_words]
	
	def flatten_to_strings(self, listOfLists):
		"""Flatten a list of (lists of (lists of strings)) for any level 
		of nesting"""
		result = []

		for i in listOfLists:
			# Only append if i is a basestring (superclass of string)
			if isinstance(i, str):
				result.append(i)
			# Otherwise call this function recursively
			else:
				result.extend(self.flatten_to_strings(i))
		return result
				
	def expand(self, phrase):
		SENTENCE = "S"
		NP = "NP"
		VP = "VP"
		ADJ = "ADJ"
		N = "N"
		PP = "PP"
		DET = "DET"
		ADV = "ADV"
		TV = "V"
		DTV = "V"
		SV = "SV"
		S = "S"
		P = "P"
		if phrase == SENTENCE:
			return [NP, VP]
		elif phrase == NP:
			return [DET, N]
		elif phrase == N:
			r = random.random()
			if r < 1/2:
				return [ADJ, N]
			else:
				return [N, PP]
		elif phrase == VP:
			r = random.random()
			if r < 1/4:
				return [VP, ADV]
			elif r < 2/4:
				return [TV, NP]
			elif r < 3/4:
				return [DTV, NP, NP]
			else:
				return [SV, S]
		elif phrase == PP:
			return [P, NP]
		return phrase
		
if __name__ == "__main__":
	s = Story()