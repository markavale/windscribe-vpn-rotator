import subprocess
from utils.logger import Logger

class Windscribe:
    def __init__(self, user, password):
        """Logs into Windscribe."""
        self.logger = Logger().get_logger()
        self._login(user, password)

    def _login(self, user, password):
        """Logs into Windscribe using provided credentials."""
        self.logger.info("Attempting to login to Windscribe...")
        commands = ["windscribe-cli", "login"]
        try:
            proc = subprocess.Popen(commands, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.communicate(input=f"{user}\n{password}\n")
            if proc.returncode != 0:
                self.logger.error("Login failed. Please check your credentials.")
            else:
                self.logger.info("Successfully logged in to Windscribe")
        except subprocess.SubprocessError as e:
            self.logger.error(f"An error occurred during login: {e}")

    def locations(self):
        """Prints the locations available to connect to in the shell."""
        self.logger.info("Fetching available locations...")
        self._run_command("windscribe-cli locations")

    def connect(self, server=None, rand=True):
        """Connects to given server, best available server if no server given, or random server."""
        self.logger.info(f"Connecting to server: {server if server else 'best available'}")
        command = f"windscribe-cli connect {server}" if server else "windscribe-cli connect"
        self._run_command(command)

    def disconnect(self):
        """Disconnects from the current server."""
        self.logger.info("Disconnecting from Windscribe...")
        self._run_command("windscribe-cli disconnect")

    def logout(self):
        """Logs out of Windscribe."""
        self.logger.info("Logging out from Windscribe...")
        self._run_command("windscribe-cli logout")

    def _run_command(self, command):
        """Runs a shell command and handles errors."""
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            self.logger.info(output)
        except subprocess.CalledProcessError as e:
            error = e.stderr.decode('utf-8')
            self.logger.error(f"Command '{command}' failed with error: {error}")