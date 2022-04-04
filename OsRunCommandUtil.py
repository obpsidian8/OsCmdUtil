import os
import threading
import time
from Utilities.LoggerConfig import setup_python_logging

logger = setup_python_logging(__file__)


class CmdParams:
    def __init__(self, cmd):
        self.cmd = cmd
        self.output = None
        self.errors = None


class OSRunCmd:

    def __init__(self):
        self.output_file_name = "output_from_running_cmd.txt"
        self.errror_file_name = "errors_from_running_cmd.txt"

    def _run_cmd(self, cmd):
        """
        Function that uses the os module to run the command
        :param cmd:
        :return:
        """
        logger.info(f"Executing command: {cmd}")
        o_code = os.system(f"{cmd}")
        logger.info(f"Command finished.")
        logger.info(f"Command output code: {o_code}")

    def _remove_output_file(self, file_name):
        """
        Remove prior output files, so that new content can be written.
        ** In the default operation, redirecting the output to a file will always
        overwrite previous file.
        :return:
        """
        logger.info(f'Removing output file {file_name}')
        try:
            os.remove(file_name)
            logger.info(f"Output file {file_name} removed\n")
        except Exception as e:
            logger.info(f"Error Details: {e}")

    def _open_state_file(self, file_name):
        time.sleep(1)
        try:
            logger.info(f"Opening status file: {file_name}")
            with open(file_name, 'r+') as datafile:
                output = datafile.read()
                return output
        except Exception as e:
            logger.info(f"Error accessing status file {self.output_file_name}: Details: {e}")
            return None

    def run_cmd(self, cmd_to_run, time_limit=None):
        """
        Runs a command using the os module.
        The output is captured using an output file.
        The output file is returned from the function.
        :param time_limit: Time limit for the command to run
        :param cmd_to_run: Command to run
        :return:
        """

        logger.info(f"Starting Operation")
        self._remove_output_file(self.output_file_name)
        self._remove_output_file(self.errror_file_name)

        # Set up output and error handler
        io_handler = CmdParams(cmd_to_run)

        formatted_cmd = f"({cmd_to_run}) > {self.output_file_name} 2> {self.errror_file_name}"

        t = threading.Thread(target=self._run_cmd, args=(formatted_cmd,), daemon=True)
        # Thread is set to daemon to enforce the time limit specified. Without it, the main program will not exit if the output is still
        # not found after the time limit is up. Main program will still be waiting for the command , which is being run in the thread to complete.
        t.start()
        if not time_limit:
            time_limit = 5  # Does not matter what this is set to as long as it is greater than 0.
            # The join will block the rest of the function in the thread until the command is executed anyhow.
            # ** We used t.join because if there is no time limit specified, it means we want the command to run
            # as long as it needs to to complete. So, we use join to block the rest of the program and let the command complete
            t.join()

        # ** If there is not time limit specified, the command passed to the thread will have already ended before this point is reached or it might still
        # be running. If it is still running, the code below will then check if the timer is exceeded before the code completes.
        output = None
        errors = None
        timer_now = 0
        # Now, we just continually check the output and error files if the output or errors have been written to them.
        # Note: Os module will only write output to the files if the process is completed.
        while timer_now <= time_limit and not output and not errors:
            logger.info(f"Output check has been running for {timer_now} seconds")
            output = self._open_state_file(self.output_file_name)
            errors = self._open_state_file(self.errror_file_name)
            io_handler.output = output
            io_handler.errors = errors
            timer_now = timer_now + 1

        if not output and not errors and timer_now > time_limit:
            logger.info(f"Operation timed out after {timer_now} seconds")
            return io_handler

        return io_handler


def main():
    pShell = OSRunCmd()
    start_time = time.time()
    # res = pShell.run_cmd(cmd_to_run="ping yahoo.com", time_limit=60)
    # res = pShell.run_cmd(cmd_to_run="virsh --list all", time_limit=60)
    # res = pShell.run_cmd(cmd_to_run="ls -lst", time_limit=60)
    # res = pShell.run_cmd(cmd_to_run="dir", time_limit=60)
    # res = pShell.run_cmd(cmd_to_run="cat password.txt | sudo /etc/shadow", time_limit=20)
    res = pShell.run_cmd(cmd_to_run="ping google.com && dir && ping yahoo.com", time_limit=12)
    # res = pShell.run_cmd(cmd_to_run="AskQ.bat < ans.txt")
    # res = pShell.run_cmd(cmd_to_run="python TestFile_ThreadingDemo.py")

    end = time.time()
    logger.info("")
    logger.info(f"Operation completed in {round(end - start_time, 2)} seconds")
    logger.info("")
    logger.info(">>>>>>>>>>>>>>>>>>>>>> BEGIN OUTPUT FROM CMD >>>>>>>>>>>>>>>>>>>>>> ")
    logger.info(f"{res.output}")
    logger.info(">>>>>>>>>>>>>>>>>>>>>> END OUTPUT FROM CMD>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    logger.info(f"The errors are:>>>>>>\n{res.errors}")

    return


if __name__ == "__main__":
    main()
