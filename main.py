from getkey import getkey
from rich.console import Console
from rich.markdown import Markdown
import os
from datetime import datetime

console = Console()

print("CLI Notes")

def list_notes():
    "Lists all notes"
    notes = []
    console.print('Notes: ')
    for file in os.listdir():
        if file.endswith('.clinote'):
            note = file.split('.')[0]
            console.print(note)

def add_note():
    "Adds a note"
    note_name = input('Type the name of your note or leave it empty for a default name: ')
    if note_name == "":
        note_name = str(datetime.now()) + '.clinote'
    else:
        if '.clinote' not in note_name:
            note_name += '.clinote'
    console.print(f"{note_name} made. You may type the contents of it as you wish:")
    with open(note_name,'w') as new_note:
        print("You may enter as many lines as you want. When you are done, enter: \"COMPLETE_NOTE\"")
        new_line = input("Enter a new line: ")
        while new_line != "COMPLETE_NOTE":
            new_line = input("Enter a new line: ")
            new_note.write(new_line + "\n")
    print("Note saved successfully! Press any key to continue.")

def edit_note():
    "Edits a note"
    note_name = input('Type the name of your note to edit: ')
    while note_name == "":
        note_name = input('Please type the name of your note: ')
    if '.clinote' not in note_name:
        note_name += '.clinote'
    console.print(f"{note_name} will be edited. Here is the contents of the note:")
    keep_editing = 'y'
    while keep_editing == 'y':
        view_note(note_name,True)
        line_no = 1
        target_line_no = int(input('Enter the line number you want to edit: '))
        with open(note_name + ".temp_new_note", 'w') as new_note:
            with open(note_name, 'r') as old_note:
                for line in old_note:
                    if line_no == target_line_no:
                        console.print(f"Old line content: {line}")
                        console.print("Enter what you would like this line to be replaced with below: ")
                        new_content = input()
                        new_note.write(new_content + "\n")
                    else:
                        new_note.write(line)
                    line_no += 1
        os.rename(note_name + ".temp_new_note", note_name)
        console.print(f"Note saved successfully! Would you like to keep editing? (y/n)")
        keep_editing = getkey()
    print("Note saved successfully! Press any key to continue.")

def delete_note():
    "Deletes an existing note"
    note_name = input('Type the name of your note: ')
    while note_name == "":
        note_name = input('Please type the name of your note: ')
    else:
        if '.clinote' not in note_name:
            note_name += '.clinote'
    console.print(f"{note_name} will be deleted. Are you sure you want to continue? (y/n)")
    selection = getkey()
    if selection == 'n':
        return
    else:
        try:
            os.remove(note_name)
            console.print(f"{note_name} has successfully been deleted.")
        except Exception as e:
            console.print(f"Could not delete \"{note_name}\".")
            console.print(f"Error: {e}")



def view_note(note_name=None,show_lines=False):
    "Outputs the contents of a note"
    if note_name == None:
        note_name = input('Type the name of the note to view it: ')
    if '.clinote' not in note_name:
            note_name += '.clinote'
    with open(note_name, 'r') as note:
        line_no = 1
        for line in note:
            md = Markdown(line)
            if show_lines:
                content = f"{line_no}. {md.markup}".strip('\n')
            else:
                content = md
            console.print(content)
            line_no += 1

class Action():
    command: str
    description: str
    rel_fn: None

    def __init__(self,command,description,rel_fn):
        self.command = command
        self.description = description
        self.rel_fn = rel_fn
    
    def perform_action(self):
        self.rel_fn()

# list of possible actions
actions = [
    Action('l','List notes',list_notes),
    Action('n','Add a new note',add_note),
    Action('d','Delete an existing note',delete_note),
    Action('e','Edit an existing note',edit_note),
    Action('v','View an existing note',view_note),
    Action('q','Quit program',exit)
]

def perform_action(selection):
    "Core function that performs an action given user input"
    for action in actions:
        if action.command == selection:
            action.perform_action()

while True:
    console.print("-----------------------------------------------")
    for action in actions:
        console.print(f"{action.command} - {action.description}")

    console.print("Select an action: ")
    selection = getkey()
    perform_action(selection)