from dotenv import load_dotenv
from pathlib import Path
import os

def get_user_creds():
    '''
    check env for previously stored creds
    if none create local env to store user input creds
    return USER and PASS
    '''
    env_path = Path('.') / '.env'
    if Path.is_file(env_path): # you already logged in successfully
        pass
    else: # you have not yet logged in successfully
        with open(".env", "w") as f:
            f.write("USER = '{}'".format(str(input("Enter username: "))))
            f.write("\n")
            f.write("PASS = '{}'".format(str(input("Enter password: "))))
        
    load_dotenv(dotenv_path=env_path)
    USER = os.getenv("USER")
    PASS = os.getenv("PASS")
    return USER, PASS