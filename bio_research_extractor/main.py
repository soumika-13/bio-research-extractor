import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_arxiv_data():
    url = "https://arxiv.org/search/?query=machine+learning&searchtype=all&source=header"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all("li", class_="arxiv-result")

    data_list = []

    for i, result in enumerate(results[:5], 1):
        title = result.find("p", class_="title").get_text(strip=True)
        authors = result.find("p", class_="authors").get_text(strip=True).replace("Authors:", "")
        abstract = result.find("span", class_="abstract-full").get_text(strip=True).replace("▼ Less", "").replace("▲ More", "")
        pdf_tag = result.select_one("p.list-title a[href*='pdf']")
        pdf_link = "https://arxiv.org" + pdf_tag['href'] if pdf_tag else "N/A"

        data_list.append({
            "Title": title,
            "Authors": authors,
            "Abstract": abstract,
            "PDF Link": pdf_link
        })

        print(f"\n📄 {i}. {title}")
        print(f"👩‍💻 Authors: {authors}")
        print(f"📝 Abstract: {abstract}")
        print(f"📎 PDF Link: {pdf_link}")

    # Save to CSV
    if data_list:
        df = pd.DataFrame(data_list)
        df.to_csv("papers.csv", index=False)
        print("\n✅ Research paper data saved to papers.csv")
    else:
        print("\n⚠️ No data extracted. Please check the source site or scraping logic.")

if __name__ == "__main__":
    print("✅ Extracting Research Paper Data from arXiv...\n")
    extract_arxiv_data()
