import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize 

def handler(event, context):

    #grabs 2 current articles from nbcnews 
    site = requests.get('https://marquee.nbcnews.com/data/bento/latest.json')
    parse1 = site.json()[0]
    parse2 = site.json()[1]
    link1 = parse1["link"]
    link2 = parse2["link"]

    #Retreveing text from links
    page1 = requests.get(link1 or "https://www.nbcnews.com/tech/tech-news/visa-moves-allow-payment-settlements-using-cryptocurrency-rcna534").text
    page2 = requests.get(link2 or "https://www.nbcnews.com/tech/tech-news/visa-moves-allow-payment-settlements-using-cryptocurrency-rcna534").text

    #turning page to beautiful Soup object 
    soup1 = BeautifulSoup(page1, 'html.parser')
    soup2 = BeautifulSoup(page2, 'html.parser')

    #get headline command
    headline1 = soup1.find('h1').get_text()
    headline2 = soup2.find('h1').get_text()

    #get text from paragraph tags 
    par_tags1 = soup1.find_all('p')
    par_tags2 = soup2.find_all('p')

    #getting text from each paragraph and striping the white
    par_tags_text1 = [tag1.get_text().strip() for tag1 in par_tags1]
    par_tags_text2 = [tag2.get_text().strip() for tag2 in par_tags2]

    # taking out any new lines and anything that does not contain a period
    sentence_list = [sentence for sentence in par_tags_text1 if not '\n' in sentence] 
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    sentence_list1 = [sentence1 for sentence1 in par_tags_text2 if not '\n' in sentence1] 
    sentence_list1 = [sentence1 for sentence1 in sentence_list1 if '.' in sentence1]

    #combine list items to string
    article1 = ' '.join(sentence_list)
    article2 = ' '.join(sentence_list1)

    #summarize function from gensim
    summary1 = summarize(article1, ratio=0.3)
    summary2 = summarize(article2, ratio=0.3)

    #summarized article1
    
    summaries = {
        "sum1": f'Article summary: \n {summary1}', 
        "sum2": f'Article summary: \n {summary2}'
    }
    x = summaries["sum1"]
    y = summaries["sum2"] 

    return x,y

print(handler(0,0))