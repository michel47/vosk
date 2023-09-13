#!/usr/bin/env python3

import subprocess
import sys
import json

from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(1)

SAMPLE_RATE = 16000
model = Model(lang="fr")

# Large vocabulary free form recognition
rec = KaldiRecognizer(model, SAMPLE_RATE)

# You can also specify the possible word list
#rec = KaldiRecognizer(model, 16000, "zero oh one two three four five six seven eight nine")

with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                            sys.argv[1],
                            "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                            stdout=subprocess.PIPE) as process:

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            #print(rec.Result())
            res = json.loads(rec.Result())
            print(res["text"])

    res = json.loads(rec.FinalResult())
    print(res["text"])
