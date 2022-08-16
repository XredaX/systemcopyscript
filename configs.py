import os
class Config:
    ADMIN_ID = str(os.environ.get('ADMIN_ID', None))
