from collections import UserDict
import pickle
import re
import difflib
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

class Field:
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value 

class Name(Field):
    pass
    pass
    pass

class Phone(Field):
     
    @Field.value.setter
    def value(self, value):
        if not re.match(r'^\+\d{12}$', value):
            raise ValueError("Incorrect phone number format, should be +380638108107.")
        if not value.isnumeric():
            raise ValueError('Invalid phone number format.')
        self._value = value

class Email(Field):
    @Field.value.setter
    def value(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Invalid email format.")
        self._value = value

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

    def save_addressbook(self):
        with open("addressbook.bin", "wb") as f:
            pickle.dump(self.data, f)

    def load_notebook(self, file):
        with open(file, "rb") as f:
            self.data = pickle.load(f)
    

class NoteBook(UserDict):
    # Потрібно для створення унікального неймінгу кожної нотатки
    def __init__(self):
        super().__init__()
        self.__id = 1

    def add_note(self, notes):
        # Додавання нотатки в записник
        if len(notes) >= 1:
            self.data[f"note-{self.__id}"] = Notes(notes)
            self.__id += 1
        else:
            print("Note is empty!")
    
    def search_notes(self, search_match):
        if len(search_match) >= 1:
            # print(self.data['note-1'])
            res = "Note "
            for value in self.data.values():
                # print(type(str(value)))
                # print(str(value))
                if (search_match in str(value)):
                    res += str(value) + ""
                    print(f'{res} is found')

    def add_tag(self, text):
        # Звернення йде шляхом вводу імені нотатки і введення тегу для цієї нотатки.
        # Якщо після введеня імені нотатки не буде вказаний тег, функція поверне відповідне повідомлення.
        name_of_note = text.split(" ")[0]
        tag_to_add = text.removeprefix(name_of_note).strip()
        print(tag_to_add)
        if len(name_of_note) >= 1 and len(tag_to_add) >= 1:
            for key, value in self.data.items():
                if key == name_of_note:
                    if tag_to_add not in self.data[name_of_note].tags:
                        return self.data[name_of_note].tags.append(tag_to_add)
                    else:
                        print(f"This tag is already entered for this note!")
            return print(f"{name_of_note} was not found in NoteBook")
        elif len(name_of_note) == 0:
            print("Enter name of note to add tag!")
        elif len(tag_to_add) == 0:
            print("Tag is empty!")

    def edit_note(self, text):
        name_of_note = text.split(" ")[0]
        new_note_text = text.removeprefix(name_of_note).strip()
        if len(name_of_note) >= 1 and len(new_note_text) >= 1:
            for key, value in self.data.items():
                if key == name_of_note:
                    self.data[name_of_note].note = new_note_text
                    return print(f'{name_of_note} edited!')
            return print(f"{new_note_text} was not found in NoteBook")
        elif len(name_of_note) == 0:
            print(f'Enter name of note to edit!')
        elif len(new_note_text) == 0:
            print(f"Enter new text for {name_of_note}")

    def delete_note(self, note_name):
        if len(note_name) >= 1:
            for key, value in self.data.items():
                if key == note_name:
                    return self.data.pop(note_name)
            return print(f"{note_name} was not found in NoteBook")
        else:
            print("Enter name of note to delete")

    def save_notebook(self):
        with open("notebook.bin", "wb") as f:
            pickle.dump((self.data, self.__id), f)

    def load_notebook(self, file):
        with open(file, "rb") as f:
            info_from_file = pickle.load(f)
            self.data = info_from_file[0]
            self.__id = info_from_file[1]

    def show_notebook(self):
        for name, note in self.data.items():
            print(f"{name}: {note}")

class Notes():
    def __init__(self, note):
        self.note = note
        self.tags = []

    def __str__(self):
        if len(self.tags) == 0:
            return f'{self.note}'
        else:
            return f'{self.note} | Tags are: {self.tags}'
        

def main():
    try:
        contact_book = AddressBook()
        contact_book.load_notebook("addressbook.bin")
    except FileNotFoundError:
        contact_book = AddressBook()

    try:
        list_of_notes = NoteBook()
        list_of_notes.load_notebook("notebook.bin")
    except FileNotFoundError:
        list_of_notes = NoteBook()

    # def search_note_func():
    #     if len(text_after_command) > 1:
    #         print(search_notes(list_of_notes, text_after_command))
    #     else:
    #         print("You haven`t entered text to search.")

    all_commands = {
            # General commands
            "hello": lambda: print("Hi! To get commands list print 'info'."),
            "hi": lambda: print("Hi! To get commands list print 'info'."),
            "good bye": lambda: print("Good bye!"),
            "close": lambda: print("Good bye!"),
            "exit": lambda: print("Good bye!"),
            "info": lambda: print(''.join(f"Command list:"), [key for key in all_commands]),
            # AddressBook commands
            "save addressbook": contact_book.save_addressbook(),
            "load addressbook": lambda: contact_book.load_notebook(text_after_command),
            # NoteBook commands
            "add note": lambda: list_of_notes.add_note(text_after_command),
            "add tag": lambda: list_of_notes.add_tag(text_after_command),
            "delete note": lambda: list_of_notes.delete_note(text_after_command),
            "edit note": lambda: list_of_notes.edit_note(text_after_command),
            "search note": lambda: list_of_notes.search_notes(text_after_command),
            "save notebook": list_of_notes.save_notebook,
            "load notebook": lambda: list_of_notes.load_notebook(text_after_command),
            "show notebook": list_of_notes.show_notebook,
            "show notebooks": lambda: print(list_of_notes)
        }
    
    while True:
        commands = list(all_commands.keys())
        command_completer = WordCompleter(commands)

        closing_words = ["good bye", "close", "exit"]

        command = ""
        text_after_command = ""

        # input_your_command = input(f'Enter your command: ')
        input_your_command = prompt('Enter your command: ', completer=command_completer)

        for i in all_commands.keys():
            if input_your_command.lower().startswith(i):
                command = i
                text_after_command = input_your_command.lower().removeprefix(i).strip()
        command_to_check_for_dif = " ".join(input_your_command.split(" ")[0:2])

        # print(f"Your command is: {command}")
        # print(f'Text after command is: {text_after_command}')

        if command in closing_words:
            list_of_notes.save_notebook()
            all_commands[command]()
            break
        elif command in all_commands:
            all_commands[command]()
        else:
            most_similar_command = difflib.get_close_matches(command_to_check_for_dif, commands, n=1)
            print(f"Invalid command. Print 'info' to see list of commands. "
                  f"The most similar to command: '{command}' is: '{most_similar_command[0]}'")


if __name__ == '__main__':
    main()
