import re

def extract_lexical_features(url):
    features = []
    features.append(len(url))
    features.append(len(re.findall(r'[.-_@?=&]', url)))

    suspicious_keywords = ['login','secure','account','update','signin','banking']
    features.append(1 if any(k in url.lower() for k in suspicious_keywords) else 0)

    try:
        hostname = url.split('/')[2]
        features.append(1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname) else 0)
    except:
        features.append(0)

    return features