import re

def sanitize_url(user_input: str) -> str:
    # Regular expression to identify standard schemes or anything before "://"
    pattern = re.compile(r'^(https?://)?(.*)$', re.IGNORECASE)

    # Search for matches in the user input
    match = pattern.match(user_input)

    # Extract the domain and path part, ignoring any incorrect scheme
    domain_and_path = match.group(2) if match else user_input

    # In case the '://' was part of an incorrect scheme and got removed, check again for its presence
    if '://' in domain_and_path:
        # Split on '://' and take the part after it, assuming the first part is an incorrect scheme
        domain_and_path = domain_and_path.split('://', 1)[1]

    # Prepend 'https://' to ensure the correct scheme
    sanitized_url = 'https://' + domain_and_path

    return sanitized_url
