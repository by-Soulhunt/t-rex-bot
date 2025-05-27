from PIL import Image
import pyautogui

class TrexBot:
    def __init__(self):
        self.color = None
        self.counter = 0
        self.pixels = None
        self.bw_screen = None
        self.screen = None
        self.fly_pixel_middle = 0
        self.cactus_pixel_bot = 0


    def run(self):
        while True:
            # Take screen and load pixels
            self.screen = pyautogui.screenshot(region=(135, 600, 300, 248))
            self.bw_screen = self.img_to_bw(self.screen)
            self.pixels = self.bw_screen.load()

            # Refresh obstacle count
            self.cactus_pixel_bot = 0
            self.fly_pixel_middle = 0

            # Flag to break from loop
            should_jump = False

            # Analyze screen from right/bot to left/top
            for h_pixel in range(self.bw_screen.height - 1, -1, -1):
                for w_pixel in range(self.bw_screen.width - 1, -1, -1):
                    self.color = self.pixels[w_pixel, h_pixel]
                    # Check cactus and bot bird zone
                    if self.color == 0 and 145 < h_pixel < 200:
                        self.cactus_pixel_bot += 1
                    # Check middle bird zone
                    elif self.color == 0 and 100 < h_pixel < 144:
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
    def img_to_bw(screen):
        """
        Convert current screen into black/white image
        :param screen: Screenshot zone to analyze
        :return: Inverted black/white image
        """
        gray_screen = screen.convert('L')
        bw_screen = gray_screen.point(lambda x: 0 if x < 128 else 255, '1')

        return bw_screen


if __name__ == "__main__":
    app = TrexBot()
    pyautogui.sleep(2.0)
    app.run()