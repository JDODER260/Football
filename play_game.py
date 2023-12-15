import sys
import json, random, time
from field import Field
import PySimpleGUI as sg
sg.theme_add_new(
    'JDODER',
    {
        'BACKGROUND': '#240000',
        'TEXT': '#f3f3f3',
        'INPUT': '#515151',
        'TEXT_INPUT': '#f6f6f6',
        'SCROLL': '#622200',
        'BUTTON': ('#f86', '#433c2c'),
        'PROGRESS': ('#791717', '#ababab'),
        'BORDER': 1,
        'SLIDER_DEPTH': 1,
        'PROGRESS_DEPTH': 1,
    }
)
sg.theme('JDODER')

def display_field(field):
    while not loading_finished.is_set():
        for i in range(4):
            sys.stdout.write("Loading" + "." * i + "   \r")
            sys.stdout.flush()
            time.sleep(0.5)
        for i in range(4, 0, -1):
            sys.stdout.write("Loading" + "." * i + "   \r")
            sys.stdout.flush()
            time.sleep(0.5)


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
        [sg.Cancel()],
    ]
    return layout

    # Function to update the GUI values


def update_gui(window, field, noP, tstart):
    passes_completed = field.passes
    total_passes = noP  # Assuming you have 'noP' as a field attribute
    percentage = (passes_completed / total_passes) * 100
    elapsed_time = time.time() - tstart
    estimated_time_left = (
        (elapsed_time / passes_completed) * (total_passes - passes_completed)
        if passes_completed != 0
        else "Unlimited"
    )

    window["passes_completed"].update(f"{passes_completed}/{total_passes}")
    window["percentage"].update(f"{percentage:.2f}%")
    window["time_left"].update(
        f"{estimated_time_left:.2f} sec"
        if isinstance(estimated_time_left, float)
        else f"{estimated_time_left} sec:"
    )
    window["shots"].update(f"{field.shots}")
    window["shots_on_target"].update(f"{field.shots_on_target}")
    window["opponent_goals"].update(f"{field.opponent_goals}")
    window["user_goals"].update(f"{field.user_goals}")

    # Process events and keep the window responsive
    event, values = window.read(timeout=0)
    if event == sg.WINDOW_CLOSED or event == "Cancel":
        window.close()
        sys.exit()





def play_game(user_team, opponent_team, user):
    field = Field()
    field.x = (
        round(user_team["overallaverage"] / 500)
        if 0 != round(user_team["overallaverage"] / 500) % 2
        else round(user_team["overallaverage"] / 500) - 1
        if user_team["overallaverage"] < opponent_team["overallaverage"]
        else round(opponent_team["overallaverage"] / 500)
        if 0 != round(opponent_team["overallaverage"] / 500) % 2
        else round(opponent_team["overallaverage"] / 500) - 1
    )
    field.y = (
        field.x - round(field.x / 3)
        if 0 != (field.x - round(field.x / 3)) % 2
        else (field.x - round(field.x / 3)) - 1
    )
    if field.x < 31 or field.y < 19:
        field.x = 31
        field.y = 19
    if field.x > 81 or field.y > 49:
        field.x = 81
        field.y = 49
    print(field.x, field.y)
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
    field.display_debug()
    window = sg.Window("Game Progress", create_layout_game(), finalize=True)
    update_gui(window, field, noP, tstart)
    while field.passes <= noP:
        field.pass_ball()
        field.game_continue()
        field.display_debug()
        update_gui(window, field, noP, tstart)
        time.sleep(.01)
    window.close()
    print("")
    field.display_debug()
    print(
        f"Goals for opponent {round(field.opponent_goals)}\nUser: {round(field.user_goals)}\nShots: {field.shots}({field.shots_on_target})\nPasses: {field.passes}"
    )
    if (
        round(field.opponent_goals / 10) == round(field.user_goals / 10) and 5 == 9
    ):  # doesnt work
        winner = (
            field.user_team["name"]
            if field.user_goals >= field.opponent_goals
            else field.opponent_team["name"]
        )
        print(
            f"The teams went to penalty shootout and {winner} won!\nThe points were.\nUser: {round(field.user_goals / 10)}({str(field.user_goals)[1]})\nOpponent: {round(field.opponent_goals / 10)}({str(field.opponent_goals)[1]})"
        )
    if field.opponent_goals >= 2:
        income = round(
            round(user_team["income"] * field.user_goals)
            / int(field.opponent_goals / 2)
        )
    else:
        income = round(user_team["income"] * field.user_goals)
    user_team["money"] += income
    if field.user_goals >= 2:
        incomeop = round(
            round(user_team["income"] * field.opponent_goals)
            / int(field.user_goals / 2)
        )
    else:
        incomeop = round(opponent_team["income"] * field.opponent_goals)
    opponent_team["money"] += incomeop
    with open("users.json", "r") as f:
        users = json.load(f)
    for i in users:
        if i["username"] == user["username"]:
            i["team"] = user_team
            break
    with open("users.json", "w") as f:
        json.dump(users, f)

    with open("teams.json", "r") as f:
        teams = json.load(f)
    for i, team in enumerate(teams):
        if team["name"] == opponent_team["name"]:
            teams[i] = opponent_team
            break
    with open("teams.json", "w") as f:
        json.dump(teams, f)
    with open("users.json", "r") as f:
        users = json.load(f)
    for i in users:
        if i["username"] == user["username"]:
            print(i["team"]["money"])
            break
    with open("teams.json", "r") as f:
        teams = json.load(f)
    for i, team in enumerate(teams):
        if team["name"] == opponent_team["name"]:
            print(team["money"], "2")
            break


if __name__ == "__main__":
    # Check if there are enough command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python play_game.py user_team opponent_team user")
        sys.exit(1)

    # Extract command-line arguments
    user_team_name = sys.argv[1]
    opponent_team_name = sys.argv[2]
    user_name = sys.argv[3]

    with open("users.json", "r") as f:
        users = json.load(f)
    user = next((user for user in users if user["username"] == user_name), None)
    # Load team data from JSON files
    with open("teams.json", "r") as f:
        teams = json.load(f)

    # Find user_team and opponent_team based on names
    user_team = next((team for team in teams if team["name"] == user_team_name), None)
    opponent_team = next(
        (team for team in teams if team["name"] == opponent_team_name), None
    )

    if user_team is None or opponent_team is None or user is None:
        print("Invalid team names. Make sure they exist in teams.json.", user)
        sys.exit(1)

    # Call the play_game function with the loaded teams
    play_game(user_team, opponent_team)
