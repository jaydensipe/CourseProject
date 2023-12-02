from external.apis.external_api import ExternalAPI
from external.external import get_external_api_tokens
from langchain.document_loaders import WeatherDataLoader
from helpers.helpers import Helpers
from components.mouth import Mouth


class OpenWeather(ExternalAPI):
    def __init__(self, name):
        super().__init__(name)
        self.set_token()

    def process_input(self, intent, human_input: str) -> None:
        self.set_token()

        if (self.token == None or self.token == ""):
            raise Exception(
                f"Please enable and provide an {self.name} token.")

        match intent:
            case "get_weather":
                self.__get_weather(human_input)
            case _:
                (f"External Module ({self.name}): Cannot match intent.")

    def set_token(self) -> str:
        self.token = get_external_api_tokens().get(self.name)

    def __get_weather(self, human_input: str) -> None:
        loader = WeatherDataLoader.from_params(
            [Helpers.extract_location(human_input).title()], openweathermap_api_key=self.token
        )

        documents = loader.load()
        if (len(documents) == 0):
            raise Exception("No weather data found.")

        # Speak the weather data
        Mouth.speak(documents[0].page_content)
