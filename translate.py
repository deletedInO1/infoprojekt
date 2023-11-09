from googletrans import Translator
translator = Translator()
def translate(x):
    return translator.translate(x, dest="en", src="de").text