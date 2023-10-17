from collections import UserDict
from datetime import datetime
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
    # Ініціалізація об'єкта Name
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)


class Phone(Field):
    # Ініціалізація об'єкта Phone
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)

    @Field.value.setter
    def value(self, value):
        if not re.match(r'^(\+380\d{9}|0\d{9})$', value):
            print("Incorrect phone number format, should be +380638108107 or 0638108107.")
        else:
            self._value = value


class Email(Field):
    # Ініціалізація об'єкта Email
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)

    @Field.value.setter
    def value(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            print("Invalid email format.")
        self._value = value


class Address(Field):
    # Ініціалізація об'єкта Address
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    # Ініціалізація об'єкта Birthday
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)
    
    @Field.value.setter
    def value(self, value):
        # Валідація формату дати
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Incorrect birthday format, should be YYYY-MM-DD.")
        self._value = value


class Record:
    
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = Birthday(birthday)

    def __str__(self):
        # Перетворення об'єкта контакту в рядок
        phones_str = '; '.join(str(p) for p in self.phones)
        emails_str = '; '.join(str(e) for e in self.emails)
        addresses_str = '; '.join(str(a) for a in self.addresses)

        return f"Contact name: {self.name.value}, phones: {phones_str}, " \
               f"emails: {emails_str}, addresses: {addresses_str}, birthday: {self.birthday}"


class AddressBook(UserDict):

    def add_contact(self, text):
        # Додавання контакту
        if len(text) >= 2:
            new_contact = Record(text.title())
            if new_contact.name.value not in list(self.data.keys()):
                self.data[new_contact.name.value] = new_contact
            else:
                print(f'Contact {new_contact.name.value} is already in AddressBook')
        else:
            print("Name of contact is not correct!")
    
    def add_phone_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і номера телефону
        # Якщо після введеня імені не буде вказаний номер телефону то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        phone_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(phone_to_add) >= 1:
            for key, value in self.data.items():
                if key == name_input:
                    phone_to_add_new = Phone(phone_to_add)
                    phone_to_add_new.value = phone_to_add
                    if phone_to_add_new.value not in list(i.value.lower() for i in self.data[name_input].phones):
                        return self.data[name_input].phones.append(Phone(phone_to_add_new.value))
                    else:
                        return print(f"This phone is already entered for this addressbook!")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(phone_to_add) == 0:
            print("No phone number!")

    def add_email_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і мейлу
        # Якщо після введеня імені не буде вказаний мейл то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        email_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(email_to_add) >= 5:
            for key, value in self.data.items():
                if key == name_input:
                    if email_to_add not in list(i.value.lower() for i in self.data[name_input].emails):
                        return self.data[name_input].emails.append(Email(email_to_add))
                    else:
                        return print(f"This email is already entered for this addressbook!")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(email_to_add) == 0:
            print("No email!")

    def add_address_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і адреси
        # Якщо після введеня імені не буде вказана адреса то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        address_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(address_to_add) >= 5:
            for key, value in self.data.items():
                if key == name_input:
                    if address_to_add not in list(i.value.lower() for i in self.data[name_input].addresses):
                        return self.data[name_input].addresses.append(Address(address_to_add))
                    else:
                        return print(f"This address is already entered for this addressbook!")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(address_to_add) == 0:
            print("No address!")

    def add_birthday_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і дня народження
        # Якщо після введеня імені не буде вказаний день народження то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        birthday_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(birthday_to_add) >= 10:
            for key, value in self.data.items():
                if key == name_input:
                    if self.data[name_input].birthday.value is None:
                        self.data[name_input].birthday = Birthday(birthday_to_add)
                        return
                    else:
                        return print(f"Birthday for this contact is already set. Use 'edit' func")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(birthday_to_add) == 0:
            print("No birthday date!")

    def find_contact_by_name(self, contact_name):  # Пошук контакту
        return self.data.get(contact_name)

    def search_matches_in_addressbook(self, match):  # Шукаємо збіги в адресній книзі
        found_matches = []

        for name, contact in self.data.items():
            list_of_phones = list(i.value.lower() for i in self.data[name].phones)
            list_of_emails = list(i.value.lower() for i in self.data[name].emails)
            list_of_addresses = list(i.value.lower() for i in self.data[name].addresses)

            if any(match in phone for phone in list_of_phones)\
                    or any(match in email for email in list_of_emails)\
                    or any(match in address for address in list_of_addresses):
                if contact not in found_matches:
                    found_matches.append(contact)

            if match == contact.birthday.value:
                print(f'Contact {name} has birthday {match}')

        for contact in found_matches:
            print(f"{contact}")
            
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
                if search_match in str(value):
                    res += str(value) + ""
                    print(f'Note "{res}" is found')
    
    def search_notes_by_tag(self, tag):
        found_notes = []
        for name, note in self.data.items():
            if tag in note.tags:
                found_notes.append((name, note))

        found_notes = sorted(found_notes, key=lambda x: x[1].note.split()[0].lower())
        if found_notes:
            print("Notes found:")
            for name, note in found_notes:
                print(f"{name}: {note}")
        else:
            print("No notes found for the tag.")
        return found_notes

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


class Notes:
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

    all_commands = {
            # General commands
            "hello": lambda: print("Hi! To get commands list print 'info'."),
            "hi": lambda: print("Hi! To get commands list print 'info'."),
            "good bye": lambda: print("Good bye!"),
            "close": lambda: print("Good bye!"),
            "exit": lambda: print("Good bye!"),
            "info": lambda: print(''.join(f"Command list:"), [key for key in all_commands]),
            # AddressBook commands
            "save addressbook": contact_book.save_addressbook,
            "load addressbook": lambda: contact_book.load_notebook(text_after_command),
            "add contact": lambda: contact_book.add_contact(text_after_command),
            "add phone": lambda: contact_book.add_phone_to_contact(text_after_command),
            "add email": lambda: contact_book.add_email_to_contact(text_after_command),
            "add address": lambda: contact_book.add_address_to_contact(text_after_command),
            "add birthday": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "edit phone": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "edit birthday": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "edit email": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "delete contact": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "show addressbook": lambda: contact_book.show_addressbook(),
            "show addressbooks": lambda: print(contact_book),
            "show birthdays": lambda: contact_book.add_birthday_to_contact(text_after_command),
            "find contact": lambda: contact_book.find_contact_by_name(text_after_command),
            "find matches": lambda: contact_book.search_matches_in_addressbook(text_after_command),
            # NoteBook commands
            "add note": lambda: list_of_notes.add_note(text_after_command),
            "add tag": lambda: list_of_notes.add_tag(text_after_command),
            "delete note": lambda: list_of_notes.delete_note(text_after_command),
            "edit note": lambda: list_of_notes.edit_note(text_after_command),
            "search note": lambda: list_of_notes.search_notes(text_after_command),
            "search tag": lambda: list_of_notes.search_notes_by_tag(text_after_command),
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

        input_your_command = prompt('Enter your command: ', completer=command_completer)

        for i in all_commands.keys():
            if input_your_command.lower().startswith(i):
                command = i
                text_after_command = input_your_command.lower().removeprefix(i).strip()
        command_to_check_for_dif = " ".join(input_your_command.split(" ")[0:2])

        if command in closing_words:
            list_of_notes.save_notebook()
            contact_book.save_addressbook()
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
