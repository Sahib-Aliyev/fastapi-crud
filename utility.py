import bcrypt

def hashPassword(password):
    salt = bcrypt.gensalt()  
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verifyPassword(stored_password, input_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password)