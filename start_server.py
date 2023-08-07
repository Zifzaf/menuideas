import subprocess
import time
import threading
import schedule


def start_server():
    subprocess.Popen(["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"])


def check_server():
    while True:
        if (
            subprocess.run(
                ["pgrep", "-f", "gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app"],
                stdout=subprocess.PIPE,
            ).returncode
            != 0
        ):
            print("Gunicorn is not running. Restarting...")
            start_server()
        time.sleep(60)


def run_crawler():
    subprocess.run(["python3", "crawler.py"])


if __name__ == "__main__":
    # Start Gunicorn server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    run_crawler()

    # Schedule crawler to run once a day
    schedule.every().day.at("02:00").do(run_crawler)

    # Start the server checking thread
    check_thread = threading.Thread(target=check_server)
    check_thread.start()

    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(3600)
