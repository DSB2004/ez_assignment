
import os
import django
import argparse
import logging
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.user.models import User,Role
from utils.hashing import Hashing



logger = logging.getLogger(__name__)

def main(email, password,is_verified):
   
    hashed_password=Hashing.hash_password(password=password)
    User.objects.create(email=email,password=hashed_password,role=Role.OPERATION,is_verified=is_verified)
    logger.info(f"Operation user created successfully:{email}")  


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("email")
    parser.add_argument("password")
    parser.add_argument("is_verified")

    args = parser.parse_args()

    main(args.email, args.password,args.is_verified=="true")


# To run -> python scripts/create_operation_user.py johndoe@ex.com johndoe@1990 true