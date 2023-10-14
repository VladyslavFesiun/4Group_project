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

class Email(Field):
    pass

class Address(Field):
    pass

class Birthday(Field):
    pass


class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthdays = []

    def __str__(self):                  #представлення даних у виглядів рядка
        
        phones_str = ';'.join(str(p) for p in self.phones)
        emails_str = ';'.join(str(e) for e in self.phones)
        addresses_str = ';'.join(str(a) for a in self.phones)
        birthdays_str = ';'.join(str(b) for b in self.phones)

        return f'Contact name: {self.name.value}, phones'  f'Contact name: {self.name.value}, phones: {phones_str},  '\
               f'emails: {emails_str}, addresses: {addresses_str}, birthdays: {birthdays_str}'                           
        

class AddressBook(UserDict):
    
    def add_contact(self, contact):
    
    # Додаємо новий контакт до книги адрес
        self.data[contact.name.value] = contact

    def search_contact(self, search_item):

        # Пошук контакту за рядком пошуку у всіх полях
        found_contacts = []

        for contact in self.data.values():
            if (
                search_item.lower() in contact.name.value.lower() or
                any(search_item.lower() in str(phone).lower() for phone in contact.phones) or
                any(search_item.lower() in str(email).lower() for email in contact.emails) or
                any(search_item.lower() in str(address).lower() for address in contact.addresses) or
                any(search_item.lower() in str(birthday).lower() for birthday in contact.birthdays)
            ):
                found_contacts.append(contact)
        return found_contacts
    

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

        result_for_search_note = "".join(input_your_command[0:11])
        note_text = " ".join(input_divided[1::])
        note_text_search=  " ".join(input_divided[2::])

        print(note_text)
        print(note_text_search)

        if result_for_search_note in all_commands:
            all_commands[result_for_search_note]()
            
        elif split_command in all_commands:
            all_commands[split_command]()
            
        elif input_your_command() in all_commands:
            all_commands[input_your_command.lower()]()
            
        else:
            print("Invalid command. Use 'hello', 'add', 'change', 'phone', 'show all', 'good bye', 'close', or 'exit'")

        

if __name__ == '__main__':
    main()
