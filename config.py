from datetime import timedelta

# app settings
SECRET_KEY = 'dfasfj9wer@456357sdG#!#TAY&()@$VCb3563rsdgfsa#$%34'
PROPAGATE_EXCEPTIONS = True

# JWT settings
JWT_SECRET_KEY = 'sdfsdirkn#@$%$#G$#&5446^6dfgDSFGfdsDrff34SD0978cf'
JWT_TOKEN_LOCATION = "headers"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# MySQL settings
MYSQL_HOST: str = 'bzteltestapi.mysql.pythonanywhere-services.com'
MYSQL_USER: str = 'testapi'
MYSQL_PASSWORD: str = 'sDS2745tTJt2q5K'
MYSQL_DB: str = 'bzteltestapi'
MYSQL_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

# SQLite settings
SQLITE_URL = "sqlite:///testapi.db"
