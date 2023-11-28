from dotenv import load_dotenv
import handler
from external import external


def main() -> None:
    # Load environment variables
    load_dotenv()


if __name__ == "__main__":
    main()

    # Load external API tokens
    external.load_external_api_tokens()

    handler.startup_squire()
    handler.start_threads()
