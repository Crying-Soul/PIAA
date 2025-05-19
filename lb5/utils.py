from colorama import Fore, Style, init  # type: ignore

# Инициализация colorama для работы с цветами в консоли
init(autoreset=True)

# === Логирование ===
def log_section(title):
    print(Fore.BLUE + f"\n{'='*10} {title.upper()} {'='*10}")

def log_substep(message):
    print(Fore.CYAN + f"→ {message}")

def log_action(message):
    print(Fore.YELLOW + f"  └─ {message}")

def log_info(message):
    print(Fore.WHITE + f"     • {message}")

def log_success(message):
    print(Fore.GREEN + f"✔ {message}")

def log_warning(message):
    print(Fore.RED + f"⚠ {message}")

def log_result(message):
    print(Fore.MAGENTA + f"⇒ {message}")
