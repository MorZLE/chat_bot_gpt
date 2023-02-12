@echo off

call %~dp0chat_bot_gpt\Scripts\activate

cd %~dp0D:\python\chat_bot_gpt

python main.py

pause