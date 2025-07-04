import re

def custom_slugify(text):
    text = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF\s]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')
