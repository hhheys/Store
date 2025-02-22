import hashlib
from fastapi.templating import Jinja2Templates

def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

templates = Jinja2Templates(directory="../templates")
