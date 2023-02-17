import re

# Sample text
text = "This is a sample text with a referral link: https://example.com/?ref=abc123. Here is a link with UTM parameters: http://www.example.org/foo/bar/?utm_source=google&utm_medium=cpc&utm_campaign=summer_sale"

# Define the regular expression pattern to match tracking links and capture the entire URL
pattern = r'\b(https?:\/\/\S+\.\S+\/\S*\?(ref|utm_source)=\S+)\b'

# Find all matches of the pattern in the text and extract the captured URLs
matches = re.findall(pattern, text)
links = [match[0] for match in matches]

# Print the links
print(links)