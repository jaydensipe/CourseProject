import spacy


class Helpers:

    # Initialize NLP
    global nlp
    nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def clean_up_sentence(sentence: str) -> None:
        # Lemmatize each word
        sentence_words = nlp(sentence)
        lemmatized_words = [token.lemma_ for token in sentence_words]

        return lemmatized_words
