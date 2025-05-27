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
            self.screen = pyautogui.screenshot(region=(120, 600, 300, 248))
            self.bw_screen = self.img_to_bw(self.screen)
            self.pixels = self.bw_screen.load()

            self.cactus_pixel_bot = 0

            should_jump = False

            for h_pixel in range(self.bw_screen.height - 1, -1, -1):
                for w_pixel in range(self.bw_screen.width - 1, -1, -1):
                    self.color = self.pixels[w_pixel, h_pixel]
                    if self.color == 0 and 145< h_pixel < 200:
                        self.cactus_pixel_bot += 1
                    else:
                        self.cactus_pixel_bot = 0
                    if self.cactus_pixel_bot > 15:
                        pyautogui.press("space")
                        should_jump = True
                        break
                if should_jump:
                    break

    @staticmethod
    def img_to_bw(screen):
        gray_screen = screen.convert('L')
        bw_screen = gray_screen.point(lambda x: 0 if x < 128 else 255, '1')

        return bw_screen


if __name__ == "__main__":
    app = TrexBot()
    pyautogui.sleep(2.0)
    app.run()