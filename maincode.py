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
def savegame(decision): #records which decision the player stopped at
	savefile = open(save, 'w')
	savefile.write(decision)
	savefile.close()

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
		savegame("firstdecision") #tells the save file you're at the first decision.
		input("\nSaving the game, see you later!\n\nPress Enter to exit the program.")
		sys.exit()
		
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
		savegame("seconddecision")
		input("\nSaving the game, see you later!\n\nPress Enter to exit the program.")
		sys.exit()
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
		savegame("thirddecision")
		input("\nSaving the game, see you later!\n\nPress Enter to exit the program.")
		sys.exit()
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
			loadsavefile = open(save, 'r')
			savefilecontents = loadsavefile.read()
			loadsavefile.close()
		else:
			savefilecontents = "" #no save file beside maincode.py, so fall through to a new game
	
		if savefilecontents == "firstdecision":
			print("\nOkay! Loading up your save!")
			print("----------\n")
			firstdecision()
		
		elif savefilecontents == "seconddecision":
			print("\nOkay! Loading up your save!")
			print("----------\n")
			seconddecision()

		elif savefilecontents == "thirddecision":
			print("\nOkay! Loading up your save!")
			print("----------\n")
			thirddecision()
		
		elif savefilecontents == "":
			print("\nIt doesn't look like you have a save, so we'll start you at the beginning.")
			print("----------\n")
			firstdecision()
		
		else:
			print("\nThat wasn't an option! Press Enter to exit the program.")
			input("")
			sys.exit()
		

	elif hassavefile == "NO":
		newsave = open(save, 'w') #clears any previous save and prepares for saving
		newsave.close()
		print("\nEnjoy the game! Type SAVE at any time to SAVE and quit.")
		print("----------\n")
		firstdecision()

	else:
		print("\nThat wasn't an option! Press Enter to exit the program.")
		input("")
		sys.exit()

if __name__ == "__main__":
	main()
