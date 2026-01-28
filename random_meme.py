# -*- coding: utf-8 -*-
"""
random_meme
==============

Play a random meme from a directory

Pull all .mp4 files from a directory and add them to a list to
be randomly played when the programm is called.

Author: Riley Ava
Created: 21/01/2026
Last Modified: 26/01/2026
Version: 1.1.0
License: MPL 2.0
Repository: https://github.com/RileyMeta/random_meme

Requirements:
    - Python 3.10 (or newer)

Usage:
    random_meme [option] <directory>

Copyright (c) 2026 Riley Ava
"""
import os
import sys
import getopt
import subprocess
from pathlib import Path
from random import randrange

class Config:
    REPLAY: bool = False
    PLAYER: str = ""
    PLAYERS: list = ["vlc", "mpv", "smplayer", "mplayer"]

class RandomMeme:
    def __init__(self, directory: str):
        self.directory: str = directory
        self.meme_list: list = []
        self.video_played: str = ""
        self.tmp_file: str = "/tmp/meme"
        self.last_video: str = ""
        self.check_players()
        self.get_last()
        self.populate_list()

    def program_exists(self, program: str, search_prog: str) -> bool:
        command: list = []
        if search_prog == "command":
            command = ["bash", "-c", "command", "-v"]
        else:
            command = ["which"]

        command.append(program)

        try:
            subprocess.run(command, check=True,
                           stderr=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL)
            return True

        except subprocess.CalledProcessError:
            return False

    def check_players(self):
        for player in Config.PLAYERS:
            if self.program_exists(player, "command") or self.program_exists(player, "which"):
                Config.PLAYER = player
                break

        if not Config.PLAYER or Config.PLAYER == "":
            print(f"No suitable video player was found...")
            last: int = (len(Config.PLAYERS) - 1)

            for a, player in enumerate(Config.PLAYERS):
                print(f"{player}{", " if a != last else "\n"}", end="")

            sys.exit(-1)

    def folder_exists(self, directory: str) -> bool:
        folder_dir: Path = Path(directory).expanduser().resolve()

        if folder_dir.exists():
            return True
        return False

    def populate_list(self):
        extensions: tuple = (".mp4", ".mov")
        tmpdir = self.directory
        directory = Path(tmpdir)

        if not self.folder_exists(self.directory):
            print(f"{self.directory} folder does not exist.")
            sys.exit(-1)

        for file in directory.iterdir():
            if file.is_file():
                if str(file).endswith(extensions):
                    self.meme_list.append(file)

    def cache_video(self):
        path: str = str(self.tmp_file)

        if not self.video_played:
            return None

        try:
            with open(path, 'w') as f:
                f.write(str(self.video_played))

        except Exception as err:
            print(f"Error [cache_video]: {err}")

    def get_last(self):
        path: str = str(self.tmp_file)

        try:
            with open(path, 'r') as f:
                self.last_video = f.readline()

        except FileNotFoundError:
            self.last_video = ""

        except Exception as err:
            print(f"Error [get_last]: {err}")

    def play_random_video(self):
        memes_len: int = len(self.meme_list)
        video = randrange(0, memes_len)

        if not Config.REPLAY:
            self.video_played = self.meme_list[video]
        else:
            self.video_played = self.last_video
        self.play_video(self.video_played)

        vid_path = Path(self.video_played).expanduser().resolve()
        self.cache_video()

        print(f"Video Played: {vid_path}")

    def play_video(self, video: str):
        video_player: str = Config.PLAYER
        subprocess.Popen([video_player, video],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

def usage():
    print("Usage: random_meme [option] <directory>")

def help_menu():
    usage()
    print("""Play a random meme from a specific folder.

  -p, --player   specify a video player (default: VLC)
  -r, --replay   replay the most recent video

      --help     display this help information and exit
  -v, --version  display version information and exit

Report bugs to: <https://github.com/RileyMeta/random_meme/pulls>""")

def version_menu():
    print("""random_meme (random meme player) 1.1.0
Copyright (C) 2026 Riley Ava.
License MPL2.0: Mozilla Public License 2.0 <https://www.mozilla.org/en-US/MPL/2.0/>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Riley Ava.""")

if __name__ == "__main__":
    # Default meme folder path
    user: str = os.getlogin()
    meme_dir: str = f"/home/{user}/Videos/memes"

    try:
        short_opts: str = "Vrp:"
        long_opts: list = ["version", "help", "replay", "player="]

        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)

    except getopt.GetoptError as err:
        print(f"{err}")
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("--help"):
            help_menu()
            sys.exit(0)
        elif opt in ("-V", "--version"):
            version_menu()
            sys.exit(0)
        elif opt in ("-p", "--player"):
            Config.PLAYER = arg
        elif opt in ("-r", "--replay"):
            Config.REPLAY = True

    if args:
        meme_dir = args[0]

    RM = RandomMeme(meme_dir)
    RM.play_random_video()