# progressive_renderer.py
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
from typing import List, Callable, Optional

gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')

from gi.repository import Gtk, GLib


class ProgressiveRenderer:
    """
    A general-purpose progressive renderer that can render any list of items
    in batches to avoid blocking the UI. This is useful for large datasets
    that would otherwise cause UI freezing.

    Can be used for emojis, large lists, search results, etc.
    """

    def __init__(self, container: Gtk.Widget, batch_size: int = 20, batch_delay: int = 5):
        """
        Initialize progressive renderer

        Args:
            container: The GTK container to add items to
            batch_size: Number of items to render per batch
            batch_delay: Milliseconds between batches
        """
        self.container = container
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.current_batch = 0
        self.item_queue: List = []
        self.is_rendering = False
        self.completion_callback: Optional[Callable] = None

    def render_progressive(self, items: List, item_factory: Callable,
                          completion_callback: Optional[Callable] = None):
        """
        Render items progressively in batches

        Args:
            items: List of data to render
            item_factory: Function that creates widgets from data items
            completion_callback: Callback when all items are rendered
        """
        if self.is_rendering:
            self.stop_rendering()

        self.item_queue = items.copy()
        self.current_batch = 0
        self.is_rendering = True
        self.completion_callback = completion_callback

        # Start rendering first batch immediately
        GLib.timeout_add(1, self._render_next_batch, item_factory)

    def _render_next_batch(self, item_factory: Callable) -> bool:
        """Render the next batch of items"""
        if not self.is_rendering or not self.item_queue:
            self._finish_rendering()
            return False

        start_idx = self.current_batch * self.batch_size
        end_idx = min(start_idx + self.batch_size, len(self.item_queue))

        batch = self.item_queue[start_idx:end_idx]

        # Render this batch
        for item_data in batch:
            try:
                widget = item_factory(item_data)
                if hasattr(self.container, 'append'):
                    self.container.append(widget)
                elif hasattr(self.container, 'add_child'):
                    self.container.add_child(widget)
                else:
                    # Fallback for other container types
                    self.container.add(widget)
            except Exception as e:
                print(f"Error creating widget in progressive renderer: {e}")

        self.current_batch += 1

        # Check if we're done
        if end_idx >= len(self.item_queue):
            self._finish_rendering()
            return False

        # Schedule next batch
        GLib.timeout_add(self.batch_delay, self._render_next_batch, item_factory)
        return False

    def _finish_rendering(self):
        """Clean up and call completion callback"""
        self.is_rendering = False
        if self.completion_callback:
            self.completion_callback()
            self.completion_callback = None

    def stop_rendering(self):
        """Stop current rendering operation"""
        self.is_rendering = False
        self.item_queue.clear()
        self.completion_callback = None

    def is_busy(self) -> bool:
        """Check if currently rendering"""
        return self.is_rendering


class ProgressiveEmojiRenderer(ProgressiveRenderer):
    """
    Specialized progressive renderer for emoji widgets.
    Provides emoji-specific defaults and convenience methods.
    """

    def __init__(self, container: Gtk.FlowBox):
        # Emoji-specific defaults: smaller batches, faster rendering
        super().__init__(container, batch_size=20, batch_delay=5)

    def render_emojis_progressive(self, emoji_list: List, emoji_factory: Callable,
                                 completion_callback: Optional[Callable] = None):
        """
        Convenience method for rendering emojis specifically

        Args:
            emoji_list: List of emoji data to render
            emoji_factory: Function that creates emoji button widgets
            completion_callback: Callback when all emojis are rendered
        """
        return self.render_progressive(emoji_list, emoji_factory, completion_callback)
