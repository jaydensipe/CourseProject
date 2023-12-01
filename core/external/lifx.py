import requests
import os
from colour import Color
import webcolors
from external.external import get_external_api_tokens


class LIFX:
    def __init__(self):
        self.set_token()

    def process_input(self, intent, human_input: str) -> None:
        self.set_token()

        if (self.token == None or self.token == ""):
            raise Exception(
                "Please enable and provide a LIFX token.")

        match intent:
            case "turn_light_on":
                self.__turn_on()
            case "turn_light_off":
                self.__turn_off()
            case "set_light_color":
                self.__set_color(human_input)
            case _:
                print("External Module (LIFX): Cannot match intent.")

    def set_token(self) -> str:
        self.token = get_external_api_tokens().get("lifx")

    def get_status(self) -> None:
        response = requests.get(
            "https://api.lifx.com/v1/lights/all", auth=(self.token, "")
        )
        print(response.json())

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
        color = [i for i in response.split(" ") if self.__check_color(i)]
        response = requests.put(
            "https://api.lifx.com/v1/lights/all/state",
            auth=(self.token, ""),
            data={"color": webcolors.name_to_hex(color[0].lower())},
        )
        print(response.json())

    @staticmethod
    def __check_color(color) -> bool:
        try:
            Color(color)
            return True
        except ValueError:
            return False
