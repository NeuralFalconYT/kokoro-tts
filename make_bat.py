bat_content = '''@echo off
call myenv\\Scripts\\activate
@python.exe app.py %*
@pause
'''

# Save the content to a .bat file
with open('run_app.bat', 'w') as bat_file:
    bat_file.write(bat_content)

print("The 'run_app.bat' file has been created.")
