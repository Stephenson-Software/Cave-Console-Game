import os
import sys

save = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savefile.txt")

#----------------------------------------------------------------
# Art
def cave():
	print("     _ ")
	print("   /   \\")
	print("  / / \\ \\")
	print(" / /   \\ \\")
	
def chest():
	print("  __________")
	print(" |          |")
	print(" |          |")
	print(" |          |")
	
def hole():
	print("    _____")
	print("   /     \\")
	print("  |       |")
	print("   \\     /")
	

#----------------------------------------------------------------
# Decisions
def savegame(decision): #records which decision the player stopped at; returns False if the save file couldn't be written
	try:
		with open(save, 'w') as savefile:
			savefile.write(decision)
	except OSError:
		return False
	return True

def saveandquit(decision):
	if savegame(decision):
		input("\nSaving the game, see you later!\n\nPress Enter to exit the program.")
	else:
		input("\nYour game couldn't be saved, because your save file (savefile.txt beside maincode.py) can't be written. Press Enter to exit the program.")
	sys.exit()

def firstdecision():
	cave()
	print("\nYou come across a cave! Do you want to go inside? YES or NO?")
	
	goinside = input("> ").strip().upper()
		
	if goinside == "YES":
		seconddecision()

	elif goinside == "NO":
		print("\nYou sit outside, staring at the sun until you go blind. You live out the rest of your days like that. Game over.")
		input("\nPress Enter to exit the program.")
		sys.exit()
		
	elif goinside == "SAVE":
		saveandquit("firstdecision") #tells the save file you're at the first decision.
		
	else:
		print("\nThat wasn't an option! Press Enter to exit the program.")
		input("")
		sys.exit()
		
def seconddecision():
	chest()
	print("\nYou find a treasure chest in the cave! Do you want to open it? YES or NO?")
	openchest = input("> ").strip().upper()
		
	if openchest == "YES":
		thirddecision()
		
	elif openchest == "NO":
		print("\nThe chest suddenly grows a face and looks displeased. It eats you. Game over.")
		input("\nPress Enter to exit the program.")
		sys.exit()
		
	elif openchest == "SAVE":
		saveandquit("seconddecision")
	else:
		print("\nThat wasn't an option! Press Enter to exit the program.")
		input("")
		sys.exit()

def thirddecision():
	hole()
	print("\nThere's a hole in the chest that leads further downwards! Do you want to go down it or do you want to leave the cave? DOWN or LEAVE?")
	thirdanswer = input("> ").strip().upper()
	if thirdanswer == "DOWN":
		print("\nAs you begin to descend, the hole tightens around your body, stopping when you can no longer move. You're trapped. Game over.")
		input("\nPress Enter to exit the program.")
		sys.exit()
		
	elif thirdanswer == "LEAVE":
		print("\nScrew this. You exit the cave, drive home, sit on the couch and crack open a Pepsi. No way to get in trouble here!")
		input("\nYou won! Press Enter to exit the program.")
		sys.exit()
		
	elif thirdanswer == "SAVE":
		saveandquit("thirddecision")
	else:
		print("\nThat wasn't an option! Press Enter to exit the program.")
		input("")
		sys.exit()

# ------------------------------------------------------------------
# Actual Gameplay - What the user sees
def main():
	print("\nWelcome to Cave! Do you have a save file? YES or NO?")

	hassavefile = input("> ").strip().upper()

	if hassavefile == "YES":
		if os.path.exists(save):
			try:
				with open(save, 'r') as loadsavefile:
					savefilecontents = loadsavefile.read().strip()
			except (OSError, UnicodeDecodeError):
				savefilecontents = None #the save file is there but can't be opened or decoded, so it's reported as unreadable below
		else:
			savefilecontents = "" #no save file beside maincode.py, so fall through to a new game
	
		if savefilecontents == "firstdecision":
			print("\nOkay! Loading up your save! Type SAVE at any time to SAVE and quit.")
			print("----------\n")
			firstdecision()
		
		elif savefilecontents == "seconddecision":
			print("\nOkay! Loading up your save! Type SAVE at any time to SAVE and quit.")
			print("----------\n")
			seconddecision()

		elif savefilecontents == "thirddecision":
			print("\nOkay! Loading up your save! Type SAVE at any time to SAVE and quit.")
			print("----------\n")
			thirddecision()
		
		elif savefilecontents == "":
			print("\nIt doesn't look like you have a save, so we'll start you at the beginning. Type SAVE at any time to SAVE and quit.")
			print("----------\n")
			firstdecision()
		
		else:
			print("\nYour save file couldn't be read. Answer NO next time to start a new game. Press Enter to exit the program.")
			input("")
			sys.exit()
		

	elif hassavefile == "NO":
		if not savegame(""): #clears any previous save and prepares for saving
			print("\nYour save file (savefile.txt beside maincode.py) can't be written, so saving won't work this game.")
		print("\nEnjoy the game! Type SAVE at any time to SAVE and quit.")
		print("----------\n")
		firstdecision()

	else:
		print("\nThat wasn't an option! Press Enter to exit the program.")
		input("")
		sys.exit()

if __name__ == "__main__":
	try:
		main()
	except (EOFError, KeyboardInterrupt): #input ended (Ctrl-D, or a pipe ran out of answers) or Ctrl-C was pressed, so quit instead of crashing
		print("")
		sys.exit()
