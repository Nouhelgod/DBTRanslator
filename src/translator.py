from googletrans import Translator


translator = Translator()

def translate(input_: str) -> str:
    """
    Translate a given string into Kazakh.

    Args:
        input_ (str): The string to be translated.

    Returns:
        str: The translated string in Kazakh.
    """
    return translator.translate(input_, dest='kk').text