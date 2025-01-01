# Batch content for running app.py
bat_content_app = '''@echo off
call myenv\\Scripts\\activate
@python.exe app.py %*
@pause
'''

# Save the content to run_app.bat
with open('run_app.bat', 'w') as bat_file:
    bat_file.write(bat_content_app)

print("The 'run_app.bat' file has been created.")

# Batch content for running cli.py
bat_content_cli = '''@echo off
call myenv\\Scripts\\activate
@python.exe cli.py %*
@pause
'''

# Save the content to run_cli.bat
with open('run_cli.bat', 'w') as bat_file:
    bat_file.write(bat_content_cli)

print("The 'run_cli.bat' file has been created.")

# Batch content for running get_latest_voices.py
bat_content_voices = '''@echo off
call myenv\\Scripts\\activate
@python.exe get_latest_voices.py %*
@pause
'''
# Save the content to run_get_latest_voices.bat
with open('get_new_voice.bat', 'w') as bat_file:
    bat_file.write(bat_content_voices)
print("The 'get_new_voice.bat' file has been created.")
