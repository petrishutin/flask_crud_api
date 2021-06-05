import os
from datetime import timedelta

# app settings
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dfasfj9wer@456357sdG#!#TAY&()@$VCb3563rsdgfsa#$%34'
PROPAGATE_EXCEPTIONS = True

# app consts
TODO_STATUSES = ['TODO', 'INPROGRESS', 'DONE', 'CANCELED']

# JWT settings
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or '1d!d4rkn#@$%$G$#&5446^6dfgDSFGfdsDrff34SD0978cfs@dffsfserw234rsd'
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_BLOCK_LIST = set()

# SQLite settings
SQLITE_URL = "sqlite:///testapi.db"
