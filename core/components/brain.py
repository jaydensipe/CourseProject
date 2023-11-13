from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from enum import Enum
from components.mouth import Mouth
import preprogrammed.responses as responses
import os
from external.lifx import LIFX
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


class Brain:
    # Brain states
    class BrainState(Enum):
        THINKING = 1
        SPEAKING = 2
        ALERT = 3

    current_state = BrainState.THINKING
    lamatizer = WordNetLemmatizer()
    intents = json.loads(
        open("core/training/intents/intents.json").read()
    )  # Load intents.json file
    words = pickle.load(open("core/training/intents/words.pkl", "rb"))
    classes = pickle.load(open("core/training/intents/classes.pkl", "rb"))
    model = load_model("core/training/intents/squire_assistant.keras")

    def __init__(self, name: str, personality: str, mouth: Mouth) -> None:
        self.name = name
        self.personality = personality
        self.mouth = mouth

    # Awakens Squire
    def awaken(self):
        print("Hello, my name is " + self.name + ". How can I help you?")

        # Initialize GPT
        receptor = self.__initialize_gpt()

        # Begin listening and responding
        self.__interpret_and_reflect(receptor)

    def __initialize_gpt(self):
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

    def __interpret_and_reflect(self, receptor: LLMChain) -> None:
        lifx = LIFX()

        while True:
            if self.current_state != Brain.BrainState.ALERT:
                self.current_state = Brain.BrainState.THINKING

            print("Speak Anything: ")
            try:
                # Process the input
                self.__process_input(
                    receptor=receptor, lifx=lifx, human_input=str(input()))
            except Exception as e:
                print("Sorry, an error has occurred while processing your input. Reason: " + str(e))

    def __process_input(self, receptor: LLMChain, lifx: LIFX, human_input: str) -> None:
        # Get intent from speech
        intent = self.__predict_class(sentence=human_input)

        # If we are in Alert, disregard messages unless they are to end the alert
        if self.current_state == Brain.BrainState.ALERT:
            if intent[0]["intent"] == "end_alert_response":
                self.mouth.speak(self.__get_response(intent_list=intent))
                self.__reset_state()
                return

            self.mouth.speak(responses.continued_alert_response)
            return

        # Begin speaking
        self.current_state = Brain.BrainState.SPEAKING

        # Match intent to an action
        match (intent[0]["intent"]):
            case "turn_light_on":
                lifx.turn_on()
            case "turn_light_off":
                lifx.turn_off()
            case "set_light_color":
                lifx.set_color(response=human_input)
            case "initiate_alert_response":
                self.mouth.speak(responses.initiated_alert)
                self.current_state = Brain.BrainState.ALERT
            case "shut_down":
                exit()
            case "talk_to_gpt":
                self.mouth.speak(receptor.predict(human_input=human_input))
            case _:
                self.mouth.speak(receptor.predict(human_input=human_input))

    def __clean_up_sentence(self, sentence: str):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lamatizer.lemmatize(
            word) for word in sentence_words]

        return sentence_words

    def __bag_of_words(self, sentence: str):
        sentence_words = self.__clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1

        return np.array(bag)

    def __predict_class(self, sentence: str):
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
                result = random.choice(i["responses"])
                break

        return result

    # Reset the state of the brain to THINKING
    def __reset_state(self) -> None:
        self.current_state = Brain.BrainState.THINKING
