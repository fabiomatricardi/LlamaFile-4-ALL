@echo off
d:
cd D:\HFTESTS\#nanollava
echo call python310 -m venv venv
call .\venv\Scripts\activate.bat
echo pip install openai
echo streamlit run .\st-Qwen1.5-110B-Chat.py
echo copy .\llamafile-0.8.4.exe qwen1_5-0_5b-chat-q8.llamafile
echo .\zipalign.exe -j0 qwen1_5-0_5b-chat-q8.llamafile qwen1_5-0_5b-chat-q8_0.gguf .args
echo ren qwen1_5-0_5b-chat-q8.llamafile qwen1_5-0_5b-chat-q8.exe
start cmd.exe /k .\qwen1_5-0_5b-chat-q8.exe --nobrowser
python .\autoQwen.py
PAUSE