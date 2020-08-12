# import libraries
import requests, lxml.html, csv
from bs4 import BeautifulSoup, Comment
import time


# open session
s = requests.session()

# specify the url
url = 'http://elections.sos.ga.gov/GAElection/CandidateDetails'

parties = ['D', 'G', 'I', 'L', 'NP', 'O', 'R', 'S', 'U', 'W']
office_types = ['F', 'S', 'C']
candidates_info = []

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

for office in office_types:
    time.sleep(1) # to keep the server from thinking it's a DOS attack
    for party in parties:
        print('office = {}, party = {}'.format(office, party))
        time.sleep(1) # to keep the server from thinking it's a DOS attack
        # apply form values
        payload = {
            'nbElecYear': '2018',
            'id_election': '34147',
            'cd_party': party,
            'cdOfficeType': office,
            'cdFlow': 'S'
        }
        if office == 'C':
            payload['id_office'] = '0' # not needed since all display on one page
            payload['idTown'] = '044' # dekalb

        response = s.post(url, data=payload)

        # parse html with bs4
        soup = BeautifulSoup(response.text, "html.parser")

        # collect and iterate through offices
        offices_options = soup.find(id="id_office").find_all('option')
        office_values = [_.get('value') for _ in offices_options if _.get('value') != '0']
        if office != 'C':
            for office_value in office_values:
                print('    office_value = {}'.format(office_value))
                time.sleep(1)
                payload['id_office'] = office_value
                response = s.post(url, data=payload)
                soup = BeautifulSoup(response.text, "html.parser")
                for tr in soup.findAll("tr"):
                    u = tr.u
                    info = tr.find('td', {'class': 'candidate2'})
                    comment = tr.find(text=lambda text:isinstance(text, Comment))
                    if u is not None:

                        candidates_info.append('\n')
                        candidates_info.append('\n')
                        candidates_info.append(u.text)
                        candidates_info.append('\n')
                    if info is not None and info.text != candidates_info[-1]:
                        if info.text == 'E-mail: [email protected]':
                            href = info.a['href']
                            
                            candidates_info.append('E-mail: {}'.format(cfDecodeEmail(href[28:])))
                        else:
                            candidates_info.append(info.text)
                    if comment is not None and comment[50:53] == 'AGE':
                        candidates_info.append(comment[50:57])

        else:
            # get values
            print('    office_value = C')
            for tr in soup.findAll("tr"):
                u = tr.u
                info = tr.find('td', {'class': 'candidate2'})
                comment = tr.find(text=lambda text:isinstance(text, Comment))
                if u is not None:
                    candidates_info.append('\n')
                    candidates_info.append('\n')
                    candidates_info.append(u.text)
                    candidates_info.append('\n')
                if info is not None and info.text != candidates_info[-1]:
                    if info.text == 'E-mail: [email protected]':
                        href = info.a['href']
                        
                        candidates_info.append('E-mail: {}'.format(cfDecodeEmail(href[28:])))
                    else:
                        candidates_info.append(info.text)
                if comment is not None and comment[50:53] == 'AGE':
                    candidates_info.append(comment[50:57])

with open("first_run.txt", "w") as out:
        for r in candidates_info:
            out.write(r+'\n')
