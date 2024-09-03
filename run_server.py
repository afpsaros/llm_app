import webbrowser
import subprocess
import sys

def run_server():
    # Start the Flask server using subprocess
    server_process = subprocess.Popen([sys.executable, 'server.py'])
    return server_process

def open_browser():
    # Automatically open the default web browser to the Flask app
    webbrowser.open_new('http://127.0.0.1:5000')

def main():
    server_process = run_server()
    open_browser()

    try:
        # Keep the script running while the server is active
        server_process.communicate()
    except KeyboardInterrupt:
        server_process.terminate()
        print("\nServer stopped.")

if __name__ == '__main__':
    main()
