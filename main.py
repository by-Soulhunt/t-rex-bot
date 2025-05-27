from PIL import Image
import pyautogui
import mss
import time

class TrexBot:
    def __init__(self):
        self.color = None
        self.night_mode = False
        self.pixels = None
        self.bw_screen = None
        self.screen = None
        self.fly_pixel_middle = 0
        self.cactus_pixel_bot = 0
        self.left_screen_distance = 135
        self.screen_width = 200
        self.game_speed = -1
        self.start_time = time.time()


    def run(self):
        """
        Main game logic
        :return: None
        """
        while True:
            self.change_game_speed()
            # Take screen and load pixels
            self.screen = self.fast_screenshot()
            # self.screen.save("test.png") # TEST
            # break # TEST

            # Check normal/night game mode
            tmp_pixels = self.screen.load()
            game_mode_pixel_check = tmp_pixels[199, 269]
            if game_mode_pixel_check[0] < 255:
                self.night_mode = True
            else:
                self.night_mode = False
            print(f"Night mode: {self.night_mode}") # TEST


            self.bw_screen = self.img_to_bw(self.screen, self.night_mode)
            self.pixels = self.bw_screen.load()

            # Refresh obstacle count
            self.cactus_pixel_bot = 0
            self.fly_pixel_middle = 0

            # Flag to break from loop
            should_jump = False

            # Analyze screen from right/bot to left/top
            for h_pixel in range(self.bw_screen.height - 1, -1, self.game_speed):
                for w_pixel in range(self.bw_screen.width - 1, -1, self.game_speed):
                    self.color = self.pixels[w_pixel, h_pixel]
                    # Check cactus and bot bird zone
                    if self.color == 0 and 145 < h_pixel < 210:
                        print(f"145-200 zone: {h_pixel}") # TEST
                        self.cactus_pixel_bot += 1
                    # Check middle bird zone
                    elif self.color == 0 and 100 < h_pixel < 144:
                        print(f"100-144 zone: {h_pixel}")  # TEST
                        self.fly_pixel_middle += 1
                    else: # If white pixel found - refresh counts
                        self.cactus_pixel_bot = 0
                        self.fly_pixel_middle = 0
                    # If obstacle found - jump and break from inner loop
                    if self.cactus_pixel_bot > 15 or self.fly_pixel_middle > 10:
                        pyautogui.press("space")
                        should_jump = True
                        break
                # Break from outer loop
                if should_jump:
                    break

    @staticmethod
    def img_to_bw(screen, mode):
        """
        Convert current screen into black/white image
        :param mode: True if game in night mode
        :param screen: Screenshot zone to analyze
        :return: Inverted black/white image
        """
        gray_screen = screen.convert('L')
        if mode:
            bw_screen = gray_screen.point(lambda x: 0 if x > 128 else 255, '1')
        else:
            bw_screen = gray_screen.point(lambda x: 0 if x < 128 else 255, '1')

        return bw_screen


    def fast_screenshot(self):
        with mss.mss() as sct:
            monitor = {"top": 600, "left": self.left_screen_distance, "width": self.screen_width, "height": 270}
            sct_img = sct.grab(monitor)
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
            return img

    def change_game_speed(self):
        """
        Compare start game time and current. Change analyse pixels regarding game speed.
        :return: Value to use in range like step.
        """
        game_time = time.time() - self.start_time
        if game_time < 10:
            self.left_screen_distance = 135
            print("🔵 Speed 1") # TEST
            print(f"Speed distance {self.left_screen_distance}") # TEST
        elif game_time < 20:
            self.left_screen_distance = 200
            print("🔵 Speed 1") # TEST
            print(f"Speed distance {self.left_screen_distance}")  # TEST
        elif game_time < 35:
            self.left_screen_distance = 250
            print("🔵 Speed 1") # TEST
            print(f"Speed distance {self.left_screen_distance}")  # TEST
        elif game_time < 60:
            self.game_speed = -2
            self.left_screen_distance = 300
            print("🔴 Speed 2") # TEST
            print(f"Speed distance {self.left_screen_distance}")  # TEST

        else:
            self.game_speed = -3
            self.left_screen_distance = 400
            print("🔴 Speed 3") # TEST



if __name__ == "__main__":
    app = TrexBot()
    pyautogui.sleep(2.0)
    app.run()