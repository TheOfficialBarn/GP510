# machine.py
# GP 510
# Collaborators: Aiden, Liam, Sam
# Project: Formal Music Language
# Due: May 9th (Stop Day) @ Midnight


# Below is a list of notes, octaves, durations with their respective beat count, symbols, and accidentals
# _ represents a rest
# | represents the end of a measure
# ⊥ represents the end of a music piece
# For non-music people, an accidental is a half-step pitch adjuster. (e.g. b lowers a pitch a half step & # raises a pitch a half step)
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

# This is a list of every possible char a string could have to be in the language 
languageList = notes + octaves + symbols + list(durations.keys()) + accidentals + [" "]

# If we have a char that is not in languageList, we know difinitively that the string is not in the language
def charInLanguage(inputString):
	for char in inputString:
		if char not in languageList: print(char, "\t NOT IN LANGUAGE\n"); return False
	else: return True

# Below accept an inputString and returns a Bool based on if it is in the language or not
def stringInMusicLang(inputString):


	state="S" # The current state. state var is initialized with the starting state, S
	stack="$" # The stack (idk why I used a string instead of a list, but... it works)

	# Easy test to see if a string isn't in the language
	if not charInLanguage(inputString): return False

	# Let's go through each char, and follow the state transitions/stack updates
	# To see if we end up in the final state with an empty stack
	for char in inputString:

		# For this language, spaces are allowed anywhere and generally do nothing
		# They are purely cosmetic and can help with legibility.
		if char == " ": continue

		# Debugging
		print("Char:\t",char)
		print("Stack:\t", stack)
		print("State\t", state)
		print()

		# Below is where we follow the state transitions
		if state=="S":
			if char not in notes and char not in symbols: return False

			# Notes
			elif char == notes[-1]: state="D" # Char is rest note "_"
			elif char in notes[:-1]: state = "N" # Char is A-G
			
			# Symbols
			elif char == symbols[0] and stack=="$"+"X"*32:
				stack = "$"
				state="S"
			elif char == symbols[1] and stack=="$"+"X"*32:
				state="F"
				stack=""

		elif state=="N":
			if char not in accidentals and char not in octaves: return False # Accidentals allowed
			elif char in accidentals: state = "A"
			elif char in octaves: state = "D"

		elif state=="A": # This state prevents multiple accidentals
			if char not in octaves: return False
			state = "D"

		elif state=="D":
			if char not in durations: return False
			else: 
				stack+="X"*durations[char] # Add X's to the stack (amount of X's pushed corresponds to the duration of the char)
				state = "S" # Loop back to the starting state

		elif state=="F": # Final State!!
			return False # If you end up here, a char was added after "⊥", which is not allowed
		else: # For debugging incase an unexpected state was somehow reached
			print("Wut happened")

	# Debugging (prints the final state and final stack in color 🌈)
	print(f"\033[31mFinal state: {state}\nFinal stack: {stack}\n\033[0m")
	
	# If you end up here, that means the string is in the language and successfully ended at state "F"
	# Optionally, we could add a check here that ensures the stack is empty, however this check is 
	# already enforced during the transition from state "S" to state "F"
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