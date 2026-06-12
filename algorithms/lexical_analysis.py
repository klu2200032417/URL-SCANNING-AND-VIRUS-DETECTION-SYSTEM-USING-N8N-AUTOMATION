import re


def calculate_risk_score(url):

    score = 0

    # Extract hostname safely
    try:
        hostname = url.split('/')[2]
    except:
        hostname = url

    # Suspicious keywords
    suspicious_keywords = [
        "login",
        "secure",
        "account",
        "update",
        "signin",
        "bank",
        "verify",
        "password",
        "confirm"
    ]

    # Check keywords anywhere in URL
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        score += 2

    # Rule: IP address instead of domain
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname):
        score += 3

    # Rule: Very long URL
    if len(url) > 75:
        score += 1

    # Rule: Too many special characters
    if len(re.findall(r'[.\-_@?=&]', url)) > 10:
        score += 1

    # Rule: '@' symbol trick
    if '@' in url:
        score += 2

    # Rule: Excessive subdomains
    if hostname.count('.') > 3:
        score += 2

    return score


def lexical_detect(url):

    score = calculate_risk_score(url)

    # Threshold for suspicious detection
    if score >= 2:
        return True
    else:
        return False