import requests
from bs4 import BeautifulSoup

#HELPER FUNCTIONS
def get_html(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

#INTERNAL FUNCTIONS
def get_article_heading(url):
    try:
        #TODO: Do this in a prettier way!?
        if "gp.se" in url:
            return get_gp_heading(url)
        elif "aftonbladet.se" in url:
            return get_aftonbladet_heading(url)
        elif "expressen.se" in url:
            return get_expressen_heading(url)
        elif "svt.se" in url: 
            return get_svt_heading(url)
        elif "dn.se" in url: 
            return get_dn_heading(url)
        elif "svd.se" in url: 
            return get_svd_heading(url)
        elif "sverigesradio.se" in url: 
            return get_sr_heading(url)
        elif "kvartal.se" in url: 
            return get_kvartal_heading(url)
        elif "resume.se" in url: 
            return get_resume_heading(url)
        elif "nyheteridag.se" in url: 
            return get_nyheteridag_heading(url)
        elif "bulletin.nu" in url: 
            return get_bulletin_heading(url)
        elif "fokus" in url: 
            return get_bulletin_heading(url)
        else:
            return get_generic_heading(url)
    except Exception as e:
        print("Error. Returning url: " + url)
        return url

######TWITTER EVENTS###########

def get_gp_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1', class_='c-article__heading')
    heading = elements[0].text
    return heading.replace('\n', ' ')

def get_aftonbladet_heading(url):
    soup = get_html(url)
    elements = soup.findAll("h1",attrs={"data-test-id":"headline"})
    heading = elements[0].text
    return heading.replace('\n', ' ')

def get_expressen_heading(url):
    soup = get_html(url)
    elements = soup.find_all('header', class_='article__header')
    heading = elements[0].find('h1').text
    return heading.replace('\n', ' ')

def get_svt_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1', class_='nyh_article__heading')
    heading = elements[0].text
    return heading.replace('\n', ' ')
    
def get_dn_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1', class_='article__title')
    heading = elements[0].text
    return heading.replace('\n', ' ')

def get_svd_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1', class_='ArticleHead-heading')
    heading = elements[0].text
    return heading.replace('\n', ' ')

def get_sr_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1', class_='heading')
    heading = elements[0].text
    return heading.replace('\n', ' ')

def get_kvartal_heading(url):
    soup = get_html(url)
    elements = soup.find_all('article')
    heading = elements[0].find('h1').text
    return heading.replace('\n', ' ')

def get_bulletin_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1')
    heading = elements[0].text
    return heading.replace('\n', ' ')

def get_fokus_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1', class_=sdsd)
    heading = elements[0].find('h1').text
    return heading.replace('\n', ' ')

def get_nyheteridag_heading(url):
    soup = get_html(url)
    elements = soup.find_all('article', class_='article')
    heading = elements[0].find('h1').text
    return heading.replace('\n', ' ')

def get_resume_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1')
    heading = elements[0].text
    return heading.replace('\n', ' ')

def get_generic_heading(url):
    soup = get_html(url)
    elements = soup.find_all('h1')
    heading = elements[0].text
    return heading.replace('\n', ' ')

########POLICE EVENTS#############

def get_police_details(police_url):
    soup = get_html(police_url)
    details = ""
    details_body = soup.find_all('div', class_='text-body editorial-html')
    for details in details_body:
        details = details.text + "\r" 
    print("Url: " + police_url + " has been updated with details: " + details)
    return str(details)


