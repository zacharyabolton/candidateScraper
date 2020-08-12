import smtplib, csv, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

candidates_input = 'candidates_table_2.csv'
msg_body_input = 'test_msg_body.txt'
fromaddr = "zacbolton2129@gmail.com"
wait_time = 40

def write_msg_body():
    msg_body = ''
    with open(msg_body_input, 'r') as input:
        for l in input:
            msg_body += l
    return msg_body

def send_email(toaddr, fields):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = '{Name} for {Office}'.format(**fields)
    body = write_msg_body().format(**fields)
    # print('FROM: {}'.format(msg['From']))
    print('TO: {}'.format(msg['To']))
    # print('SUBJECT: {}\n'.format(msg['Subject']))
    # print(body)
    # cont = input('Press enter to stop. Press any other key(s), and then enter, to continue.')
    # if not cont:
    #     print('quitting')
    #     exit()
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "zEa-KfD-dGQ-J6S")
    text = msg.as_string()
    callback = server.sendmail(fromaddr, toaddr, text)
    server.quit()
    if callback:
        print('callback = {}'.format(callback))

def loop_through_candidates():
    fallbacks = {
        'Name': 'Friend', 
        'OCCUPATION': 'professional', 
        'WEBSITE': 'your campaign', 
        'PHONE NUMBER': 'your phone number', 
        'Office': 'the office you\'re running for', 
        'INCUMBENT': 'incumbent status unknown', 
        'AGE': 'your age', 
        'QUALIFIED DATE': 'the date you qualified', 
        'PARTY': 'your political party'
    }
    with open(candidates_input, 'r') as input:
        reader = csv.reader(input, delimiter=',')
        headers = next(reader)
        for c in reader:
            fields = {}
            for f, i in zip(c, range(len(c))):
                if headers[i] == 'INCUMBENT':
                    if f == 'Yes':
                        fields[headers[i]] = 'constituents'
                    else:
                        fields[headers[i]] = 'potential constituents'
                elif headers[i] == 'WEBSITE':
                    if f:
                        fields[headers[i]] = 'studied your platform at {}'.format(f.lower())
                    else:
                        fields[headers[i]] = 'some questions about your platform'
                elif f:
                    fields[headers[i]] = f
                elif headers[i] == 'E-mail':
                    fields = None
                    break
                else:
                    fields[headers[i]] = fallbacks[headers[i]]     
            if fields:
                send_email(fields['E-mail'], fields)
                print('email sent. Waiting {} seconds...'.format(wait_time))
                time.sleep(wait_time)
                print('next email:')

loop_through_candidates()