# lazy_loader.py
#
# Copyright 2025 Nicholas La Roux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import gi
import threading
from typing import Dict, List, Callable, Optional
from time import time_ns

gi.require_version('GLib', '2.0')
from gi.repository import GLib


class LazyEmojiLoader:
    """
    A lazy loader for emoji data that:
    1. Loads emoji data in background threads
    2. Calls callbacks when data is ready
    3. Ensures thread-safe access to loaded data
    """

    def __init__(self):
        self.emoji_data: Optional[Dict] = None
        self.emoji_categories: Optional[Dict] = None
        self.is_loading = False
        self.is_loaded = False
        self.load_callbacks: List[Callable] = []
        self._load_lock = threading.Lock()

    def load_async(self, callback: Optional[Callable] = None):
        """
        Asynchronously load emoji data in a background thread

        Args:
            callback: Function to call when loading is complete
        """
        if self.is_loaded:
            if callback:
                callback()
            return

        if callback:
            self.load_callbacks.append(callback)

        with self._load_lock:
            if self.is_loading:
                return
            self.is_loading = True

        # Start background loading
        thread = threading.Thread(target=self._load_emoji_data)
        thread.daemon = True
        thread.start()

    def _load_emoji_data(self):
        """Load emoji data in background thread"""
        try:
            start_time = time_ns()

            # Import the large emoji dataset
            from ..assets.emoji_list import emojis, emoji_categories

            load_time = (time_ns() - start_time) / 1_000_000  # Convert to milliseconds

            with self._load_lock:
                self.emoji_data = emojis
                self.emoji_categories = emoji_categories
                self.is_loaded = True
                self.is_loading = False

            # Execute callbacks on main thread
            GLib.idle_add(self._execute_callbacks)

        except Exception as e:
            print(f"Error loading emoji data: {e}")
            with self._load_lock:
                self.is_loading = False

    def _execute_callbacks(self):
        """Execute all registered callbacks on the main thread"""
        callbacks_to_execute = self.load_callbacks.copy()
        self.load_callbacks.clear()

        for callback in callbacks_to_execute:
            try:
                callback()
            except Exception as e:
                print(f"Error executing emoji load callback: {e}")

    def get_emoji_data(self) -> Optional[Dict]:
        """Thread-safe access to emoji data"""
        with self._load_lock:
            return self.emoji_data

    def get_emoji_categories(self) -> Optional[Dict]:
        """Thread-safe access to emoji categories"""
        with self._load_lock:
            return self.emoji_categories

    def is_currently_loading(self) -> bool:
        """Check if data is currently being loaded"""
        return self.is_loading

    def is_data_loaded(self) -> bool:
        """Check if data has been loaded"""
        return self.is_loaded


# Global lazy loader instance
emoji_loader = LazyEmojiLoader()
