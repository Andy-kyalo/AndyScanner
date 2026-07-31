"""
sound_notifier.py

Sound Notification Channel.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import os
import subprocess


class SoundNotifier:
    """
    Plays an alert sound when a notification is sent.
    """

    def __init__(self, sound_file=None):

        self.sound_file = sound_file

    # ==================================================
    # Configuration
    # ==================================================

    def set_sound(self, sound_file):

        self.sound_file = sound_file

    @property
    def configured(self):

        return (
            self.sound_file is not None
            and os.path.exists(self.sound_file)
        )

    # ==================================================
    # Send
    # ==================================================

    def send(
        self,
        notification,
    ):

        if not self.configured:

            return False

        try:

            subprocess.run(
                [
                    "termux-media-player",
                    "play",
                    self.sound_file,
                ],
                check=False,
            )

        except Exception:

            return False

        notification.mark_sent()

        return True

    # ==================================================
    # Stop
    # ==================================================

    def stop(self):

        try:

            subprocess.run(
                [
                    "termux-media-player",
                    "stop",
                ],
                check=False,
            )

        except Exception:

            return False

        return True

    # ==================================================
    # Information
    # ==================================================

    @property
    def sound(self):

        return self.sound_file