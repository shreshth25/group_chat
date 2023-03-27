import secrets

def email_generator():
    return f"{secrets.token_hex(8)}@gmail.com"
        