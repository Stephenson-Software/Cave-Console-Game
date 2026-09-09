import os

save = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savefile.txt")

#----------------------------------------------------------------
# Art
def cave():
	print "     _ "
	print "   /   \\"
	print "  / / \\ \\"
	print " / /   \\ \\"
	
def chest():
	print "  __________"
	print " |          |"
	print " |          |"
	print " |          |"
	
def hole():
	print "    _____"
	print "   /     \\"
	print "  |       |"
	print "   \\     /"
	

#----------------------------------------------------------------
# Decisions
def savegame(decision): #records which decision the player stopped at
	savefile = open(save, 'w')
	savefile.write(decision)
	savefile.close()

def firstdecision():
	cave()
	print "\nYou come across a cave! Do you want to go inside? YES or NO?"
	
	goinside = raw_input("> ")
		
	if goinside == "YES":
		seconddecision()

	elif goinside == "NO":
		print "\nYou sit outside, staring at the sun until you go blind. You live out the rest of your days like that. Game over."
		raw_input("\nPress Enter to exit the program.")
		exit()
		
	elif goinside == "SAVE":
		savegame("firstdecision") #tells the save file you're at the first decision.
		raw_input("\nSaving the game, see you later!\n\nPress Enter to exit the program.")
		quit()
		
	else:
		print "\nThat wasn't an option! Press Enter to exit the program."
		raw_input("")
		quit()
		
def seconddecision():
	chest()
	print "\nYou find a treasure chest in the cave! Do you want to open it? YES or NO?"
	openchest = raw_input("> ")
		
	if openchest == "YES":
		thirddecision()
		
	elif openchest == "NO":
		print "\nThe chest suddenly grows a face and looks displeased. It eats you. Game over."
		raw_input("\nPress Enter to exit the program.")
		exit()
		
	elif openchest == "SAVE":
		savegame("seconddecision")
		raw_input("\nSaving the game, see you later!\n\nPress Enter to exit the program.")
		quit()
	else:
		print "\nThat wasn't an option! Press Enter to exit the program."
		raw_input("")
		quit()

def thirddecision():
	hole()
	print "\nThere's a hole in the chest that leads further downwards! Do you want to go down it or do you want to leave the cave? DOWN or LEAVE?"
	thirdanswer = raw_input("> ")
	if thirdanswer == "DOWN":
		print "\nAs you begin to descend, the hole tightens around your body, stopping when you can no longer move. You're trapped. Game over."
		raw_input("\nPress Enter to exit the program.")
		exit()
		
	elif thirdanswer == "LEAVE":
		print "\nScrew this. You exit the cave, drive home, sit on the couch and crack open a Pepsi. No way to get in trouble here!"
		raw_input("\nYou won! Press Enter to exit the program.")
		exit()
		
	elif thirdanswer == "SAVE":
		savegame("thirddecision")
		raw_input("\nSaving the game, see you later!\n\nPress Enter to exit the program.")
		quit()
	else:
		print "\nThat wasn't an option! Press Enter to exit the program."
		raw_input("")
		quit()

# ------------------------------------------------------------------
# Actual Gameplay - What the user sees
print "\nWelcome to Cave! Do you have a save file? YES or NO?"

hassavefile = raw_input("> ")

if hassavefile == "YES":
	if os.path.exists(save):
		loadsavefile = open(save, 'r')
		savefilecontents = loadsavefile.read()
		loadsavefile.close()
	else:
		savefilecontents = "" #no save file beside maincode.py, so fall through to a new game
	
	if savefilecontents == "firstdecision":
		print "\nOkay! Loading up your save!"
		print "----------\n"
		firstdecision()
		
	elif savefilecontents == "seconddecision":
		print "\nOkay! Loading up your save!"
		print "----------\n"
		seconddecision()

	elif savefilecontents == "thirddecision":
		print "\nOkay! Loading up your save!"
		print "----------\n"
		thirddecision()
		
	elif savefilecontents == "":
		print "\nIt doesn't look like you have a save, so we'll start you at the beginning."
		print "----------\n"
		firstdecision()
		
	else:
		print "\nThat wasn't an option! Press Enter to exit the program."
		raw_input("")
		quit()
		

elif hassavefile == "NO":
	newsave = open(save, 'w') #clears any previous save and prepares for saving
	newsave.close()
	print "\nEnjoy the game! Type SAVE at any time to SAVE and quit."
	print "----------\n"
	firstdecision()

else:
		print "\nThat wasn't an option! Press Enter to exit the program."
		raw_input("")
		quit()