import requests
from urllib.parse import urlparse, parse_qs
import tldextract

url = "https://vk.cc/clyU0P"
# url = "https://clck.ru/33MSmy"


def getFinalUrl(url: str):
    response = requests.get(url)
    final_url = response.url

    response = requests.get(url, allow_redirects=False)

    if response.status_code == 302 and final_url == "https://away.vk.com/away.php":
        redirect_url = response.headers['Location']
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        to_url = query_params['to'][0]
        print(to_url)
    else:
        print(final_url)

def get_domain_of_ref(url: str):
    domain = tldextract.extract(url).registered_domain
    return domain


if __name__ == '__main__':
    print(getFinalUrl(url))