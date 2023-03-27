import bcrypt
  
def encrypt_pass(password: str) -> str:
    """
    To encrypt password
    """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
  
def check_pass(password: str, hash: str) -> bool:
    """
    To check password
    """
    hash = hash.encode('ascii')
    userBytes = password.encode('utf-8')
    result = bcrypt.checkpw(userBytes, hash)
    return result