from io import FileIO
from typing import List, Dict

message = '''
Выберите опцию:
1 - Просмотр контактов
2 - Редактирование контактов
3 - Поиск контакта по телефону
4 - Поиск контакта по email
5 - Поиск контакта по ФИО
6 - Вывод контактов с пустыми полями
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


def deserialize(contact: str, delimiter=',')->Contact:
    '''Десериализует объект типа Contact из строчки'''
    a, b, c = contact.split(delimiter)
    return Contact(a, b, c)

def show_contacts(contacts):
    '''Выводит контакты в консоль'''
    print('ID\tНомер\tФИО\tEmail')
    for i in range(len(contacts)):
        print(str(i)+'\t'+contacts[i].serialized("\t"))
def show_contacts_keep_ids(contacts:Dict[int,Contact]):
    '''Выводит контакты в консоль, сохраняя оригинальные ID'''
    print('ID\tНомер\tФИО\tEmail')
    for i in contacts:
        print(str(i)+'\t'+contacts[i].serialized("\t"))
def edit_contact_dialogue(contacts)->List[Contact]:
    '''Замены данных на list объектов Contact'''
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
    '''Перезаписывает файл новыми данными из contacts'''
    file.seek(0)
    for i in contacts:
        file.write(i.serialized()+'\n')
    file.truncate()
    file.flush()

def search_by_phone(phone_number:str,contacts:List[Contact]):
    '''Выводит в консоль список контактов с телефоном содержащим поисковое значение'''
    show_contacts_keep_ids({id:x for id,x in enumerate(contacts) if phone_number in x.phone})
def search_by_email(email:str,contacts:List[Contact]):
    '''Выводит в консоль список контактов с email-ом содержащим поисковое значение'''
    show_contacts_keep_ids({id:x for id,x in enumerate(contacts) if email in x.email})
def search_by_name(name_query:str,contacts:List[Contact]):
    '''Выводит в консоль список контактов с именем содержащим поисковое значение'''
    show_contacts_keep_ids({id:x for id,x in enumerate(contacts) if name_query in x.bio})
def search_empty_fields(contacts:List[Contact]):
    '''Выводит в консоль список контактов с пустым значением в полях email и phone'''
    show_contacts_keep_ids({id: x for id, x in enumerate(contacts) if (not x.email or not x.phone)})
def start_main_loop(file: FileIO):
    '''Запускает главный диалог взаимодействия с программой'''
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
        elif choice==4:
            search_by_email(input("Введите email для поиска:"), contacts)
        elif choice==5:
            search_by_name(input("Введите имя для поиска:"), contacts)
        elif choice==6:
            search_empty_fields(contacts)
if __name__ == "__main__":
    file_name = input("Введите адрес файла контактов:")
    with open(file_name, 'r+',encoding='utf-8') as file:
        start_main_loop(file)



