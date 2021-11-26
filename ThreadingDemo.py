import json
import threading
from time import sleep


def randomTask(time_to_complete):
    """
    This is a function that defines a pseudo task, with a specified time to complete.
    :param time_to_complete:
    :return:
    """
    # Notes
    # .join() will block the main thread at the point where it applied in the main thread.

    # Using join for a thread should only be used if the thread actually has an ending condition
    # If the thread continues to run, using .join essentially blocks the main program and the main program will not go past the join part
    # In this application, essentially, we remove the point of using a thread if the target of the thread is a non ending function.

    # If the function does end, using join  will make it so that the main program will not run past that point of adding the join until that particular thread done.

    # Not using a .join will just the the target in a different thread and continue running the main thread. Even if the main program ends, the thread or threads started must end before
    # the program as a whole will end.

    # This is where deamon comes in. If the deamon argument of the thread object is set to true, then the when the main program thread ends, the thread (whether it is a non ending function
    # or not will be stopped (beacause of the deamon parameter)
    output_file_name = 'output.json'
    max_time_for_task = 30
    counter = 0
    while counter <= max_time_for_task:
        print(f"Operation will run for a maximum of {max_time_for_task} seconds")
        print(f"Operation has been running for {counter} seconds")
        # Update output file
        with open(output_file_name, "w+") as file:
            if counter < time_to_complete:
                results = {"taskName": "Test Task",
                           "status": "InProgess"
                           }
            else:
                results = {"taskName": "Test Task",
                           "status": "Completed"
                           }
            file.write(json.dumps(results))

        sleep(1)

        counter = counter + 1
    return


def checkTaskCompletion(time_to_complete):
    """
    This function starts up a task that takes a specified time to complete.
    This functions spins up the task and then checks an output file to see (reads the file only) to see the status of the task.
    When the task is complete, the programs ends
    :param time_to_complete:
    :return:
    """
    print(f"Starting task with completion time {time_to_complete}")
    check_output = threading.Thread(target=randomTask, args=(time_to_complete,), daemon=True)
    check_output.start()
    output_file_name = 'output.json'
    print(f'//////////////// Checking output beginning')
    while True:
        try:
            print(f"\nChecking process completion. Program will end on process completion")
            sleep(1)
            with open(output_file_name, 'r') as file:
                results = file.read()
                json_result = json.loads(results)

            if json_result.get("status") == "Completed":
                print(f"\nPROCESS HAS COMPLETED. Program will stop now.\n")
                return
        except Exception as e:
            print(f"ERROR Occurred while checking output: {e}")


def main():
    print(f"Starting process")
    checkTaskCompletion(10)


if __name__ == "__main__":
    main()
