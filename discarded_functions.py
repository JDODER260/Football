def calculate_place_to_tackle(self, coords, team):
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
    elif self.check_if_valid_pass(x_pos, y_pos, opposing_player_two[0], opposing_player_two[1]) if opposing_player_two else 3 == 4:
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
                        -round(current_rating / 10), round(current_rating / 10)
                    )
                    offset_y = random.randint(
                        -round(current_rating / 10), round(current_rating / 10)
                    )
                    new_x = max(0, min(self.x - 1, x_pos + offset_x))
                    new_y = max(0, min(self.y - 1, y_pos + offset_y))
                else:
                    new_coords = []
                    for i in range(round(current_rating / 10)):
                        while True:
                            offset_x = random.randint(
                                -round(current_rating / 10),
                                round(current_rating / 10),
                            )
                            offset_y = random.randint(
                                -round(current_rating / 10),
                                round(current_rating / 10),
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
                    coord_two = self.calculate_place_to_tackle(
                        new_coords, self.field_positions[x_pos][y_pos]
                    )
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




def game_continue1(self):
    for x_pos in range(31):
        for y_pos in range(13):
            try:
                if self.field_positions[x_pos][y_pos] and self.field_positions[x_pos][y_pos]["position"] != "GK":
                    for i in self.opponent_team["players"]:
                        if self.field_positions[x_pos][y_pos]["player"] == i["name"]:
                            for x in range(10):
                                x_pos1 = x_pos + random.randint(0, 3)
                                # int(int(i["rating"])/10))
                                y_pos1 = y_pos + random.randint(0, 3)
                                # int(int(i["rating"])/10))
                                try:
                                    if not self.field_positions[x_pos1][y_pos1]:
                                        self.field_positions[x_pos1][y_pos1] = {
                                            "player": i["name"], "position": i["position"]}
                                        self.field_positions[x_pos][y_pos] = {
                                        }
                                        print("break")
                                        break
                                except:
                                    print("exept")
                    for i in self.user_team["players"]:
                        if self.field_positions[x_pos][y_pos]["player"] == i["name"]:
                            for x in range(10):
                                x_pos1 = x_pos + random.randint(0, 3)
                                # int(int(i["rating"])/10))
                                y_pos1 = y_pos + random.randint(0, 3)
                                # int(int(i["rating"])/10))
                                if not x_pos1 <= 0 and not x_pos1 >= 31 and not y_pos1 < 0 and not y_pos1 > 12 and not self.field_positions[x_pos1][y_pos1]:
                                    self.field_positions[x_pos1][y_pos1] = {
                                        "player": i["name"], "position": i["position"]}
                                    self.field_positions[x_pos][y_pos] = {
                                    }
                                    print("break")
                                    break
            except:
                print("big exept")


    def find_nearest_player(self, x_pos, y_pos, team):
        player_coords = []
        player_coords_lined = []
        for i in team:
            if self.field_positions[x_pos][y_pos]["player"] != i["name"]:
                for x in range(31):
                    for y in range(13):
                        if self.field_positions[x][y]["player"] == i["name"]:
                            player_coords.append({"x_pos": x, "y_pos": y})
        for i in range(len(player_coords)):
            if i == 0:
                player_coords_lined.append(i)
                break
            for z in range(len(player_coords_lined)):




def pass_ball(self, team):
        for x_pos in range(31):
            for y_pos in range(13):
                if x_pos == self.ball["x_pos"] and y_pos == self.ball["y_pos"]:
                    if self.field_positions[x_pos][y_pos]["player"]:
                        coords = self.find_nearest_player(x_pos, y_pos, team)
                        self.field_positions[x_pos][y_pos] = {"player": self.field_positions[x_pos][y_pos]["player"],
                                                              "position": self.field_positions[x_pos][y_pos]["position"], "rating": self.field_positions[x_pos][y_pos]["rating"]}
                        self.ball = {
                            "x_pos": coords[0], "y_pos": coords[1]}
                        self.field_positions[coords[0]][coords[1]] = {"player": self.field_positions[coords[0]][coords[1]]["player"], "position": self.field_positions[
                            coords[0]][coords[1]]["position"], "rating": self.field_positions[coords[0]][coords[1]]["rating"], "x_pos": coords[0], "y_pos": coords[1]}



















def find_player_starting_pos(self, position, side):
        if side == "left":
            print((round(self.x/2)), " left")
            for x_pos in range(round(self.x/2)):
                for y_pos in range(self.y):
                    try:
                        if self.field_positions[x_pos][y_pos]["position"] == position:
                            return x_pos, y_pos
                    except:
                        pass

        if side == "right":
            print(round(self.x/2)-2)
            for x_pos in range(round(self.x/2-2), self.x):
                for y_pos in range(self.y):
                    try:
                        if self.field_positions[x_pos][y_pos]["position"] == position:
                            return x_pos, y_pos
                    except:
                        pass
        else:
            exception: print("Something went wrong")

    def place_player(self, x_pos, y_pos, name, position, rating):
        self.field_positions[x_pos][y_pos] = {
            "player": name, "position": position, "rating": rating}

    def place_team(self, team, side):
        random_squad = []
        squad = []
        for i in team:
            random_squad.append(
                {"name": i["name"], "position": i["position"], "rating": i["rating"]})
        random.shuffle(random_squad)
        for i in self.positions:
            for x in random_squad:
                if i == x["position"]:
                    squad.append(x)
                    break

        for player in squad:
            pos = self.find_player_starting_pos(
                player["position"], side)
            try:
                self.place_player(
                    pos[0], pos[1], player["name"], player["position"], player["rating"])
            except:
                print(f"couldn't place {pos}")
