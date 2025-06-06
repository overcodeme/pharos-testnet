from anticaptchaofficial.recaptchav2proxyless import *
from main import settings
from colorama import Fore, Style


async def createCaptchaTask(url, key):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(settings['ANTICAPTCHA_KEY'])
    solver.set_website_url(url)
    solver.set_website_key(key)

    token = solver.solve_and_return_solution()
    if token != 0:
        return token
    else:
        print(Fore.RED + 'Error while solving captcha' + Style.RESET_ALL)