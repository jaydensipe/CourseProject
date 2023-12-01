import json


def load_external_api_tokens() -> None:
    global external_api_tokens

    with open("core/settings.json", "r") as f:
        external_api_tokens = json.load(f).get("api_keys")


def save_external_api_tokens(api: str, new_value: str) -> None:
    if (new_value == None or new_value == ""):
        raise Exception(
            "Please provide a valid value for the API token.")

    external_api_tokens[api] = new_value.strip()
    with open("core/settings.json", "w") as f:
        json.dump({"api_keys": external_api_tokens}, f, indent=4)


def get_external_api_tokens() -> dict:
    return external_api_tokens
