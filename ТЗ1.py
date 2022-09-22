from io import FileIO
from typing import List

message = '''
Выберите опцию:
1 - Просмотр контактов
2 - Редактирование контактов
3 - Поиск контакта по телефону
'''
message2 = '''
Выберите что редактировать:
1 - ФИО
2 - Телефон
3 - Email
'''


class Contact:
    def __init__(self, phone: str = "", bio: str = "", email: str = ""):
        self.phone = phone
        self.bio = bio
        self.email = email

    def serialized(self, delimeter=','):
        return f'{self.phone}{delimeter}{self.bio}{delimeter}{self.email}'


def deserialize(contact: str, delimiter=','):
    a, b, c = contact.split(delimiter)
    return Contact(a, b, c)

def show_contacts(contacts):
    print('ID\tНомер\tФИО\tEmail')
    for i in range(len(contacts)):
        print(str(i)+'\t'+contacts[i].serialized("\t"))

def edit_contact_dialogue(contacts):
    while True:
        try:
            id = int(input("Введите ID контакта:"))
            if id>=len(contacts):
                raise Exception()
            choice = int(input(message2))

            break
        except:
            print("Выберите одну из предложенных опций.")
            continue
    change = input("Введите новое значение:")
    if choice == 1:
        contacts[id].bio = change
    elif choice == 2:
        contacts[id].phone = change
    elif choice == 3:
        contacts[id].email = change
    return contacts

def update(file:FileIO,contacts:List[Contact]):
    file.seek(0)
    for i in contacts:
        file.write(i.serialized()+'\n')
    file.truncate()
    file.flush()

def search_by_phone(phone_number:str,contacts:List[Contact]):

    show_contacts([x for x in contacts if phone_number in x.phone])
def start_main_loop(file: FileIO):
    contacts = []
    for contact in file.read().split('\n'):
        if contact:
            contacts.append(deserialize(contact))

    while True:
        try:
            choice = int(input(message))
        except:
            print("Выберите одну из предложенных опций.")
            continue

        if choice == 1:
            show_contacts(contacts)
        elif choice == 2:
            contacts = edit_contact_dialogue(contacts)
            update(file,contacts)
        elif choice == 3:
            search_by_phone(input("Введите телефон для поиска:"),contacts)

if __name__ == "__main__":
    file_name = input("Введите адрес файла контактов:")
    with open(file_name, 'r+') as file:
        start_main_loop(file)



