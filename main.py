import csv, asyncio, os

from tasks.pumpfun import Pumpfun
from tasks.fart_ai import fart_detect
from tasks.test_fart import test_fart_detect


async def main():
    pumpfun = Pumpfun()

    # For test purposes
    # mp3_file_path = r"audio\2890-preview.mp3"     # Zipper
    # mp3_file_path = r'audio\2891-preview.mp3'  # Fart
    # mp3_file_path = r'audio\3050-preview.mp3'     # Fart
    # mp3_file_path = r'audio\3051-preview.mp3'     # Fart
    # mp3_file_path = r'audio\3053-preview.mp3'     # Fart
    # mp3_file_path = r'audio\3054-preview.mp3'     # Fart
    # mp3_file_path = r'audio\3055-preview.mp3'     # Fart
    # mp3_file_path = r'audio\fart-02.mp3'          # Fart
    # test_fart_detect(mp3_file_path)

    fart_detect()
    await pumpfun.create_token()


if __name__ == '__main__':
    # if platform.system() == "Windows":
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
