from types import SimpleNamespace


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "6cb202ccb3e6d592920c7011309710a8baac34ec7bd8db075abc753c9fab3032"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Tags for sorting requests in OpenAPI
TAGS = SimpleNamespace(
    USER='Users',
    GAME='Games',
    AUTH='Authentication'
)