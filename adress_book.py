from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
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
