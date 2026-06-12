import re
def calculate_risk_score(url):
    """
    Analyzes a URL based on a set of heuristic rules and returns a risk score.
    """
    score = 0
    reasons = []

    # Rule 1: Check for IP Address in the domain
    try:
        hostname = url.split('/')[2]
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname):
            score += 3
            reasons.append("URL uses an IP address instead of a domain name.")
    except IndexError:
        # Handle cases where the URL format is unusual and doesn't have a hostname
        score += 1
        reasons.append("URL has an unusual format.")
        return score, reasons  # Exit early if format is too strange

    # Rule 2: Check for suspicious keywords
    suspicious_keywords = ['login', 'secure', 'account', 'update', 'signin', 'banking', 'verify']
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        score += 2
        reasons.append("URL contains suspicious keywords.")

    # Rule 3: Check for excessive URL length
    if len(url) > 75:
        score += 1
        reasons.append("URL is unusually long.")

    # Rule 4: Count of special characters
    if len(re.findall(r'[.-_@?=&]', url)) > 10:
        score += 1
        reasons.append("URL contains an excessive number of special characters.")

    # Rule 5: Presence of '@' symbol
    if '@' in url:
        score += 2
        reasons.append("URL contains an '@' symbol, which can be used for trickery.")

    # Rule 6: Number of subdomains
    if hostname.count('.') > 3:
        score += 2
        reasons.append("URL has an excessive number of subdomains.")

    return score, reasons


def get_verdict(score):
    """
    Returns a verdict based on the calculated risk score.
    """
    if score >= 5:
        return "High Risk (Likely Malicious)"
    elif score >= 3:
        return "Medium Risk (Suspicious)"
    else:
        return "Low Risk (Likely Benign)"


# --- Main part of the script ---
if __name__ == "__main__":
    # Get a URL from the user
    input_url = input("Enter the URL you want to check: ")

    # Calculate the risk score and get the reasons
    risk_score, analysis_reasons = calculate_risk_score(input_url)

    # Get the final verdict
    verdict = get_verdict(risk_score)

    # Print the final report
    print(f"\n--- Analysis Report for: {input_url} ---")
    print(f"Final Verdict: {verdict}")
    print(f"Calculated Risk Score: {risk_score}")
    if analysis_reasons:
        print("Reasons for score:")
        for reason in analysis_reasons:
            print(f"- {reason}")
    else:
        print("No suspicious patterns were found.")