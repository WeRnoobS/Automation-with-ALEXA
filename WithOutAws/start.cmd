@echo off
@REM start cmd /k ..\Client_api\launch.cmd

start cmd /k python local_debugger.py --portNumber 3001 --skillEntryFile lambda_function.py --lambdaHandler lambda_handler

start cmd /k ngrok.exe http 3001
