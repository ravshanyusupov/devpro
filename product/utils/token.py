import jwt, datetime


def generate_token(user):
    payload = {"phone": user['phone'],
               "id": user['id'],
               "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
               "iat": datetime.datetime.utcnow()
               }
    token = jwt.encode(payload, "secret", algorithm='HS256')
    return token