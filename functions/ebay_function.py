from bs4 import BeautifulSoup
import requests
import pandas as pd
import math

def category_no(keyword = str) -> int:
  '''
  This function returns an integer for item category for collect_ebay function.
  It returns 1 for bracelet, 2 for shoes and 3 for dress.

  Parameters:

  keyword (str): bracelet, shoes or dress

  Returns:

  int: id number for category
  '''

  if keyword == "bracelet":
      number = 1
  elif keyword == "shoes":
      number = 2
  elif keyword =="dress":
      number = 3
  return number


def collect_ebay(no_examples = int, keyword = str) -> pd.DataFrame:
  '''
  This function performs scraping on on ebay UK website for a specified category of item and returns
  pandas dataframe with information about shop items.

  Parameters:

  no_examples (int): number of samples of item categories to be returned
  keyword (str): an item category to be searched on ebay

  Returns:

  pd.DataFrame: pandas dataframe table with no_examples samples of keyword category. Item's category number, title, price,
  url to item and url of item's image are returned in the table format.

  '''

  #creating variables to store data from ebay
  category = []
  titles = []
  prices = []
  urlItems = []
  urlImages = []

  #calculating the number of iterations needed to scrape the requested number of samples
  no_iterations = math.ceil((no_examples/192))
  
  #scraping ebay website
  for iteration in range(1, no_iterations+1):
    page = requests.get(f"https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={keyword}&_sacat=1&_ipg=192&_pgn={iteration}", headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'}))
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", class_="s-item__wrapper clearfix")

    #scraping necessary information for table
    for item in items:

      #item category
      category.append(keyword)

      #item title
      title = item.find("h3", class_="s-item__title").getText()
      titles.append(title)

      #item price
      price = item.find("span", class_="s-item__price").getText()
      prices.append(price)

      #url to item page
      urlItem = item.find("a", class_="s-item__link")["href"]
      urlItems.append(urlItem)

      #url to item image
      urlImage = item.find("img", class_="s-item__image-img")["src"]
      urlImages.append(urlImage)
  
  #applying category_no function for each element in category column to give category id for each category
  category = [category_no(i) for i in category]

  #returning pandas dataframe table
  ebay = pd.DataFrame({
      "category" : category,
      "title" : titles,
      "price" : prices,
      "urlItem" : urlItems,
      "urlImage" : urlImages
  })
  return ebay


