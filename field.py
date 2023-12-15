import random, sys
import pygame


class Field:
    def __init__(self):
        self.x = 31
        self.y = 19
        self.ball = {"x_pos": round(self.x / 2) - 1, "y_pos": round((self.y - 1) / 2)}
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
        self.previous_ball_pos = False

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
            (round((self.x) / 2) - 2, round((self.y - 1) / 2), {"position": "ST"}),
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

    import sys

    def display_debug(self):  # by ChatGPT
        self.screen_width = self.x * 30
        self.screen_height = self.y * 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Football Field")
        player_icons = {
            "user": pygame.Color("blue"),
            "opponent": pygame.Color("red"),
            "ball": pygame.Color("black"),
        }
        field_icons = [
            [pygame.Color("green") for _ in range(self.y)] for _ in range(self.x)
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
                    field_icons[x_pos][y_pos] = player_icons.get(
                        team, pygame.Color("white")
                    )

        # Save the previous ball position before updating it
        if self.previous_ball_pos:
            prev_ball_x = self.previous_ball_pos[0]
            prev_ball_y = self.previous_ball_pos[1]
        else:
            prev_ball_x = 0
            prev_ball_y = 0

        # Set the previous ball position to grey
        field_icons[prev_ball_x][prev_ball_y] = pygame.Color("grey")

        # Find the player holding the ball and display the ball with that player's icon
        ball_x = self.ball["x_pos"]
        ball_y = self.ball["y_pos"]
        self.previous_ball_pos = (self.ball["x_pos"], self.ball["y_pos"])
        player_with_ball_info = self.field_positions[ball_x][ball_y]
        player_with_ball = player_with_ball_info.get("player")
        if player_with_ball:
            team = (
                "user"
                if player_with_ball in [i["name"] for i in self.user_team["players"]]
                else "opponent"
            )
            field_icons[ball_x][ball_y] = player_icons.get(
                "ball", pygame.Color("white")
            )

        # Display the field in Pygame
        cell_size = 30
        for x_pos in range(self.x):
            for y_pos in range(self.y):
                pygame.draw.rect(
                    self.screen,
                    field_icons[x_pos][y_pos],
                    (x_pos * cell_size, y_pos * cell_size, cell_size, cell_size),
                )

        pygame.display.flip()

    def display_debug1(self):  # by ChatGPT
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

        # Move the cursor to the beginning of the line using carriage return
        sys.stdout.write("\r")

        # Display the field without a newline
        sys.stdout.flush()
        for row in field_icons:
            sys.stdout.write(" ".join(row) + " ")
            sys.stdout.write("\n")

        # Flush the output to ensure it's visible immediately
        sys.stdout.flush()

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

    def calculate_place_to_pass(self, coords, player):
        for coord in coords:
            if (
                coord[0] <= self.ball["x_pos"]
                and self.possession == self.right_team
                or coord[0] >= self.ball["x_pos"]
                and self.possession == self.left_team
            ):
                continue
            if self.check_if_valid_pass(
                self.ball["x_pos"], self.ball["y_pos"], coord[0], coord[1]
            ):
                return coord[0], coord[1]
        return False

    def calculate_place_to_tackle(self, coords, team):
        return False
        x_pos, y_pos = self.ball["x_pos"], self.ball["y_pos"]

        opposing_player_one = self.find_nearest_player(
            self.ball["x_pos"], self.ball["y_pos"]
        )  # self.field_positions[self.ball["x_pos"]][self.ball["y_pos"]]
        opposing_player_two = self.find_nearest_player_tward_goal(
            self.ball["x_pos"], self.ball["y_pos"], team
        )
        if self.check_if_valid_pass(
            x_pos, y_pos, opposing_player_one[0], opposing_player_one[1]
        ):
            for coord in coords:  # Middle
                if (
                    (coord[0] > x_pos and coord[0] < opposing_player_one[0])
                    or (coord[0] < x_pos and coord[0] > opposing_player_one[0])
                    and (
                        coord[1] > y_pos and coord[1] < opposing_player_one[1]
                        if y_pos - opposing_player_one[1] < 0
                        else coord[1] < y_pos and coord[1] > opposing_player_one[1]
                    )
                ):
                    return coord[0], coord[1]
        if (
            self.check_if_valid_pass(
                x_pos, y_pos, opposing_player_two[0], opposing_player_two[1]
            )
            if opposing_player_two
            else 3 == 4
        ):
            for coord in coords:  # Middle
                if (
                    (coord[0] > x_pos and coord[0] < opposing_player_two[0])
                    or (coord[0] < x_pos and coord[0] > opposing_player_two[0])
                    and (
                        coord[1] > y_pos and coord[1] < opposing_player_two[1]
                        if y_pos - opposing_player_two[1] < 0
                        else coord[1] < y_pos and coord[1] > opposing_player_two[1]
                    )
                ):
                    return coord[0], coord[1]
        for coord in coords:
            if coord[0] == self.ball["x_pos"] or coord[1] == self.ball["y_pos"]:
                return coord[0], coord[1]
        return False

    def game_continue(self):
        on_game_players = []
        for x_pos in range(self.x):
            for y_pos in range(self.y):
                if self.possession == self.right_team:
                    x_pos = self.x - 1 - x_pos
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
                    for i in self.left_team["players"]:
                        if i["name"] == current_player:
                            team = self.left_team
                            break
                        else:
                            team = self.right_team
                    current_rating = self.field_positions[x_pos][y_pos]["rating"]
                    current_position = self.field_positions[x_pos][y_pos]["position"]
                    division_factor = (
                        10
                        if current_rating < 1000
                        else current_rating / (current_rating / 10)
                        if current_rating < 3000
                        else current_rating / (current_rating / 100)
                    )
                    if not current_player or current_position == "GK":
                        continue
                    new_coords = []
                    if (
                        self.ball.get("x_pos") == self.x - 1
                        or self.ball.get("x_pos") == 0
                    ):
                        for i in range(round(current_rating / division_factor)):
                            for _ in range(int(current_rating)):
                                offset_x = random.randint(
                                    -round(self.x / 10),
                                    round(self.x / 10),
                                )
                                offset_y = random.randint(
                                    -round(self.x / 10),
                                    round(self.x / 10),
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

                        coord = self.calculate_place_to_pass(
                            new_coords, self.field_positions[x_pos][y_pos]
                        )
                        coord_two = False
                        if coord:
                            new_x, new_y = coord[0], coord[1]
                        else:
                            coord_two = self.calculate_place_to_tackle(new_coords, team)

                        if coord_two:
                            new_x, new_y = coord_two[0], coord_two[1]
                        else:
                            closest_player = min(
                                new_coords,
                                key=lambda p: (p[0] - self.ball["x_pos"]) ** 2
                                + (p[1] - self.ball["y_pos"]) ** 2,
                            )
                            new_x, new_y = closest_player
                    else:
                        for i in range(round(current_rating / division_factor)):
                            for _ in range(int(current_rating)):
                                offset_x = random.randint(
                                    -round(self.x / 10),
                                    round(self.x / 10),
                                )
                                offset_y = random.randint(
                                    -round(self.x / 10),
                                    round(self.x / 10),
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

                        coord = self.calculate_place_to_pass(
                            new_coords, self.field_positions[x_pos][y_pos]
                        )
                        coord_two = self.calculate_place_to_tackle(new_coords, team)
                        if coord:
                            new_x, new_y = coord[0], coord[1]
                        elif coord_two:
                            new_x, new_y = coord_two[0], coord_two[1]
                        else:
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

                        # Check if the player had the ball, and if so, move the ball with them "GPT"(some i did most myself)
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
                        if self.check_if_valid_pass(x_pos, y_pos, coords[0], coords[1]) and self.field_positions[coords[0]][coords[1]]["position"] != "GK":
                            self.move_ball(x_pos, y_pos, coords[0], coords[1])
                            self.passes += 1
                            return
                        else:
                            coords = self.find_nearest_player(x_pos, y_pos)
                            if self.field_positions[coords[0]][coords[1]]["position"] != "GK":
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
        goal_y = round((self.y - 1) / 2)  # Middle of the goal
        player = self.field_positions[x_pos][y_pos].get("player")
        for i in team["players"]:
            if player:
                if player != i["name"]:
                    for x in range(self.x):
                        for y in range(self.y):
                            try:
                                if self.field_positions[x][y]["player"] == i["name"]:
                                    player_coords.append({"x_pos": x, "y_pos": y})
                            except:
                                pass
            else:
                return False

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
                        player = self.field_positions[x_to - x][y_to - y].get("player")
                        if player in [i["name"] for i in self.possession["players"]]:
                            continue
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
                        player = self.field_positions[x_to - x][y_to - y].get("player")
                        if player in [i["name"] for i in self.possession["players"]]:
                            continue
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
                            player = self.field_positions[x_to - x][y_to - y].get(
                                "player"
                            )
                            if player in [i["name"] for i in self.possession["players"]]:
                                continue
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
                            player = self.field_positions[x_to - x][y_to - y].get(
                                "player"
                            )
                            if player in [i["name"] for i in self.possession["players"]]:
                                continue
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
                goal_y = round((self.y - 1) / 2)
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
        self.ball = {"x_pos": round(self.x / 2) - 1, "y_pos": round((self.y - 1) / 2)}
        self.left_team = self.right_team
        self.right_team = team
        self.field_positions = [[{} for _ in range(self.y)] for _ in range(self.x)]

        # Positioning of players dynamic
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
            (round((self.x) / 2) - 2, round((self.y - 1) / 2), {"position": "ST"}),
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
