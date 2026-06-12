from urllib.parse import urlparse

# simple blacklist list
BLACKLIST = [
    "phishing.com",
    "malicious.com",
    "badsite.net"
]

def check_blacklist(url):
    domain = urlparse(url).netloc

    for bad in BLACKLIST:
        if bad in domain:
            return True

    return False