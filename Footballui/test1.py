import PySimpleGUI as sg

sg.theme("Reds")
# Define the window's contents

ask_layout = [
    [sg.Text('Do you want to "Login" or "Create"?')],
    [sg.Input(key="input")],
    [sg.Text(key="error")],
    [sg.Button("Submit")],
]
window = sg.Window("Login/Create", ask_layout)
event, values = window.read()
print(values["input"].lower())
window.close()
login_layout = [
    [sg.Text("Login")],
    [sg.Text("Username"), sg.Input(key="username", size=(20, 1), justification="left")],
    [
        sg.Text("Password"),
        sg.Input(key="password", size=(20, 1), justification="left", password_char="*"),
    ],
    [sg.Text(key="error")],
    [sg.Button("Submit")],
]
window = sg.Window("Login", login_layout)
event, values = window.read()
window.close()
create_layout = [
    [sg.Text("Create")],
    [sg.Text("Username"), sg.Input(key="username", size=(20, 1), justification="left")],
    [
        sg.Text("Password"),
        sg.Input(key="password", size=(20, 1), justification="left", password_char="*"),
    ],
    [sg.Text(key="error")],
    [sg.Button("Submit")],
]
window = sg.Window("Create", create_layout)
event, values = window.read()
window.close()


main_layout = [
    [sg.Text(f"Current balance is 'user['team']['money']'M")],
    [sg.Text("It costs 10M to upgrade or 5M to train")],
    [sg.Text("Please select an action (upgrade, train, play):")],
    [sg.Text(key="error")],
    [
        sg.Button("Upgrade", key="upgrade"),
        sg.Button("Train", key="train"),
        sg.Button("Play", key="play"),
    ],
]
window = sg.Window("Main", main_layout)
event, values = window.read()
print(event)
window.close()
used_teams = []
user = {"team": {"name": "Your Team"}}
teams = [{"name": "Team 1"}, {"name": "Team 2"}, {"name": "Team 3"}]

select_layout = [
    [sg.Text("Please select an opponent:")],
    [
        sg.Listbox(
            values=[
                team["name"] for team in teams if team["name"] != user["team"]["name"]
            ],
            size=(20, 5),
            key="opponent",
            enable_events=False,
        )
    ],
    [sg.Text(key="error")],
    [sg.Button("Select")],
]

window = sg.Window("Select A Team", select_layout)
event, values = window.read()
print(values)
window.close()

userteamselect_layout = [
    [sg.Text("Please select a team:")],
    [
        sg.Listbox(
            values=[team["name"] for team in teams if team["name"] not in used_teams],
            size=(20, 5),
            key="team",
            enable_events=False,
        )
    ],
    [sg.Text(key="error")],
    [sg.Button("Select")],
]

window = sg.Window("Select A Team", userteamselect_layout)
event, values = window.read()
print(values)
window.close()
