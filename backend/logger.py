from datetime import datetime


def log(message):
    time = datetime.now().strftime("%H:%M:%S")

    log_message = f"[{time}] {message}"

    print(log_message)

    with open("logs/scanner.log", "a") as file:
        file.write(log_message + "\n")