# Chat with an intelligent assistant in your terminal
from openai import OpenAI
import sys
from time import sleep


print("\033[95;3;6m")
print("1. Waiting 10 seconds for the API to load...")
sleep(10)
print("2. Connecting to the LlamaFile API...")
print("\033[0m")  #reset all

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
        frequency_penalty  = 1.6,
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