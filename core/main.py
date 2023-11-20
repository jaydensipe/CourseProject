from dotenv import load_dotenv
import handler

def main() -> None:
    # Load environment variables
    load_dotenv()
    

if __name__ == "__main__":
    main()
    handler.start_threads()