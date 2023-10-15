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

'''___________________________________________________________________________________________'''

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = None

    def add_phone(self, phone):
        # Додавання телефону до контакту
        self.phones.append(Phone(phone))

    def add_email(self, email):
        # Додавання електронної адреси до контакту
        self.emails.append(Email(email))

    def add_address(self, address):
        # Додавання адреси до контакту
        self.addresses.append(Address(address))

    def add_birthday(self, birthday):
        # Додавання дня народження до контакту
        self.birthday = birthday

    def __str__(self):
        # Перетворення об'єкта контакту в рядок
        phones_str = '; '.join(str(p) for p in self.phones)
        emails_str = '; '.join(str(e) for e in self.emails)
        addresses_str = '; '.join(str(a) for a in self.addresses)

        return f"Contact name: {self.name.value}, phones: {phones_str}, " \
               f"emails: {emails_str}, addresses: {addresses_str}, birthday: {self.birthday}"


class AddressBook(UserDict):

    # def user_input(self, input_text):
    #     # Розділення тексту на частини
    #     parts = input_text.split()
    #     command = parts[0].lower            # зчитуємо першу команду (нижній регістр)
    #
    #     if command == 'add':
    #         #Розпідзнавання підкоманди: phone, email, address, birthday
    #         sub_command = parts[1].lower()
    #         if sub_command == 'phone':
    #             self.add_phone_to_contact(parts[2:])        # відсікаємо службові команди add phone
    #         elif sub_command == 'email':
    #             self.add_email_to_contact(parts[2:])        # відсікаємо службові команди add e-mail
    #         elif sub_command == 'address':
    #             self.add_address_to_contact(parts[2:])      # відсікаємо службові команди add address
    #         elif sub_command == 'birthday':
    #             self.add_birthday_to_contact(parts[2:])     # відсікаємо службові команди add birthday
    #         else:
    #             print("Uncorrect sub-command. Valid sub-commands: phone, email, address, birthday")


    def add_phone_to_contact(self, input_parts):                            # Додаємо телефон
        # Отримання імені та телефону з тексту
        contact_name, phone = input_parts[0], ' '.join(input_parts[1:])
        contact = self.find_contact_by_name(contact_name)
        if contact:
            # Додавання телефону до контакту
            contact.add_phone(phone)
        else:
            print(f"Contact with name '{contact_name}' not found.")

    def add_email_to_contact(self, input_parts):                             # Додаємо email
        # Отримання імені та мейлу з тексту
        contact_name, email = input_parts[0], ' '.join(input_parts[1:])
        contact = self.find_contact_by_name(contact_name)
        if contact:
            # Додавання електронної адреси до контакту
            contact.add_email(email)
        else:
            print(f"Contact with name '{contact_name}' not found.")

    def add_address_to_contact(self, input_parts):                              # Додаємо адресу
        # Вилучення імені та адреси з частин введеного тексту
        contact_name, address = input_parts[0], ' '.join(input_parts[1:])
        contact = self.find_contact_by_name(contact_name)
        if contact:
            # Додавання адреси до контакту
            contact.add_address(address)
        else:
            print(f"Contact with name '{contact_name}' not found.")

    def add_birthday_to_contact(self, input_parts):                             # Додаємо день народження
        # Вилучення імені та дня народження з частин введеного тексту
        contact_name, birthday = input_parts[0], ' '.join(input_parts[1:])
        contact = self.find_contact_by_name(contact_name)
        if contact:
            # Додавання дня народження до контакту
            contact.add_birthday(birthday)
        else:
            print(f"Contact with name '{contact_name}' not found.")
    
    def find_contact_by_name(self, contact_name):                               # Пошук контакту    
        return self.data.get(contact_name)

    '''___________________________________________________________________________________________'''

    def save_addressbook(self):
        with open("addressbook.bin", "wb") as f:
            pickle.dump(self.data, f)

    def load_notebook(self, file):
        with open(file, "rb") as f:
            self.data = pickle.load(f)

    def show_addressbook(self):
        for name, contact in self.data.items():
            print(f"{name}: {contact}")

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
            res = ""
            for value in self.data.values():
                # print(type(str(value)))
                # print(str(value))
                if (search_match in str(value)):
                    res += str(value) + ""
                    print(f'Note "{res}" is found')

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
            "add contact": lambda: contact_book.add_phone_to_contact(text_after_command),
            "add phone": lambda: contact_book.add_phone_to_contact(text_after_command),
            "add email": lambda: contact_book.add_email_to_contact(text_after_command),
            "add birthday": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "edit phone": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "edit birthday": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "edit email": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "delete contact": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "show addressbook": lambda: contact_book.show_addressbook,
            "show birthdays": lambda: contact_book.add_birthday_to_contact(text_after_command),
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
            print(f"Invalid command. Print 'info' to see list of commands.\n"
                  f"The most similar to command: '{command_to_check_for_dif}' is: '{most_similar_command[0]}'") \
                if (len(most_similar_command) > 0) \
                else (print(f"Invalid command. Print 'info' to see list of commands. "))


if __name__ == '__main__':
    main()
