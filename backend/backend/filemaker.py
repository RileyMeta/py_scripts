from pathlib import Path
from getpass import getpass

class Config:
    VERBOSE: bool = False
    FAILURES: list = []
    SUCCESSES: list = []

class FileMaker:
    def __init__(self, name: str, extension: str):
        """
        Initialize the FileMaker class for a program

        Args:
            name          (str): String name of the program
            extension     (str): The new file's extension
            file_template (str): The actual contents to be written
        """
        self.name: str = name
        self.extension: str = extension
        self.file_template: str = ""

    def confirm_overwrite(self, filename: str) -> bool:
        """
        Confirm if a file should be overwritten

        Args:
            filename (str): name of the file to be confirmed

        Returns:
            bool: True for Yes, False for No
        """
        prompt: str = f"{filename} already exists.\n"
        prompt += "Would you like to overwrite it?\n"

        try:
            while True:
                print(prompt)
                response: str = input("[Y]es or [N]o: ").lower()

                if response in ["y", "yes"]:
                    return True
                elif response in ["n", "no"]:
                    return False
                else:
                    print(f"{repsonse} is not recognized.")
                    getpass("Press [enter] to continue")
                    continue
        except KeyboardInterrupt as e:
            print("\nOperation was cancelled.")
            sys.exit(-1)

    def clean_filename(self, filename: str) -> str:
        """
        Clean a filename (remove extension)

        Args:
            filename (str): the name of the file to be cleaned

        Returns:
            str: The cleaned file name
        """
        full_name: str = Path(filename)
        full_fb: str = Path(f"{filename}{self.extension}")

        if full_name.is_dir():
            print(f"{self.name}: {full_name} is a directory, please provide a name for the file.")
            return None

        if full_name.exists() or full_fb.exists():
            if not self.confirm_overwrite(full_name):
                Config.FAILURES.append(full_name)
                return None

        if filename.endswith(self.extension):
            filename = filename.replace(self.extension, "")

        return str(filename)

    def create_file(self, filename: str):
        """
        Create the actual file

        Args:
            filename (str): name of the file to be created

        Returns:
            None: If failed to create file name
        """
        new_file: str = self.clean_filename(filename)
        if new_file == None:
            return None

        new_file = new_file + self.extension

        ft: str = self.file_template

        try:
            with open(new_file, 'w') as f:
                f.write(ft)
                Config.SUCCESSES.append(new_file)
        except Exception as e:
            Config.FAILURES.append(new_file)
            print(f"[{self.name}] Error: {e}")

    def finish(self) -> None:
        """
        Print successes and failures after execution

        Returns:
            None: There is nothign to return
        """
        successes: list = Config.SUCCESSES
        success_len: int = len(successes)
        print(f"{self.name}: {success_len} file(s) created.")

        if Config.VERBOSE:
            for a, file in enumerate(successes, 1):
                print(f"  {a}. {file}")

        fails: list = Config.FAILURES
        fail_len: int = len(Config.FAILURES)
        if fail_len > 0:
            print(f"There were {fail_len} files that could not be created:")
            for a, file in enumerate(fails, 1):
                print(f"  {a}. {file}")
