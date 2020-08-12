import csv, time
content = []
headers = set()
headers.add('Name')
headers.add('Office')
headers.add('Misc')
with open('first_run_2.txt', 'r') as data:
    entry = {}
    name_number = 0
    for l in data:
        if l != '\n':
            if 'Name' in entry and entry['Name'] == l.strip():
                continue
            elif ':' not in l:

                while True:
                    unlabeled_field = input('{} = name/office/misc/phone/space? [n/o/m/p/space]'.format(l))
                    
                    if unlabeled_field.lower() == 'n':
                        entry['Name'] = l.strip()
                        break
                    if unlabeled_field.lower() == 'o':
                        current_office = l.strip()
                        entry['Office'] = l.strip()
                        break
                    if unlabeled_field.lower() == 'm':
                        entry['Misc'] = l.strip()
                        break
                    if unlabeled_field.lower() == 'p':
                        entry['PHONE NUMBER'] = l.strip()
                        break
                    if unlabeled_field.lower() == ' ':
                        break
                    print('You have made an invalid choice, try again.')
                    time.sleep(1)
            else:
                i = l.index(':')
                headers.add(l[:i].strip())
                entry[l[:i]] = l[i + 2:].strip()
        else:
            if 'Name' in entry:
                if 'Office' not in entry:
                    entry['Office'] = current_office
                content.append(entry)
                entry = {}
    if 'Name' in entry:
        if 'Office' not in entry:
            entry['Office'] = current_office
        content.append(entry)
headers = list(headers)
table = [headers]

for row in content:
    table.append([])
    for column in headers:
        if column in row:
            table[-1].append(row[column].title())
        else:
            table[-1].append(None)

with open('candiates_table.csv', 'w') as out:
    writer = csv.writer(out, quoting=csv.QUOTE_ALL)
    for can in table:
        writer.writerow(can)
