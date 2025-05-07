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
languageList = notes + octaves + symbols + list(durations.keys()) + accidentals + [" "]

def charInLanguage(inputString):
	for char in inputString:
		if char not in languageList: print(char, "\t NOT IN LANGUAGE\n"); return False
	else: return True

def stringInMusicLang(inputString):
	state="S"
	stack="$"

	if not charInLanguage(inputString): return False

	for char in inputString:
		if char == " ": continue
		print("Char:\t",char)
		print("Stack:\t", stack)
		print("State\t", state)
		print()

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
				stack=""

		elif state=="N":
			if char not in accidentals and char not in octaves: return False
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

	print(f"\033[31mFinal state: {state}\nFinal stack: {stack}\n\033[0m")
	return state == "F"


# Test cases
tests = [
	("A4q B4q C5q D5q | E5h F5h ⊥",     True),  # Two full bars
	("_hG3h|F#3hG3h ⊥",                 True),  # Rest and notes, 4/4 each
	("D#5hEb5h|F5w ⊥",                  True),  # Mixed accidentals
	("_s _s _s _s _q _e _e _q | C4w ⊥",             True),  # Rests and whole note
	("G4e A4e B4e C5e D5h ⊥",        True),  # Eighth notes
	("Bb3Q C3Q D3q ⊥",                  True),  # Two dotted quarter notes and a quarter note
	("A4q B4q C#4q D4q E4q ⊥",             False),
	("C4w|G4q ⊥",                      False),
	("A4q|B4q",                        False),
	("F4z|G4q ⊥",                      False),
	("_|C4q ⊥",                        False),
	("A4Q|B4Q | ⊥",                   False),
]

for idx, (sequence, expected) in enumerate(tests, start=1):
	print(f"\033[34mASSERTION #{idx}\033[0m")
	assert stringInMusicLang(sequence) == expected

print("\033[36mPASSED ALL TESTS!\033[0m 🎉")