import re
import csv
from pprint import pprint

with open("data/phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

new_contacts = []
for contact in contacts_list:
    full_name = " ".join(contact[:3]).split()
    lastname = full_name[0]
    firstname = full_name[1] if len(full_name) > 1 else ""
    surname = full_name[2] if len(full_name) > 2 else ""

    while len(contact) < 7:
        contact.append("")

    new_contacts.append([lastname, firstname, surname] + contact[3:])

phone_pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*доб\.*\s*(\d+))?")
phone_format = r"+7(\2)\3-\4-\5 доб.\7"

for contact in new_contacts:
    if len(contact) > 5 and contact[5]:
        contact[5] = re.sub(phone_pattern, phone_format, contact[5]).strip()
        contact[5] = contact[5].replace(" доб.None", "")
contacts_dict = {}

for contact in new_contacts:
    key = (contact[0], contact[1])
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        for i in range(len(contact)):
            if not contacts_dict[key][i]:
                contacts_dict[key][i] = contact[i]

final_contacts_list = list(contacts_dict.values())

print(final_contacts_list)

with open("data/phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)