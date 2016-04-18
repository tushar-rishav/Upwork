# -*- coding: utf-8 -*-


def passToShip(name: str, health: int, intel: int, output: int):
	"""
	Criteria to board ship

	1.	If their intelligence is above 90 or their economic output is above 85, 
		they must be permitted to board the with a message indicating they meet
		the “exceptional” criteria.
	2.	If their health, intelligence, and economic output are all above 60, 
		they must be permitted to board the ship with a message congratulating
		them.
	3.	In all other cases, they should not be permitted to board the ship, 
		and a message must be displayed that apologises for this.
	:param name:
		The name of the person.
	:param health:
		The health, an integer between 0 and 100.
	:param intel:
		Intelligence, an integer between 0 and 100; and,
	:param output:
		Economic output, an integer between 0 and 100.
	:returns:
		A suitable message informing if the person is allowed to board the ship.
	"""
	if intel > 90 or output > 85:
		return "You're allowed to board the ship. You meet the exceptional criteria"
	elif health > 60 and intel > 60 and output > 60:
		return "Congratulations! You're allowed to board the ship."
	else:
		return "Sadly, you won't board the ship. Accept our sincere apologises."

def main():
	name = input(">Name: ")
	health = int(input(">Health (an int between 0 and 100): "))
	intel = int(input(">Intelligence (an int between 0 and 100): "))
	output = int(input(">Economic output (an int between 0 and 100): "))
	result = passToShip(name, health, intel, output)
	print("{}".format(result))
	
if __name__ == "__main__":
	main()