import asyncio
import pyautogui
import cv2
import numpy as np
from tensorflow.python.data.experimental.ops.testing import sleep


async def find_captcha(sample_image_path):
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Load the sample image
    sample_image = cv2.imread(sample_image_path, cv2.IMREAD_UNCHANGED)
    if sample_image is None:
        raise ValueError(f"Sample image at {sample_image_path} could not be loaded.")

    # Perform template matching
    result = cv2.matchTemplate(screenshot, sample_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Define a threshold for detecting a match
    threshold = 0.8
    if max_val >= threshold:
        # Coordinates of the top-right corner
        top_left = max_loc
        h, w = sample_image.shape[:2]
        x = top_left[0] + 30
        y = top_left[1] + 30
        # Move the mouse cursor and click
        pyautogui.moveTo(x, y, duration=1)  # Smooth movement to the point
        await asyncio.sleep(0.5)

        pyautogui.click()  # Perform a left-click
        return top_left
    else:
        return None


async def solve_captcha(times: int, delay: int | None = 1):
    sample_image_path = "cloudflare.png"  # Path to your sample image
    if delay is None:
        delay = 1
    count = 0
    while True:
        try:
            result = await find_captcha(sample_image_path)
            if result:
                print(f"Captcha found at coordinates: {result}!")
                break
            else:
                if count > times:
                    break
                print(f"No Captcha found. Trying again in {delay} seconds..")
                count += 1
                await asyncio.sleep(delay)

        except ValueError as e:
            print(e)
