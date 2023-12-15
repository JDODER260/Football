import json
import math
import os, sys, time
import threading
from getpass import getpass
import random
from endecoder import decode, encode

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


class Field:
    def __init__(self):
        self.x = 31
        self.y = 13
        self.ball = {"x_pos": round(self.x / 2) - 1, "y_pos": round(self.y / 2)}
        self.fouls = 0
        self.red_cards = 0
        self.yellow_cards = 0
        self.shots = 0
        self.shots_on_target = 0
        self.passes = 0
        self.opponent_goals = 0
        self.user_goals = 0
        self.positions = ["GK", "LW", "RW", "LB", "RB", "CB", "ST", "CM", "LM", "RM"]
        self.opponent_team = "team"
        self.user_team = "team"
        self.right_team = "team"
        self.left_team = "team"
        self.possession = "team"
        # 31 by 13
        self.field_positions = [[{} for _ in range(self.y)] for _ in range(self.x)]

        # Positioning of players based on the original 31x14 grid
        positions = [
            (0, round((self.y - 1) / 2), {"position": "GK"}),
            (
                round((self.x - 1) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LB"},
            ),
            (
                round((self.x - 1) / 2 / 2 / 2),
                round((self.y - 1) / 2),
                {"position": "CB"},
            ),
            (
                round((self.x - 1) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RB"},
            ),
            (
                round((self.x - 1) / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LM"},
            ),
            (round((self.x - 1) / 2 / 2), round((self.y - 1) / 2), {"position": "CM"}),
            (
                round((self.x - 1) / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RM"},
            ),
            (
                round((self.x) / 2) - 2,
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LW"},
            ),
            (round((self.x) / 2) - 2, round((self.y) / 2), {"position": "ST"}),
            (round((self.x) / 2) - 2, round((self.y - 1) / 2 / 2), {"position": "RW"}),
            (self.x - 1, round((self.y - 1) / 2), {"position": "GK"}),
            (
                round(self.x - (self.x) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LB"},
            ),
            (
                round(self.x - (self.x) / 2 / 2 / 2),
                round((self.y - 1) / 2),
                {"position": "CB"},
            ),
            (
                round(self.x - (self.x) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RB"},
            ),
            (
                round(self.x - (self.x) / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LM"},
            ),
            (
                round(self.x - (self.x) / 2 / 2),
                round((self.y - 1) / 2),
                {"position": "CM"},
            ),
            (
                round(self.x - (self.x) / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RM"},
            ),
            (
                round(self.x - (self.x) / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LW"},
            ),
            (
                round((self.x) / 2) - 1,
                round((self.y - 1) / 2),
                {
                    "position": "ST",
                    "x_pos": round((self.x) / 2),
                    "y_pos": round((self.y - 1) / 2),
                },
            ),
            (
                round(self.x - (self.x) / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RW"},
            ),
        ]  # right side
        for x_pos, y_pos, position_data in positions:
            self.field_positions[x_pos][y_pos] = position_data

    def find_player_starting_pos(self, position, side):
        if side == "left":
            for x_pos in range(16):
                for y_pos in range(13):
                    try:
                        if self.field_positions[x_pos][y_pos]["position"] == position:
                            return x_pos, y_pos
                    except:
                        pass

        if side == "right":
            for x_pos in range(14, 31):
                for y_pos in range(13):
                    try:
                        if self.field_positions[x_pos][y_pos]["position"] == position:
                            return x_pos, y_pos
                    except:
                        pass
        else:
            exception: print("Something went wrong")

    def find_player_starting_pos(self, position, side):
        if side == "left":
            for x_pos in range(round(self.x / 2)):
                for y_pos in range(self.y):
                    p_position = self.field_positions[x_pos][y_pos].get("position")
                    if p_position and p_position == position:
                        return x_pos, y_pos
        if side == "right":
            for x_pos in range(round(self.x / 2) - 1, self.x):
                for y_pos in range(self.y):
                    p_position = self.field_positions[x_pos][y_pos].get("position")
                    if p_position and p_position == position:
                        return x_pos, y_pos
        return None

    def place_player(self, x_pos, y_pos, name, position, rating):
        self.field_positions[x_pos][y_pos] = {
            "player": name,
            "position": position,
            "rating": rating,
        }

    def place_team(self, team, side):
        random_squad = []
        squad = []
        for i in team:
            random_squad.append(
                {"name": i["name"], "position": i["position"], "rating": i["rating"]}
            )
        random.shuffle(random_squad)
        for i in self.positions:
            for x in random_squad:
                if i == x["position"]:
                    squad.append(x)
                    break

        for player in squad:
            pos = self.find_player_starting_pos(player["position"], side)
            try:
                self.place_player(
                    pos[0], pos[1], player["name"], player["position"], player["rating"]
                )
            except:
                print(f"couldn't place {pos}")

    def display_debug(self):
        player_icons = {"user": "🟦", "opponent": "🟥", "ball": "⚽"}
        field_icons = [
            ["🟩" for _ in range(self.y)] for _ in range(self.x)
        ]  # Green background

        # Add player icons to the field
        for x_pos in range(self.x):
            for y_pos in range(self.y):
                player_info = self.field_positions[x_pos][y_pos]
                player = player_info.get("player")
                if player:
                    team = (
                        "user"
                        if player in [i["name"] for i in self.user_team["players"]]
                        else "opponent"
                    )
                    field_icons[x_pos][y_pos] = player_icons.get(team, "⬜️")

        # Find the player holding the ball and display the ball with that player's icon
        ball_x = self.ball["x_pos"]
        ball_y = self.ball["y_pos"]
        player_with_ball_info = self.field_positions[ball_x][ball_y]
        player_with_ball = player_with_ball_info.get("player")
        if player_with_ball:
            team = (
                "user"
                if player_with_ball in [i["name"] for i in self.user_team["players"]]
                else "opponent"
            )
            field_icons[ball_x][ball_y] = player_icons.get("ball", "⚽")

        # Display the field
        for row in field_icons:
            print(" ".join(row))

    def find_player(self, position, team):
        for player in team["players"]:
            if player["position"] == position:
                for x_pos in range(self.x):
                    for y_pos in range(self.y):
                        if (
                            self.field_positions[x_pos][y_pos]
                            and self.field_positions[x_pos][y_pos]["position"]
                            == position
                        ):
                            return (x_pos, y_pos, player)

    def game_continue(self):
        on_game_players = []
        for x_pos in range(self.x):
            for y_pos in range(self.y):
                if (
                    self.field_positions[x_pos][y_pos] != {}
                    and self.field_positions != self.ball
                    and not self.field_positions[x_pos][y_pos]
                    in [i for i in on_game_players]
                ):
                    try:
                        current_player = self.field_positions[x_pos][y_pos]["player"]
                    except:
                        break
                    current_rating = self.field_positions[x_pos][y_pos]["rating"]
                    current_position = self.field_positions[x_pos][y_pos]["position"]
                    if not current_player or current_position == "GK":
                        continue
                    if current_player in [
                        i["name"] for i in self.opponent_team["players"]
                    ]:
                        team = self.opponent_team
                    else:
                        team = self.user_team
                    position = self.field_positions[x_pos][y_pos].get("position")
                    if (
                        self.ball.get("x_pos") == self.x - 1
                        or self.ball.get("x_pos") == 0
                    ):
                        offset_x = random.randint(
                            -round(current_rating / 100), round(current_rating / 100)
                        )
                        offset_y = random.randint(
                            -round(current_rating / 100), round(current_rating / 100)
                        )
                        new_x = max(0, min(self.x - 1, x_pos + offset_x))
                        new_y = max(0, min(self.y - 1, y_pos + offset_y))
                    else:
                        new_coords = []
                        for i in range(round(current_rating / 100)):
                            while True:
                                offset_x = random.randint(
                                    -round(current_rating / 100),
                                    round(current_rating / 100),
                                )
                                offset_y = random.randint(
                                    -round(current_rating / 100),
                                    round(current_rating / 100),
                                )
                                new_x = max(0, min(self.x - 1, x_pos + offset_x))
                                new_y = max(0, min(self.y - 1, y_pos + offset_y))
                                if (new_x, new_y) not in [i for i in new_coords]:
                                    if (
                                        new_x != self.ball["x_pos"]
                                        or new_y != self.ball["y_pos"]
                                    ):
                                        new_coords.append((new_x, new_y))
                                        break
                        closest_player = min(
                            new_coords,
                            key=lambda p: (p[0] - self.ball["x_pos"]) ** 2
                            + (p[1] - self.ball["y_pos"]) ** 2,
                        )
                        new_x, new_y = closest_player

                    on_game_players.append(self.field_positions[new_x][new_y])
                    if not self.field_positions[new_x][new_y]:
                        self.field_positions[new_x][new_y] = {
                            "player": current_player,
                            "position": current_position,
                            "rating": current_rating,
                        }
                        self.field_positions[x_pos][y_pos] = {}

                        # Check if the player had the ball, and if so, move the ball with them
                        if self.ball["x_pos"] == x_pos and self.ball["y_pos"] == y_pos:
                            intercept_c = self.pass_intercept(
                                x_pos, y_pos, new_x, new_y
                            )
                            if intercept_c == None:
                                self.ball = {"x_pos": new_x, "y_pos": new_y}
                                self.field_positions[new_x][new_y] = {
                                    "player": self.field_positions[new_x][new_y][
                                        "player"
                                    ],
                                    "position": self.field_positions[new_x][new_y][
                                        "position"
                                    ],
                                    "rating": self.field_positions[new_x][new_y][
                                        "rating"
                                    ],
                                    "x_pos": new_x,
                                    "y_pos": new_y,
                                }
                                self.field_positions[x_pos][y_pos] = {}
                            else:
                                magic_number = round(
                                    self.field_positions[new_x][new_y]["rating"]
                                )
                                list_rating1 = [i for i in range(magic_number)]
                                random.shuffle(list_rating1)
                                num1 = random.choice(list_rating1)
                                list_rating = [
                                    i
                                    for i in range(
                                        round(
                                            self.field_positions[intercept_c[0]][
                                                intercept_c[1]
                                            ]["rating"]
                                        )
                                    )
                                ]
                                random.shuffle(list_rating)
                                num = random.choice(list_rating)
                                if num1 >= num:
                                    self.move_ball(
                                        x_pos, y_pos, intercept_c[0], intercept_c[1]
                                    )

    def move_ball(self, x_from, y_from, x_to, y_to):
        try:
            self.field_positions[x_from][y_from] = {
                "player": self.field_positions[x_from][y_from]["player"],
                "position": self.field_positions[x_from][y_from]["position"],
                "rating": self.field_positions[x_from][y_from]["rating"],
            }
        except:
            pass
        self.ball = {"x_pos": x_to, "y_pos": y_to}
        self.field_positions[x_to][y_to] = {
            "player": self.field_positions[x_to][y_to]["player"],
            "position": self.field_positions[x_to][y_to]["position"],
            "rating": self.field_positions[x_to][y_to]["rating"],
            "x_pos": x_to,
            "y_pos": y_to,
        }

    def pass_ball(self):
        for x_pos in range(self.x):
            for y_pos in range(self.y):
                if x_pos == self.ball["x_pos"] and y_pos == self.ball["y_pos"]:
                    try:
                        self.field_positions[x_pos][y_pos]["player"]
                    except:
                        coords = self.find_nearest_player(x_pos, y_pos)
                        self.move_ball(x_pos, y_pos, coords[0], coords[1])
                        return
                    if self.field_positions[x_pos][y_pos]["player"]:
                        if (
                            x_pos
                            >= random.randrange(
                                (self.x - 1) - round(self.y / 2), self.x - 1
                            )
                            and self.field_positions[x_pos][y_pos]["position"] != "GK"
                            and self.possession == self.right_team
                        ):
                            l_1 = self.shoot_goal(x_pos, y_pos)
                            if l_1 == True:
                                self.possession = self.right_team
                                self.passes += 1
                                return
                            elif l_1 != None:
                                if self.possession == self.right_team:
                                    self.possession = self.left_team
                                else:
                                    self.possession = self.right_team
                                coords = l_1
                                self.move_ball(x_pos, y_pos, coords[0], coords[1])
                                self.passes += 1
                                return
                        if (
                            x_pos
                            <= random.randrange(0, (self.x - 1) - round(self.y / 2))
                            and self.field_positions[x_pos][y_pos]["position"] != "GK"
                            and self.possession == self.left_team
                        ):
                            l_1 = self.shoot_goal(x_pos, y_pos)
                            if l_1 == True:
                                self.possession = self.right_team
                                self.passes += 1
                                return
                            elif l_1 != None:
                                if self.possession == self.right_team:
                                    self.possession = self.left_team
                                else:
                                    self.possession = self.right_team
                                coords = l_1
                                self.move_ball(x_pos, y_pos, coords[0], coords[1])
                                self.passes += 1
                                return
                        coords = self.find_nearest_player_tward_goal(
                            x_pos, y_pos, self.possession
                        )
                        if self.check_if_valid_pass(x_pos, y_pos, coords[0], coords[1]):
                            self.move_ball(x_pos, y_pos, coords[0], coords[1])
                            self.passes += 1
                            return
                        else:
                            coords = self.find_nearest_player(x_pos, y_pos)
                            if (
                                self.pass_intercept(x_pos, y_pos, coords[0], coords[1])
                                == None
                            ):
                                self.move_ball(x_pos, y_pos, coords[0], coords[1])
                                self.passes += 1
                                return
                            else:
                                coord_plural = self.pass_intercept(
                                    x_pos, y_pos, coords[0], coords[1]
                                )
                                x_pos_old = x_pos
                                y_pos_old = y_pos
                                x_pos = coord_plural[0]
                                y_pos = coord_plural[1]
                                for i in self.right_team["players"]:
                                    if (
                                        self.field_positions[x_pos][y_pos]["player"]
                                        == i["name"]
                                    ):
                                        self.possession = self.right_team
                                        team = self.possession
                                        # print(f"{i['name']} intercepted {self.field_positions[x_pos_old][y_pos_old]['player']}'s pass to {self.field_positions[coords[0]][coords[1]]['player']}")
                                for i in self.left_team["players"]:
                                    if (
                                        self.field_positions[x_pos][y_pos]["player"]
                                        == i["name"]
                                    ):
                                        self.possession = self.left_team
                                        team = self.possession

                                        # print(f"{i['name']} intercepted {self.field_positions[x_pos_old][y_pos_old]['player']}'s pass to {self.field_positions[coords[0]][coords[1]]['player']}")
                                self.move_ball(
                                    x_pos_old,
                                    y_pos_old,
                                    coord_plural[0],
                                    coord_plural[1],
                                )
                                self.passes += 1
                                return

    def find_nearest_player(self, x_pos, y_pos):
        player_coords = []

        for i in self.possession["players"]:
            for x in range(self.x):
                for y in range(self.y):
                    try:
                        if (
                            self.field_positions[x][y]["player"] == i["name"]
                            and x != x_pos
                            or y != y_pos
                        ):
                            player_coords.append({"x_pos": x, "y_pos": y})
                    except:
                        pass

        if player_coords:
            # Calculate the distance to each player and find the closest one
            closest_player = min(
                player_coords,
                key=lambda p: (p["x_pos"] - x_pos) ** 2 + (p["y_pos"] - y_pos) ** 2,
            )
            if (
                self.field_positions[closest_player["x_pos"]][closest_player["y_pos"]][
                    "position"
                ]
                == "GK"
            ):
                closest_player = random.choice(player_coords)
            return closest_player["x_pos"], closest_player["y_pos"]

        # Return None if no players are found
        return None, None

    def find_nearest_player_tward_goal(self, x_pos, y_pos, team):
        player_coords = []
        # Goal coordinates based on the team
        goal_x = self.x - 1 if self.possession == self.left_team else 0
        goal_y = round(self.y / 2)  # Middle of the goal
        for i in team["players"]:
            if self.field_positions[x_pos][y_pos]["player"] != i["name"]:
                for x in range(self.x):
                    for y in range(self.y):
                        try:
                            if self.field_positions[x][y]["player"] == i["name"]:
                                player_coords.append({"x_pos": x, "y_pos": y})
                        except:
                            pass

        if player_coords:
            # Calculate the distance to each player and find the closest one
            closest_player = min(
                player_coords,
                key=lambda p: (p["x_pos"] - goal_x) ** 2 + (p["y_pos"] - goal_y) ** 2,
            )
            return closest_player["x_pos"], closest_player["y_pos"]

        # Return None if no players are found
        return None, None

    def check_if_valid_pass(self, x_from, y_from, x_to, y_to):
        if x_from <= x_to and y_from <= y_to:
            for x in range(x_from - x_to):
                for y in range(y_from - y_to):
                    if (
                        self.field_positions[x_from - x][y_from - y] == {}
                        or x == 0
                        or y == 0
                    ):
                        pass
                    else:
                        return False
        elif x_from >= x_to and y_from <= y_to:
            for x in range(x_to - x_from):
                for y in range(y_to - y_from):
                    if (
                        self.field_positions[x_to - x][y_to - y] == {}
                        or x == 0
                        or y == 0
                    ):
                        pass
                    else:
                        return False
        elif x_from >= x_to and y_from >= y_to:
            for x in range(x_from + x_to):
                for y in range(y_from + y_to):
                    if x_from + x <= self.x - 1 and y_from + y <= self.y - 1:
                        if (
                            self.field_positions[x_from + x][y_from + y] == {}
                            or x == 0
                            or y == 0
                        ):
                            pass
                        else:
                            return False
        elif x_from <= x_to and y_from >= y_to:
            for x in range(x_to + x_from):
                for y in range(y_to + y_from):
                    if x_to + x <= self.x - 1 and y_to + y <= self.y - 1:
                        if (
                            self.field_positions[x_to + x][y_to + y] == {}
                            or x == 0
                            or y == 0
                        ):
                            pass
                        else:
                            return False
        else:
            print("Nothing")
        return True

    def pass_intercept(self, x_from, y_from, x_to, y_to):
        if x_from <= x_to and y_from <= y_to:
            for x in range(x_from - x_to):
                for y in range(y_from - y_to):
                    if (
                        self.field_positions[x_from - x][y_from - y] == {}
                        or x == 0
                        or y == 0
                    ):
                        pass
                    else:
                        return (x_from - x, y_from - y)
        elif x_from >= x_to and y_from <= y_to:
            for x in range(x_to - x_from):
                for y in range(y_to - y_from):
                    if (
                        self.field_positions[x_to - x][y_to - y] == {}
                        or x == 0
                        or y == 0
                    ):
                        pass
                    else:
                        return (x_to - x, y_to - y)
        elif x_from >= x_to and y_from >= y_to:
            for x in range(x_from + x_to):
                for y in range(y_from + y_to):
                    if x_from + x <= self.x - 1 and y_from + y <= self.y - 1:
                        if (
                            self.field_positions[x_from + x][y_from + y] == {}
                            or x == 0
                            or y == 0
                        ):
                            pass
                        else:
                            return (x_from + x, y_from + y)
        elif x_from <= x_to and y_from >= y_to:
            for x in range(x_to + x_from):
                for y in range(y_to + y_from):
                    if x_to + x <= self.x - 1 and y_to + y <= self.y - 1:
                        if (
                            self.field_positions[x_to + x][y_to + y] == {}
                            or x == 0
                            or y == 0
                        ):
                            pass
                        else:
                            return (x_to + x, y_to + y)
        else:
            print("Nothing")
        return None

    def shoot_goal(self, x_from, y_from):
        self.shots += 1
        for i in self.possession["players"]:
            if self.field_positions[x_from][y_from]["player"] == i["name"]:
                goal_x = self.x - 1 if self.possession == self.left_team else 0
                goal_y = round(self.y / 2)  # Middle of the goal
                coords = self.pass_intercept(x_from, y_from, goal_x, goal_y)
                if not coords:
                    pass
                else:
                    # print(f"intercepted goal by {self.field_positions[coords[0]][coords[1]]['player']}")
                    return (coords[0], coords[1])
                magic_number = round(
                    self.field_positions[goal_x][goal_y].get("rating")
                    if self.field_positions[goal_x][goal_y].get("rating") != None
                    else random.randint(70, 200)
                )
                list_rating1 = [i for i in range(magic_number)]
                random.shuffle(list_rating1)
                num1 = random.choice(list_rating1)
                list_rating = [
                    i
                    for i in range(
                        round(self.field_positions[x_from][y_from]["rating"])
                    )
                ]
                random.shuffle(list_rating)
                num = random.choice(list_rating)
                if num1 >= num:
                    # print(f"Goal blocked by {self.field_positions[goal_x][goal_y]['player']}.")
                    self.shots_on_target += 1
                    self.move_ball(x_from, y_from, goal_x, goal_y)
                    self.possession = (
                        self.right_team if goal_x == self.x - 1 else self.left_team
                    )
                    self.game_continue()
                    for i in range(1000):
                        coords = self.find_nearest_player_tward_goal(
                            goal_x, goal_y, self.possession
                        )
                        if self.check_if_valid_pass(
                            goal_x, goal_y, coords[0], coords[1]
                        ):
                            self.move_ball(goal_x, goal_y, coords[0], coords[1])
                            self.passes += 1
                            return True
                        self.game_continue()
                    return True
                if self.possession == self.user_team:
                    self.user_goals += 1
                    # print(f"Goal scored by {self.field_positions[x_from][y_from]['player']}, Possession is: {self.possession['manager']} \n{self.user_team['manager']}: {self.user_goals}\n{self.opponent_team['manager']}: {self.opponent_goals}")
                    self.shots_on_target += 1
                    self.setup(self.opponent_team)
                    self.place_team(self.opponent_team["players"], "right")
                    self.place_team(self.user_team["players"], "left")
                else:
                    self.opponent_goals += 1
                    # print(f"Goal scored by {self.field_positions[x_from][y_from]['player']}, Possession is: {self.possession['manager']} \n{self.user_team['manager']}: {self.user_goals}\n{self.opponent_team['manager']}: {self.opponent_goals}")
                    self.setup(self.user_team)
                    self.place_team(self.opponent_team["players"], "left")
                    self.place_team(self.user_team["players"], "right")
                return True

    def setup(self, team):
        self.possession = team
        self.ball = {"x_pos": round(self.x / 2) - 1, "y_pos": round(self.y / 2)}
        self.left_team = self.right_team
        self.right_team = team
        self.field_positions = [[{} for _ in range(self.y)] for _ in range(self.x)]

        # Positioning of players based on the original 31x14 grid
        positions = [
            (0, round((self.y - 1) / 2), {"position": "GK"}),
            (
                round((self.x - 1) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LB"},
            ),
            (
                round((self.x - 1) / 2 / 2 / 2),
                round((self.y - 1) / 2),
                {"position": "CB"},
            ),
            (
                round((self.x - 1) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RB"},
            ),
            (
                round((self.x - 1) / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LM"},
            ),
            (round((self.x - 1) / 2 / 2), round((self.y - 1) / 2), {"position": "CM"}),
            (
                round((self.x - 1) / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RM"},
            ),
            (
                round((self.x) / 2) - 2,
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LW"},
            ),
            (round((self.x) / 2) - 2, round((self.y) / 2), {"position": "ST"}),
            (round((self.x) / 2) - 2, round((self.y - 1) / 2 / 2), {"position": "RW"}),
            (self.x - 1, round((self.y - 1) / 2), {"position": "GK"}),
            (
                round(self.x - (self.x) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LB"},
            ),
            (
                round(self.x - (self.x) / 2 / 2 / 2),
                round((self.y - 1) / 2),
                {"position": "CB"},
            ),
            (
                round(self.x - (self.x) / 2 / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RB"},
            ),
            (
                round(self.x - (self.x) / 2 / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LM"},
            ),
            (
                round(self.x - (self.x) / 2 / 2),
                round((self.y - 1) / 2),
                {"position": "CM"},
            ),
            (
                round(self.x - (self.x) / 2 / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RM"},
            ),
            (
                round(self.x - (self.x) / 2),
                round((self.y - 1) / 2 / 2 + self.y / 2),
                {"position": "LW"},
            ),
            (
                round((self.x) / 2) - 1,
                round((self.y - 1) / 2),
                {
                    "position": "ST",
                    "x_pos": round((self.x) / 2),
                    "y_pos": round((self.y - 1) / 2),
                },
            ),
            (
                round(self.x - (self.x) / 2),
                round((self.y - 1) / 2 / 2),
                {"position": "RW"},
            ),
        ]  # right side
        for x_pos, y_pos, position_data in positions:
            self.field_positions[x_pos][y_pos] = position_data


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


def create_user():
    username = input("Please enter a username: ")
    password = getpass("Please enter a password: ")
    team = select_team()
    password = encode(password)
    new_user = {"username": username, "password": password, "team": team}
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
    current_users.append(new_user)
    with open("users.json", "w") as f:
        json.dump(current_users, f, indent=3)
    print("User {} created!".format(username))
    return new_user


def login():
    username = input("Username: ")
    password = getpass("Password: ")
    with open("users.json", "r") as f:
        users = json.load(f)
    for user in users:
        if user["username"] == username and decode(user["password"]) == password:
            return user
    return None


def select_team():
    with open("teams.json", "r") as f:
        teams = json.load(f)
    team_names = [team for team in teams if team["name"] not in used_teams]
    print("Please select a team: ")
    for index, name in enumerate(team_names):
        print(f"{index + 1}. {name['name']}")
    selected_index = int(input())
    selected_team = team_names[selected_index - 1]
    used_teams.append(selected_team["name"])
    return selected_team


def select_opponent():
    with open("teams.json", "r") as f:
        teams = json.load(f)
    opponent_names = [team for team in teams if team["name"] != user["team"]["name"]]
    print("Please select an opponent: ")
    for index, name in enumerate(opponent_names):
        print(f"{index + 1}. {name['name']}")
    selected_index = int(input())
    selected_team = opponent_names[selected_index - 1]
    return selected_team


def get_user_team():
    with open("users.json", "r") as f:
        user_data = json.load(f)
    for i in user_data:
        if i["username"] == user["username"]:
            return i["team"]["name"]
    return user_data["team"]["name"]


def main():
    global user
    while True:
        action = input("Please select an action (login, create): ")
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
            action = input(
                f"Current balance is {user['team']['money']}M\nIt costs 10M to upgrade 5M to train\n\nPlease select an action (upgrade, train, play): "
            )
        except:
            user = login()
            action = "new"
        user_team = user["team"]
        if action == "upgrade":
            upgrade_stadium(user["team"])
        elif action == "train":
            train_players(user["team"])
        elif action == "train all":
            train_players_all(user["team"])
        elif action == "play":
            opponent_team = select_opponent()
            # threads = []
            # num_threads = 5
            # for _ in range(num_threads):
            # print(_)
            # thread = threading.Thread(target=play_game, args=(user_team, opponent_team))
            # threads.append(thread)
            # thread.start()

            # for thread in threads:
            # thread.join()
            # play_game(user_team, opponent_team)
            loading_finished = threading.Event()

            # Start the loading animation in a separate thread
            loading_thread = threading.Thread(
                target=loading_animation, args=(loading_finished,)
            )
            loading_thread.daemon = True
            loading_thread.start()

            # Start the play_game function in another thread
            game_thread = threading.Thread(
                target=play_game, args=(user_team, opponent_team)
            )
            game_thread.start()

            # Wait for the game thread to finish
            game_thread.join()
            loading_finished.set()
            train_players(opponent_team)
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
        training_boost = player["traning_rate"]

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


def train_players_all(team):
    while True:
        if team["money"] < 5:
            print("You don't have enough money to train.")
            return
        team["money"] -= 5
        for player in team["players"]:
            training_boost = player["traning_rate"]

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


def calculate_overall_strength(team):
    overall_strength = 0
    for player in team["players"]:
        overall_strength += player["rating"]
    return overall_strength


def play_game(user_team, opponent_team):
    field = Field()
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
    field.place_team(who_goes_last_players, "left")
    field.place_team(who_goes_first_players, "right")
    field.display_debug()
    noP = random.randint(400, 500)
    while field.passes < noP:
        field.pass_ball()
        field.game_continue()
    print("")
    field.display_debug()
    print(
        f"Goals for opponent {field.opponent_goals}\nUser: {field.user_goals}\nShots: {field.shots}({field.shots_on_target})\nPasses: {field.passes}"
    )
    income = round(
        round(user_team["income"] * field.user_goals) / round(field.opponent_goals / 2)
    )
    user_team["money"] += income
    incomeop = round(
        round(user_team["income"] * field.opponent_goals) / round(field.user_goals / 2)
    )
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


if __name__ == "__main__":
    main()
