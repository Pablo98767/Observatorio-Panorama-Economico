
from bs4 import BeautifulSoup
import requests

html = requests.get("http://indiceseconomicos.secovi.com.br/indicadormensal.php?idindicador=59").content
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())



















