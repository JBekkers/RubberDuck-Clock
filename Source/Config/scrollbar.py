import tkinter as tk
from Source.Config import style


class FlatScrollbar(tk.Canvas):

    def __init__(
        self,
        parent,
        command,
        bg= style.SCROLLBAR_BACKGROUND,
        width=style.SCROLLBAR_WIDTH,
        thumb_color=style.SCROLLBAR_THUMB,
        hover_color=style.SCROLLBAR_THUMB_HOVER,
        thumb_width=style.SCROLLBAR_THUMB_WIDTH,
        min_thumb_height=style.SCROLLBAR_MIN_THUMB_HEIGHT
    ):

        super().__init__(
            parent,
            width=width,
            bg=bg,
            highlightthickness=0,
            bd=0,
            relief="flat"
        )

        self.command = command

        self.scrollbar_bg = bg

        self.thumb_color = thumb_color
        self.hover_color = hover_color

        self.thumb_width = thumb_width
        self.min_thumb_height = min_thumb_height

        self.first = 0.0
        self.last = 1.0

        self.thumb_top = 0
        self.thumb_bottom = 0

        self.dragging = False
        self.drag_start_y = 0
        self.drag_start_position = 0.0

        self.current_color = self.thumb_color

        self.bind(
            "<Configure>",
            self._redraw
        )

        self.bind(
            "<Enter>",
            self._mouse_enter
        )

        self.bind(
            "<Leave>",
            self._mouse_leave
        )

        self.bind(
            "<Button-1>",
            self._button_press
        )

        self.bind(
            "<B1-Motion>",
            self._drag
        )

        self.bind(
            "<ButtonRelease-1>",
            self._button_release
        )

    # --------------------------------------------------
    # SCROLLBAR POSITION
    # --------------------------------------------------

    def set(self, first, last):

        self.first = float(first)
        self.last = float(last)

        self._redraw()

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def _redraw(self, event=None):

        self.delete("all")

        height = self.winfo_height()

        if height <= 1:
            return

        # Nothing to scroll.
        if self.last - self.first >= 1.0:
            return

        thumb_height = max(
            self.min_thumb_height,
            height * (self.last - self.first)
        )

        thumb_height = min(
            thumb_height,
            height
        )

        available_height = height - thumb_height

        thumb_top = (
            self.first * available_height
        )

        thumb_top = max(
            0,
            min(
                thumb_top,
                available_height
            )
        )

        thumb_bottom = (
            thumb_top + thumb_height
        )

        self.thumb_top = thumb_top
        self.thumb_bottom = thumb_bottom

        center_x = self.winfo_width() / 2

        half_width = self.thumb_width / 2

        start_y = (
            thumb_top + half_width
        )

        end_y = (
            thumb_bottom - half_width
        )

        # Prevent invalid line geometry
        if end_y < start_y:
            start_y = (
                thumb_top + thumb_height / 2
            )

            end_y = start_y

        # Outlook-style pill.
        self.create_line(
            center_x,
            start_y,
            center_x,
            end_y,
            fill=self.current_color,
            width=self.thumb_width,
            capstyle=tk.ROUND,
            tags="thumb"
        )

    # --------------------------------------------------
    # MOUSE ENTER
    # --------------------------------------------------

    def _mouse_enter(self, event=None):

        self.current_color = self.hover_color

        self._redraw()

    # --------------------------------------------------
    # MOUSE LEAVE
    # --------------------------------------------------

    def _mouse_leave(self, event=None):

        if not self.dragging:

            self.current_color = self.thumb_color

            self._redraw()

    # --------------------------------------------------
    # CLICK
    # --------------------------------------------------

    def _button_press(self, event):

        # Clicked directly on thumb.
        if (
            self.thumb_top
            <= event.y
            <= self.thumb_bottom
        ):

            self.dragging = True

            self.drag_start_y = event.y

            self.drag_start_position = self.first

            self.current_color = self.hover_color

            self._redraw()

            return

        # Clicked above thumb.
        if event.y < self.thumb_top:

            self.command(
                "scroll",
                -1,
                "pages"
            )

            return

        # Clicked below thumb.
        if event.y > self.thumb_bottom:

            self.command(
                "scroll",
                1,
                "pages"
            )

    # --------------------------------------------------
    # DRAG
    # --------------------------------------------------

    def _drag(self, event):

        if not self.dragging:
            return

        height = self.winfo_height()

        thumb_height = (
            self.thumb_bottom
            - self.thumb_top
        )

        available_height = (
            height - thumb_height
        )

        if available_height <= 0:
            return

        mouse_delta = (
            event.y
            - self.drag_start_y
        )

        position_delta = (
            mouse_delta
            / available_height
        )

        new_position = (
            self.drag_start_position
            + position_delta
        )

        new_position = max(
            0.0,
            min(
                1.0,
                new_position
            )
        )

        self.command(
            "moveto",
            new_position
        )

    # --------------------------------------------------
    # RELEASE
    # --------------------------------------------------

    def _button_release(self, event=None):

        self.dragging = False

        self.current_color = self.hover_color

        self._redraw()