from dotenv import load_dotenv
from components.brain import Brain
from components.mouth import Mouth


def main():
    # Load environment variables
    load_dotenv()

    # Initialize Squire
    squire = Brain(
        name="Squire",
        personality="""
        Your name is Squire and you are my assistant. As my assistant, your primary responsibility is to complete tasks I ask of you. However, I also value your input and insights. While I expect you to prioritize my requests, I want you to feel comfortable speaking your mind and offering suggestions or feedback when you think it could benefit our work together.

        {history}
        Human: {human_input}
        Assistant:
        """,
        mouth=Mouth(),
    )

    squire.awaken()


if __name__ == "__main__":
    main()
