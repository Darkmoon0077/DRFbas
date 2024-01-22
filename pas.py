from django.contrib.auth.hashers import make_password
from django.conf import settings
settings.configure()
hashed_password = make_password("nimda4321")
print(hashed_password)
