from EmailChecker import SidraELEzz
import pyfiglet
import requests
G = '\033[1;31m'
M = pyfiglet.figlet_format('Gmail Check')
print(G+M)
id = input('\033[1;31m└─[\033[1;32mID\033[1;31m]>\033[1;33m')
tok = input('\033[1;31m└─[\033[1;32mEnter Token \033[1;31m]>\033[1;33m')
email = input('\033[1;31m└─[\033[1;32mEnter File Combo \033[1;31m]>\033[1;33m')
file = open(email, 'r')
while True:
		BT=file.readline().split('\n')[0]
		username = BT.split(':')[0]
		checker = SidraELEzz.Gmail(str(username))
		if checker ==True:
			requests.post(f'https://api.telegram.org/bot{tok}/sendMessage?chat_id={id}&text=Available Email Gmail \nGMAIL 👇\n{username}')
			print('\033[1;31m└─[\033[1;32mEmail Available\033[1;31m]>\033[1;33m')
		elif checker ==False:
			print('\033[1;31m└─[\033[1;32mEmail Not Available\033[1;31m]>\033[1;33m')
