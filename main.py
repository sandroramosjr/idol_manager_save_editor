import json
import os
import shutil
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk


PARAM_TYPES = {
    0: "Cute",
    1: "Cool",
    2: "Sexy",
    3: "Pretty",
    4: "Vocals",
    5: "Dance",
    6: "Funny",
    7: "Smart",
}

MBTI = {
    "ISTJ": "Detail-oriented: -10% chance of concert accidents",
    "ISTP": "Problem-solver: -50% chance of failing accident resolution",
    "ISFJ": "Loyal: +10% producer influence gain",
    "ISFP": "Uniqueness: +10% hardcore appeal",
    "INFJ": "Public Advocate: +5 to all show stats",
    "INFP": "Empathetic: +10% handshake sales",
    "INTJ": "Analytical: Smart increases with age 2x faster",
    "INTP": "Inventive: Café novelty decays 50% slower",
    "ESTP": "Risk-taking: +5 stats during risky marketing",
    "ESTJ": "Dedicated: -20% training time",
    "ESFP": "Entertainer: +5% theater sales",
    "ESFJ": "Community-minded: +5 team chemistry",
    "ENFP": "Diverse Work: -10% stamina cost for new businesses",
    "ENFJ": "Charismatic: +20% election votes",
    "ENTP": "Rebellious: +5 stats when having scandal points",
    "ENTJ": "Driven: +5 stats when pushed",
}

TRAITS = {
    0: ("None", "No effect"),
    1: ("Prodigy", "Trains 30% faster"),
    2: ("Hypochondriac", "Uses 2x stamina in handshake events"),
    3: ("Thick Skin", "Immune to bullying"),
    4: ("Clumsy", "Penalty to dance, bonus to comedy"),
    5: ("Jack of All Trades", "Learns lowest stat 50% faster"),
    6: ("Annoying", "Group events consume 1.2x stamina from others"),
    7: ("Tenacious", "30% chance to not consume stamina below 50%"),
    8: ("Lazy", "Physical stamina cap reduced by 30"),
    9: ("Misandry", "Poor interactions with male fans"),
    10: ("Asexual", "Will not engage in relationships"),
    11: ("Indiscreet", "May leak secrets"),
    12: ("Snitch", "Reports scandals even with bad relationship"),
    13: ("Maternal", "Better relationships with younger idols"),
    14: ("Precocious", "Better relationships with older idols"),
    15: ("Weak Vocal Chords", "Uses 2x stamina in performances"),
    16: ("Underdog", "Bonus to all stats if last single didn’t top charts"),
    17: ("Defeatist", "Penalty to all stats if last single failed"),
    18: ("Worrier", "Penalty to all stats when having scandal points"),
    19: ("Arrogant", "Becomes less likable after centering a single"),
    20: ("Complacent", "Performance stats decrease after centering"),
    21: ("Lone Wolf", "Stat bonus when performing solo"),
    22: ("Anxiety", "Small stat reduction after major events"),
    23: ("Live Fast", "Aging penalties are stronger"),
    24: ("Late Bloomer", "Stats increase with age instead of decreasing"),
    25: ("Forgiving", "Does not hold grudges"),
    26: ("Paranoid", "Reports both real and false scandals"),
    27: ("Secretive", "Does not report scandals to the player"),
    28: ("Trendy", "Appeal bonus with teens and young adults, penalty with adults"),
    29: ("Perfectionist", "Mental stamina decreases if events go poorly"),
    30: ("High Maintenance", "Stamina drains 1.5x faster, spa restores 4x more"),
    31: ("Photogenic", "2x bonus payments from photoshoots"),
    32: ("Meme Queen", "Higher chance of viral marketing success"),
    33: ("Amorous", "More likely to engage in relationships"),
    34: ("Loyal", "Relationship damage from events is reduced"),
    35: ("Steadfast", "Greatly reduces penalties from low stamina"),
    36: ("Resilient", "Recovers stamina faster below 65%"),
    37: ("Shameless", "Not afraid of scandals"),
    38: ("Spoiled", "Consumes double stamina, recovers half"),
    39: ("Moonlighter", "Trains 10x faster but costs 5x stamina"),
    2801: ("Perfect Pitch", "+50 vocal"),
    2802: ("Polyglot", "+20% more fans on world tours"),
    2803: ("Old Money", "No negative effects from low salary"),
    2804: ("Beauty Guru", "+30 pretty"),
    2805: ("Mensa Member", "+50 smart"),
    2806: ("Quick Wit", "+50% rewards from variety shows"),
    2807: ("Fashionista", "+20% appeal with female fans"),
    2808: ("Flirty", "+20% appeal with male fans"),
    2809: ("Well Endowed", "+30 sexy"),
    2810: ("Idol Otaku", "+20% appeal with hardcore fans"),
    2811: ("Wooden Acting", "-50% rewards from dramas"),
    2812: ("Sadistic", "Double mental stamina damage from bullying"),
    2813: ("Reckless", "Increased injury chance, may get injured below 60 stamina"),
    2814: ("Job Hopper", "Plans to graduate in one year"),
    2815: ("Aerophobia", "-50 mental stamina on world tours"),
    2816: ("Stage Fright", "-30 mental stamina when MCing or centering"),
    2817: ("Cult Leader", "+50 election votes"),
    2818: ("Tone Deaf", "-30 vocal"),
    2819: ("Homely", "-10 pretty, cute, sexy and cool"),
    2820: ("Thespian", "-50% stamina cost in dramas"),
}

