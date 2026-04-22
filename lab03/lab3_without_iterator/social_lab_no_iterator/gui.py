from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Iterable

from .models import INTEREST_CATEGORIES, User, UserPoint
from .point_space import Recommendation, UserPointSpaceNoIterator


class SocialLabAppNoIterator(tk.Tk):
    def __init__(self, space: UserPointSpaceNoIterator) -> None:
        super().__init__()
        self.space = space
        self.current_user_id = min(self.space.users.keys()) if self.space.users else None

        self.demo_recommendations: list[Recommendation] = []
        self.demo_index = 0

        self.title("Recommendation Lab (No Iterator Pattern)")
        self.geometry("1320x760")
        self.minsize(1120, 680)

        self._bg_main = "#10141b"
        self._bg_panel = "#181f2b"
        self._bg_card = "#202a39"
        self._fg_main = "#e5ecf6"
        self._fg_muted = "#9eb0c8"
        self._accent = "#5ad1e6"
        self._accent_secondary = "#f6bd60"
        self._grid = "#2d3a4f"

        self.configure(bg=self._bg_main)
        self._configure_ttk_theme()

        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.friend_ids_var = tk.StringVar()
        self.base_user_id_var = tk.StringVar()
        self.demo_status_var = tk.StringVar(value="Recommendation list is not initialized yet.")

        self.interest_vars = {
            category: tk.BooleanVar(value=False) for category in INTEREST_CATEGORIES
        }

        self._build_layout()
        self._refresh_user_selection()
        self._refresh_all_views()

    def _configure_ttk_theme(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self._bg_card,
            fieldbackground=self._bg_card,
            foreground=self._fg_main,
            bordercolor=self._bg_card,
            rowheight=27,
        )
        style.map("Treeview", background=[("selected", "#2b6f99")])
        style.configure(
            "Treeview.Heading",
            background="#263345",
            foreground=self._fg_main,
            relief="flat",
            borderwidth=0,
            padding=(6, 6),
        )
        style.configure(
            "TButton",
            background="#2a3b53",
            foreground=self._fg_main,
            borderwidth=0,
            padding=(10, 8),
        )
        style.map("TButton", background=[("active", "#355278")])
        style.configure(
            "TCombobox",
            fieldbackground=self._bg_card,
            background=self._bg_card,
            foreground=self._fg_main,
            arrowcolor=self._fg_main,
        )

    def _build_layout(self) -> None:
        root_frame = tk.Frame(self, bg=self._bg_main)
        root_frame.pack(fill="both", expand=True, padx=14, pady=14)

        left_panel = tk.Frame(root_frame, bg=self._bg_panel, width=455)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(root_frame, bg=self._bg_panel)
        right_panel.pack(side="left", fill="both", expand=True, padx=(14, 0))

        title_label = tk.Label(
            left_panel,
            text="User Registration + Recommendations",
            bg=self._bg_panel,
            fg=self._fg_main,
            font=("Segoe UI", 16, "bold"),
        )
        title_label.pack(anchor="w", padx=14, pady=(14, 10))

        form_card = tk.Frame(left_panel, bg=self._bg_card, highlightthickness=1, highlightbackground="#2c3a4f")
        form_card.pack(fill="x", padx=14)

        self._create_labeled_entry(form_card, "First name", self.first_name_var)
        self._create_labeled_entry(form_card, "Last name", self.last_name_var)
        self._create_labeled_entry(
            form_card,
            "Friend IDs (comma-separated)",
            self.friend_ids_var,
            placeholder="Example: 1,3,7",
        )

        interests_title = tk.Label(
            form_card,
            text="Interests",
            bg=self._bg_card,
            fg=self._fg_main,
            font=("Segoe UI", 10, "bold"),
        )
        interests_title.pack(anchor="w", padx=12, pady=(10, 5))

        interests_grid = tk.Frame(form_card, bg=self._bg_card)
        interests_grid.pack(fill="x", padx=10, pady=(0, 8))

        for index, category in enumerate(INTEREST_CATEGORIES):
            checkbox = tk.Checkbutton(
                interests_grid,
                text=category,
                variable=self.interest_vars[category],
                bg=self._bg_card,
                fg=self._fg_main,
                activebackground=self._bg_card,
                activeforeground=self._fg_main,
                selectcolor="#2a3a52",
                highlightthickness=0,
                font=("Segoe UI", 10),
            )
            row = index // 2
            column = index % 2
            checkbox.grid(row=row, column=column, sticky="w", padx=6, pady=2)

        action_row = tk.Frame(form_card, bg=self._bg_card)
        action_row.pack(fill="x", padx=12, pady=(8, 12))

        add_button = ttk.Button(action_row, text="Add user and refresh", command=self._handle_add_user)
        add_button.pack(side="left")

        reset_button = ttk.Button(action_row, text="Clear form", command=self._clear_form)
        reset_button.pack(side="left", padx=(8, 0))

        selection_card = tk.Frame(left_panel, bg=self._bg_card, highlightthickness=1, highlightbackground="#2c3a4f")
        selection_card.pack(fill="x", padx=14, pady=(12, 0))

        select_label = tk.Label(
            selection_card,
            text="Base user for recommendations",
            bg=self._bg_card,
            fg=self._fg_main,
            font=("Segoe UI", 10, "bold"),
        )
        select_label.pack(anchor="w", padx=12, pady=(12, 6))

        selection_row = tk.Frame(selection_card, bg=self._bg_card)
        selection_row.pack(fill="x", padx=12, pady=(0, 8))

        self.base_user_combo = ttk.Combobox(
            selection_row,
            textvariable=self.base_user_id_var,
            state="readonly",
            width=15,
        )
        self.base_user_combo.pack(side="left")

        show_button = ttk.Button(
            selection_row,
            text="Show",
            command=self._handle_select_base_user,
        )
        show_button.pack(side="left", padx=(8, 0))

        self.user_ids_hint = tk.Label(
            selection_card,
            text="",
            bg=self._bg_card,
            fg=self._fg_muted,
            font=("Consolas", 9),
            wraplength=410,
            justify="left",
        )
        self.user_ids_hint.pack(anchor="w", padx=12, pady=(0, 12))

        table_card = tk.Frame(left_panel, bg=self._bg_card, highlightthickness=1, highlightbackground="#2c3a4f")
        table_card.pack(fill="both", expand=True, padx=14, pady=(12, 14))

        table_title = tk.Label(
            table_card,
            text="Top 10 nearest users",
            bg=self._bg_card,
            fg=self._fg_main,
            font=("Segoe UI", 11, "bold"),
        )
        table_title.pack(anchor="w", padx=12, pady=(12, 8))

        columns = ("id", "name", "surname", "distance", "probability")
        self.table = ttk.Treeview(table_card, columns=columns, show="headings", height=10)
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Name")
        self.table.heading("surname", text="Surname")
        self.table.heading("distance", text="Distance")
        self.table.heading("probability", text="Probability")

        self.table.column("id", width=52, anchor="center")
        self.table.column("name", width=92, anchor="w")
        self.table.column("surname", width=92, anchor="w")
        self.table.column("distance", width=85, anchor="center")
        self.table.column("probability", width=85, anchor="center")

        table_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=table_scroll.set)

        self.table.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 8))
        table_scroll.pack(side="left", fill="y", pady=(0, 8), padx=(0, 12))

        demo_card = tk.Frame(table_card, bg="#1b2738")
        demo_card.pack(fill="x", padx=12, pady=(0, 12))

        demo_label = tk.Label(
            demo_card,
            text="Manual traversal demo (no Iterator pattern)",
            bg="#1b2738",
            fg=self._fg_main,
            font=("Segoe UI", 10, "bold"),
        )
        demo_label.pack(anchor="w", padx=10, pady=(8, 4))

        demo_status = tk.Label(
            demo_card,
            textvariable=self.demo_status_var,
            bg="#1b2738",
            fg=self._fg_muted,
            justify="left",
            wraplength=390,
            font=("Consolas", 9),
        )
        demo_status.pack(anchor="w", padx=10, pady=(0, 6))

        demo_actions = tk.Frame(demo_card, bg="#1b2738")
        demo_actions.pack(anchor="w", padx=10, pady=(0, 8))

        next_button = ttk.Button(demo_actions, text="Next candidate", command=self._manual_next)
        next_button.pack(side="left")

        reset_button = ttk.Button(
            demo_actions,
            text="Reset position",
            command=self._manual_reset,
        )
        reset_button.pack(side="left", padx=(8, 0))

        right_title = tk.Label(
            right_panel,
            text="Users on Coordinate Plane",
            bg=self._bg_panel,
            fg=self._fg_main,
            font=("Segoe UI", 16, "bold"),
        )
        right_title.pack(anchor="w", padx=14, pady=(14, 8))

        self.canvas = tk.Canvas(
            right_panel,
            bg=self._bg_main,
            highlightthickness=1,
            highlightbackground="#2c3a4f",
        )
        self.canvas.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.canvas.bind("<Configure>", lambda _event: self._draw_points())

    def _create_labeled_entry(
        self,
        parent: tk.Frame,
        label_text: str,
        variable: tk.StringVar,
        placeholder: str | None = None,
    ) -> None:
        label = tk.Label(
            parent,
            text=label_text,
            bg=self._bg_card,
            fg=self._fg_main,
            font=("Segoe UI", 10, "bold"),
        )
        label.pack(anchor="w", padx=12, pady=(10, 4))

        entry = tk.Entry(
            parent,
            textvariable=variable,
            bg="#152132",
            fg=self._fg_main,
            insertbackground=self._fg_main,
            relief="flat",
            font=("Consolas", 10),
        )
        entry.pack(fill="x", padx=12, pady=(0, 2), ipady=6)

        if placeholder:
            hint = tk.Label(
                parent,
                text=placeholder,
                bg=self._bg_card,
                fg=self._fg_muted,
                font=("Consolas", 9),
            )
            hint.pack(anchor="w", padx=12, pady=(0, 4))

    def _handle_add_user(self) -> None:
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()

        if not first_name or not last_name:
            messagebox.showerror("Validation error", "First name and last name are required.")
            return

        try:
            friend_ids = self._parse_friend_ids(self.friend_ids_var.get())
        except ValueError:
            messagebox.showerror(
                "Validation error",
                "Friend IDs must be positive integers separated by commas.",
            )
            return

        interests = {name for name, flag in self.interest_vars.items() if flag.get()}

        user = User(
            user_id=self.space.next_user_id(),
            first_name=first_name,
            last_name=last_name,
            friend_ids=friend_ids,
            interests=interests,
        )

        self.space.add_user(user)
        self.current_user_id = user.user_id
        self.base_user_id_var.set(str(user.user_id))

        self._refresh_user_selection()
        self._refresh_all_views()

    def _parse_friend_ids(self, text: str) -> list[int]:
        if not text.strip():
            return []

        values: list[int] = []
        for chunk in text.split(","):
            item = chunk.strip()
            if not item:
                continue

            parsed = int(item)
            if parsed <= 0:
                raise ValueError("Friend id must be positive.")
            values.append(parsed)

        return sorted(set(values))

    def _handle_select_base_user(self) -> None:
        if not self.base_user_id_var.get().strip():
            return

        selected_id = int(self.base_user_id_var.get())
        if selected_id not in self.space.users:
            messagebox.showerror("Selection error", f"User id {selected_id} was not found.")
            return

        self.current_user_id = selected_id
        self._refresh_all_views()

    def _refresh_user_selection(self) -> None:
        user_ids = sorted(self.space.users.keys())
        id_values = [str(user_id) for user_id in user_ids]
        self.base_user_combo.configure(values=id_values)

        if self.current_user_id is None and user_ids:
            self.current_user_id = user_ids[0]

        if self.current_user_id is not None:
            self.base_user_id_var.set(str(self.current_user_id))

        rendered = ", ".join(id_values) if id_values else "none"
        self.user_ids_hint.configure(text=f"Available user IDs: {rendered}")

    def _refresh_all_views(self) -> None:
        self._populate_table()
        self._prepare_manual_demo()
        self._draw_points()

    def _populate_table(self) -> None:
        for row_id in self.table.get_children():
            self.table.delete(row_id)

        if self.current_user_id is None:
            return

        recommendations = self.space.get_recommendations(self.current_user_id, limit=10)
        for recommendation in recommendations:
            self.table.insert(
                "",
                "end",
                values=(
                    recommendation.user.user_id,
                    recommendation.user.first_name,
                    recommendation.user.last_name,
                    f"{recommendation.distance:.3f}",
                    f"{recommendation.probability:.3f}",
                ),
            )

    def _prepare_manual_demo(self) -> None:
        if self.current_user_id is None:
            self.demo_recommendations = []
            self.demo_index = 0
            self.demo_status_var.set("No base user selected.")
            return

        self.demo_recommendations = self.space.get_recommendations(self.current_user_id, limit=10)
        self.demo_index = 0

        total = len(self.demo_recommendations)
        if total == 0:
            self.demo_status_var.set("Recommendation list is empty.")
        else:
            self.demo_status_var.set(f"List ready: position {self.demo_index}/{total}.")

    def _manual_next(self) -> None:
        total = len(self.demo_recommendations)
        if total == 0:
            self.demo_status_var.set("Recommendation list is empty.")
            return

        if self.demo_index >= total:
            self.demo_status_var.set(f"List exhausted at {self.demo_index}/{total}.")
            return

        recommendation = self.demo_recommendations[self.demo_index]
        self.demo_index += 1

        self.demo_status_var.set(
            f"Next -> user_id={recommendation.user.user_id}, "
            f"distance={recommendation.distance:.3f}, "
            f"position={self.demo_index}/{total}"
        )

        for row_id in self.table.get_children():
            values = self.table.item(row_id, "values")
            if not values:
                continue
            if int(values[0]) == recommendation.user.user_id:
                self.table.selection_set(row_id)
                self.table.focus(row_id)
                self.table.see(row_id)
                break

    def _manual_reset(self) -> None:
        total = len(self.demo_recommendations)
        self.demo_index = 0
        self.demo_status_var.set(f"Position reset: {self.demo_index}/{total}.")

    def _draw_points(self) -> None:
        self.canvas.delete("all")

        width = max(self.canvas.winfo_width(), 300)
        height = max(self.canvas.winfo_height(), 300)

        self._draw_background(width, height)

        points = self.space.points
        if not points:
            return

        world_limit = self._compute_world_limit(points.values())

        zero_x, zero_y = self._to_screen(0.0, 0.0, world_limit, width, height)
        self.canvas.create_line(0, zero_y, width, zero_y, fill="#4a607f", width=1)
        self.canvas.create_line(zero_x, 0, zero_x, height, fill="#4a607f", width=1)

        for point in points.values():
            self._draw_single_point(point, world_limit, width, height)

        self.canvas.create_text(
            16,
            16,
            anchor="nw",
            text="cyan: selected user | orange: other users",
            fill=self._fg_muted,
            font=("Consolas", 10),
        )

    def _draw_background(self, width: int, height: int) -> None:
        stripes = 16
        for i in range(stripes):
            ratio = i / max(stripes - 1, 1)
            shade = int(16 + ratio * 22)
            color = f"#{shade:02x}{(shade + 6):02x}{(shade + 16):02x}"
            y0 = int((i / stripes) * height)
            y1 = int(((i + 1) / stripes) * height)
            self.canvas.create_rectangle(0, y0, width, y1, fill=color, outline=color)

        for step in range(1, 10):
            x = int((step / 10.0) * width)
            y = int((step / 10.0) * height)
            self.canvas.create_line(x, 0, x, height, fill=self._grid)
            self.canvas.create_line(0, y, width, y, fill=self._grid)

    def _draw_single_point(
        self,
        point: UserPoint,
        world_limit: float,
        width: int,
        height: int,
    ) -> None:
        x, y = self._to_screen(point.x, point.y, world_limit, width, height)

        is_selected = point.user_id == self.current_user_id
        radius = 7 if is_selected else 5
        fill = self._accent if is_selected else self._accent_secondary
        outline = "#ffffff" if is_selected else "#1f2a3a"

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=fill,
            outline=outline,
            width=1,
        )
        self.canvas.create_text(
            x + radius + 4,
            y - radius,
            anchor="sw",
            text=str(point.user_id),
            fill=self._fg_main,
            font=("Consolas", 9),
        )

    def _compute_world_limit(self, points: Iterable[UserPoint]) -> float:
        max_abs = 1.0
        for point in points:
            max_abs = max(max_abs, abs(point.x), abs(point.y))
        return math.ceil(max_abs + 1.0)

    def _to_screen(
        self,
        x: float,
        y: float,
        world_limit: float,
        width: int,
        height: int,
    ) -> tuple[float, float]:
        normalized_x = (x + world_limit) / (2.0 * world_limit)
        normalized_y = (y + world_limit) / (2.0 * world_limit)
        screen_x = normalized_x * width
        screen_y = height - (normalized_y * height)
        return screen_x, screen_y

    def _clear_form(self) -> None:
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.friend_ids_var.set("")
        for variable in self.interest_vars.values():
            variable.set(False)
