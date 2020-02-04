#!/usr/bin/env python3
# PhraseTrain | A command line interface (CLI) language phrase training program

import os     # path, name, environ, system (Windows), listdir, mkdir, remove
import sys    # terminal clear & title setting under *nix
import random # randint()
import copy   # deepcopy()

# Constants
choices = """
   L - Load a previous phrase list
   C - Create a new phrase list
   Q - Quit the program
"""
save_path = "PhraseTrain"

# Runtime vars
is_window_host = (os.name == "nt")
has_unsaved_changes = False
phrase_list_name = ""
domestic_language = ""
foreign_language = ""
phrases = {}

# Functions
def clear_vars():
	global has_unsaved_changes, phrase_list_name, domestic_language, foreign_language, phrases, current_phrases

	has_unsaved_changes = False
	phrase_list_name = ""
	domestic_language = ""
	foreign_language = ""
	phrases = {}
	current_phrases = {}

def clear_screen():
	if is_window_host:
		os.system("cls")
	else:
		sys.stdout.write("\033[H\033[2J") # Clear the terminal
		sys.stdout.write("\033[3J")       # Clear old buffer

def set_title(new_title: str):
	if is_window_host:
		os.system(f'title "{new_title}"')
	else:
		sys.stdout.write(f"\x1b]2;{new_title}\x07") # Set title

def prompt(text: str):
	print(text, end = "")
	return input().strip()

def read_lines(file_path: str):
	try:
		lines = []
		with open(file_path, "r") as file:
			lines = file.readlines()
		return lines
	except:
		return []

def write_text(file_path: str, content: str):
	try:
		with open(file_path, "w+") as file:
			file.write(content)
		return True
	except:
		return False

def set_header(title_text: str):
	clear_screen()
	header_text = "PhraseTrain"
	if title_text != "":
		header_text += f" | {title_text}"
	print(header_text)
	print("-" * len(header_text))
	set_title(header_text)

def create_list():
	global phrase_list_name, domestic_language, foreign_language

	clear_vars()
	set_header("Create a new phrase list")

	# Set phrase_list_name & create empty file
	phrases_file = ""
	while True:
		try:
			print("\nWhat is the name for the new phrase list?")
			phrase_list_name = prompt("Name >> ")
			if phrase_list_name == "":
				return

			phrases_file = f"{save_path}/{phrase_list_name}.txt"
			if os.path.exists(phrases_file):
				print("\nWarning: The specified list already exists. Should it be overwritten?")
				choice = prompt("Choice (y/N) >> ").upper()
				if choice != "Y":
					print("Please specify another name!")
					continue
			if write_text(phrases_file, ""):
				break
			else:
				print("Phrase list name is invalid; try using less special characters!")
		except:
			print("Phrase list name is invalid; try using less special characters!")

	print("\nWhat is the domestic (source) language of this list (e.g. English)?")
	domestic_language = prompt("Language >> ")

	print("\nWhat is the foreign (target) language of this list (e.g. Russian)?")
	foreign_language = prompt("Language >> ")

	write_text(phrases_file, f"{domestic_language}:{foreign_language}")

def add_phrase(domestic_phrase: str, foreign_phrase: str):
	global phrases, has_unsaved_changes

	phrases[domestic_phrase] = foreign_phrase
	if not has_unsaved_changes:
		has_unsaved_changes = True

def remove_phrase(domestic_phrase_match: str):
	global has_unsaved_changes

	try:
		del phrases[domestic_phrase_match]
		if not has_unsaved_changes:
			has_unsaved_changes = True
		return True
	except KeyError:
		return False

def modify_phrase(domestic_phrase_match: str, foreign_phrase: str, previous_domestic_phrase_match = ""):
	global has_unsaved_changes

	try:
		# Update foreign phrase
		if previous_domestic_phrase_match == "":
			phrases[domestic_phrase_match] = foreign_phrase

		# Update domestic phrase
		else:
			del phrases[previous_domestic_phrase_match]
			add_phrase(domestic_phrase_match, foreign_phrase)

		if not has_unsaved_changes:
			has_unsaved_changes = True
		return True
	except KeyError:
		return False

