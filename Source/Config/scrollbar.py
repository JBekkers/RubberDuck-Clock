import tkinter as tk
from Source.Config import style


class FlatScrollbar(tk.Canvas):

    def __init__(
        self,
        parent,
        command,
        bg=style.SCROLLBAR_BACKGROUND,
        width=style.SCROLLBAR_WIDTH,
        thumb_color=style.SCROLLBAR_THUMB,
        hover_color=style.SCROLLBAR_THUMB_HOVER,
        thumb_width=style.SCROLLBAR_THUMB_WIDTH,
        thumb_height=style.SCROLLBAR_THUMB_HEIGHT,
        arrow_height=style.SCROLLBAR_ARROW_HEIGHT,
        arrow_color=style.SCROLLBAR_ARROW_COLOR,
        arrow_hover_color=style.SCROLLBAR_ARROW_HOVER,
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
        self.thumb_height = thumb_height

        self.arrow_height = arrow_height
        self.arrow_color = arrow_color
        self.arrow_hover_color = arrow_hover_color
        self.arrow_current_color = arrow_color
        self.pressed_arrow = None

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

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return

        center_x = width / 2
        arrow_size = style.SCROLLBAR_ARROW_SIZE

        # Use integer coordinates for consistent pixel alignment.
        center_x = round(center_x)
        arrow_size = round(arrow_size)

        # Up arrow
        up_center_y = round(self.arrow_height / 2)

        self.create_polygon(
            center_x,
            up_center_y - arrow_size // 2,
            center_x - arrow_size,
            up_center_y + arrow_size // 2,
            center_x + arrow_size,
            up_center_y + arrow_size // 2,
            fill=self.arrow_current_color,
            outline="",
            tags="up_arrow",
        )

        # Down arrow: mirror the up arrow vertically.
        down_center_y = height - up_center_y

        self.create_polygon(
            center_x,
            down_center_y + arrow_size // 2,
            center_x - arrow_size,
            down_center_y - arrow_size // 2,
            center_x + arrow_size,
            down_center_y - arrow_size // 2,
            fill=self.arrow_current_color,
            outline="",
            tags="down_arrow",
        )

        # No thumb is needed when the content fits.
        if self.last - self.first >= 1.0:
            return

        track_top = self.arrow_height
        track_bottom = height - self.arrow_height
        track_height = track_bottom - track_top

        if track_height <= 1:
            return

        thumb_height = min(
            self.thumb_height,
            track_height
        )

        available_height = track_height - thumb_height

        scroll_range = 1.0 - (self.last - self.first)

        if scroll_range <= 0:
            scroll_position = 0.0
        else:
            scroll_position = self.first / scroll_range

        scroll_position = max(
            0.0,
            min(1.0, scroll_position)
        )

        thumb_top = (
            track_top
            + scroll_position * available_height
        )

        thumb_bottom = thumb_top + thumb_height

        self.thumb_top = thumb_top
        self.thumb_bottom = thumb_bottom

        half_width = self.thumb_width / 2

        start_y = thumb_top + half_width
        end_y = thumb_bottom - half_width

        if end_y < start_y:
            start_y = thumb_top + thumb_height / 2
            end_y = start_y

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
        self.arrow_current_color = self.arrow_hover_color
        self._redraw()

    # --------------------------------------------------
    # MOUSE LEAVE
    # --------------------------------------------------

    def _mouse_leave(self, event=None):
        if not self.dragging:
            self.current_color = self.thumb_color
            self.arrow_current_color = self.arrow_color
            self._redraw()

    # --------------------------------------------------
    # CLICK
    # --------------------------------------------------

    
    def _button_press(self, event):
        height = self.winfo_height()

        if event.y < self.arrow_height:
            self.command("scroll", -1, "units")
            return

        if event.y >= height - self.arrow_height:
            self.command("scroll", 1, "units")
            return

        if self.last - self.first >= 1.0:
            return

        thumb_height = self.thumb_bottom - self.thumb_top
        track_top = self.arrow_height
        track_bottom = height - self.arrow_height
        track_height = track_bottom - track_top
        available_height = track_height - thumb_height

        if available_height <= 0:
            return

        # Clicked on the thumb: start dragging.
        if self.thumb_top <= event.y <= self.thumb_bottom:
            self.dragging = True
            self.drag_start_y = event.y
            self.drag_start_position = self.first
            self.current_color = self.hover_color
            self._redraw()
            return

        # Clicked on the track: jump to the clicked position.
        scroll_range = 1.0 - (self.last - self.first)

        if scroll_range <= 0:
            return

        target_position = (
            event.y - track_top - thumb_height / 2
        ) / available_height

        target_position = max(
            0.0,
            min(1.0, target_position)
        )

        self.command(
            "moveto",
            target_position * scroll_range
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

        track_height = (
            self.winfo_height()
            - 2 * self.arrow_height
        )

        available_height = (
            track_height
            - (self.thumb_bottom - self.thumb_top)
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

        scroll_range = (
            1.0
            - (self.last - self.first)
        )

        new_position = (
            self.drag_start_position
            + (
                position_delta
                * scroll_range
            )
        )

        new_position = max(
            0.0,
            min(
                scroll_range,
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