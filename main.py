from getkey import getkey

print("CLI Notes")

class Action():
    command: str
    description: str
    rel_fn: function

    def __init__(self,command,description,rel_fn):
        self.command = command
        self.description = description
        self.rel_fn = rel_fn
    
    def perform_action(self):
        self.rel_fn()

actions = [
    Action('l','List notes'),
    Action('n','Add a new note'),
    Action('d','Delete an existing note'),
    Action('e','Edit an existing note')
]

def perform_action(selection):
    for action in actions:
        if action.command == selection:
            print(action.perform_action)


for action in actions:
    print(f"{action.command} - {action.description}")

print("Select an action: ")
selection = getkey()
perform_action(selection)