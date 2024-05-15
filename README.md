# LlamaFile-4-ALL
A quantized LLM and API webserver in one single executable file


### How to create .exe files in Windows

- download a GGUF smaller than 4Gb (in my example qwen1_5-0_5b-chat-q8_0.gguf, from official Qwen repo: it has already chat template and tokenizer included in the GGUF)
- download the zip file for llamafile latest release [here](https://github.com/Mozilla-Ocho/llamafile/releases/download/0.8.4/llamafile-0.8.4.zip) and unzip in the same folder of the GGUF
- > rename the extension to `.exe`
- download zipalign from [here](https://github.com/Mozilla-Ocho/llamafile/releases/download/0.8.4/zipalign-0.8.4) and unzip it in the same folder
- > rename the extension to `.exe`

**nOTE**: in my video I renamed it as zip.exe

In my case i want the executable to run the API server with few more arguments (context length)

Create a `.arg` file as explained in [Creating Llamafiles](https://github.com/Mozilla-Ocho/llamafile#creating-llamafiles)

the file will contain
```
-m
qwen1_5-0_5b-chat-q8_0.gguf
--host
0.0.0.0
-c
12000
...
```

in the terminal run the following to have the base binary
```
copy .\llamafile-0.8.4.exe qwen1_5-0_5b-chat-q8.llamafile
```

Then club together with zipalign the llamafile, the GGUF file and the arguments
```
.\zipalign.exe -j0 qwen1_5-0_5b-chat-q8.llamafile qwen1_5-0_5b-chat-q8_0.gguf .args
```

Finally rename the `.llamafile` into `.exe`
```
ren qwen1_5-0_5b-chat-q8.llamafile qwen1_5-0_5b-chat-q8.exe
```

<img src='https://github.com/fabiomatricardi/LlamaFile-4-ALL/raw/main/videos/LlamaFileCREATE.gif' width=900>


### Difference between normal/--nobrowser

<img src='https://github.com/fabiomatricardi/LlamaFile-4-ALL/blob/main/videos/LlamaFileRunTerminal.gif' width=900>

### Run the Qwen model 
from the terminal run
```
.\qwen1_5-0_5b-chat-q8.exe --nobrowser
```

This will load the model and start the webserver without opening the browser.


### Python API call
```
from openai import OpenAI
import sys

# Point to the local server
client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")
history = [
    {"role": "system", "content": "You are QWEN05, an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful. Always reply in the language of the instructions."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]
print("\033[92;1m")
while True:
    userinput = ""
    completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=history,
        temperature=0.3,
        frequency_penalty  = 1.4,
        max_tokens = 600,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    print("\033[1;30m")  #dark grey
    print("Enter your text (end input with Ctrl+D on Unix or Ctrl+Z on Windows) - type quit! to exit the chatroom:")
    print("\033[91;1m")  #red
    lines = sys.stdin.readlines()
    for line in lines:
        userinput += line + "\n"
    if "quit!" in lines[0].lower():
        print("\033[0mBYE BYE!")
        break
    history = [
            {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
            ]
    history.append({"role": "user", "content": userinput})
    print("\033[92;1m")
```
Accepting multi line entries in the input: when finished Ctrl+Z and Enter

To exit type quit! and  Ctrl+Z and Enter

<img src='https://github.com/fabiomatricardi/LlamaFile-4-ALL/raw/main/videos/LlamaFileInferenceAPI.gif' width=900>


### provided Python file
you can download it from [here](https://github.com/fabiomatricardi/LlamaFile-4-ALL/raw/main/apitestqwen05.py)

---


