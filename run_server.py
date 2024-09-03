import webbrowser
import subprocess
import sys
import time
import requests

def run_server():
    server_process = subprocess.Popen([sys.executable, 'server.py'])
    return server_process

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

def wait_for_server():
    url = 'http://127.0.0.1:5000'
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(1)

def main():
    try:
        server_process = run_server()
        wait_for_server()
        open_browser()

        server_process.communicate()

    except KeyboardInterrupt:
        server_process.terminate()
        print("\nServer stopped.")

    except Exception as e:
        print(f"An error occurred: {e}")
        server_process.terminate()

if __name__ == '__main__':
    main()
