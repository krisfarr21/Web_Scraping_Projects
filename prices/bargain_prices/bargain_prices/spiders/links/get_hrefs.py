# to extract necessary hrefs from homepages (found in homepages.txt)
import os
from typing import Dict
#rudimentary function to get green links into dictionary
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
print(THIS_FOLDER)
def green_categories(file_name='greens_links.txt') -> Dict:
    '''
    outputs dictionaries {categories:urls}
    '''
    file_ = os.path.join(THIS_FOLDER, file_name)
    with open(file_, 'r') as f:
        lines = f.readlines()
        URL_NUMBER = '&pg=1&sort=Position&sortd=Asc'
        urls = [link.strip('\n')+URL_NUMBER for link in lines]
        categories = ['household', 'fruits&veg', 'butcher', 'dairy',
                    'deli', 'bakery', 'fish', 'organic', 'beverages',
                    'winecellar']
        urls_cat = dict(zip(categories, urls))
    return urls_cat

print(green_categories())
