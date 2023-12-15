import os
import time
import random
import pygame
from pygame.locals import *
from math import radians, sin, cos
running = True
def stop():
    global running
    running = False

def main():
    global running
    def random_color() -> tuple:
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def random_speed() -> float:
        return float(random.uniform(min_speed, max_speed))

    def round_color(color: list) -> tuple:
        return tuple(round(x) for x in color)

    def check_collision(obj1, obj2):
        if (obj1["x"] + obj1["size"] / 2) < (obj2["x"] - obj2["size"] / 2):
            return False  # No collision from the left

        if (obj1["x"] - obj1["size"] / 2) > (obj2["x"] + obj2["size"] / 2):
            return False  # No collision from the right

        if (obj1["y"] + obj1["size"] / 2) < (obj2["y"] - obj2["size"] / 2):
            return False  # No collision from the top

        if (obj1["y"] - obj1["size"] / 2) > (obj2["y"] + obj2["size"] / 2):
            return False  # No collision from the bottom

        return True  # Colliding in one or more directions

        dx = obj2["x"] - obj1["x"]
        dy = obj2["y"] - obj1["y"]
        distance = (dx**2) - (dx**2) / 0.5
        print(dx, dy, distance)
        if distance < (obj1["size"] + obj2["size"]):
            return True
        return False

    def calc_speed():
        for i in range(3):
            color_speed[i] = (to_color[i] - from_color[i]) / speed

    # Initialize Pygame
    pygame.init()
    info_object = pygame.display.Info()
    w, h = info_object.current_w, info_object.current_h
    screen = pygame.display.set_mode((w, h), pygame.DOUBLEBUF, pygame.HWSURFACE)
    pygame.display.set_caption("ScreenSaver")

    # Initialize colors and speeds
    from_color = (23, 142, 60)
    current_color = [0, 0, 0]
    to_color = random_color()
    min_speed = 0.5
    max_speed = 3.0
    color_speed = [0.0, 0.0, 0.0]  # Initialize color_speed
    st = time.time()
    # Initialize 3D objects
    objects = []
    num_objects = 30

    for _ in range(num_objects):
        obj = {
            "x": random.uniform(0, w),
            "y": random.uniform(0, h),
            "dx": random.uniform(-1, 1),
            "dy": random.uniform(-1, 1),
            "size": random.uniform(10, 100),
            "color": random_color(),
            "speed": random_speed(),
        }
        objects.append(obj)

    # Initialize 2D shapes (Circles, Triangles, Lines)
    shapes = []
    num_shapes = 20

    for _ in range(num_shapes):
        shape = {
            "x": random.uniform(0, w),
            "y": random.uniform(0, h),
            "dx": random.uniform(-1, 1),
            "dy": random.uniform(-1, 1),
            "size": random.uniform(10, 50),
            "color": random_color(),
            "speed": random_speed(),
        }
        shapes.append(shape)

    # Initialize "Loading" text
    font = pygame.font.Font(None, 90)
    text = font.render("Loading", True, (255, 255, 255))
    text2 = font.render("Loading", True, (255, 255, 255))
    text3 = font.render("Loading", True, (255, 255, 255))
    text_x, text_y = w // 2 - text.get_width() // 2, h // 2 - text.get_height() // 2

    text_angle = 20
    text_speed = 50  # Adjust the speed of text movement

    # Additional variables for controlling the screensaver duration
    screensaver_duration = 1000000000  # Duration in seconds
    current_timer = 0.0
    start_time = time.time()
    speed = 3
    # Main loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        now = time.time()
        delta = now - start_time
        current_timer += delta
        start_time = now
        n = now - st
        if n >= screensaver_duration:
            running = False

        current_color[0] += delta * color_speed[0]
        current_color[1] += delta * color_speed[1]
        current_color[2] += delta * color_speed[2]

        if current_timer >= speed:
            current_timer = 0.0
            current_color = list(to_color)
            from_color = to_color
            to_color = random_color()
            speed = random_speed()
            calc_speed()

        for obj in objects:
            obj["x"] += obj["dx"] * obj["speed"]
            obj["y"] += obj["dy"] * obj["speed"]

            # Bounce off the screen edges
            if obj["x"] < 0 or obj["x"] + obj["size"] > w:
                obj["dx"] *= -1
            if obj["y"] < 0 or obj["y"] + obj["size"] > h:
                obj["dy"] *= -1

            # Check collisions with other objects
            for other_obj in objects:
                if obj != other_obj:
                    if check_collision(obj, other_obj):
                        # Reverse directions for both objects
                        obj["dx"], obj["dy"] = -obj["dx"], -obj["dy"]
                        other_obj["dx"], other_obj["dy"] = (
                            -other_obj["dx"],
                            -other_obj["dy"],
                        )

        for shape in shapes:
            shape["x"] += shape["dx"] * shape["speed"]
            shape["y"] += shape["dy"] * shape["speed"]

            # Bounce off the screen edges
            if shape["x"] < 0 or shape["x"] + shape["size"] > w:
                shape["dx"] *= -1
            if shape["y"] < 0 or shape["y"] + shape["size"] > h:
                shape["dy"] *= -1

        # Update text position and angle
        text_x += text_speed * delta
        text_y = h // 2 - text.get_height() // 2
        text_angle += text_speed * delta

        # Wrap text to the other side of the screen
        if text_x > w:
            text_x = -text.get_width()

        # Update text position and angle
        text_x += text_speed * delta
        text_y = h // 2 - text2.get_height() // 2 + 6
        text_angle += text_speed * delta

        # Wrap text to the other side of the screen
        if text_x > w:
            text_x = -text2.get_width()
        text_x += text_speed * delta
        text_y = h // 2 - text3.get_height() // 2 + 2
        text_angle += text_speed * delta

        # Wrap text to the other side of the screen
        if text_x > w:
            text_x = -text3.get_width()
        screen.fill(round_color(current_color))
        for obj in objects:
            pygame.draw.rect(
                screen, obj["color"], (obj["x"], obj["y"], obj["size"], obj["size"])
            )
        for shape in shapes:
            pygame.draw.circle(
                screen,
                shape["color"],
                (int(shape["x"]), int(shape["y"])),
                int(shape["size"]),
            )

        # Rotate and draw the text
        rotated_text = pygame.transform.rotate(text, text_angle)
        screen.blit(rotated_text, (text_x, text_y))
        rotated_text = pygame.transform.rotate(text2, text_angle)
        screen.blit(rotated_text, (text_x, text_y))
        rotated_text = pygame.transform.rotate(text3, text_angle)
        screen.blit(rotated_text, (text_x, text_y))

        pygame.display.flip()

    # Clean up
    pygame.quit()


main()
