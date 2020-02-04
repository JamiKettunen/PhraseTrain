# PhraseTrain
🎌 A command line interface (CLI) language phrase training program written in Python.

### Main menu
```
PhraseTrain | Test
------------------

   P - Practice the chosen list
   M - Modify the current list
   S - Save the current list
   R - Remove the current list
   L - Load a previous phrase list
   C - Create a new phrase list
   Q - Quit the program

What would you like to do?
Choice >> m
```

### Modify your phrase lists
```
PhraseTrain | Modify 'Test' (English -> Russian)
------------------------------------------------

   1. monday -> понедельник
   2. tuesday -> вторник
   3. wednesday -> среда
   4. thursday -> Четверг
   5. friday -> пятница

   A - Add a new phrase
   B - Back

Select a phrase by number, or action by letter.
Choice >> b
```

### Customize your practice session
```
PhraseTrain | Setup practice for 'Test' (English -> Russian)
------------------------------------------------------------

How many phrases should get asked?
Number (1-5) >> 5

Would you like randomized initial phrases (e.g. which language phrase gets asked)?
Choice (Y/n) >> n

Languages:

   1. English
   2. Russian

Which language would you like to get initial phrases for?
Number (1-2) >> 1
```

### Learn from your mistakes
```
PhraseTrain | 'Test' (English -> Russian)
-----------------------------------------

   Your current score: 3/5 (100%)

4. What is "friday" in Russian?
Phrase in Russian >> пятнице

Incorrect!

Your answer:    пятнице
Correct answer: пятница

Press enter to continue...
```

### Know how to improve
```
PhraseTrain | 'Test' (English -> Russian)
-----------------------------------------

   Your final score: 3/5 (60%)

   You should study the following phrases more:

   friday -> пятница
   monday -> понедельник

Press enter to continue...
```