ZODIAC_RULES = [
    ("Capricorn", (12, 22), (1, 19), "Relationships improve 20% more with girls who don't date"),
    ("Aquarius", (1, 20), (2, 18), "20% less penalty to relationship if pushed girl has less skills than her"),
    ("Pisces", (2, 19), (3, 20), "All relationships improve 10% more"),
    ("Aries", (3, 21), (4, 19), "20% bonus to relationships when she's pushed"),
    ("Taurus", (4, 20), (5, 20), "Relationships fluctuate 20% less"),
    ("Gemini", (5, 21), (6, 20), "Relationships fluctuate 20% more"),
    ("Cancer", (6, 21), (7, 22), "Relationships improve 10% more with her clique"),
    ("Leo", (7, 23), (8, 22), "+10 bonus to smart and funny when choosing clique leader"),
    ("Virgo", (8, 23), (9, 22), "Relationships improve 10% more with girls with >70 average skill"),
    ("Libra", (9, 23), (10, 22), "Relationships improve 20% more with bullied girls"),
    ("Scorpio", (10, 23), (11, 21), "20% less chance of being bullied"),
    ("Sagittarius", (11, 22), (12, 21), "Relationships improve 20% more with scandal girls"),
]


class IdolManagerEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Idol Manager Save Editor")
        self.geometry("1260x900")
        self.minsize(1260, 900)
        self.resizable(False, False)

        self.data = {}
        self.file_path = None
        self.girls = []
        self.current_girl = None
        self.current_selection = None
        self._suppress_sync = False

        self.status_var = tk.StringVar(value="Open a save file to begin.")
        self.player_first_name_var = tk.StringVar()
        self.player_last_name_var = tk.StringVar()
        self.group_name_var = tk.StringVar()
        self.money_var = tk.IntVar()
        self.scandal_var = tk.IntVar()
        self.birthday_var = tk.StringVar()
        self.zodiac_var = tk.StringVar()
        self.trait_var = tk.StringVar()
        self.mbti_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.nickname_var = tk.StringVar()
        self.last_name_var = tk.StringVar()

        self.parameter_vars = {}
        self.param_rows = []
        self.trivia_vars = []
        self.trivia_count_labels = []
        self.trait_desc_var = tk.StringVar()
        self.mbti_desc_var = tk.StringVar()
        self.zodiac_desc_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="Open Save", command=self.open_save).pack(side="left", padx=(0, 8))
        ttk.Button(top, text="Save", command=self.save_save).pack(side="left", padx=(0, 8))
        ttk.Button(top, text="Save As", command=self.save_as_save).pack(side="left", padx=(0, 8))
        ttk.Label(top, textvariable=self.status_var).pack(side="left")

        global_frame = ttk.LabelFrame(self, text="Global Save Data", padding=12)
        global_frame.pack(fill="x", padx=10, pady=(0, 10))
        global_frame.grid_columnconfigure(1, minsize=180)
        global_frame.grid_columnconfigure(3, minsize=150)

        ttk.Label(global_frame, text="Player First Name", width=16, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)
        ttk.Entry(global_frame, textvariable=self.player_first_name_var, width=20).grid(row=0, column=1, sticky="w")

        ttk.Label(global_frame, text="Player Last Name", width=16, anchor="w").grid(row=0, column=2, sticky="w", padx=(10, 10), pady=4)
        ttk.Entry(global_frame, textvariable=self.player_last_name_var, width=20).grid(row=0, column=3, sticky="w")

        ttk.Label(global_frame, text="Group Name", width=16, anchor="w").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=4)
        ttk.Entry(global_frame, textvariable=self.group_name_var, width=30).grid(row=1, column=1, columnspan=3, sticky="w")

        ttk.Label(global_frame, text="Money", width=16, anchor="w").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=4)
        ttk.Entry(global_frame, textvariable=self.money_var, width=14).grid(row=2, column=1, sticky="w")

        ttk.Label(global_frame, text="Scandal Points", width=16, anchor="w").grid(row=2, column=2, sticky="w", padx=(10, 10), pady=4)
        ttk.Entry(global_frame, textvariable=self.scandal_var, width=10).grid(row=2, column=3, sticky="w")

        ttk.Button(global_frame, text="Apply Global Changes", command=self.apply_global_changes).grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))

        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left = ttk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 12))

        left_header = ttk.Label(left, text="Idols", font=("Segoe UI", 10, "bold"))
        left_header.pack(anchor="w", pady=(0, 6))

        self.idol_list = tk.Listbox(left, width=38, height=18, exportselection=False, justify="left")
        self.idol_list.pack(side="left", fill="y", expand=True)
        self.idol_list.bind("<<ListboxSelect>>", self.select_idol)

        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True)

        editor = ttk.LabelFrame(right, text="Selected Idol", padding=12)
        editor.pack(fill="both", expand=True)
        editor.grid_columnconfigure(0, weight=0)
        editor.grid_columnconfigure(1, weight=0)
        editor.grid_columnconfigure(2, weight=0)
        editor.grid_columnconfigure(3, weight=1)

        name_frame = ttk.Frame(editor)
        name_frame.pack(fill="x", pady=(0, 10))
        name_frame.grid_columnconfigure(1, minsize=175)
        name_frame.grid_columnconfigure(3, minsize=175)
        name_frame.grid_columnconfigure(5, minsize=175)

        ttk.Label(name_frame, text="First Name", width=12, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        ttk.Entry(name_frame, textvariable=self.first_name_var, width=16).grid(row=0, column=1, sticky="w", padx=(0, 12), pady=2)
        ttk.Label(name_frame, text="Nickname", width=12, anchor="w").grid(row=0, column=2, sticky="w", padx=(0, 6), pady=2)
        ttk.Entry(name_frame, textvariable=self.nickname_var, width=16).grid(row=0, column=3, sticky="w", padx=(0, 12), pady=2)
        ttk.Label(name_frame, text="Last Name", width=12, anchor="w").grid(row=0, column=4, sticky="w", padx=(0, 6), pady=2)
        ttk.Entry(name_frame, textvariable=self.last_name_var, width=16).grid(row=0, column=5, sticky="w", pady=2)

        row2 = ttk.Frame(editor)
        row2.pack(fill="x", pady=(0, 10))
        row2.grid_columnconfigure(1, minsize=220)
        ttk.Label(row2, text="Birthday", width=12, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        ttk.Entry(row2, textvariable=self.birthday_var, width=24).grid(row=0, column=1, sticky="w", padx=(0, 12), pady=2)
        ttk.Label(row2, text="Zodiac", width=12, anchor="w").grid(row=0, column=2, sticky="w", padx=(0, 6), pady=2)
        zodiac_values = [sign for sign, _, _, _ in ZODIAC_RULES]
        self.zodiac_combo = ttk.Combobox(row2, values=zodiac_values, state="readonly", width=14)
        self.zodiac_combo.grid(row=0, column=3, sticky="w", padx=(0, 12), pady=2)
        self.zodiac_combo.bind("<<ComboboxSelected>>", self.on_zodiac_change)
        ttk.Label(row2, textvariable=self.zodiac_desc_var, wraplength=520).grid(row=0, column=4, sticky="w", pady=2)

        row3 = ttk.Frame(editor)
        row3.pack(fill="x", pady=(0, 10))
        row3.grid_columnconfigure(1, minsize=150)
        ttk.Label(row3, text="MBTI", width=12, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        self.mbti_combo = ttk.Combobox(row3, values=list(MBTI.keys()), state="readonly", width=12)
        self.mbti_combo.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=2)
        self.mbti_combo.bind("<<ComboboxSelected>>", self.on_mbti_change)
        ttk.Label(row3, textvariable=self.mbti_desc_var, wraplength=560).grid(row=0, column=2, sticky="w", pady=2)

        row4 = ttk.Frame(editor)
        row4.pack(fill="x", pady=(0, 10))
        row4.grid_columnconfigure(1, minsize=430)
        ttk.Label(row4, text="Trait ID", width=12, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        trait_values = [f"{k} – {v[0]}" for k, v in sorted(TRAITS.items())]
        self.trait_combo = ttk.Combobox(row4, values=trait_values, state="readonly", width=52)
        self.trait_combo.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=2)
        self.trait_combo.bind("<<ComboboxSelected>>", self.on_trait_change)
        ttk.Label(row4, textvariable=self.trait_desc_var, wraplength=700).grid(row=0, column=2, sticky="w", pady=2)

        ttk.Label(editor, text="Parameters", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(6, 4))
        self.param_frame = ttk.Frame(editor)
        self.param_frame.pack(fill="both", expand=True)

        ttk.Label(editor, text="Trivia (max 4)", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
        self.trivia_frame = ttk.Frame(editor)
        self.trivia_frame.pack(fill="x")

        trivia_button_row = ttk.Frame(editor)
        trivia_button_row.pack(fill="x", pady=(6, 0))
        ttk.Button(trivia_button_row, text="Add Trivia", command=self.add_trivia).pack(side="left", padx=(0, 6))
        ttk.Button(trivia_button_row, text="Remove Last", command=self.remove_trivia).pack(side="left")

        ttk.Button(editor, text="Apply Idol Changes", command=self.apply_idol_changes).pack(anchor="e", pady=(12, 0))

    def open_save(self):
        file_path = filedialog.askopenfilename(
            title="Open Idol Manager save JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.data = json.load(handle)
            self.file_path = file_path
            self.girls = self.data.get("data_girls__Girls", []) or []
            self._load_global_values()
            self._populate_idol_list()
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
        except Exception as exc:
            messagebox.showerror("Load failed", f"Could not read the save file.\n\n{exc}")

    def save_save(self):
        if not self.file_path:
            self.save_as_save()
            return

        self._write_json(self.file_path)

    def save_as_save(self):
        file_path = filedialog.asksaveasfilename(
            title="Save JSON As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not file_path:
            return

        self._write_json(file_path)

    def _write_json(self, file_path):
        try:
            shutil.copyfile(file_path, file_path + ".bak") if os.path.exists(file_path) else None
            with open(file_path, "w", encoding="utf-8") as handle:
                json.dump(self.data, handle, indent=2, ensure_ascii=False)
                handle.write("\n")
            self.file_path = file_path
            self.status_var.set(f"Saved: {os.path.basename(file_path)}")
        except Exception as exc:
            messagebox.showerror("Save failed", f"Could not write the save file.\n\n{exc}")

    def _load_global_values(self):
        player_data = self.data.get("staticVars__PlayerData", {})
        self.player_first_name_var.set(player_data.get("FirstName", ""))
        self.player_last_name_var.set(player_data.get("LastName", ""))
        self.group_name_var.set(player_data.get("GroupName", ""))

        for resource in self.data.get("resources__Resources", []):
            resource_type = resource.get("Type")
            if resource_type == 0:
                self.money_var.set(int(resource.get("Val", 0)))
            elif resource_type == 3:
                self.scandal_var.set(int(resource.get("Val", 0)))

    def _populate_idol_list(self):
        self.idol_list.delete(0, tk.END)
        for idx, girl in enumerate(self.girls):
            if not isinstance(girl, dict):
                continue
            name = self._idol_display_name(girl)
            self.idol_list.insert(tk.END, f"{idx + 1}. {name}")

    def _idol_display_name(self, girl):
        first = girl.get("firstName", "")
        last = girl.get("lastName", "")
        nick = girl.get("nickname", "")
        if nick:
            return f'{first} "{nick}" {last}'.strip()
        return f"{first} {last}".strip()

    def select_idol(self, event):
        selection = self.idol_list.curselection()
        if not selection:
            return

        idx = int(selection[0])
        if idx >= len(self.girls):
            return

        self.current_selection = idx
        self.current_girl = self.girls[idx]
        self._populate_idol_editor()

    def _populate_idol_editor(self):
        if not self.current_girl:
            return

        self.first_name_var.set(self.current_girl.get("firstName", ""))
        self.nickname_var.set(self.current_girl.get("nickname", ""))
        self.last_name_var.set(self.current_girl.get("lastName", ""))
        self.birthday_var.set(self.current_girl.get("birthday", ""))
        self._update_zodiac_from_birthday()

        variables = self.current_girl.get("Variables", [])
        mbti_value = variables[0] if variables else ""
        self.mbti_var.set(mbti_value)
        self.mbti_combo.set(mbti_value)
        self.mbti_desc_var.set(MBTI.get(mbti_value, ""))

        trait_id = int(self.current_girl.get("trait", 0) or 0)
        self.trait_var.set(f"{trait_id} – {TRAITS.get(trait_id, ('Unknown', ''))[0]}")
        self.trait_combo.set(self.trait_var.get())
        self.trait_desc_var.set(TRAITS.get(trait_id, ("Unknown", ""))[1])

        self._render_parameters()
        self._load_trivia_fields()

    def _render_parameters(self):
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        self.parameter_vars = {}
        self.param_rows = []

        parameters = self.current_girl.get("parameters", []) if self.current_girl else []
        for index, param in enumerate(parameters):
            if param.get("type") not in PARAM_TYPES:
                continue

            row = ttk.Frame(self.param_frame)
            row.pack(fill="x", pady=2)
            self.param_rows.append(row)

            ttk.Label(row, text=f"{PARAM_TYPES[param.get('type')]}:").pack(side="left")

            value_var = tk.IntVar(value=int(param.get("_val", 0) or 0))
            potential_var = tk.IntVar(value=int(param.get("potential", 0) or 0))

            ttk.Entry(row, textvariable=value_var, width=6).pack(side="left", padx=(6, 4))
            ttk.Button(row, text="MAX", command=lambda value=value_var: value.set(100)).pack(side="left", padx=(0, 6))
            ttk.Label(row, text="/").pack(side="left")
            ttk.Entry(row, textvariable=potential_var, width=6).pack(side="left", padx=(4, 4))
            ttk.Button(row, text="MAX", command=lambda cap=potential_var: cap.set(100)).pack(side="left", padx=(0, 10))

            self.parameter_vars[param.get("type")] = {"_val": value_var, "potential": potential_var}

    def _load_trivia_fields(self):
        for widget in self.trivia_frame.winfo_children():
            widget.destroy()

        self.trivia_vars = []
        self.trivia_count_labels = []
        trivia_lines = self.current_girl.get("Trivia", []) if self.current_girl else []
        for line in trivia_lines[:4]:
            var = tk.StringVar(value=line)
            var.trace_add("write", self._on_trivia_write)
            self.trivia_vars.append(var)

        self._refresh_trivia_ui()

    def _on_trivia_write(self, *_):
        for idx, var in enumerate(self.trivia_vars):
            text = var.get()
            if len(text) > 80:
                var.set(text[:80])
                text = var.get()
            count_label = self.trivia_count_labels[idx] if idx < len(self.trivia_count_labels) else None
            if count_label is not None:
                count_label.config(text=f"{len(text)}/80")

    def _refresh_trivia_ui(self):
        for widget in self.trivia_frame.winfo_children():
            widget.destroy()

        self.trivia_count_labels = []
        for idx, var in enumerate(self.trivia_vars, start=1):
            row = ttk.Frame(self.trivia_frame)
            row.pack(fill="x", pady=2)

            ttk.Label(row, text=f"{idx}.", width=2, anchor="w").pack(side="left")
            ttk.Entry(row, textvariable=var, width=86).pack(side="left", fill="x", expand=True)
            count_label = ttk.Label(row, text=f"{len(var.get())}/80", width=8, anchor="w")
            count_label.pack(side="left", padx=(8, 0))
            self.trivia_count_labels.append(count_label)

    def add_trivia(self):
        if not self.current_girl:
            return
        if len(self.trivia_vars) >= 4:
            return

        var = tk.StringVar(value="")
        var.trace_add("write", self._on_trivia_write)
        self.trivia_vars.append(var)
        self._refresh_trivia_ui()

    def remove_trivia(self):
        if not self.trivia_vars:
            return
        self.trivia_vars.pop()
        self._refresh_trivia_ui()

    def apply_global_changes(self):
        player_data = self.data.setdefault("staticVars__PlayerData", {})
        player_data["FirstName"] = self.player_first_name_var.get().strip()
        player_data["LastName"] = self.player_last_name_var.get().strip()
        player_data["GroupName"] = self.group_name_var.get().strip()

        for resource in self.data.get("resources__Resources", []):
            if resource.get("Type") == 0:
                resource["Val"] = int(self.money_var.get())
            elif resource.get("Type") == 3:
                resource["Val"] = int(self.scandal_var.get())

        self.status_var.set("Global values applied to the in-memory save.")

    def apply_idol_changes(self):
        if not self.current_girl:
            return

        self.current_girl["firstName"] = self.first_name_var.get().strip()
        self.current_girl["nickname"] = self.nickname_var.get().strip()
        self.current_girl["lastName"] = self.last_name_var.get().strip()
        self.current_girl["birthday"] = self.birthday_var.get().strip()

        selected_trait = self.trait_combo.get()
        try:
            trait_id = int(selected_trait.split("–", 1)[0].strip())
            self.current_girl["trait"] = trait_id
        except (ValueError, AttributeError):
            self.current_girl["trait"] = 0

        vars_list = self.current_girl.setdefault("Variables", [])
        mbti_value = self.mbti_combo.get().strip()
        if vars_list:
            vars_list[0] = mbti_value
        else:
            vars_list.append(mbti_value)

        for param_type, values in self.parameter_vars.items():
            for param in self.current_girl.get("parameters", []):
                if param.get("type") == param_type:
                    param["_val"] = int(values["_val"].get())
                    param["potential"] = int(values["potential"].get())
                    break

        self.current_girl["Trivia"] = [var.get().strip() for var in self.trivia_vars if var.get().strip()]

        self._update_idol_list_entry()
        self.status_var.set(f"Changes applied to {self._idol_display_name(self.current_girl)}.")

    def _update_idol_list_entry(self):
        if self.current_selection is None:
            return
        self.idol_list.delete(self.current_selection)
        self.idol_list.insert(self.current_selection, f"{self.current_selection + 1}. {self._idol_display_name(self.current_girl)}")
        self.idol_list.selection_set(self.current_selection)

    def on_trait_change(self, event):
        if not self.current_girl:
            return
        text = self.trait_combo.get()
        try:
            trait_id = int(text.split("–", 1)[0].strip())
        except ValueError:
            return
        self.trait_desc_var.set(TRAITS.get(trait_id, ("Unknown", ""))[1])

    def on_mbti_change(self, event):
        if not self.current_girl:
            return
        self.mbti_desc_var.set(MBTI.get(self.mbti_combo.get(), ""))

    def on_zodiac_change(self, event):
        if not self.current_girl or self._suppress_sync:
            return

        selected_sign = self.zodiac_combo.get()
        if not selected_sign:
            return

        try:
            current_year = datetime.strptime(self.birthday_var.get(), "%Y-%m-%d %H:%M:%S").year
        except ValueError:
            current_year = datetime.now().year

        for sign, (start_m, start_d), (end_m, end_d), effect in ZODIAC_RULES:
            if sign != selected_sign:
                continue
            new_date = datetime(current_year, start_m, start_d, 0, 0, 0)
            self._suppress_sync = True
            self.birthday_var.set(new_date.strftime("%Y-%m-%d %H:%M:%S"))
            self._suppress_sync = False
            self.zodiac_desc_var.set(effect)
            break

    def _update_zodiac_from_birthday(self):
        if not self.current_girl or self._suppress_sync:
            return

        try:
            birthday = datetime.strptime(self.birthday_var.get(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return

        found_sign = None
        found_effect = ""
        for sign, (start_m, start_d), (end_m, end_d), effect in ZODIAC_RULES:
            if (birthday.month, birthday.day) >= (start_m, start_d):
                if (birthday.month, birthday.day) <= (end_m, end_d):
                    found_sign = sign
                    found_effect = effect
                    break
            if (start_m > end_m) and ((birthday.month, birthday.day) >= (start_m, start_d) or (birthday.month, birthday.day) <= (end_m, end_d)):
                found_sign = sign
                found_effect = effect
                break

        if found_sign:
            self.zodiac_combo.set(found_sign)
            self.zodiac_desc_var.set(found_effect)


if __name__ == "__main__":
    app = IdolManagerEditor()
    app.mainloop()
