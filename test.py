import requests
import re
from bs4 import BeautifulSoup

urls = 'http://www.scp-wiki.net/scp-'
content = ""


def get_single_scp(scp_id):
    """Returns soup for a given SCP item number."""

    try:
        r = requests.get(url=urls + str(scp_id))
        if r.status_code == 200:
            return BeautifulSoup(r.content)
        else:
            print('Failed to access SCP Wiki page. HTTP Status Code ' + str(r.status_code))
            return
    except requests.RequestException as e:
        print('Failed to access SCP Wiki page. Request Error: ' + e)
        return

def main():
    scp = get_single_scp('003')
    content = scp.find('div', id='page-content')

    try:
        for item in content.find_all('p'):
                if item.strong:
                    key = item.strong.get_text(strip=True).rstrip(':')
                    value = item.strong.next_sibling.strip()
                    print(key + ":" + value)
    except AttributeError:
        print('Unknown')

if __name__ == "__main__":
    main()