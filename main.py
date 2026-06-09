
# pyrefly: ignore [missing-import]
from sst import speech_to_text
from llm import llm_model
# pyrefly: ignore [missing-import]
from tts import speak

while True:
    query = speech_to_text()

    if query:
        response = llm_model(query)
        print("Miko: ", response)
        speak(response)
    
        