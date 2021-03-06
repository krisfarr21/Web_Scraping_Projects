# Functions returning links of categories in different websites - the links are first scraped through the scrapy interacative terminal

def greens_categories():
    '''
    Output: links for each category in greens 
    '''
    base_url = 'https://www.greens.com.mt'
    categories = ['/products?cat=chilledanddairy',
 '/products?cat=delicatessen',
 '/products?cat=confectionary&cat2=bakery',
 '/products?cat=fish',
 '/products?cat=organic',
 '/products?cat=beverages',
 '/products?cat=winecellar',
 '/products?cat=pets',
 '/products?cat=household&cat2=groceries&cat3=personalcare',
 '/products?cat=fruitsandvegetables',
 '/products?cat=butcher']
    return [base_url+url for url in categories]

# print(greens_categories())