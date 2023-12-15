import json
import math
import os
import sys
import time
import threading
from getpass import getpass
import random
from endecoder import decode, encode
import PySimpleGUI as sg
from field import Field

threading_main = False


def create_layout_game():
    layout = [
        [
            sg.Text("Passes Completed:", size=(15, 1)),
            sg.Text("", key="passes_completed"),
        ],
        [sg.Text("Percentage:", size=(15, 1)), sg.Text("", key="percentage")],
        [sg.Text("Time Left:", size=(15, 1)), sg.Text("", key="time_left")],
        [sg.Text("Shots:", size=(15, 1)), sg.Text("", key="shots")],
        [sg.Text("Shots on Target:", size=(15, 1)), sg.Text("", key="shots_on_target")],
        [sg.Text("Opponent Goals:", size=(15, 1)), sg.Text("", key="opponent_goals")],
        [sg.Text("User Goals:", size=(15, 1)), sg.Text("", key="user_goals")],
        [sg.Text("Income:", size=(15, 1)), sg.Text("", key="income")],
        [sg.Cancel()],
    ]
    return layout


# Function to update the GUI values
def update_gui(window, field, noP, tstart):
    passes_completed = field.passes
    total_passes = noP
    percentage = (passes_completed / total_passes) * 100
    elapsed_time = time.time() - tstart
    estimated_time_left = (elapsed_time / passes_completed) * (
        total_passes - passes_completed
    )

    window["passes_completed"].update(f"{passes_completed}/{total_passes}")
    window["percentage"].update(f"{percentage:.2f}%")
    window["time_left"].update(f"{estimated_time_left:.2f} seconds")
    window["shots"].update(f"{field.shots}")
    window["shots_on_target"].update(f"{field.shots_on_target}")
    window["opponent_goals"].update(f"{field.opponent_goals}")
    window["user_goals"].update(f"{field.user_goals}")
    window["income"].update(f"{round(field.user_team['income'] * field.user_goals)}M")


def play_game(user_team, opponent_team, game_number, windows_list):
    field = Field()
    field.x = random.randint(31, 81)
    field.y = random.randint(19, 49)
    who_goes_first = [user_team, opponent_team]
    random.shuffle(who_goes_first)
    who_goes_last = who_goes_first[1]
    who_goes_first = who_goes_first[0]
    who_goes_last_players = who_goes_last["players"]
    who_goes_first_players = who_goes_first["players"]
    field.user_team = user_team
    field.opponent_team = opponent_team
    field.right_team = who_goes_first
    field.left_team = who_goes_last
    field.possession = field.right_team
    field.setup(user_team)
    field.place_team(who_goes_last_players, "left")
    field.place_team(who_goes_first_players, "right")
    noP = random.randint(600, 1000)
    tstart = time.time()
    window = sg.Window(
        f"Game {game_number + 1} Progress", create_layout_game(), finalize=True
    )
    windows_list.append(window)

    while field.passes <= noP:
        field.pass_ball()
        field.game_continue()
        event, values = window.read(timeout=0)
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break
        update_gui(window, field, noP, tstart)

    window.close()
    field.display_debug()
    print(f"Game {game_number + 1} Results:")
    print(f"Goals for opponent {round(field.opponent_goals)}")
    print(f"User: {round(field.user_goals)}")
    print(f"Shots: {field.shots}({field.shots_on_target})")
    print(f"Passes: {field.passes}")
    print("")


