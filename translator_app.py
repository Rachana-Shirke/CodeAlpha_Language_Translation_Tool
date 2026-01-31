
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import ipywidgets as widgets
from IPython.display import display, Audio, clear_output

translator = Translator()

text_input = widgets.Textarea(
    placeholder='Enter text to translate',
    description='Text:',
    layout=widgets.Layout(width='700px', height='150px')
)
display(text_input)

language_names = list(LANGUAGES.values())
source_lang = widgets.Dropdown(options=language_names, value='english', description='Source:')
target_lang = widgets.Dropdown(options=language_names, value='hindi', description='Target:')
display(source_lang, target_lang)

output = widgets.Output()

def translate_text(b):
    with output:
        clear_output()
        if text_input.value.strip() == "":
            print(" Please enter some text.")
            return
        
        try:
            src_code = [k for k, v in LANGUAGES.items() if v == source_lang.value][0]
            tgt_code = [k for k, v in LANGUAGES.items() if v == target_lang.value][0]

            result = translator.translate(text_input.value, src=src_code, dest=tgt_code)
            print(" Translated Text:
")
            print(result.text)

            global translated_text
            translated_text = result.text
            global target_code
            target_code = tgt_code

        except Exception as e:
            print(" Translation failed. Check internet connection.")

translate_button = widgets.Button(description="Translate")
translate_button.on_click(translate_text)
display(translate_button, output)

copy_output = widgets.Textarea(
    placeholder='Translated text will appear here for easy copy',
    layout=widgets.Layout(width='700px', height='100px')
)

def show_copy_area(b):
    try:
        copy_output.value = translated_text
        display(copy_output)
    except:
        print("Translate text first.")

copy_button = widgets.Button(description="Copy Text")
copy_button.on_click(show_copy_area)
display(copy_button)

def speak_text(b):
    try:
        tts = gTTS(text=translated_text, lang=target_code)
        tts.save("speech.mp3")
        display(Audio("speech.mp3", autoplay=True))
    except:
        print(" Text-to-speech not supported.")

tts_button = widgets.Button(description=" Speak Translation")
tts_button.on_click(speak_text)
display(tts_button)
