from dotenv import load_dotenv
from termcolor import cprint
import os

def env_to_var(name: str) -> str:
    cprint(f"Getting {name} from .env file.", "blue", attrs=["bold"])
    load_dotenv()
    var = os.getenv(name)
    
    if var == None:
        raise Exception(f"{name} not found in .env file.")
    
    return var

def main() -> None:
    print(env_to_var("GROQ_KEY"))

if __name__ == '__main__':
    main()