import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os
import random
import string


# ============================================================
# RESTAURACJA KANAPKOWA
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RestauracjaKanapkowa(ctk.CTk):

    ADMIN_CODE = "4781"
    PLIK_DANYCH = "dane_restauracji.json"

    # ========================================================
    # KOLORY
    # ========================================================

    BG = "#182235"
    SIDEBAR = "#202D43"
    PANEL = "#273750"
    CARD = "#30425E"
    CARD_HOVER = "#3B4F6D"

    BLUE = "#38BDF8"
    BLUE_HOVER = "#0EA5E9"

    GREEN = "#22C55E"
    GREEN_HOVER = "#16A34A"

    RED = "#EF4444"
    RED_HOVER = "#DC2626"

    ORANGE = "#F59E0B"

    TEXT = "#F8FAFC"
    MUTED = "#B7C3D4"
    BORDER = "#465A76"

    # ========================================================
    # START
    # ========================================================

    def __init__(self):
        super().__init__()

        self.title("Restauracja kanapkowa")

        self.fullscreen = True

        self.attributes(
            "-fullscreen",
            True
        )

        self.bind(
            "<F11>",
            self.przelacz_pelny_ekran
        )

        self.bind(
            "<Escape>",
            self.wylacz_pelny_ekran
        )

        self.configure(
            fg_color=self.BG
        )

        # ----------------------------------------------------
        # DANE
        # ----------------------------------------------------

        self.produkty = self.domyslne_produkty()

        self.gotowe_kanapki = []

        self.historia_zamowien = []

        self.numer_zamowienia = 1

        self.reset_zamowienie()

        self.wczytaj_dane()

        self.menu_glowne()

    # ========================================================
    # PEŁNY EKRAN
    # ========================================================

    def przelacz_pelny_ekran(self, event=None):

        self.fullscreen = not self.fullscreen

        self.attributes(
            "-fullscreen",
            self.fullscreen
        )

    def wylacz_pelny_ekran(self, event=None):

        self.fullscreen = False

        self.attributes(
            "-fullscreen",
            False
        )

        self.geometry(
            "1350x850"
        )

    # ========================================================
    # DOMYŚLNE PRODUKTY
    # ========================================================

    def domyslne_produkty(self):

        return {

            "typy": [
                {
                    "nazwa": "Bułka",
                    "dostepny": True
                },
                {
                    "nazwa": "Chleb",
                    "dostepny": True
                },
                {
                    "nazwa": "Rogal",
                    "dostepny": True
                }
            ],

            "bulki": [
                {
                    "nazwa": "Ziarnella",
                    "dostepny": True
                },
                {
                    "nazwa": "Pszenna",
                    "dostepny": True
                },
                {
                    "nazwa": "Kajzerka",
                    "dostepny": True
                },
                {
                    "nazwa": "Dyniowa",
                    "dostepny": True
                },
                {
                    "nazwa": "Ze skyrem",
                    "dostepny": True
                },
                {
                    "nazwa": "Ziemniaczana",
                    "dostepny": True
                }
            ],

            "chleby": [
                {
                    "nazwa": "Staropolski",
                    "dostepny": True
                },
                {
                    "nazwa": "Zwykły",
                    "dostepny": True
                },
                {
                    "nazwa": "Żytni razowy",
                    "dostepny": True
                }
            ],

            "rogale": [
                {
                    "nazwa": "Z makiem",
                    "dostepny": True
                },
                {
                    "nazwa": "Zwykły",
                    "dostepny": True
                }
            ],

            "skladniki": [
                {
                    "nazwa": "Szynka",
                    "dostepny": True
                },
                {
                    "nazwa": "Ser",
                    "dostepny": True
                },
                {
                    "nazwa": "Twaróg",
                    "dostepny": True
                },
                {
                    "nazwa": "Pasztet",
                    "dostepny": True
                },
                {
                    "nazwa": "Sałata",
                    "dostepny": True
                }
            ],

            "warzywa": [
                {
                    "nazwa": "Ogórek",
                    "dostepny": True
                },
                {
                    "nazwa": "Pomidor",
                    "dostepny": True
                },
                {
                    "nazwa": "Rzodkiewka",
                    "dostepny": True
                }
            ],

            "napoje": [
                {
                    "nazwa": "Sok jabłkowy",
                    "dostepny": True
                },
                {
                    "nazwa": "Sok pomarańczowy",
                    "dostepny": True
                },
                {
                    "nazwa": "Sok wieloowocowy",
                    "dostepny": True
                },
                {
                    "nazwa": "Herbata",
                    "dostepny": True
                },
                {
                    "nazwa": "Woda",
                    "dostepny": True
                }
            ],

            "miejsca_dostawy": [
                {
                    "nazwa": "Odbiór osobisty",
                    "dostepny": True
                }
            ]
        }

    # ========================================================
    # RESET ZAMÓWIENIA
    # ========================================================

    def reset_zamowienie(self):

        self.typ = ""

        self.pieczywo = ""

        self.skladniki = {}

        self.warzywa = {}

        self.napoje = {}

        self.miejsce_dostawy = ""

        self.wczytane_id_kanapki = None

    # ========================================================
    # ZAPIS JSON
    # ========================================================

    def zapisz_dane(self):

        dane = {

            "produkty": self.produkty,

            "gotowe_kanapki":
                self.gotowe_kanapki,

            "historia_zamowien":
                self.historia_zamowien[:10],

            "numer_zamowienia":
                self.numer_zamowienia
        }

        try:

            with open(
                self.PLIK_DANYCH,
                "w",
                encoding="utf-8"
            ) as plik:

                json.dump(
                    dane,
                    plik,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as e:

            messagebox.showerror(
                "Błąd zapisu",
                f"Nie udało się zapisać danych:\n\n{e}"
            )

    # ========================================================
    # WCZYTANIE JSON
    # ========================================================

    def wczytaj_dane(self):

        if not os.path.exists(
            self.PLIK_DANYCH
        ):

            self.zapisz_dane()

            return

        try:

            with open(
                self.PLIK_DANYCH,
                "r",
                encoding="utf-8"
            ) as plik:

                zawartosc = plik.read().strip()

            if not zawartosc:

                self.zapisz_dane()

                return

            dane = json.loads(
                zawartosc
            )

            if not isinstance(
                dane,
                dict
            ):

                raise ValueError(
                    "Główny element JSON musi być obiektem."
                )

            zapisane_produkty = dane.get(
                "produkty"
            )

            if (
                isinstance(
                    zapisane_produkty,
                    dict
                )
                and
                len(zapisane_produkty) > 0
            ):

                domyslne = (
                    self.domyslne_produkty()
                )

                for key, value in domyslne.items():

                    if key not in zapisane_produkty:

                        zapisane_produkty[key] = value

                self.produkty = (
                    zapisane_produkty
                )

            else:

                self.produkty = (
                    self.domyslne_produkty()
                )

            gotowe = dane.get(
                "gotowe_kanapki",
                []
            )

            if isinstance(
                gotowe,
                list
            ):

                self.gotowe_kanapki = gotowe

            else:

                self.gotowe_kanapki = []

            historia = dane.get(
                "historia_zamowien",
                []
            )

            if isinstance(
                historia,
                list
            ):

                self.historia_zamowien = (
                    historia[:10]
                )

            else:

                self.historia_zamowien = []

            try:

                self.numer_zamowienia = int(
                    dane.get(
                        "numer_zamowienia",
                        1
                    )
                )

            except:

                self.numer_zamowienia = 1

            zmieniono = False

            for kanapka in self.gotowe_kanapki:

                if not kanapka.get("id"):

                    kanapka["id"] = (
                        self.wygeneruj_id_kanapki()
                    )

                    zmieniono = True

            if zmieniono:

                self.zapisz_dane()

        except (
            json.JSONDecodeError,
            ValueError
        ):

            self.produkty = (
                self.domyslne_produkty()
            )

            self.gotowe_kanapki = []

            self.historia_zamowien = []

            self.numer_zamowienia = 1

            self.zapisz_dane()

            messagebox.showwarning(
                "Naprawiono dane",
                "Plik dane_restauracji.json "
                "był pusty lub niepoprawny.\n\n"
                "Program utworzył poprawne dane."
            )

        except Exception as e:

            self.produkty = (
                self.domyslne_produkty()
            )

            self.gotowe_kanapki = []

            self.historia_zamowien = []

            self.numer_zamowienia = 1

            messagebox.showwarning(
                "Problem z danymi",
                f"Nie udało się odczytać pliku.\n\n"
                f"{e}\n\n"
                "Program użyje danych domyślnych."
            )

    # ========================================================
    # ID KANAPKI
    # ========================================================

    def wygeneruj_id_kanapki(self):

        while True:

            znaki = (
                string.ascii_uppercase
                + string.digits
            )

            kod = "".join(
                random.choice(znaki)
                for _ in range(8)
            )

            identyfikator = (
                "KAN-" + kod
            )

            istnieje = any(
                k.get("id")
                == identyfikator
                for k in self.gotowe_kanapki
            )

            if not istnieje:

                return identyfikator

    # ========================================================
    # ID ZAMÓWIENIA
    # ========================================================

    def wygeneruj_id_zamowienia(self):

        while True:

            znaki = (
                string.ascii_uppercase
                + string.digits
            )

            kod = "".join(
                random.choice(znaki)
                for _ in range(6)
            )

            identyfikator = (
                "ZAM-" + kod
            )

            istnieje = any(
                z.get("id")
                == identyfikator
                for z in self.historia_zamowien
            )

            if not istnieje:

                return identyfikator

    # ========================================================
    # CZYSZCZENIE
    # ========================================================

    def clear(self):

        for widget in self.winfo_children():

            widget.destroy()

    # ========================================================
    # TOPBAR
    # ========================================================

    def topbar(self, krok=None):

        top = ctk.CTkFrame(
            self,
            height=78,
            fg_color=self.SIDEBAR,
            corner_radius=0
        )

        top.pack(
            fill="x"
        )

        top.pack_propagate(False)

        ctk.CTkLabel(
            top,
            text="🥪",
            font=ctk.CTkFont(size=32)
        ).pack(
            side="left",
            padx=(28, 10)
        )

        ctk.CTkLabel(
            top,
            text="Restauracja kanapkowa",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        if krok:

            progress = ctk.CTkFrame(
                top,
                fg_color="transparent"
            )

            progress.pack(
                side="left",
                padx=55
            )

            for i in range(1, 7):

                if i < krok:

                    color = self.GREEN

                elif i == krok:

                    color = self.BLUE

                else:

                    color = "#596B84"

                ctk.CTkLabel(
                    progress,
                    text=str(i),
                    width=30,
                    height=30,
                    corner_radius=15,
                    fg_color=color,
                    text_color="white",
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    )
                ).pack(
                    side="left",
                    padx=5
                )

        ctk.CTkButton(
            top,
            text="⚙ Administrator",
            width=175,
            height=40,
            corner_radius=12,
            fg_color=self.CARD,
            hover_color=self.CARD_HOVER,
            command=self.admin_login
        ).pack(
            side="right",
            padx=25
        )

    # ========================================================
    # UKŁAD
    # ========================================================

    def content_layout(
        self,
        show_order=True
    ):

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=24
        )

        if not show_order:

            return container

        container.grid_columnconfigure(
            0,
            weight=4
        )

        container.grid_columnconfigure(
            1,
            weight=1
        )

        container.grid_rowconfigure(
            0,
            weight=1
        )

        left = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 20)
        )

        right = ctk.CTkFrame(
            container,
            fg_color=self.PANEL,
            corner_radius=24,
            width=290
        )

        right.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        right.grid_propagate(False)

        self.panel_zamowienia(
            right
        )

        return left

    # ========================================================
    # PANEL ZAMÓWIENIA
    # ========================================================

    def panel_zamowienia(
        self,
        parent
    ):

        ctk.CTkLabel(
            parent,
            text="🛒 Twoje zamówienie",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(24, 18)
        )

        self.order_section(
            parent,
            "🍞 PIECZYWO",
            self.pieczywo
            or "Jeszcze nie wybrano"
        )

        self.order_section(
            parent,
            "🥩 SKŁADNIKI",
            "\n".join(
                self.get_selected(
                    self.skladniki
                )
            )
            or "Brak"
        )

        self.order_section(
            parent,
            "🥬 WARZYWA",
            "\n".join(
                self.get_selected(
                    self.warzywa
                )
            )
            or "Brak"
        )

        self.order_section(
            parent,
            "🥤 NAPOJE",
            "\n".join(
                self.get_selected(
                    self.napoje
                )
            )
            or "Brak"
        )

        self.order_section(
            parent,
            "📍 MIEJSCE DOSTAWY",
            self.miejsce_dostawy
            or "Jeszcze nie wybrano"
        )

    def order_section(
        self,
        parent,
        title,
        content
    ):

        box = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=15
        )

        box.pack(
            fill="x",
            padx=15,
            pady=6
        )

        ctk.CTkLabel(
            box,
            text=title,
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=13,
            pady=(11, 3)
        )

        ctk.CTkLabel(
            box,
            text=content,
            text_color=self.TEXT,
            justify="left",
            wraplength=230,
            font=ctk.CTkFont(size=12)
        ).pack(
            anchor="w",
            padx=13,
            pady=(0, 11)
        )

    # ========================================================
    # TYTUŁ
    # ========================================================

    def page_title(
        self,
        parent,
        eyebrow,
        title,
        subtitle
    ):

        ctk.CTkLabel(
            parent,
            text=eyebrow,
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(
                size=29,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(4, 4)
        )

        ctk.CTkLabel(
            parent,
            text=subtitle,
            text_color=self.MUTED,
            font=ctk.CTkFont(size=13),
            justify="left",
            wraplength=1000
        ).pack(
            anchor="w"
        )

    # ========================================================
    # MENU GŁÓWNE
    # ========================================================

    def menu_glowne(self):

        self.clear()

        self.topbar()

        center = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        center.pack(
            expand=True
        )

        ctk.CTkLabel(
            center,
            text="🥪",
            font=ctk.CTkFont(size=80)
        ).pack()

        ctk.CTkLabel(
            center,
            text="Restauracja kanapkowa",
            font=ctk.CTkFont(
                size=34,
                weight="bold"
            )
        ).pack(
            pady=(8, 5)
        )

        ctk.CTkLabel(
            center,
            text="Stwórz własną kanapkę albo wybierz gotową.",
            text_color=self.MUTED,
            font=ctk.CTkFont(size=14)
        ).pack(
            pady=(0, 30)
        )

        buttons = ctk.CTkFrame(
            center,
            fg_color="transparent"
        )

        buttons.pack()

        ctk.CTkButton(
            buttons,
            text="＋ Stwórz własną kanapkę",
            width=270,
            height=62,
            corner_radius=18,
            fg_color=self.BLUE,
            hover_color=self.BLUE_HOVER,
            text_color="#001018",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.nowa_kanapka
        ).pack(
            side="left",
            padx=7
        )

        ctk.CTkButton(
            buttons,
            text="🥪 Gotowe kanapki",
            width=230,
            height=62,
            corner_radius=18,
            fg_color=self.CARD,
            hover_color=self.CARD_HOVER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.menu_gotowych
        ).pack(
            side="left",
            padx=7
        )

        box = ctk.CTkFrame(
            center,
            fg_color=self.PANEL,
            corner_radius=18
        )

        box.pack(
            pady=28
        )

        ctk.CTkLabel(
            box,
            text="🆔 Wpisz ID gotowej kanapki",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            pady=(16, 8)
        )

        row = ctk.CTkFrame(
            box,
            fg_color="transparent"
        )

        row.pack(
            padx=15,
            pady=(0, 16)
        )

        self.id_entry = ctk.CTkEntry(
            row,
            width=210,
            height=42,
            placeholder_text="KAN-XXXXXXXX",
            corner_radius=11
        )

        self.id_entry.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            row,
            text="Wczytaj",
            width=100,
            height=42,
            corner_radius=11,
            command=self.wczytaj_id
        ).pack(
            side="left",
            padx=5
        )

    # ========================================================
    # NOWA KANAPKA
    # ========================================================

    def nowa_kanapka(self):

        self.reset_zamowienie()

        self.etap1()

    # ========================================================
    # WCZYTYWANIE ID
    # ========================================================

    def wczytaj_id(self):

        identyfikator = (
            self.id_entry.get()
            .strip()
            .upper()
        )

        if not identyfikator:

            messagebox.showwarning(
                "Brak ID",
                "Wpisz ID gotowej kanapki."
            )

            return

        kanapka = next(
            (
                k
                for k in self.gotowe_kanapki
                if str(
                    k.get("id", "")
                ).upper()
                == identyfikator
            ),
            None
        )

        if not kanapka:

            messagebox.showerror(
                "Nie znaleziono",
                "Nie znaleziono kanapki o takim ID."
            )

            return

        self.wybierz_gotowa(
            kanapka
        )

    # ========================================================
    # KAFEL PRODUKTU
    # ========================================================

    def product_tile(
        self,
        parent,
        index,
        nazwa,
        icon,
        dostepny,
        command,
        columns=3
    ):

        row = index // columns

        col = index % columns

        frame = ctk.CTkFrame(
            parent,
            fg_color=(
                self.CARD
                if dostepny
                else "#253043"
            ),
            corner_radius=20,
            border_width=1,
            border_color=self.BORDER
        )

        frame.grid(
            row=row,
            column=col,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        ctk.CTkLabel(
            frame,
            text=icon,
            font=ctk.CTkFont(size=43)
        ).pack(
            pady=(24, 8)
        )

        ctk.CTkLabel(
            frame,
            text=nazwa,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack()

        if dostepny:

            ctk.CTkButton(
                frame,
                text="WYBIERZ",
                width=140,
                height=37,
                corner_radius=11,
                fg_color=self.BLUE,
                hover_color=self.BLUE_HOVER,
                text_color="#001018",
                command=command
            ).pack(
                pady=20
            )

        else:

            ctk.CTkLabel(
                frame,
                text="BRAK",
                text_color=self.RED,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).pack(
                pady=22
            )

    # ========================================================
    # KAFEL WYBORU
    # ========================================================

    def toggle_tile(
        self,
        parent,
        index,
        nazwa,
        icon,
        selected,
        dostepny,
        command,
        columns=2
    ):

        row = index // columns

        col = index % columns

        frame = ctk.CTkFrame(
            parent,
            fg_color=(
                self.CARD
                if dostepny
                else "#253043"
            ),
            corner_radius=20,
            border_width=(
                2
                if selected
                else 1
            ),
            border_color=(
                self.GREEN
                if selected
                else self.BORDER
            )
        )

        frame.grid(
            row=row,
            column=col,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        ctk.CTkLabel(
            frame,
            text=icon,
            font=ctk.CTkFont(size=40)
        ).pack(
            pady=(20, 7)
        )

        ctk.CTkLabel(
            frame,
            text=nazwa,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack()

        if not dostepny:

            ctk.CTkLabel(
                frame,
                text="BRAK",
                text_color=self.RED,
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).pack(
                pady=20
            )

            return

        if selected:

            text = "✓ WYBRANO"

            color = self.GREEN

            hover = self.GREEN_HOVER

        else:

            text = "WYBIERZ"

            color = self.BLUE

            hover = self.BLUE_HOVER

        ctk.CTkButton(
            frame,
            text=text,
            width=145,
            height=37,
            corner_radius=11,
            fg_color=color,
            hover_color=hover,
            command=command
        ).pack(
            pady=18
        )

    # ========================================================
    # ETAP 1
    # ========================================================

    def etap1(self):

        self.clear()

        self.topbar(1)

        left = self.content_layout()

        self.page_title(
            left,
            "KROK 1 Z 6",
            "Wybierz rodzaj pieczywa",
            "Bułka, chleb czy rogal?"
        )

        grid = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        grid.pack(
            fill="both",
            expand=True,
            pady=20
        )

        for i in range(3):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        icons = {

            "Bułka": "🥖",

            "Chleb": "🍞",

            "Rogal": "🥐"
        }

        for i, produkt in enumerate(
            self.produkty["typy"]
        ):

            self.product_tile(
                grid,
                i,
                produkt["nazwa"],
                icons.get(
                    produkt["nazwa"],
                    "🍞"
                ),
                produkt.get(
                    "dostepny",
                    True
                ),
                lambda n=produkt["nazwa"]:
                    self.wybierz_typ(n)
            )

        ctk.CTkButton(
            left,
            text="← Cofnij do menu",
            width=170,
            height=45,
            corner_radius=13,
            fg_color=self.CARD,
            hover_color=self.CARD_HOVER,
            command=self.menu_glowne
        ).pack(
            pady=(10, 5)
        )

    def wybierz_typ(
        self,
        nazwa
    ):

        self.typ = nazwa

        self.etap2()

    # ========================================================
    # ETAP 2
    # ========================================================

    def etap2(self):

        self.clear()

        self.topbar(2)

        left = self.content_layout()

        self.page_title(
            left,
            "KROK 2 Z 6",
            f"Wybierz {self.typ.lower()}",
            "Wybierz konkretny rodzaj pieczywa."
        )

        if self.typ == "Bułka":

            key = "bulki"

            icon = "🥖"

        elif self.typ == "Chleb":

            key = "chleby"

            icon = "🍞"

        else:

            key = "rogale"

            icon = "🥐"

        grid = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        grid.pack(
            fill="both",
            expand=True,
            pady=15
        )

        for i in range(3):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        for i, produkt in enumerate(
            self.produkty[key]
        ):

            self.product_tile(
                grid,
                i,
                produkt["nazwa"],
                icon,
                produkt.get(
                    "dostepny",
                    True
                ),
                lambda n=produkt["nazwa"]:
                    self.wybierz_pieczywo(n)
            )

        self.bottom_buttons(
            left,
            self.etap1,
            None
        )

    def wybierz_pieczywo(
        self,
        nazwa
    ):

        self.pieczywo = nazwa

        self.etap3()

    # ========================================================
    # ETAP 3
    # ========================================================

    def etap3(self):

        self.clear()

        self.topbar(3)

        left = self.content_layout()

        self.page_title(
            left,
            "KROK 3 Z 6",
            "Ustaw składniki",
            "Szynka i ser mogą być razem. "
            "Pasztet i twaróg są samodzielne. "
            "Sałatę można łączyć ze wszystkim."
        )

        grid = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        grid.pack(
            fill="both",
            expand=True,
            pady=15
        )

        for i in range(2):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        icons = {

            "Szynka": "🥩",

            "Ser": "🧀",

            "Twaróg": "🥣",

            "Pasztet": "🍖",

            "Sałata": "🥬"
        }

        for i, produkt in enumerate(
            self.produkty["skladniki"]
        ):

            nazwa = produkt["nazwa"]

            self.toggle_tile(
                grid,
                i,
                nazwa,
                icons.get(
                    nazwa,
                    "🥩"
                ),
                self.skladniki.get(
                    nazwa,
                    False
                ),
                produkt.get(
                    "dostepny",
                    True
                ),
                lambda n=nazwa:
                    self.toggle_skladnik(n),
                columns=2
            )

        self.bottom_buttons(
            left,
            self.etap2,
            self.etap4
        )

    def toggle_skladnik(
        self,
        nazwa
    ):

        if self.skladniki.get(
            nazwa,
            False
        ):

            self.skladniki[nazwa] = False

            self.etap3()

            return

        if nazwa == "Pasztet":

            if any(
                self.skladniki.get(
                    x,
                    False
                )
                for x in [
                    "Szynka",
                    "Ser",
                    "Twaróg"
                ]
            ):

                messagebox.showwarning(
                    "Nie można połączyć",
                    "Pasztet może być tylko samodzielnie."
                )

                return

        if nazwa == "Twaróg":

            if any(
                self.skladniki.get(
                    x,
                    False
                )
                for x in [
                    "Szynka",
                    "Ser",
                    "Pasztet"
                ]
            ):

                messagebox.showwarning(
                    "Nie można połączyć",
                    "Twaróg może być tylko samodzielnie."
                )

                return

        if nazwa in [
            "Szynka",
            "Ser"
        ]:

            if (
                self.skladniki.get(
                    "Twaróg",
                    False
                )
                or
                self.skladniki.get(
                    "Pasztet",
                    False
                )
            ):

                messagebox.showwarning(
                    "Nie można połączyć",
                    "Szynka i ser nie mogą być "
                    "łączone z twarogiem ani pasztetem."
                )

                return

        self.skladniki[nazwa] = True

        self.etap3()

    # ========================================================
    # ETAP 4
    # ========================================================

    def etap4(self):

        self.clear()

        self.topbar(4)

        left = self.content_layout()

        self.page_title(
            left,
            "KROK 4 Z 6",
            "Ustaw warzywa",
            "Wybierz dowolną liczbę warzyw."
        )

        grid = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        grid.pack(
            fill="both",
            expand=True,
            pady=20
        )

        for i in range(3):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        icons = {

            "Ogórek": "🥒",

            "Pomidor": "🍅",

            "Rzodkiewka": "🌱"
        }

        for i, produkt in enumerate(
            self.produkty["warzywa"]
        ):

            nazwa = produkt["nazwa"]

            self.toggle_tile(
                grid,
                i,
                nazwa,
                icons.get(
                    nazwa,
                    "🥬"
                ),
                self.warzywa.get(
                    nazwa,
                    False
                ),
                produkt.get(
                    "dostepny",
                    True
                ),
                lambda n=nazwa:
                    self.toggle_warzywo(n),
                columns=3
            )

        self.bottom_buttons(
            left,
            self.etap3,
            self.etap5
        )

    def toggle_warzywo(
        self,
        nazwa
    ):

        self.warzywa[nazwa] = not self.warzywa.get(
            nazwa,
            False
        )

        self.etap4()

    # ========================================================
    # ETAP 5
    # ========================================================

    def etap5(self):

        self.clear()

        self.topbar(5)

        left = self.content_layout()

        self.page_title(
            left,
            "KROK 5 Z 6",
            "Ustaw napoje",
            "Wybierz dowolną liczbę napojów."
        )

        grid = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        grid.pack(
            fill="both",
            expand=True,
            pady=15
        )

        for i in range(2):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        icons = {

            "Sok jabłkowy": "🍎",

            "Sok pomarańczowy": "🍊",

            "Sok wieloowocowy": "🧃",

            "Herbata": "🍵",

            "Woda": "💧"
        }

        for i, produkt in enumerate(
            self.produkty["napoje"]
        ):

            nazwa = produkt["nazwa"]

            self.toggle_tile(
                grid,
                i,
                nazwa,
                icons.get(
                    nazwa,
                    "🥤"
                ),
                self.napoje.get(
                    nazwa,
                    False
                ),
                produkt.get(
                    "dostepny",
                    True
                ),
                lambda n=nazwa:
                    self.toggle_napoj(n),
                columns=2
            )

        self.bottom_buttons(
            left,
            self.etap4,
            self.etap6
        )

    def toggle_napoj(
        self,
        nazwa
    ):

        self.napoje[nazwa] = not self.napoje.get(
            nazwa,
            False
        )

        self.etap5()

    # ========================================================
    # ETAP 6 - MIEJSCE DOSTAWY
    # ========================================================

    def etap6(self):

        self.clear()

        self.topbar(6)

        left = self.content_layout()

        self.page_title(
            left,
            "KROK 6 Z 6",
            "Wybierz miejsce dostarczenia",
            "Wybierz miejsce, do którego ma zostać dostarczona kanapka."
        )

        grid = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        grid.pack(
            fill="both",
            expand=True,
            pady=15
        )

        for i in range(2):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        if not self.produkty["miejsca_dostawy"]:

            ctk.CTkLabel(
                grid,
                text="📍\n\nBrak dostępnych miejsc dostawy.",
                text_color=self.MUTED,
                font=ctk.CTkFont(
                    size=17
                ),
                justify="center"
            ).pack(
                pady=80
            )

        for i, produkt in enumerate(
            self.produkty["miejsca_dostawy"]
        ):

            nazwa = produkt["nazwa"]

            self.toggle_tile(
                grid,
                i,
                nazwa,
                "📍",
                self.miejsce_dostawy == nazwa,
                produkt.get(
                    "dostepny",
                    True
                ),
                lambda n=nazwa:
                    self.wybierz_miejsce_dostawy(n),
                columns=2
            )

        self.bottom_buttons(
            left,
            self.etap5,
            self.podsumowanie
        )

    def wybierz_miejsce_dostawy(
        self,
        nazwa
    ):

        if self.miejsce_dostawy == nazwa:

            self.miejsce_dostawy = ""

        else:

            self.miejsce_dostawy = nazwa

        self.etap6()

    # ========================================================
    # PRZYCISKI DÓŁ
    # ========================================================

    def bottom_buttons(
        self,
        parent,
        back,
        next_command
    ):

        bar = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        bar.pack(
            fill="x",
            pady=(12, 0)
        )

        ctk.CTkButton(
            bar,
            text="← Cofnij",
            width=140,
            height=45,
            corner_radius=13,
            fg_color=self.CARD,
            hover_color=self.CARD_HOVER,
            command=back
        ).pack(
            side="left"
        )

        if next_command:

            ctk.CTkButton(
                bar,
                text="Dalej →",
                width=150,
                height=45,
                corner_radius=13,
                fg_color=self.GREEN,
                hover_color=self.GREEN_HOVER,
                font=ctk.CTkFont(
                    weight="bold"
                ),
                command=next_command
            ).pack(
                side="right"
            )

    # ========================================================
    # PODSUMOWANIE
    # ========================================================

    def podsumowanie(self):

        if not self.miejsce_dostawy:

            messagebox.showwarning(
                "Brak miejsca dostawy",
                "Wybierz miejsce dostarczenia kanapki."
            )

            self.etap6()

            return

        self.clear()

        self.topbar()

        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        main.pack(
            fill="both",
            expand=True,
            padx=100,
            pady=35
        )

        header = ctk.CTkFrame(
            main,
            fg_color=self.PANEL,
            corner_radius=25
        )

        header.pack(
            fill="x"
        )

        ctk.CTkLabel(
            header,
            text="✓",
            width=55,
            height=55,
            corner_radius=28,
            fg_color=self.GREEN,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            pady=(22, 8)
        )

        ctk.CTkLabel(
            header,
            text="Twoja kanapka jest gotowa!",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            )
        ).pack()

        opis = (
            f"{self.typ} • {self.pieczywo}"
        )

        if self.wczytane_id_kanapki:

            opis += (
                f"\nID gotowej kanapki: "
                f"{self.wczytane_id_kanapki}"
            )

        ctk.CTkLabel(
            header,
            text=opis,
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            justify="center"
        ).pack(
            pady=(5, 22)
        )

        self.summary_box(
            main,
            "🥩 Składniki",
            self.get_selected(
                self.skladniki
            )
        )

        self.summary_box(
            main,
            "🥬 Warzywa",
            self.get_selected(
                self.warzywa
            )
        )

        self.summary_box(
            main,
            "🥤 Napoje",
            self.get_selected(
                self.napoje
            )
        )

        self.summary_box(
            main,
            "📍 Miejsce dostawy",
            [self.miejsce_dostawy]
            if self.miejsce_dostawy
            else []
        )

        buttons = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        buttons.pack(
            pady=20
        )

        ctk.CTkButton(
            buttons,
            text="✓ Złóż zamówienie",
            width=210,
            height=52,
            corner_radius=15,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.zloz_zamowienie
        ).pack(
            side="left",
            padx=6
        )

        ctk.CTkButton(
            buttons,
            text="← Edytuj",
            width=150,
            height=52,
            corner_radius=15,
            fg_color=self.CARD,
            hover_color=self.CARD_HOVER,
            command=self.etap6
        ).pack(
            side="left",
            padx=6
        )

    def summary_box(
        self,
        parent,
        title,
        items
    ):

        box = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=17,
            border_width=1,
            border_color=self.BORDER
        )

        box.pack(
            fill="x",
            pady=5
        )

        ctk.CTkLabel(
            box,
            text=title,
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(11, 3)
        )

        content = (
            " • ".join(items)
            if items
            else "Brak"
        )

        ctk.CTkLabel(
            box,
            text=content,
            font=ctk.CTkFont(size=14),
            justify="left",
            wraplength=900
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 11)
        )

    # ========================================================
    # ZAMÓWIENIE
    # ========================================================

    def zloz_zamowienie(self):

        if not self.pieczywo:

            messagebox.showwarning(
                "Brak pieczywa",
                "Najpierw wybierz pieczywo."
            )

            return

        if not self.miejsce_dostawy:

            messagebox.showwarning(
                "Brak miejsca dostawy",
                "Wybierz miejsce dostarczenia kanapki."
            )

            return

        id_zamowienia = (
            self.wygeneruj_id_zamowienia()
        )

        zamowienie = {

            "id": id_zamowienia,

            "numer":
                self.numer_zamowienia,

            "czas":
                datetime.now().strftime(
                    "%d.%m.%Y %H:%M:%S"
                ),

            "typ":
                self.typ,

            "pieczywo":
                self.pieczywo,

            "skladniki":
                self.get_selected(
                    self.skladniki
                ),

            "warzywa":
                self.get_selected(
                    self.warzywa
                ),

            "napoje":
                self.get_selected(
                    self.napoje
                ),

            "miejsce_dostawy":
                self.miejsce_dostawy
        }

        self.historia_zamowien.insert(
            0,
            zamowienie
        )

        self.historia_zamowien = (
            self.historia_zamowien[:10]
        )

        self.numer_zamowienia += 1

        self.zapisz_dane()

        self.ekran_zamowienia(
            zamowienie
        )

    # ========================================================
    # EKRAN KOŃCOWY
    # ========================================================

    def ekran_zamowienia(
        self,
        zamowienie
    ):

        self.clear()

        self.topbar()

        center = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        center.pack(
            fill="both",
            expand=True,
            padx=80,
            pady=60
        )

        ctk.CTkLabel(
            center,
            text="✓",
            width=100,
            height=100,
            corner_radius=50,
            fg_color=self.GREEN,
            text_color="white",
            font=ctk.CTkFont(
                size=52,
                weight="bold"
            )
        ).pack(
            pady=(30, 15)
        )

        ctk.CTkLabel(
            center,
            text="Zamówienie przyjęte!",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        ).pack()

        ctk.CTkLabel(
            center,
            text="Dziękujemy za zamówienie ❤️",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=15
            )
        ).pack(
            pady=(6, 15)
        )

        ctk.CTkLabel(
            center,
            text=f"📍 Dostawa: {zamowienie.get('miejsce_dostawy', '')}",
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            pady=(0, 20)
        )

        id_box = ctk.CTkFrame(
            center,
            fg_color=self.PANEL,
            corner_radius=25,
            border_width=2,
            border_color=self.BLUE
        )

        id_box.pack(
            ipadx=45,
            ipady=20
        )

        ctk.CTkLabel(
            id_box,
            text="ID TWOJEGO ZAMÓWIENIA",
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            pady=(10, 4)
        )

        ctk.CTkLabel(
            id_box,
            text=zamowienie["id"],
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            pady=(0, 10)
        )

        ctk.CTkLabel(
            id_box,
            text=(
                "Zachowaj to ID, jeśli chcesz "
                "zidentyfikować swoje zamówienie."
            ),
            text_color=self.MUTED
        ).pack(
            pady=(0, 10)
        )

        ctk.CTkButton(
            center,
            text="Wróć do menu",
            width=220,
            height=52,
            corner_radius=15,
            fg_color=self.BLUE,
            hover_color=self.BLUE_HOVER,
            text_color="#001018",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.menu_glowne
        ).pack(
            pady=30
        )

    # ========================================================
    # GOTOWE KANAPKI
    # ========================================================

    def menu_gotowych(self):

        self.clear()

        self.topbar()

        main = self.content_layout(
            show_order=False
        )

        self.page_title(
            main,
            "MENU",
            "Gotowe kanapki",
            "Wybierz jedną z gotowych propozycji."
        )

        area = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        area.pack(
            fill="both",
            expand=True,
            pady=15
        )

        if not self.gotowe_kanapki:

            ctk.CTkLabel(
                area,
                text="🥪\n\nBrak gotowych kanapek.",
                text_color=self.MUTED,
                font=ctk.CTkFont(
                    size=18
                ),
                justify="center"
            ).pack(
                pady=100
            )

        for kanapka in self.gotowe_kanapki:

            card = ctk.CTkFrame(
                area,
                fg_color=self.CARD,
                corner_radius=20,
                border_width=1,
                border_color=self.BORDER
            )

            card.pack(
                fill="x",
                pady=7
            )

            ctk.CTkLabel(
                card,
                text="🥪",
                font=ctk.CTkFont(
                    size=42
                )
            ).pack(
                side="left",
                padx=20,
                pady=15
            )

            info = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            info.pack(
                side="left",
                fill="x",
                expand=True
            )

            ctk.CTkLabel(
                info,
                text=kanapka.get(
                    "nazwa",
                    "Bez nazwy"
                ),
                font=ctk.CTkFont(
                    size=17,
                    weight="bold"
                )
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                info,
                text=(
                    "ID: "
                    + kanapka.get(
                        "id",
                        "BRAK"
                    )
                ),
                text_color=self.BLUE,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                info,
                text=(
                    f"{kanapka.get('typ', '')} • "
                    f"{kanapka.get('pieczywo', '')}"
                ),
                text_color=self.MUTED
            ).pack(
                anchor="w"
            )

            ctk.CTkButton(
                card,
                text="Wybierz",
                width=120,
                height=40,
                corner_radius=12,
                fg_color=self.GREEN,
                hover_color=self.GREEN_HOVER,
                command=lambda k=kanapka:
                    self.wybierz_gotowa(k)
            ).pack(
                side="right",
                padx=20
            )

        ctk.CTkButton(
            main,
            text="← Wróć",
            width=140,
            height=45,
            command=self.menu_glowne
        ).pack(
            pady=10
        )

    # ========================================================
    # WYBÓR GOTOWEJ
    # ========================================================

    def wybierz_gotowa(
        self,
        kanapka
    ):

        self.reset_zamowienie()

        self.typ = kanapka.get(
            "typ",
            ""
        )

        self.pieczywo = kanapka.get(
            "pieczywo",
            ""
        )

        self.skladniki = {
            x: True
            for x in kanapka.get(
                "skladniki",
                []
            )
        }

        self.warzywa = {
            x: True
            for x in kanapka.get(
                "warzywa",
                []
            )
        }

        self.napoje = {
            x: True
            for x in kanapka.get(
                "napoje",
                []
            )
        }

        self.wczytane_id_kanapki = (
            kanapka.get("id")
        )

        self.etap6()

    # ========================================================
    # GET SELECTED
    # ========================================================

    def get_selected(
        self,
        dictionary
    ):

        return [
            nazwa
            for nazwa, wybrane
            in dictionary.items()
            if wybrane
        ]

    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    def admin_login(self):

        dialog = ctk.CTkInputDialog(
            text="Podaj kod administratora:",
            title="Panel administratora"
        )

        code = dialog.get_input()

        if code == self.ADMIN_CODE:

            self.admin_panel()

        elif code:

            messagebox.showerror(
                "Błąd",
                "Nieprawidłowy kod administratora."
            )

    # ========================================================
    # ADMIN PANEL
    # ========================================================

    def admin_panel(self):

        self.clear()

        self.topbar()

        main = self.content_layout(
            show_order=False
        )

        self.page_title(
            main,
            "ADMINISTRATOR",
            "Panel administratora",
            "Zarządzaj produktami, miejscami dostawy, gotowymi kanapkami i zamówieniami."
        )

        stats = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            pady=(20, 15)
        )

        for i in range(3):

            stats.grid_columnconfigure(
                i,
                weight=1
            )

        self.stat_card(
            stats,
            0,
            "📦",
            "Kategorie",
            str(len(self.produkty))
        )

        self.stat_card(
            stats,
            1,
            "🥪",
            "Gotowe kanapki",
            str(len(self.gotowe_kanapki))
        )

        self.stat_card(
            stats,
            2,
            "🧾",
            "Ostatnie zamówienia",
            str(len(self.historia_zamowien))
        )

        scroll = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        scroll.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            scroll,
            text="📦 Zarządzanie produktami",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(10, 8)
        )

        options = [

            (
                "🥖",
                "Typy pieczywa",
                "typy"
            ),

            (
                "🥯",
                "Bułki",
                "bulki"
            ),

            (
                "🍞",
                "Chleby",
                "chleby"
            ),

            (
                "🥐",
                "Rogale",
                "rogale"
            ),

            (
                "🥩",
                "Składniki",
                "skladniki"
            ),

            (
                "🥬",
                "Warzywa",
                "warzywa"
            ),

            (
                "🥤",
                "Napoje",
                "napoje"
            ),

            (
                "📍",
                "Miejsca dostawy",
                "miejsca_dostawy"
            )
        ]

        for icon, nazwa, key in options:

            self.admin_option(
                scroll,
                icon,
                nazwa,
                "Dodaj, usuń lub zmień dostępność",
                lambda k=key, n=nazwa:
                    self.admin_produkty(k, n)
            )

        self.admin_option(
            scroll,
            "🥪",
            "Gotowe kanapki",
            "Twórz i usuwaj gotowe kanapki",
            self.admin_gotowe
        )

        ctk.CTkLabel(
            scroll,
            text="🧾 10 ostatnich zamówień",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(30, 10)
        )

        if not self.historia_zamowien:

            empty = ctk.CTkFrame(
                scroll,
                fg_color=self.CARD,
                corner_radius=18
            )

            empty.pack(
                fill="x"
            )

            ctk.CTkLabel(
                empty,
                text="Brak zamówień.",
                text_color=self.MUTED
            ).pack(
                pady=25
            )

        else:

            for zamowienie in (
                self.historia_zamowien[:10]
            ):

                self.order_history_card(
                    scroll,
                    zamowienie
                )

        ctk.CTkButton(
            main,
            text="← Wróć do menu",
            width=170,
            height=45,
            corner_radius=13,
            fg_color=self.CARD,
            hover_color=self.CARD_HOVER,
            command=self.menu_glowne
        ).pack(
            pady=15
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def stat_card(
        self,
        parent,
        column,
        icon,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(
                size=27
            )
        ).pack(
            pady=(13, 0)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack()

        ctk.CTkLabel(
            card,
            text=title,
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            pady=(0, 13)
        )

    # ========================================================
    # ADMIN OPTION
    # ========================================================

    def admin_option(
        self,
        parent,
        icon,
        nazwa,
        opis,
        command
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=17,
            border_width=1,
            border_color=self.BORDER
        )

        frame.pack(
            fill="x",
            pady=5
        )

        ctk.CTkLabel(
            frame,
            text=icon,
            font=ctk.CTkFont(
                size=32
            )
        ).pack(
            side="left",
            padx=(18, 14),
            pady=13
        )

        info = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            info,
            text=nazwa,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text=opis,
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkButton(
            frame,
            text="Zarządzaj →",
            width=125,
            height=38,
            corner_radius=11,
            command=command
        ).pack(
            side="right",
            padx=18
        )

    # ========================================================
    # ADMIN PRODUKTY
    # ========================================================

    def admin_produkty(
        self,
        key,
        title
    ):

        self.clear()

        self.topbar()

        main = self.content_layout(
            show_order=False
        )

        self.page_title(
            main,
            "ADMINISTRATOR",
            title,
            "Dodawaj, usuwaj produkty lub ustawiaj ich dostępność."
        )

        ctk.CTkButton(
            main,
            text="＋ Dodaj",
            width=170,
            height=42,
            corner_radius=12,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            command=lambda:
                self.dodaj_produkt(
                    key,
                    title
                )
        ).pack(
            anchor="e",
            pady=(15, 10)
        )

        area = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        area.pack(
            fill="both",
            expand=True,
            pady=(5, 5)
        )

        for index, produkt in enumerate(
            self.produkty[key]
        ):

            row = ctk.CTkFrame(
                area,
                fg_color=self.CARD,
                corner_radius=16,
                border_width=1,
                border_color=self.BORDER
            )

            row.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                row,
                text=produkt["nazwa"],
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=18,
                pady=13
            )

            status = (
                "DOSTĘPNY"
                if produkt.get(
                    "dostepny",
                    True
                )
                else "BRAK"
            )

            color = (
                self.GREEN
                if produkt.get(
                    "dostepny",
                    True
                )
                else self.RED
            )

            ctk.CTkLabel(
                row,
                text=status,
                text_color=color,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=15
            )

            ctk.CTkButton(
                row,
                text="Zmień",
                width=85,
                height=35,
                command=lambda i=index:
                    self.zmien_dostepnosc(
                        key,
                        title,
                        i
                    )
            ).pack(
                side="right",
                padx=5
            )

            ctk.CTkButton(
                row,
                text="Usuń",
                width=80,
                height=35,
                fg_color=self.RED,
                hover_color=self.RED_HOVER,
                command=lambda i=index:
                    self.usun_produkt(
                        key,
                        title,
                        i
                    )
            ).pack(
                side="right",
                padx=12
            )

        if not self.produkty[key]:

            ctk.CTkLabel(
                area,
                text="Brak pozycji.",
                text_color=self.MUTED,
                font=ctk.CTkFont(
                    size=16
                )
            ).pack(
                pady=50
            )

        ctk.CTkButton(
            main,
            text="← Wróć do panelu",
            width=160,
            height=43,
            command=self.admin_panel
        ).pack(
            pady=14
        )

    # ========================================================
    # ZMIANA DOSTĘPNOŚCI
    # ========================================================

    def zmien_dostepnosc(
        self,
        key,
        title,
        index
    ):

        self.produkty[key][index]["dostepny"] = (
            not self.produkty[key][index].get(
                "dostepny",
                True
            )
        )

        self.zapisz_dane()

        self.admin_produkty(
            key,
            title
        )

    # ========================================================
    # USUWANIE PRODUKTU
    # ========================================================

    def usun_produkt(
        self,
        key,
        title,
        index
    ):

        nazwa = (
            self.produkty[key][index]["nazwa"]
        )

        if messagebox.askyesno(
            "Usuń",
            f"Czy na pewno usunąć:\n\n{nazwa}?"
        ):

            del self.produkty[key][index]

            self.zapisz_dane()

            self.admin_produkty(
                key,
                title
            )

    # ========================================================
    # DODAWANIE PRODUKTU
    # ========================================================

    def dodaj_produkt(
        self,
        key,
        title
    ):

        dialog = ctk.CTkInputDialog(
            text="Podaj nazwę:",
            title=f"Dodaj - {title}"
        )

        nazwa = dialog.get_input()

        if not nazwa:

            return

        nazwa = nazwa.strip()

        if not nazwa:

            return

        if any(
            p["nazwa"].lower()
            == nazwa.lower()
            for p in self.produkty[key]
        ):

            messagebox.showwarning(
                "Duplikat",
                "Taka pozycja już istnieje."
            )

            return

        self.produkty[key].append(
            {
                "nazwa": nazwa,
                "dostepny": True
            }
        )

        self.zapisz_dane()

        self.admin_produkty(
            key,
            title
        )

    # ========================================================
    # ADMIN GOTOWE KANAPKI
    # ========================================================

    def admin_gotowe(self):

        self.clear()

        self.topbar()

        main = self.content_layout(
            show_order=False
        )

        self.page_title(
            main,
            "ADMINISTRATOR",
            "Gotowe kanapki",
            "Tutaj możesz tworzyć gotowe kanapki od zera."
        )

        ctk.CTkButton(
            main,
            text="＋ Utwórz gotową kanapkę",
            width=240,
            height=45,
            corner_radius=12,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            command=self.formularz_gotowej
        ).pack(
            anchor="e",
            pady=(15, 10)
        )

        area = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        area.pack(
            fill="both",
            expand=True
        )

        if not self.gotowe_kanapki:

            ctk.CTkLabel(
                area,
                text=(
                    "🥪\n\n"
                    "Nie utworzono jeszcze "
                    "żadnej gotowej kanapki."
                ),
                text_color=self.MUTED,
                font=ctk.CTkFont(
                    size=17
                ),
                justify="center"
            ).pack(
                pady=80
            )

        for index, kanapka in enumerate(
            self.gotowe_kanapki
        ):

            row = ctk.CTkFrame(
                area,
                fg_color=self.CARD,
                corner_radius=18,
                border_width=1,
                border_color=self.BORDER
            )

            row.pack(
                fill="x",
                pady=6
            )

            ctk.CTkLabel(
                row,
                text="🥪",
                font=ctk.CTkFont(
                    size=32
                )
            ).pack(
                side="left",
                padx=18,
                pady=14
            )

            info = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            info.pack(
                side="left",
                fill="x",
                expand=True
            )

            ctk.CTkLabel(
                info,
                text=kanapka.get(
                    "nazwa",
                    "Bez nazwy"
                ),
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                info,
                text=(
                    "ID: "
                    + kanapka.get(
                        "id",
                        "BRAK"
                    )
                ),
                text_color=self.BLUE,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                info,
                text=(
                    f"{kanapka.get('typ', '')} • "
                    f"{kanapka.get('pieczywo', '')}"
                ),
                text_color=self.MUTED
            ).pack(
                anchor="w"
            )

            ctk.CTkButton(
                row,
                text="Usuń",
                width=80,
                height=36,
                fg_color=self.RED,
                hover_color=self.RED_HOVER,
                command=lambda i=index:
                    self.usun_gotowa(i)
            ).pack(
                side="right",
                padx=18
            )

        ctk.CTkButton(
            main,
            text="← Wróć do panelu",
            width=160,
            height=43,
            command=self.admin_panel
        ).pack(
            pady=14
        )

    # ========================================================
    # FORMULARZ GOTOWEJ KANAPKI
    # ========================================================

    def formularz_gotowej(self):

        self.clear()

        self.topbar()

        main = self.content_layout(
            show_order=False
        )

        self.page_title(
            main,
            "ADMINISTRATOR",
            "Nowa gotowa kanapka",
            "Wybierz dokładnie, co ma zawierać gotowa kanapka."
        )

        name_box = ctk.CTkFrame(
            main,
            fg_color=self.PANEL,
            corner_radius=18
        )

        name_box.pack(
            fill="x",
            pady=(20, 12)
        )

        ctk.CTkLabel(
            name_box,
            text="Nazwa kanapki",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 5)
        )

        self.admin_name_entry = ctk.CTkEntry(
            name_box,
            height=42,
            placeholder_text="np. Kanapka klasyczna",
            corner_radius=11
        )

        self.admin_name_entry.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        scroll = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            scrollbar_button_color=self.BLUE,
            scrollbar_button_hover_color=self.BLUE_HOVER
        )

        scroll.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            scroll,
            text="1. Rodzaj pieczywa",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(8, 5)
        )

        self.admin_typ_var = ctk.StringVar(
            value=""
        )

        typ_frame = ctk.CTkFrame(
            scroll,
            fg_color=self.PANEL,
            corner_radius=15
        )

        typ_frame.pack(
            fill="x"
        )

        for produkt in self.produkty["typy"]:

            if not produkt.get(
                "dostepny",
                True
            ):

                continue

            ctk.CTkRadioButton(
                typ_frame,
                text=produkt["nazwa"],
                variable=self.admin_typ_var,
                value=produkt["nazwa"]
            ).pack(
                side="left",
                padx=15,
                pady=14
            )

        ctk.CTkLabel(
            scroll,
            text="2. Konkretne pieczywo",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.admin_pieczywo_var = ctk.StringVar(
            value=""
        )

        self.admin_pieczywo_frame = ctk.CTkFrame(
            scroll,
            fg_color=self.PANEL,
            corner_radius=15
        )

        self.admin_pieczywo_frame.pack(
            fill="x"
        )

        self.admin_typ_var.trace_add(
            "write",
            self.aktualizuj_pieczywo_admin
        )

        ctk.CTkLabel(
            scroll,
            text="3. Składniki",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.admin_skladnik_vars = {}

        skladniki_frame = ctk.CTkFrame(
            scroll,
            fg_color=self.PANEL,
            corner_radius=15
        )

        skladniki_frame.pack(
            fill="x"
        )

        for produkt in self.produkty["skladniki"]:

            if not produkt.get(
                "dostepny",
                True
            ):

                continue

            nazwa = produkt["nazwa"]

            var = ctk.BooleanVar(
                value=False
            )

            self.admin_skladnik_vars[
                nazwa
            ] = var

            ctk.CTkCheckBox(
                skladniki_frame,
                text=nazwa,
                variable=var
            ).pack(
                anchor="w",
                padx=18,
                pady=7
            )

        ctk.CTkLabel(
            scroll,
            text="4. Warzywa",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.admin_warzywo_vars = {}

        warzywa_frame = ctk.CTkFrame(
            scroll,
            fg_color=self.PANEL,
            corner_radius=15
        )

        warzywa_frame.pack(
            fill="x"
        )

        for produkt in self.produkty["warzywa"]:

            if not produkt.get(
                "dostepny",
                True
            ):

                continue

            nazwa = produkt["nazwa"]

            var = ctk.BooleanVar(
                value=False
            )

            self.admin_warzywo_vars[
                nazwa
            ] = var

            ctk.CTkCheckBox(
                warzywa_frame,
                text=nazwa,
                variable=var
            ).pack(
                anchor="w",
                padx=18,
                pady=7
            )

        ctk.CTkLabel(
            scroll,
            text="5. Napoje",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.admin_napoj_vars = {}

        napoje_frame = ctk.CTkFrame(
            scroll,
            fg_color=self.PANEL,
            corner_radius=15
        )

        napoje_frame.pack(
            fill="x"
        )

        for produkt in self.produkty["napoje"]:

            if not produkt.get(
                "dostepny",
                True
            ):

                continue

            nazwa = produkt["nazwa"]

            var = ctk.BooleanVar(
                value=False
            )

            self.admin_napoj_vars[
                nazwa
            ] = var

            ctk.CTkCheckBox(
                napoje_frame,
                text=nazwa,
                variable=var
            ).pack(
                anchor="w",
                padx=18,
                pady=7
            )

        buttons = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            pady=15
        )

        ctk.CTkButton(
            buttons,
            text="← Anuluj",
            width=140,
            height=45,
            fg_color=self.CARD,
            hover_color=self.CARD_HOVER,
            command=self.admin_gotowe
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            buttons,
            text="✓ Utwórz kanapkę",
            width=190,
            height=45,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            font=ctk.CTkFont(
                weight="bold"
            ),
            command=self.zapisz_gotowa_z_formularza
        ).pack(
            side="right"
        )

    # ========================================================
    # AKTUALIZACJA PIECZYWA
    # ========================================================

    def aktualizuj_pieczywo_admin(
        self,
        *args
    ):

        for widget in (
            self.admin_pieczywo_frame.winfo_children()
        ):

            widget.destroy()

        typ = self.admin_typ_var.get()

        if typ == "Bułka":

            key = "bulki"

        elif typ == "Chleb":

            key = "chleby"

        elif typ == "Rogal":

            key = "rogale"

        else:

            return

        self.admin_pieczywo_var.set("")

        for produkt in self.produkty[key]:

            if not produkt.get(
                "dostepny",
                True
            ):

                continue

            ctk.CTkRadioButton(
                self.admin_pieczywo_frame,
                text=produkt["nazwa"],
                variable=self.admin_pieczywo_var,
                value=produkt["nazwa"]
            ).pack(
                anchor="w",
                padx=18,
                pady=7
            )

    # ========================================================
    # ZAPIS GOTOWEJ KANAPKI
    # ========================================================

    def zapisz_gotowa_z_formularza(self):

        nazwa = (
            self.admin_name_entry
            .get()
            .strip()
        )

        typ = (
            self.admin_typ_var.get()
        )

        pieczywo = (
            self.admin_pieczywo_var.get()
        )

        if not nazwa:

            messagebox.showwarning(
                "Brak nazwy",
                "Podaj nazwę gotowej kanapki."
            )

            return

        if not typ:

            messagebox.showwarning(
                "Brak pieczywa",
                "Wybierz Bułkę, Chleb lub Rogal."
            )

            return

        if not pieczywo:

            messagebox.showwarning(
                "Brak rodzaju",
                "Wybierz konkretny rodzaj pieczywa."
            )

            return

        skladniki = [
            nazwa_skladnika
            for nazwa_skladnika, var
            in self.admin_skladnik_vars.items()
            if var.get()
        ]

        if "Twaróg" in skladniki:

            konflikty = [
                x
                for x in [
                    "Szynka",
                    "Ser",
                    "Pasztet"
                ]
                if x in skladniki
            ]

            if konflikty:

                messagebox.showwarning(
                    "Nieprawidłowe składniki",
                    "Twaróg może być tylko samodzielnie."
                )

                return

        if "Pasztet" in skladniki:

            konflikty = [
                x
                for x in [
                    "Szynka",
                    "Ser",
                    "Twaróg"
                ]
                if x in skladniki
            ]

            if konflikty:

                messagebox.showwarning(
                    "Nieprawidłowe składniki",
                    "Pasztet może być tylko samodzielnie."
                )

                return

        warzywa = [
            nazwa_warzywa
            for nazwa_warzywa, var
            in self.admin_warzywo_vars.items()
            if var.get()
        ]

        napoje = [
            nazwa_napoju
            for nazwa_napoju, var
            in self.admin_napoj_vars.items()
            if var.get()
        ]

        identyfikator = (
            self.wygeneruj_id_kanapki()
        )

        kanapka = {

            "id":
                identyfikator,

            "nazwa":
                nazwa,

            "typ":
                typ,

            "pieczywo":
                pieczywo,

            "skladniki":
                skladniki,

            "warzywa":
                warzywa,

            "napoje":
                napoje
        }

        self.gotowe_kanapki.append(
            kanapka
        )

        self.zapisz_dane()

        messagebox.showinfo(
            "Gotowe! 🥪",
            f"Gotowa kanapka została utworzona.\n\n"
            f"Nazwa:\n{nazwa}\n\n"
            f"ID kanapki:\n{identyfikator}\n\n"
            f"Klient może wpisać to ID na ekranie głównym."
        )

        self.admin_gotowe()

    # ========================================================
    # USUWANIE GOTOWEJ
    # ========================================================

    def usun_gotowa(
        self,
        index
    ):

        kanapka = (
            self.gotowe_kanapki[index]
        )

        if messagebox.askyesno(
            "Usuń kanapkę",
            f"Czy na pewno usunąć:\n\n"
            f"{kanapka.get('nazwa', 'Bez nazwy')}\n"
            f"ID: {kanapka.get('id', 'BRAK')}"
        ):

            del self.gotowe_kanapki[index]

            self.zapisz_dane()

            self.admin_gotowe()

    # ========================================================
    # HISTORIA ZAMÓWIEŃ
    # ========================================================

    def order_history_card(
        self,
        parent,
        zamowienie
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER
        )

        card.pack(
            fill="x",
            pady=6
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=18,
            pady=(14, 4)
        )

        ctk.CTkLabel(
            header,
            text=(
                "🧾 "
                + zamowienie.get(
                    "id",
                    f"#{zamowienie.get('numer', '?')}"
                )
            ),
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header,
            text=zamowienie.get(
                "czas",
                ""
            ),
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            side="right"
        )

        ctk.CTkLabel(
            card,
            text=(
                f"🍞 {zamowienie.get('typ', '')} • "
                f"{zamowienie.get('pieczywo', '')}"
            ),
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 5)
        )

        dane = [

            (
                "🥩 ",
                zamowienie.get(
                    "skladniki",
                    []
                )
            ),

            (
                "🥬 ",
                zamowienie.get(
                    "warzywa",
                    []
                )
            ),

            (
                "🥤 ",
                zamowienie.get(
                    "napoje",
                    []
                )
            )
        ]

        for emoji, lista in dane:

            tekst = (
                emoji
                +
                (
                    " • ".join(lista)
                    if lista
                    else "Brak"
                )
            )

            ctk.CTkLabel(
                card,
                text=tekst,
                text_color=self.MUTED,
                font=ctk.CTkFont(
                    size=12
                ),
                justify="left",
                wraplength=900
            ).pack(
                anchor="w",
                padx=18,
                pady=2
            )

        ctk.CTkLabel(
            card,
            text=(
                "📍 Miejsce dostawy: "
                + zamowienie.get(
                    "miejsce_dostawy",
                    "Nie wybrano"
                )
            ),
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            justify="left",
            wraplength=900
        ).pack(
            anchor="w",
            padx=18,
            pady=(5, 10)
        )


# ============================================================
# START PROGRAMU
# ============================================================

if __name__ == "__main__":

    app = RestauracjaKanapkowa()

    app.mainloop()