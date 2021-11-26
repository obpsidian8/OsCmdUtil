import os
import threading
import time


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
        print(f"Executing command: {cmd}")
        o = os.system(f"{cmd}")
        print(f"Command finished.")
        print(f"Command output code: {o}")

    def _remove_output_file(self, file_name):
        """
        Remove prior output files, so that new content can be written.
        ** In the default operation, redirecting the output to a file will always
        overwrite previous file.
        :return:
        """
        print(f'Removing output file {file_name}')
        try:
            os.remove(file_name)
            print(f"Output file {file_name} removed\n")
        except Exception as e:
            print(f"Error Details: {e}")

    def _open_state_file(self, file_name):
        time.sleep(1)
        try:
            print(f"Opening status file: {file_name}")
            with open(file_name, 'r+') as datafile:
                output = datafile.read()
                return output
        except Exception as e:
            print(f"Error accessing status file {self.output_file_name}: Details: {e}")
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
        start_time = time.time()
        print(f"Starting Operation")
        self._remove_output_file(self.output_file_name)
        self._remove_output_file(self.errror_file_name)

        # Set up output and error handler
        io_handler = CmdParams(cmd_to_run)

        formatted_cmd = f"({cmd_to_run}) > {self.output_file_name} 2> {self.errror_file_name}"

        t = threading.Thread(target=self._run_cmd, args=(formatted_cmd,), daemon=True)
        t.start()
        if not time_limit:
            time_limit = 5  # Does not matter what this is set to as long as it is greater than 0. The join will block the rest of the function until the command is executed anyhow.
            t.join()

        output = None
        errors = None
        timer_now = 0
        while timer_now <= time_limit and not output and not errors:
            print(f"Output check has been running for {timer_now} seconds")
            output = self._open_state_file(self.output_file_name)
            errors = self._open_state_file(self.errror_file_name)
            io_handler.output = output
            io_handler.errors = errors
            timer_now = timer_now + 1

        if not output and not errors and timer_now > time_limit:
            print(f"Operation timed out after {timer_now} seconds")
            return io_handler

        end = time.time()

        print(f"\nOperation completed in {round(end - start_time, 2)} seconds")
        print(f"\nThe final output from {self.output_file_name} is:\t{io_handler.output}")
        print(f"The errors are:\n\t{io_handler.errors}")

        return io_handler


def main():
    pShell = OSRunCmd()
    # pShell.run_cmd(cmd_to_run="ping yahoo.com", time_limit=60)
    pShell.run_cmd(cmd_to_run="virsh --list all", time_limit=60)
    # pShell.run_cmd(cmd_to_run="ping google.com")
    # pShell.run_cmd(cmd_to_run="AskQ.bat < ans.txt")
    return


if __name__ == "__main__":
    main()
