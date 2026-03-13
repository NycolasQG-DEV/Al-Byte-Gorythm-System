import time
import cv2
import numpy as np
import config

class EyePosition:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.left_eye_x = window_width // 2 - 160
        self.right_eye_x = window_width // 2 + 160
        self.circle_y = window_height // 2
        self.blink_state = False
        self.min_eye_distance = 320
        self.movement_offset = 0
        self.movement_direction = 1

    def draw(self, img):
        circle_radius = 100
        _state = config.ROBOT_EXPRESSION_INDEX

        if self.blink_state and _state not in [0, 6, 7, 8]:
            config.BACKGROUND_COLOR = (0, 0, 0)
            cv2.rectangle(img, (self.left_eye_x - circle_radius, self.circle_y - 10),
                          (self.left_eye_x + circle_radius, self.circle_y + 10), config.EYE_COLOR, cv2.FILLED)
            cv2.rectangle(img, (self.right_eye_x - circle_radius, self.circle_y - 10),
                          (self.right_eye_x + circle_radius, self.circle_y + 10), config.EYE_COLOR, cv2.FILLED)
        else:
            config.BACKGROUND_COLOR = (0, 0, 0)

            if _state == 1:  # NEUTRAL
                cv2.circle(img, (self.left_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (self.right_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)

            elif _state == 2:  # BORED
                cv2.circle(img, (self.left_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (self.right_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.rectangle(img, (0, self.circle_y - 200), (self.window_width, self.circle_y - 10), config.BACKGROUND_COLOR, cv2.FILLED)

            elif _state == 3:  # ANGRY
                cv2.circle(img, (self.left_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (self.right_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                triangle_points = np.array([
                    [self.left_eye_x - 60, self.circle_y - 120],
                    [self.right_eye_x + 60, self.circle_y - 120],
                    [(self.left_eye_x + self.right_eye_x) // 2, self.circle_y + 100]
                ])
                cv2.fillPoly(img, [triangle_points], config.BACKGROUND_COLOR)

            elif _state == 4:  # RIGHT CLOSED
                cv2.circle(img, (self.left_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (self.right_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.rectangle(img, (self.left_eye_x + 100, self.circle_y - 200), (self.window_width, self.circle_y + 10), config.BACKGROUND_COLOR, cv2.FILLED)

            elif _state == 5:  # LEFT CLOSED
                cv2.circle(img, (self.left_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (self.right_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.rectangle(img, (0, self.circle_y - 200), (self.right_eye_x - 100, self.circle_y + 10), config.BACKGROUND_COLOR, cv2.FILLED)

            elif _state == 6:  # LAUGHING
                offset = self.movement_offset
                thickness = 14

                # Left
                cv2.line(img, (self.left_eye_x - 60, self.circle_y + offset - 60),
                         (self.left_eye_x + 60, self.circle_y + offset), config.EYE_COLOR, thickness)
                cv2.line(img, (self.left_eye_x - 60, self.circle_y + offset + 60),
                         (self.left_eye_x + 60, self.circle_y + offset), config.EYE_COLOR, thickness)

                # Right
                cv2.line(img, (self.right_eye_x - 60, self.circle_y + offset),
                         (self.right_eye_x + 60, self.circle_y + offset - 60), config.EYE_COLOR, thickness)
                cv2.line(img, (self.right_eye_x - 60, self.circle_y + offset),
                         (self.right_eye_x + 60, self.circle_y + offset + 60), config.EYE_COLOR, thickness)

            elif _state == 7:  # SEMICOLON
                # Glitch: background and text randomly change
                flicker = np.random.rand() < 0.15  # 15% chance to invert color

                if flicker:
                    bg_color = (0, 0, 0)
                    text_color = (255, 255, 255)
                else:
                    bg_color = (255, 255, 255)
                    text_color = (0, 0, 0)

                config.BACKGROUND_COLOR = bg_color
                img[:, :] = bg_color  # apply background color directly

                # Shake
                shake_x = np.random.randint(-15, 15)
                shake_y = np.random.randint(-15, 15)
                base_x = self.window_width // 2 - 80
                base_y = self.window_height // 2 + 80
                pos_x = base_x + shake_x
                pos_y = base_y + shake_y

                # Shadow glitch
                if np.random.rand() < 0.2:
                    offset_x = np.random.randint(-5, 5)
                    offset_y = np.random.randint(-5, 5)
                    cv2.putText(img, ";", (pos_x + offset_x, pos_y + offset_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 12, (0, 255, 255), 48, cv2.LINE_AA)

                # Main
                cv2.putText(img, ";", (pos_x, pos_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 12, text_color, 48, cv2.LINE_AA)

                # Horizontal glitch lines
                if np.random.rand() < 0.3:
                    for _ in range(np.random.randint(1, 4)):
                        y = np.random.randint(0, self.window_height)
                        x1 = np.random.randint(0, self.window_width // 2)
                        x2 = np.random.randint(self.window_width // 2, self.window_width)
                        color = (np.random.randint(100, 255),)*3
                        cv2.line(img, (x1, y), (x2, y), color, thickness=np.random.randint(1, 4))

            elif _state == 8:  # ERROR SCREEN WITH FREQUENT GLITCHES + INTENSE RED BURSTS

                current_time = time.time()

                # Initialize variables if not already
                if not hasattr(self, "last_glitch_burst"):
                    self.last_glitch_burst = 0
                if not hasattr(self, "glitch_burst_active"):
                    self.glitch_burst_active = False
                if not hasattr(self, "last_interference"):
                    self.last_interference = 0
                if not hasattr(self, "glitch_lines"):
                    self.glitch_lines = {}
                if not hasattr(self, "interference_active_list"):
                    self.interference_active_list = []
                if not hasattr(self, "interference_data_list"):
                    self.interference_data_list = []

                # Red burst: more frequent
                if not self.glitch_burst_active and current_time - self.last_glitch_burst > np.random.uniform(8, 12):
                    self.glitch_burst_active = True
                    self.glitch_burst_start_time = current_time
                    self.last_glitch_burst = current_time

                # Turn off burst after 0.2s
                if self.glitch_burst_active and current_time - self.glitch_burst_start_time > 0.2:
                    self.glitch_burst_active = False

                # Set background, glitch chances
                if self.glitch_burst_active:
                    config.BACKGROUND_COLOR = (0, 0, 255)
                    base_glitch_chance = 0.9
                    interference_chance = 0.4
                    max_glitches_per_frame = 10
                    max_interference_bars = 5
                else:
                    config.BACKGROUND_COLOR = (255, 50, 50)
                    base_glitch_chance = 0.15
                    interference_chance = 0.05
                    max_glitches_per_frame = 3
                    max_interference_bars = 3

                img[:, :] = config.BACKGROUND_COLOR
                font = cv2.FONT_HERSHEY_PLAIN
                text_lines = [
                    "A problem has been detected and Windows has been shut down",
                    "to prevent damage to your robot.",
                    "",
                    "The problem seems to be caused by the following file: HORTOBOTS.EXE",
                    "",
                    "PAGE_FAULT_IN_NONPAGED_AREA",
                    "",
                    "If this is the first time you've seen this Stop error screen,",
                    "restart your robot. If this screen appears again, follow",
                    "these steps:",
                    "",
                    "Check to make sure any new hardware or software is properly installed.",
                    "If this is a new installation, ask your technician or team for help.",
                    "",
                    "Technical information:",
                    "*** STOP: 0x00000050 (0xFD3098A0, 0x00000000, 0x8054B859, 0x00000000)"
                ]

                # Glitchy line drawing
                glitches_drawn = 0
                for i, line in enumerate(text_lines):
                    y = 40 + i * 22
                    key = f"line_{i}"

                    if key not in self.glitch_lines or current_time - self.glitch_lines[key]["last"] > 0.6:
                        self.glitch_lines[key] = {
                            "glitch": np.random.rand() < base_glitch_chance,
                            "invert": np.random.rand() < 0.4,
                            "shift": np.random.randint(-20, 20),
                            "last": current_time
                        }

                    glitch_data = self.glitch_lines[key]

                    if glitch_data["glitch"] and glitches_drawn < max_glitches_per_frame:
                        glitches_drawn += 1
                        text_img = np.zeros((30, 800, 3), dtype=np.uint8)
                        color = (255, 255, 255)

                        if glitch_data["invert"]:
                            cv2.putText(text_img, line, (0, 20), font, 0.7, color, 1)
                            text_img = cv2.flip(text_img, 0)
                        else:
                            cv2.putText(text_img, line, (0, 20), font, 0.7, color, 1)

                        cut_y = np.random.randint(10, 20)
                        part1 = text_img[:cut_y]
                        part2 = text_img[cut_y:]

                        x1 = 20
                        x1_end = min(x1 + part1.shape[1], img.shape[1])
                        if x1_end > x1 and y + cut_y <= img.shape[0]:
                            img[y:y+cut_y, x1:x1_end] = part1[:, :x1_end - x1]

                        x2_start = 20 + glitch_data["shift"]
                        x2_end = x2_start + part2.shape[1]

                        if x2_start < 0:
                            part2 = part2[:, -x2_start:]
                            x2_start = 0
                        if x2_end > self.window_width:
                            part2 = part2[:, :self.window_width - x2_start]
                            x2_end = self.window_width

                        if x2_end > x2_start and part2.shape[1] > 0 and y + cut_y + part2.shape[0] <= img.shape[0]:
                            img[y+cut_y:y+cut_y+part2.shape[0], x2_start:x2_end] = part2

                    else:
                        cv2.putText(img, line, (20, y), font, 0.7, (255, 255, 255), 1)

                # Interference bars
                self.interference_active_list = [t for t in self.interference_active_list if current_time - t < 0.15]
                self.interference_data_list = self.interference_data_list[-len(self.interference_active_list):]

                if len(self.interference_active_list) < max_interference_bars and np.random.rand() < interference_chance:
                    self.interference_active_list.append(current_time)
                    y_line = np.random.randint(0, self.window_height)
                    height = np.random.randint(1, 3)
                    gray = np.random.randint(20, 50)
                    self.interference_data_list.append((y_line, height, gray))

                for i, t in enumerate(self.interference_active_list):
                    y_line, height, gray = self.interference_data_list[i]
                    cv2.rectangle(img, (0, y_line), (self.window_width, y_line + height), (gray, gray, gray), -1)

            elif _state == 9:  # SAD
                config.BACKGROUND_COLOR = (0, 0, 0)
                cv2.circle(img, (self.left_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (self.right_eye_x, self.circle_y), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (self.left_eye_x, self.circle_y - 100), circle_radius, (0, 0, 0), cv2.FILLED)
                cv2.circle(img, (self.right_eye_x, self.circle_y - 100), circle_radius, (0, 0, 0), cv2.FILLED)
                config.BACKGROUND_COLOR = (0, 0, 0)

    def update_position(self):
        if self.movement_offset > 30 or self.movement_offset < -30:
            self.movement_direction *= -1
        self.movement_offset += self.movement_direction * 8

    def blink(self):
        if config.ROBOT_EXPRESSION_INDEX not in [6, 7, 8]:
            self.blink_state = True
            time.sleep(0.1)
            self.blink_state = False

def blink_eyes(eye_position):
    while True:
        time.sleep(5)
        eye_position.blink()

def animate_eyes(eye_position):
    while True:
        time.sleep(0.05)
        eye_position.update_position()
