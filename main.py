import re
import csv
from pprint import pprint
from log_decorator import logger

@logger("phonebook.log")
def format_phone(phone):
    phone_pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*доб\.*\s*(\d+))?")
    phone_format = r"+7(\2)\3-\4-\5 доб.\7"
    formatted_phone = re.sub(phone_pattern, phone_format, phone).strip()
    return formatted_phone.replace(" доб.None", "")


@logger("phonebook.log")
def process_contacts(contacts_list):
    new_contacts = []
    for contact in contacts_list:
        full_name = " ".join(contact[:3]).split()
        lastname = full_name[0]
        firstname = full_name[1] if len(full_name) > 1 else ""
        surname = full_name[2] if len(full_name) > 2 else ""

        while len(contact) < 7:
            contact.append("")

        new_contacts.append([lastname, firstname, surname] + contact[3:])

    for contact in new_contacts:
        if len(contact) > 5 and contact[5]:
            contact[5] = format_phone(contact[5])

    contacts_dict = {}
    for contact in new_contacts:
        key = (contact[0], contact[1])
        if key not in contacts_dict:
            contacts_dict[key] = contact
        else:
            for i in range(len(contact)):
                if not contacts_dict[key][i]:
                    contacts_dict[key][i] = contact[i]

    return list(contacts_dict.values())


with open("data/phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

final_contacts_list = process_contacts(contacts_list)

pprint(final_contacts_list)

with open("data/phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)