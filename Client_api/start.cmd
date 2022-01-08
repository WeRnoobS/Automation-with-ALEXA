@echo off
 
 
start cmd /k ngrok-start.cmd
timeout /t 5 /nobreak
start cmd /k launch.cmd
python Location.py
 
start https://alexa2automation.herokuapp.com/read?id=url
start https://alexa2automation.herokuapp.com/
