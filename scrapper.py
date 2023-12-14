import requests
from bs4 import BeautifulSoup
import re
import csv

user_tag = input("Enter tag: ")
valid_tag = re.search("^[a-zA-Z]+(?:-[a-zA-Z]+)*$", user_tag)

def page_has_content(soup):
    row_divs = soup.find_all(class_ = "row")
    res = row_divs[1]
    return not("No quotes found" in res.find(class_ = "col-md-8").text)

def make_pages_run(inp_tag, page_num = 0):
  quotesList = []

  while True:
    page_num += 1

    TARGET_URL = f"http://quotes.toscrape.com/page/{page_num}/"

    page = requests.get(TARGET_URL)

    if page.status_code == 200:
      soup = BeautifulSoup(page.content, "html.parser")
      is_content = page_has_content(soup)

      if is_content:
        quotes = soup.find_all("div", class_ = "quote")

        for quote in quotes:
          tagsDiv = quote.find(class_="tags")
          tags = tagsDiv.find_all("a", class_ = "tag")
          tagsList = []

          for tag in tags:
            tagsList.append(tag.text)

          if inp_tag in tagsList:
            quotesList.append(quote)
            
      else:
        if quotesList:
          return quotesList
        else: 
          print(f"No quotes were found for the tag: {inp_tag}")
          break
    
    else:
      print("Something went wrong")
      break

def convert_result_data(results: list):
  converted_result_list = []

  for result in results:
    quote = result.find(class_ = "text").text
    author = result.find(class_ = "author").text
    
    converted_result_list.append({"text": quote, "author": author})

  return converted_result_list

if valid_tag:
  result = make_pages_run(user_tag)

  if result:
    data_list = convert_result_data(result)

    with open(f"{user_tag}_quotes.csv", "w", encoding="UTF8") as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow(["author", "quote"])

      for data in data_list:
        writer.writerow([data["author"], data["text"]])

    print("CSV file successfully created")

else:
  print("Invalid tag")