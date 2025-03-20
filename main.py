import time
from app import FlaskServer

def main():
    # create server object
    flask = FlaskServer()
    
    # % python main.py   art server in discrete thread
    flask.run()

    print("Main application running...")

    # main app loop, placeholder for sensor arbitration
    try:
        count = 0
        while True:
            time.sleep(5)  # hold time between zone changes
            message = f"{count%3}"
            print(f"Update: {message}")
            flask.send_message("update_zone", {"data": message})
            count += 1
    except KeyboardInterrupt:
        print("Shutting down...") # expand to ensure clean shutdown


if __name__ == "__main__":
    main()