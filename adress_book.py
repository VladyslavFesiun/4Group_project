from collections import UserDict, UserList


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    pass

class NoteBook(UserList):
    def add_record(self, notes):
        self.data.append(notes)

class Notes():
    #dict_of_notes = NoteBook()
    def __init__(self, note):
        self.note = note

def save_note(list_of_notes, note:Notes):
    dict_of_notes = dict()
    dict_of_notes["note"] = note.note
    print(dict_of_notes)
    list_of_notes.append(dict_of_notes)
    print (f"Note '{note.note}' has been added.")

def add_note(list_of_notes, note):
    print(note)
    new_note = Notes(note)
    save_note(list_of_notes, new_note)

def search_notes(list_of_notes, search_match):
    res = "Notes: \n"
    for i in list_of_notes:
        if (search_match in i["note"]):
            res += str(i) + "\n"
    return res

def handle_requirement(req):
    split_command = ''
    for char in req:
        if char != ' ':
            split_command += char.lower()
        else:
            break
    return split_command

def split_req(req):
    return req.split(maxsplit=3)

def main():

    list_of_notes = NoteBook()

    def add_note_func():
        if len(input_divided) > 1: 
            add_note(list_of_notes, note_text)
        else:
            print("write note.")
        

    def search_note_func():
        if len(input_divided) > 1: 
            print(search_notes(list_of_notes, note_text_search))
        else:
            print("write note.")

    all_commands = {
            "note": add_note_func,
            "search note": search_note_func,
        }
    
    while True:

        input_your_command = input(f'Write your command: ')
        input_divided = split_req(input_your_command)
        split_command = handle_requirement(input_your_command)

        note_text = " ".join(input_divided[1::])
        note_text_search=  " ".join(input_divided[2::])

        print(note_text)
        print(note_text_search)

        if split_command in all_commands:
            all_commands[split_command]()
            
        elif input_your_command() in all_commands:
            all_commands[input_your_command.lower()]()
            
        else:
            print("Invalid command. Use 'hello', 'add', 'change', 'phone', 'show all', 'good bye', 'close', or 'exit'")

        

if __name__ == '__main__':
    main()