def parse_phrases_file(phrases_file: str):
	global phrase_list_name, domestic_language, foreign_language, has_unsaved_changes

	ln = 1
	try:
		lines = read_lines(phrases_file)
		for line in lines:
			line = line.strip()
			if line != "" and ":" in line and not line.startswith("#"):
				if ln == 1:
					domestic_language, foreign_language = line.split(":")
				else:
					domestic_phrase, foreign_phrase = line.split(":")
					add_phrase(domestic_phrase, foreign_phrase)
				ln += 1
		phrase_list_name = os.path.splitext(os.path.basename(phrases_file))[0]
		has_unsaved_changes = False
	except:
		clear_vars()
		print(f'Error: Could not parse phrase list "{phrases_file}"; please check line {ln} for syntax errors!\n')
		print("Press enter to continue...", end = "")
		input()

def load_list():
	clear_vars()
	set_header("Load a previous phrase list")

	files = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path, f)) and f.endswith(".txt")]
	num = 1
	if len(files) == 0:
		print("\n   Uh oh, there are no phrase lists to load; please go create one from the main menu!\n")
		print("Press enter to continue...", end = "")
		input()
		return

	for file in files:
		print("\n   {0}. {1}".format(num, file[0:file.rfind(".")]), end = "")
		num += 1
	print()

	# Select file by number
	phrases_file = choice = ""
	while True:
		try:
			print("\nWhich phrase list to load?")
			choice = prompt(f"Number (1-{str(num - 1)}) >> ")
			if choice == "":
				return
			choice = int(choice) - 1
			phrases_file = f"{save_path}/{files[choice]}"
			break
		except:
			print(f"Error: '{choice}' is not an option in the list; please select the phrase list by number!")

	# Attempt parsing chosen file
	parse_phrases_file(phrases_file)

def save_list():
	global has_unsaved_changes

	if has_unsaved_changes:
		try:
			phrases_file = f"{save_path}/{phrase_list_name}.txt"
			content = f"{domestic_language}:{foreign_language}"
			for domestic_phrase in phrases:
				foreign_phrase = phrases[domestic_phrase]
				content += f"\n{domestic_phrase}:{foreign_phrase}"
			write_text(phrases_file, content)
			has_unsaved_changes = False
		except:
			print(f"Error: Could not save the phrase list '{phrase_list_name}'!")

def unsaved_changes_prompt():
	print(f'\nYou have unsaved changes in the phrase list "{phrase_list_name}", would you like to save?')
	choice = prompt("Choice (y/N) >> ").upper()
	if choice == "Y":
		save_list()

def add_phrase_prompt():
	set_header(f"Add a phrase to '{phrase_list_name}'")

	while True:
		print("\nWhat is the new domestic phrase you would like to add?")
		domestic_phrase = prompt(f"{domestic_language} phrase >> ")
		if domestic_phrase == "":
			return

		if domestic_phrase in phrases:
			print("\nWarning: The specified phrase already exists in the list. Should it be overwritten?")
			choice = prompt("Choice (y/N) >> ").upper()
			if choice != "Y":
				print("Please specify another domestic phrase!")
				continue
		break

	print("\nWhat is the foreign phrase for this new domestic phrase?")
	foreign_phrase = prompt(f"{foreign_language} phrase >> ")
	if foreign_phrase == "":
		return

	add_phrase(domestic_phrase, foreign_phrase)

def modify_phrase_prompt(domestic_phrase: str):
	while True:
		set_header(f"Modify a phrase in '{phrase_list_name}'")
		foreign_phrase = phrases[domestic_phrase]
		index = list(phrases).index(domestic_phrase) + 1
		print(f"\n   {index}. {domestic_phrase} -> {foreign_phrase}")

		print("\n   B - Back", end = "")
		print(f"\n   D - Change the domestic ({domestic_language}) phrase", end = "")
		print(f"\n   F - Change the foreign ({foreign_language}) phrase", end = "")
		print("\n   R - Remove this phrase from the list", end = "")
		print("\n")

		print("What would you like to do to this phrase?")
		choice = prompt(f"Choice >> ").upper()
		if choice == "B" or choice == "":
			break
		elif choice == "D":
			print(f'\nWhat is the new domestic phrase for "{foreign_phrase}"?')
			new_domestic_phrase = prompt(f"New {domestic_language} phrase >> ")
			if new_domestic_phrase == "":
				continue
			modify_phrase(new_domestic_phrase, foreign_phrase, domestic_phrase)
			domestic_phrase = new_domestic_phrase
		elif choice == "F":
			print(f'\nWhat is the new foreign phrase for "{domestic_phrase}"?')
			new_foreign_phrase = prompt(f"New {foreign_language} phrase >> ")
			if new_foreign_phrase == "":
				continue
			modify_phrase(domestic_phrase, new_foreign_phrase)
		elif choice == "R":
			remove_phrase(domestic_phrase)
			break

