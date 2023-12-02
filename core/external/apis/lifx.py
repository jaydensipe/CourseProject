import requests
import webcolors
from external.apis.external_api import ExternalAPI
from external.external import get_external_api_tokens
from helpers.helpers import Helpers


class LIFX(ExternalAPI):
    def __init__(self, name):
        super().__init__(name)
        self.set_token()

    def process_input(self, intent, human_input: str) -> None:
        self.set_token()

        if (self.token == None or self.token == ""):
            raise Exception(
                f"Please enable and provide a {self.name} token.")

        match intent:
            case "turn_light_on":
                self.__turn_on()
            case "turn_light_off":
                self.__turn_off()
            case "set_light_color":
                self.__set_color(human_input)
            case _:
                print(f"External Module ({self.name}): Cannot match intent.")

    def set_token(self) -> str:
        self.token = get_external_api_tokens().get(self.name)

    def __turn_on(self) -> None:
        response = requests.put(
            "https://api.lifx.com/v1/lights/all/state",
            auth=(self.token, ""),
            data={"power": "on"},
        )
        print(response.json())

    def __turn_off(self) -> None:
        response = requests.put(
            "https://api.lifx.com/v1/lights/all/state",
            auth=(self.token, ""),
            data={"power": "off"},
        )
        print(response.json())

    def __set_color(self, response: str) -> None:
        color = [i for i in response.split(" ") if Helpers.check_color(i)]
        response = requests.put(
            "https://api.lifx.com/v1/lights/all/state",
            auth=(self.token, ""),
            data={"color": webcolors.name_to_hex(color[0].lower())},
        )
        print(response.json())
