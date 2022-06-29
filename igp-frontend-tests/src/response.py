from colorama import Fore, Style


def info(message):
    print(f"{message}")


def testing(message):
    print(f"TESTING: {message}")


def success(message):
    print(f"{Fore.GREEN}SUCCESS: {message}{Style.RESET_ALL}")


def fail(message):
    print(f"{Fore.RED}FAIL: {message}{Style.RESET_ALL}")


def error(message):
    print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")