def modify_list():
	while True:
		set_header(f"Modify '{phrase_list_name}' ({domestic_language} -> {foreign_language})")

		if len(phrases) == 0:
			print("\n   There are no phrases in this list yet, go ahead and add a few!")
		else:
			num = 1
			for domestic_phrase in phrases:
				foreign_phrase = phrases[domestic_phrase]
				print("\n   {0}. {1} -> {2}".format(num, domestic_phrase, foreign_phrase), end = "")
				num += 1
			print("")

		print("\n   A - Add a new phrase", end = "")
		print("\n   B - Back", end = "")
		print("\n")

		print("Select a phrase by number, or action by letter.")
		choice = prompt("Choice >> ").upper()

		if choice == "A":
			add_phrase_prompt()
		elif choice == "B":
			break
		else:
			if len(phrases) > 0:
				try:
					choice = int(choice) - 1
					domestic_phrase = list(phrases)[choice]
					modify_phrase_prompt(domestic_phrase)
				except ValueError:
					pass

def switch_phrase_languages(current_phrases: dict):
	global domestic_language, foreign_language

	new_phrases = {}
	for domestic_phrase in current_phrases:
		foreign_phrase = current_phrases[domestic_phrase]
		new_phrases[foreign_phrase] = domestic_phrase

	last_domestic_language = domestic_language
	domestic_language = foreign_language
	foreign_language = last_domestic_language
	return new_phrases

def practice_done(score: int, num_phrases: int, problem_phrases: dict, last_domestic_language: str, last_foreign_language: str):
	global domestic_language, foreign_language

	# Reset list default languages
	domestic_language = last_domestic_language
	foreign_language = last_foreign_language

	set_header(f"'{phrase_list_name}' ({domestic_language} -> {foreign_language})")
	print(f"\n   Your final score: {score}/{num_phrases} ({int(score / num_phrases * 100)}%)")

	if len(problem_phrases) > 0:
		print(f"\n   You should study the following phrases more:")
		for problem_phrase in problem_phrases:
			problem_phrase_ans = problem_phrases[problem_phrase]
			if not problem_phrase in list(phrases.keys()):
				problem_phrase_prev = problem_phrase
				problem_phrase = problem_phrase_ans
				problem_phrase_ans = problem_phrase_prev
			print("\n   {0} -> {1}".format(problem_phrase, problem_phrase_ans), end = "")
	else:
		compliments = [ "Amazing", "Awesome", "Breathtaking", "Impressive", "Spectacular", "Good", "Great" ]
		random.shuffle(compliments)
		print(f"\n   {compliments[0]} job!", end = "")

	print("\n\nPress enter to continue...", end = "")
	input()

def practice_loop(num_phrases: int, current_phrases: dict, random_first_phrases: bool, start_with_foreign: bool, last_domestic_language: str, last_foreign_language: str):
	# Keep track of score and problematic phrases
	score = 0
	max_score = 0
	problem_phrases = {}

	while len(current_phrases) > 0:
		# Swap starting phrase languages randomly with a chance of 1 in 3 (33%)
		if random_first_phrases and random.randint(1, 3) == 2:
			current_phrases = switch_phrase_languages(current_phrases)
			start_with_foreign = not start_with_foreign

		set_header(f"'{phrase_list_name}' ({domestic_language} -> {foreign_language})")

		max_score = num_phrases - len(current_phrases)
		if max_score > 0:
			print(f"\n   Your current score: {score}/{num_phrases} ({int(score / max_score * 100)}%)")

		# Get answer to one of the phrase pairs
		current_phrase = list(current_phrases.keys())[0]
		current_phrase_ans = current_phrases.pop(current_phrase)
		print(f'\n{max_score + 1}. What is "{current_phrase}" in {foreign_language}?')
		ans = prompt(f"Phrase in {foreign_language} >> ")
		if ans == current_phrase_ans:
			score += 1
		else:
			problem_phrases[current_phrase] = current_phrase_ans
			print("\nIncorrect!")
			print(f"\nYour answer:    {ans}")
			print(f"Correct answer: {current_phrase_ans}")
			print("\nPress enter to continue...", end = "")
			input()

	# We're done here, show the results!
	practice_done(score, num_phrases, problem_phrases, last_domestic_language, last_foreign_language)

