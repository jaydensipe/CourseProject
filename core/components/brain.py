import signal
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from enum import Enum
from components.mouth import Mouth
from helpers.helpers import Helpers
from tensorflow.keras.models import load_model
import os
import json
import pickle
import numpy as np
import random
from external.lifx import LIFX
from external.openweather import OpenWeather


class Brain:
    # Brain states
    class BrainState(Enum):
        THINKING = 1
        SPEAKING = 2

    current_state = BrainState.THINKING
    intents = json.loads(
        open("core/training/intents/intents.json").read()
    )  # Load intents.json file
    words = pickle.load(open("core/training/intents/words.pkl", "rb"))
    classes = pickle.load(open("core/training/intents/classes.pkl", "rb"))
    model = load_model("core/training/intents/squire_assistant.keras")

    def __init__(self, name: str, personality: str) -> None:
        self.name = name
        self.personality = personality

    # Awakens Squire
    def awaken(self) -> None:
        # Loads external pieces
        self.__load_external()

    def __load_external(self) -> None:
        # Initialize GPT
        global receptor
        receptor = self.__initialize_gpt()

        # Initialize LIFX
        global lifx
        lifx = LIFX()

        global weather
        weather = OpenWeather()

    def __initialize_gpt(self) -> None:
        prompt = PromptTemplate(
            input_variables=["history", "human_input"],
            template=self.personality,
        )

        chatgpt_chain = LLMChain(
            llm=OpenAI(
                temperature=0,
                openai_api_key=os.getenv("open_ai_key"),
            ),
            prompt=prompt,
            memory=ConversationBufferWindowMemory(k=2),
        )

        return chatgpt_chain

    def interpret_and_reflect(self, human_input: str) -> None:
        self.current_state = Brain.BrainState.THINKING

        try:
            # Process the input
            self.__process_input(human_input=human_input)
        except Exception as e:
            Mouth.speak(
                "Sorry, an error has occurred while processing your input. Reason: " + str(e), is_error=True)

    def __process_input(self, human_input: str) -> None:
        # Get intent from speech
        intent = self.__predict_class(sentence=human_input)

        # Begin speaking
        self.current_state = Brain.BrainState.SPEAKING

        # Match intent to an action and speak
        self.__match_intent(intent=intent, human_input=human_input)

    def __match_intent(self, intent, human_input: str = "") -> None:
        match (intent[0]["intent"]):
            case "turn_light_on" | "turn_light_off" | "set_light_color":
                lifx.process_input(
                    intent=intent[0]["intent"], human_input=human_input)
                Mouth.speak(self.__get_response(intent_list=intent))
            case "get_weather":
                weather.process_input(
                    intent=intent[0]["intent"], human_input=human_input)
            case "shut_down":
                os.kill(os.getpid(), signal.SIGTERM)
            case "talk_to_gpt":
                Mouth.speak(receptor.predict(human_input=human_input))
            case _:
                # Default to GPT if cannot match intent
                Mouth.speak(receptor.predict(human_input=human_input))

    def __bag_of_words(self, sentence: str) -> None:
        sentence_words = Helpers.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1

        return np.array(bag)

    def __predict_class(self, sentence: str) -> None:
        bow = self.__bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append(
                {"intent": self.classes[r[0]], "probability": str(r[1])})

        return return_list

    def __get_response(self, intent_list: list) -> str:
        tag = intent_list[0]["intent"]
        list_of_intents = self.intents["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                if (len(i["responses"]) == 0):
                    result = ""
                    break

                result = random.choice(i["responses"])
                break

        return result
