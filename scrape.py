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


def get_scp_name(scp_id):
    # get the name (which unfortunately isn't listed on the single page)
    try:
        if int(scp_id) < 1000:
            # Series I
            url = 'http://www.scp-wiki.net/scp-series'
        elif int(scp_id) < 2000:
            # Series II
            url = 'http://www.scp-wiki.net/scp-series-2'
        elif int(scp_id) < 3000:
            # Series III
            url = 'http://www.scp-wiki.net/scp-series-3'
        elif int(scp_id) < 4000:
            # Series IV
            url = 'http://www.scp-wiki.net/scp-series-4'
        elif int(scp_id) < 5000:
            # Series V
            url = 'http://www.scp-wiki.net/scp-series-5'
        elif int(scp_id) < 6000:
            # Series VI
            url = 'http://www.scp-wiki.net/scp-series-6'                    
        else:
            # Series XXX
            print('Unavailable SCP Series')
            return

        r = requests.get(url=url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content)
            content = soup.find('div', id='page-content')
            list_elements = content.find_all('li')
            for li in list_elements:
                try:
                    if re.findall('[0-9]+', li.next['href']):
                        if int(re.findall('[0-9]+', li.next['href'])[0]) == scp_id:
                            return re.split(' - ', li.get_text())[-1]
                except KeyError:
                    continue
        else:
            print('Failed to access SCP Wiki page. HTTP Status Code ' + str(r.status_code))
            return
    except requests.RequestException as e:
        print('Failed to access SCP Wiki page. Request Error: ' + e)
        return


def get_value_from_content(content, target_var):
    try:
        for item in content.find_all('p'):
                if item.strong:
                    if(target_var in item.strong.get_text(strip=True).rstrip(':')):
                        key = item.strong.get_text(strip=True).rstrip(':')
                        value = item.strong.next_sibling.strip()
                        return value
    except AttributeError:
       return 'Unknown'


def parse_scp(soup, scp_id):

    if soup is None:
        return None

    # get the content block
    content = soup.find('div', id='page-content')

    # get the rating
    try:
        rating = soup.find('span', {'class': 'rate-points'}).contents[1].contents[0].replace('+', '')
    except AttributeError:
        # print('no rating found')
        rating = 0

    # get class
    try:
        scp_class = get_value_from_content(content, "Object Class")
    except AttributeError:
        # print('no class found')
        scp_class = "Unknown"     

    # get containment proc
    try:
        scp_containment_proc = get_value_from_content(content, "Containment Procedure")
    except AttributeError:
        # print('no Containment Procedures found')
        scp_class = "Unknown"             

    # get the main image
    try:
        main_image = content.find('div', {'class': 'scp-image-block'}).contents[0]['src']
    except AttributeError:
        # print('no main_image found')
        main_image = None
    except KeyError:
        # print('no main_image found')
        main_image = None

    # get the image caption
    try:
        image_caption = content.find('div', {'class': 'scp-image-block'}).contents[2].contents[1].contents[0]
    except AttributeError:
        # print('no image_caption found')
        image_caption = None

    # get page info
    page_info = soup.find('div', id='page-info')
    revision = re.findall('\d+', page_info.next)[0]
    last_updated = page_info.find('span')['class'][1].replace('time_', '')

    # get the tags
    tags_list = soup.find('div', {'class': 'page-tags'}).find('span')
    tags = [tag.string for tag in tags_list if tag.string != '\n']

    # get a link to the discussion page
    discussion_link = 'http://www.scp-wiki.net' + soup.find('a', id='discuss-button')['href']

    return {
        'id': scp_id,
        'rating': int(rating),
        'scp_class': scp_class,
        'containment_procedure':scp_containment_proc,
        'image': {
            'src': main_image
        },
        'revision': int(revision),
        'last_edited': int(last_updated),
        'tags': tags,
        'discussion': discussion_link
    }


def scp(scp_id):
    """
    Returns a dictionary with as much content as possible regarding the SCP ID.
    :param scp_id: Either a string with the established format (002) or an integer (2)
    """

    if len(str(int(scp_id))) == 1:
        scp_id = '00' + str(int(scp_id))
    elif len(str(int(scp_id))) == 2:
        scp_id = '0' + str(int(scp_id))

    scp_name = get_scp_name(int(scp_id))
    site_content = get_single_scp(str(scp_id))

    parsed_content = parse_scp(site_content, int(scp_id))

    parsed_content['name'] = scp_name

    return parsed_content


# list = []
# for i in range(2, 100):
#     try:
#         list.append(parse_scp(get_single_scp(i)))
#     except:
#         continue
# print(json.dumps(list))

# print(scp(1))

