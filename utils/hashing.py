import bcrypt 


class Hashing:
    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8') 

    @staticmethod
    def check_password(password,hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))