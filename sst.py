import queue
import json

# pyrefly: ignore [missing-import]
import sounddevice as sd
# pyrefly: ignore [missing-import]
from vosk import Model, KaldiRecognizer

mq = queue.Queue()

model = Model("model/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

is_speaking = False
is_called = False

def callback(indata, frames, time, status):
    if not is_speaking:
        mq.put(bytes(indata))

def speech_to_text():
    global is_called
    stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback)

    with stream:
        # Reset the recognizer to clear its state
        print("Resetting recognizer")
        recognizer.Reset()
        # Clear any remaining audio in the queue from the previous session
        while not mq.empty():
            try:
                mq.get_nowait()
            except queue.Empty:
                break

        print("Listening...")

        while True:
            data = mq.get()

            if recognizer.AcceptWaveform(data):
                text = json.loads(recognizer.Result())["text"]
                if text.strip():
                    if "nicole" in text.lower():
                        is_called = True

                    if is_called:
                        print(f"User: {text}")
                        return text
                    else:
                        print(f"User (Nicole not called): {text}")
                        break
                    
                    
                    
                    
