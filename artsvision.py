from bs4 import BeautifulSoup
from requests import Session
import config as cfg

# the below prints the contens of the log in page
# source = requests.get('https://artsvision.net/main.asp').text
#
# soup = BeautifulSoup(source, 'lxml')
#
# print(soup.prettify())

# this works at printing the conents of the log in page
# with Session() as s:
#     site = s.get('https://artsvision.net/main.asp')
#     print(site.content)

# # no work
# with Session() as s:
#     login_data = {"username": cfg.my_usr, "password": cfg.my_pswrd}
#     s.post("https://artsvision.net/epcor.asp", login_data)
#     home_page = s.get("https://artsvision.net/main.asp")
#     soup = BeautifulSoup(home_page.text, "html.parser")
#     print(soup.prettify())

# no work
with Session() as s:
    login_data = {"username": cfg.my_usr, "password": cfg.my_pswrd}
    s.post("https://artsvision.net/epcor.asp", login_data)
    home_page = s.get("https://artsvision.net/main.asp")
    soup = BeautifulSoup(home_page.text, "html.parser")
    morp = soup.prettify()
    # print(morp)

with open('soup_file.txt', 'w') as my_file:
    my_file.write(morp)