def practice_setup(num_phrases: int, random_first_phrases: bool, start_with_foreign: bool):
	global domestic_language, foreign_language

	# Get ready
	last_domestic_language = domestic_language
	last_foreign_language = foreign_language
	current_phrases = copy.deepcopy(phrases)

	# Randomize & trim phrase count
	rand_keys = list(current_phrases.keys())
	random.shuffle(rand_keys)
	rand_dict = {}
	for i in range(num_phrases):
		key = rand_keys[i]
		rand_dict[key] = current_phrases[key]
	current_phrases = rand_dict

	# Swap phrases if starting with foreign phrases
	if start_with_foreign:
		current_phrases = switch_phrase_languages(current_phrases)

	practice_loop(num_phrases, current_phrases, random_first_phrases, start_with_foreign, last_domestic_language, last_foreign_language)

def practice_questions():
	set_header(f"Setup practice for '{phrase_list_name}' ({domestic_language} -> {foreign_language})")

	# Num of phrases
	num_phrases = 1
	while True:
		choice = ""
		try:
			print("\nHow many phrases should get asked?")
			choice = prompt(f"Number (1-{str(len(phrases))}) >> ")
			if choice == "":
				return
			num_phrases = int(choice)
			if num_phrases < 1 or num_phrases > len(phrases):
				raise ValueError
			break
		except ValueError:
			print(f"Error: '{choice}' is not a valid number; make sure it's within the range 1-{str(len(phrases))}!")

	# Randomized first phrases
	random_first_phrases = True
	print("\nWould you like randomized initial phrases (e.g. which language phrase gets asked)?")
	choice = prompt("Choice (Y/n) >> ").upper()
	if choice != "" and choice != "Y":
		random_first_phrases = False

	start_with_foreign = False
	if not random_first_phrases:
		print(f"\nLanguages:\n\n   1. {domestic_language}\n   2. {foreign_language}")
		while True:
			choice = ""
			try:
				print("\nWhich language would you like to get initial phrases for?")
				choice = prompt(f"Number (1-2) >> ")
				if choice == "":
					raise ValueError
				num_initial_lang = int(choice)
				if num_initial_lang == 2:
					start_with_foreign = True
				break
			except ValueError:
				print(f"Error: '{choice}' is not a valid number; make sure it's within the range 1-2!")

	practice_setup(num_phrases, random_first_phrases, start_with_foreign)

# First run
if not os.path.exists(save_path):
	os.mkdir(save_path)

# Main program loop
while True:
	set_header(phrase_list_name + ("*" if has_unsaved_changes else ""))
	valid_choices = ["L", "C", "Q"]

	# List options
	if phrase_list_name != "":
		if len(phrases) > 0:
			print("\n   P - Practice the chosen list", end = "")
			valid_choices.append("P")
			pass
		print("\n   M - Modify the current list", end = "")
		print("\n   S - Save the current list", end = "")
		print("\n   R - Remove the current list", end = "")
		valid_choices.extend(["M", "S", "R"])
	print(choices)

	print("What would you like to do?")
	choice = prompt("Choice >> ").upper()

	if choice in valid_choices:
		if choice == "P":
			practice_questions()
		elif choice == "M":
			modify_list()
		elif choice == "S":
			save_list()
		elif choice == "R":
			print(f'\nDo you really wish to remove the phrase list "{phrase_list_name}"?')
			choice = prompt("Choice (y/N) >> ").upper()
			if choice == "Y":
				phrases_file = f"{save_path}/{phrase_list_name}.txt"
				os.remove(phrases_file)
				clear_vars()
		elif choice == "L":
			if has_unsaved_changes:
				unsaved_changes_prompt()
			load_list()
		elif choice == "C":
			if has_unsaved_changes:
				unsaved_changes_prompt()
			create_list()
		elif choice == "Q":
			if has_unsaved_changes:
				unsaved_changes_prompt()
			clear_screen()
			exit()
