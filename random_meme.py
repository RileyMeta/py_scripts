#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
random_meme
==============

Play a random meme from a directory

Pull all .mp4 files from a directory and add them to a list to
be randomly played when the programm is called.

Author: Riley Ava
Created: 21/01/2026
Last Modified: 21/01/2026
Version: 1.0.0
License: MPL 2.0
Repository: https://github.com/RileyMeta/random_meme

Requirements:
    - Python 3.10 (or newer)

Usage:
    random_meme [option] FILE...

Copyright (c) 2026 Riley Ava
"""
import os
import sys
import getopt
import subprocess
from pathlib import Path
from random import randrange

class Config:
    VERBOSE: bool = False
    PLAYER: str = "vlc"

class RandomMeme:
    def __init__(self, directory: str):
        self.directory: str = directory
        self.meme_list: list = []
        self.populate_list()
        self.video_played: str = ""

    def populate_list(self):
        extensions: tuple = (".mp4", ".mov")
        tmpdir = self.directory
        directory = Path(tmpdir)

        for file in directory.iterdir():
            if file.is_file():
                if str(file).endswith(extensions):
                    self.meme_list.append(file)

    def play_random_video(self):
        memes_len: int = len(self.meme_list)
        video = randrange(0, memes_len)
        self.video_played = self.meme_list[video]
        self.play_video(self.video_played)
        vid_path = Path(self.video_played)
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

      --help     display this help information and exit
  -v, --version  display version information and exit

Report bugs to: <https://github.com/RileyMeta/random_meme/pulls>""")

def version_menu():
    print("""random_meme (random meme player) 1.0.0
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
        short_opts: str = "Vvp:"
        long_opts: list = ["version", "help", "verbose", "player"]

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
        elif opt in ("-v", "--verbose"):
            Config.VERBOSE = True
        elif opt in ("-p", "--player"):
            Config.PLAYER = arg

    if args:
        meme_dir = args[0]

    RM = RandomMeme(meme_dir)
    RM.play_random_video()
