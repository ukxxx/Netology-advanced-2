import csv
import re

def main(csv_file):

    contacts = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        reader = list(reader)

        for row in reader[1:]:
            # Работаем с ФИО
            pattern = r'([А-Я][а-я]+)?'
            replace = r'\1 '
            result = re.sub(pattern, replace, row[0] + row[1] + row[2])
            lastname = result.split()[0]
            firstname = result.split()[1]
            try:
                surname = result.split()[2]
            except IndexError:
                surname = ''

            # Читаем место работы
            organization = row[3]

            # Читаем должность
            position = row[4]

            # Работаем с номером телефона
            pattern = r'\+?(7?|8)?\s?\s?\(?(\d{3})\)? ?-?(\d{3})-?(\d{2})-?(\d{2}) ?\(? ?(\w?\w?\w?\.)? ?(\d{4})?\)?'
            replace = r'+7(\2)\3-\4-\5 \6\7'
            result = re.sub(pattern, replace, row[5])
            phone = "".join(result.split(','))

            # Читаем почту
            email = row[6]

            full_name = ' '.join([part for part in [lastname, firstname] if part])
  
            if full_name not in contacts:
                contacts[full_name] = {
                    'lastname': lastname,
                    'firstname': firstname,
                    'surname': surname,
                    'organization': organization,
                    'position': position,
                    'phone': phone,
                    'email': email
                }
            else:
                if surname:
                    contacts[full_name]['surname'] = surname
                if organization:
                    contacts[full_name]['organization'] = organization
                if position:
                    contacts[full_name]['position'] = position
                if phone:
                    contacts[full_name]['phone'] = phone   
                if email:
                    contacts[full_name]['email'] = email    

    # Запись очищенных данных в новый файл CSV
    output_file = 'cleaned_contacts.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for contact in contacts.values():
            writer.writerow(contact)

    return output_file

# Пример использования
if __name__ == '__main__':
    input_csv = 'phonebook_raw.csv'
    cleaned_csv = main(input_csv)
    print(f"Конечный файл: {cleaned_csv}")
