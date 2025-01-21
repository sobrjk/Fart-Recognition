import asyncio

from playwright.async_api import async_playwright, expect

import config
from config import *

from tasks.screen_ai import solve_captcha
import keyboard
import pywinauto


class Pumpfun:
    def __init__(self):
        self.url = 'https://pump.fun/create'

    async def create_token(self):
        print('Creating token')
        async with async_playwright() as p:
            context = await p.chromium.connect_over_cdp(endpoint_url='http://localhost:9222')
            default_context = context.contexts[0]
            flag = False
            for i in default_context.pages:
                if i.url == 'https://pump.fun/create':
                    await i.bring_to_front()
                    page = i
                    flag = True
            if flag is False:
                page = await context.new_page()
            await page.goto(self.url)

            # Set Token name
            name = page.locator("[id='name']")
            await expect(name).to_be_visible()
            await name.first.clear()
            await name.first.type(config.NAME, delay=150)
            await page.wait_for_timeout(1000)

            # Set token tiker
            name = page.locator("[id='ticker']")
            await expect(name).to_be_visible()
            await name.first.clear()
            await name.first.type(config.TIKER, delay=150)
            await page.wait_for_timeout(1000)

            # Set token description
            name = page.locator("[id='text']")
            await expect(name).to_be_visible()
            await name.first.clear()
            await name.first.type(config.TEXT, delay=150)
            await page.wait_for_timeout(1000)

            # Upload file
            await page.set_input_files('input[type="file"]', FILE)

            # Click Create coin button
            connect = page.get_by_role('button', name="create coin")
            await expect(connect).to_be_visible()
            await page.wait_for_timeout(1000)
            await connect.click()
            await page.wait_for_timeout(1000)

            # Fill Amount field
            amount = page.locator("[id='amount']")
            await expect(amount).to_be_visible()
            await amount.first.clear()
            await amount.click()
            await amount.first.type(config.AMOUNT, delay=150)
            await page.keyboard.press('Tab')
            await page.wait_for_timeout(1000)

            # Solve Captcha
            # captcha = page.frame_locator("#cf-chl-widget-aitlp")
            # await asyncio.sleep(5)
            # await page.keyboard.press('Tab')
            # await expect(captcha).to_be_visible(timeout=10000)
            # page = await context.new_page()
            await asyncio.sleep(1)

            await solve_captcha(times=10, delay=1)

            await page.wait_for_timeout(1000)
            # Click Create coin button again
            create = page.get_by_role('button', name="create coin")
            await expect(create).to_be_enabled(timeout=30000)
            await create.click()
            await page.wait_for_timeout(1000)

            # Click View button
            connect = page.get_by_role('button', name="View")
            await expect(connect).to_be_visible(timeout=20000)
            await connect.click()
            await page.wait_for_timeout(5000)

            await asyncio.sleep(10)
