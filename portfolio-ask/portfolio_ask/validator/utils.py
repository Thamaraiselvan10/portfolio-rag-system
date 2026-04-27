import re


def extract_numbers(text):
    pattern = r'₹?\d+(?:,\d{3})*(?:\.\d+)?%?'
    return re.findall(pattern, text)


def normalize(num):
    return num.replace("₹", "").replace(",", "").strip()