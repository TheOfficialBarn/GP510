# machine.py
# GP 510
# Collaborators: Aiden, Liam, Sam
# Project: Formal Music Language
# Due: May 9th (Stop Day) @ Midnight



notes = ["A","B","C","D","E","F","G","_"]
octaves = [str(i) for i in range(9)]
durations = {
	"s": 2,  "S": 3,
	"e": 4,  "E": 6,
	"q": 8,  "Q": 12,
	"h": 16, "H": 24,
	"w": 32
}
symbols = ["|","⊥"]
accidentals = ["b","#"]

# one mega‐list
languageList = notes + octaves + symbols + list(durations.keys()) + accidentals

def charInLanguage(inputString):
	for char in inputString:
		print(char)
		if char not in languageList: return False
	else: return True

def stringInMusicLang(inputString):
	state="S"
	stack="$"

	if not charInLanguage(inputString): return False

	for char in inputString:
		print(char)

		if state=="S":
			if char not in notes and char not in symbols: return False

			# Notes
			elif char == notes[-1]: state="D"
			elif char in notes[:-1]: state = "N"
			
			# Symbols
			elif char == symbols[0] and stack=="$"+"X"*32:
				stack = "$"
				state="S"
			elif char == symbols[1] and stack=="$"+"X"*32:
				state="F"

		elif state=="N":
			if char not in accidentals and accidentals not in octaves: return False
			elif char in accidentals: state = "A"
			elif char in octaves: state = "D"

		elif state=="A":
			if char not in octaves: return False
			state = "D"

		elif state=="D":
			if char not in durations: return False
			else: 
				stack+="X"*durations[char]
				state = "S"

		elif state=="F":
			return False
		else:
			print("Wut happened")

	return True


def main():
	# inputString = input("Type in your input")
	inputString = "Ab4H_q⊥"
	print(stringInMusicLang(inputString))

main()