if __name__ == "__main__":
    sg.theme("Reds")

    user = ""
    used_teams = []
    user_team = ""

    try:
        with open("users.json") as f:
            users = json.load(f)
        for i in users:
            used_teams.append(i["team"]["name"])
    except:
        pass

    def loading_animation(loading_finished):
        while not loading_finished.is_set():
            for i in range(4):
                sys.stdout.write("Loading" + "." * i + "   \r")
                sys.stdout.flush()
                time.sleep(0.5)
            for i in range(4, 0, -1):
                sys.stdout.write("Loading" + "." * i + "   \r")
                sys.stdout.flush()
                time.sleep(0.5)

    def message(message, color):
        sg.popup_quick_message(
            message,
            background_color=color,
            text_color="white",
            no_titlebar=True,
            keep_on_top=True,
            auto_close=True,
            auto_close_duration=3,
        )

    def create_user():
        create_layout = [
            [sg.Text("Create")],
            [
                sg.Text("Username"),
                sg.Input(key="username", size=(20, 1), justification="left"),
            ],
            [
                sg.Text("Password"),
                sg.Input(
                    key="password",
                    size=(20, 1),
                    justification="left",
                    password_char="*",
                ),
            ],
            [sg.Text(key="error")],
            [sg.Button("Submit")],
        ]
        window = sg.Window("Create", create_layout, keep_on_top=True)
        event, values = window.read()
        username = values["username"]
        password = values["password"]
        window.close()
        password = encode(password)
        try:
            with open("users.json", "r") as f:
                current_users = json.load(f)
        except:
            current_users = []
            # print("This is the first user registered.")
        if current_users:
            for i in current_users:
                if i["username"] == username:
                    print("User already exists!")
                    return None
        team = select_team()
        new_user = {"username": username, "password": password, "team": team}
        current_users.append(new_user)
        with open("users.json", "w") as f:
            json.dump(current_users, f, indent=3)
        print("User {} created!".format(username))
        return new_user

    def login():
        login_layout = [
            [sg.Text("Login")],
            [
                sg.Text("Username"),
                sg.Input(key="username", size=(20, 1), justification="left"),
            ],
            [
                sg.Text("Password"),
                sg.Input(
                    key="password",
                    size=(20, 1),
                    justification="left",
                    password_char="*",
                ),
            ],
            [sg.Text(key="error")],
            [sg.Button("Submit")],
        ]
        window = sg.Window("Login", login_layout)
        event, values = window.read()
        username = values["username"]
        password = values["password"]
        window.close()
        with open("users.json", "r") as f:
            users = json.load(f)
        for user in users:
            if user["username"] == username and decode(user["password"]) == password:
                return user
        return None

    def select_team():
        with open("teams.json", "r") as f:
            teams = json.load(f)
        userteamselect_layout = [
            [sg.Text("Please select a team:")],
            [
                sg.Listbox(
                    values=[
                        team["name"] for team in teams if team["name"] not in used_teams
                    ],
                    size=(50, 20),
                    key="team",
                    enable_events=False,
                )
            ],
            [sg.Text(key="error")],
            [sg.Button("Select")],
        ]
        team = None
        window = sg.Window("Select A Team", userteamselect_layout)
        event, values = window.read()
        selected_team = values["team"]
        for i in teams:
            if i["name"] == selected_team[0]:
                team = i
        window.close()
        return team

    def select_opponent():
        with open("teams.json", "r") as f:
            teams = json.load(f)
        team_names = [team for team in teams if team["name"] not in used_teams]
        select_layout = [
            [sg.Text("Please select an opponent:")],
            [
                sg.Listbox(
                    values=[
                        team["name"]
                        for team in teams
                        if team["name"] != user["team"]["name"]
                    ],
                    size=(50, 20),
                    key="opponent",
                    enable_events=False,
                )
            ],
            [sg.Text(key="error")],
            [sg.Button("Select")],
        ]

        window = sg.Window("Select A Team", select_layout)
        event, values = window.read()
        selected_team_name = values["opponent"][0]
        selected_team = "none"
        for i in team_names:
            if i["name"] == selected_team_name:
                selected_team = i
        window.close()
        return selected_team

    def get_user_team():
        with open("users.json", "r") as f:
            user_data = json.load(f)
        for i in user_data:
            if i["username"] == user["username"]:
                return i["team"]["name"]
        return user_data["team"]["name"]

    def main():
        global user, threading_main
        while True or not threading_main:
            ask_layout = [
                [sg.Text('Do you want to "Login" or "Create"?')],
                [sg.Input(key="input")],
                [sg.Text(key="error")],
                [sg.Button("Submit")],
            ]
            window = sg.Window("Login/Create", ask_layout)
            event, values = window.read()
            action = values["input"]
            window.close()
            if action == "create":
                user = create_user()
                break
            elif action == "login":
                user = login()
                if user is None:
                    print("Invalid login, please try again.")
                else:
                    user_team = user["team"]
                    if user_team is None:
                        user_team = select_team()
                        with open("users.json", "r") as f:
                            user_data = json.load(f)
                        user_data["team"] = user_team
                        with open("users.json", "w") as f:
                            json.dump(user_data, f)
                    break
            elif action == "j":
                username = os.environ.get("USER_FOOTBALL")
                password = os.environ.get("PASS_FOOTBALL")
                with open("users.json", "r") as f:
                    users = json.load(f)
                for i in users:
                    if i["username"] == username and decode(i["password"]) == password:
                        user = i
                        break

                user_team = user["team"]
                if user_team is None:
                    user_team = select_team()
                    with open("users.json", "r") as f:
                        user_data = json.load(f)
                    user_data["team"] = user_team
                    with open("users.json", "w") as f:
                        json.dump(user_data, f)
                break

        while True:
            try:
                main_layout = [
                    [sg.Text(f"Current balance is {user['team']['money']}M")],
                    [sg.Text("It costs 10M to upgrade or 5M to train")],
                    [sg.Text("Please select an action (upgrade, train, play):")],
                    [sg.Text(key="error")],
                    [
                        sg.Button("Upgrade", key="upgrade"),
                        sg.Button("Train", key="train"),
                        sg.Button("Train all your players", key="train_all"),
                        sg.Button("Play", key="play"),
                    ],
                ]
                window = sg.Window("Main", main_layout)
                event, values = window.read()
                action = event
                window.close()
            except:
                user = login()
                action = "new"
            user_team = user["team"]
            if action == "upgrade":
                upgrade_stadium(user["team"])
            elif action == "train":
                train_players(user["team"])
            elif action == "train all":
                train_players_all(user["team"], False)
            elif action == "train_all":
                train_players_all(user["team"], False)
            elif action == "play":
                opponent_team = select_opponent()

                # Start the play_game function in another thread
                game_thread = threading.Thread(
                    target=train_players_all, args=(opponent_team, True)
                )
                game_thread.start()
                thread2 = threading.Thread(target=main)
                thread2.start()
                threading_main = True
                play_game(user_team, opponent_team)
                game_thread.join()
                if threading_main:
                    threading_main = False
                    return

            elif action == "new":
                print("Welcome to my football game!!! good luck!")
            else:
                print("Invalid action, please try again.")

    def upgrade_stadium(team):
        if team["money"] <= 10:
            return
        team["money"] -= 10
        team["income"] = team["income"] + team["income"] / team["stadium"]
        team["stadium"] += 1
        print(
            f"Your current income is ${team['income']} and your bank account has currentlly {team['money']}M in it."
        )
        with open("teams.json", "r") as f:
            teams = json.load(f)
        for i, t in enumerate(teams):
            if t["name"] == team["name"]:
                teams[i] = team
        with open("teams.json", "w") as f:
            json.dump(teams, f)

    def train_players(team):
        if team["money"] <= 5:
            print("You don't have enough money to train.")
            return
        team["money"] -= 5
        for player in team["players"]:
            training_boost = player["training_rate"]

            # print(f"Old rating for {player['name']}, {player['rating']}")
            player["rating"] += training_boost
            # print(f"New rating for {player['name']}, {player['rating']}")
        with open("teams.json", "r") as f:
            teams = json.load(f)
        for i, t in enumerate(teams):
            if t["name"] == team["name"]:
                teams[i] = team
        with open("teams.json", "w") as f:
            json.dump(teams, f)

    def train_players_all(team, t_f):
        if not t_f:
            print(f"Training all players on {team['name']}.")
        while True:
            if team["money"] < 5:
                return
            team["money"] -= 5
            for player in team["players"]:
                training_boost = player["training_rate"]

                # print(f"Old rating for {player['name']}, {player['rating']}")
                player["rating"] += training_boost
                # print(f"New rating for {player['name']}, {player['rating']}")
            with open("teams.json", "r") as f:
                teams = json.load(f)
            for i, t in enumerate(teams):
                if t["name"] == team["name"]:
                    team["overallaverage"] = calculate_overall_strength(team)
                    teams[i] = team
            with open("teams.json", "w") as f:
                json.dump(teams, f)

    def calculate_overall_strength(team):
        overall_strength = 0
        for player in team["players"]:
            overall_strength += player["rating"]
        return overall_strength

    game_threads = []
    windows = []

    for game_number in range(3):  # Adjust the number of games as needed
        opponent_team = select_opponent()
        game_thread = threading.Thread(
            target=play_game, args=(user_team, opponent_team, game_number, windows)
        )
        game_threads.append(game_thread)
        game_thread.start()

    threading_main = True

    for game_thread in game_threads:
        game_thread.join()

    threading_main = False
