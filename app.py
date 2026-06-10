import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from search import search_image
import numpy as np
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AnimalSearchApp:
    def draw_radar_chart(
            self,
            parent,
            result
    ):

        labels = np.array([
            "HSV",
            "Color",
            "LBP",
            "GLCM",
            "HOG",
            "HU"
        ])

        values = np.array([
            result["hsv"],
            result["color"],
            result["lbp"],
            result["glcm"],
            result["hog"],
            result["hu"]
        ])

        angles = np.linspace(
            0,
            2 * np.pi,
            len(labels),
            endpoint=False
        )

        values = np.concatenate(
            (
                values,
                [values[0]]
            )
        )

        angles = np.concatenate(
            (
                angles,
                [angles[0]]
            )
        )

        fig = Figure(
            figsize=(5, 5),
            dpi=100
        )

        ax = fig.add_subplot(
            111,
            polar=True
        )

        ax.plot(
            angles,
            values,
            linewidth=2
        )

        ax.fill(
            angles,
            values,
            alpha=0.25
        )

        ax.set_xticks(
            angles[:-1]
        )

        ax.set_xticklabels(
            labels
        )

        ax.set_ylim(
            0,
            1
        )

        canvas = FigureCanvasTkAgg(
            fig,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            pady=10
        )
    def __init__(self, root):

        self.root = root

        self.root.title(
            "Animal Image Retrieval System"
        )

        self.root.geometry(
            "1800x950"
        )

        self.query_path = None

        self.result_images = []

        self.detail_window = None

        self.build_ui()

    def build_ui(self):

        self.sidebar = ctk.CTkFrame(
            self.root,
            width=350
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )
        self.sidebar.pack_propagate(False)

        self.main_area = ctk.CTkScrollableFrame(
            self.root
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            self.sidebar,
            text="Animal Search",
            font=(
                "Arial",
                28,
                "bold"
            )
        )

        title.pack(
            pady=20
        )

        self.query_label = ctk.CTkLabel(
            self.sidebar,
            text="No Image",
            width=250,
            height=250
        )

        self.query_label.pack(
            pady=10
        )

        choose_btn = ctk.CTkButton(
            self.sidebar,
            text="Choose Image",
            command=self.choose_image
        )

        choose_btn.pack(
            pady=10
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Top K"
        ).pack()

        self.top_k_entry = ctk.CTkEntry(
            self.sidebar
        )

        self.top_k_entry.insert(
            0,
            "5"
        )

        self.top_k_entry.pack(
            pady=5
        )

        self.w_hsv = self.create_slider(
            "HSV",
            0.10
        )

        self.w_color = self.create_slider(
            "Color",
            0.10
        )

        self.w_lbp = self.create_slider(
            "LBP",
            0.15
        )

        self.w_glcm = self.create_slider(
            "GLCM",
            0.10
        )

        self.w_hog = self.create_slider(
            "HOG",
            0.40
        )

        self.w_hu = self.create_slider(
            "HU",
            0.15
        )

        search_btn = ctk.CTkButton(
            self.sidebar,
            text="🔍 SEARCH",
            height=50,
            width=250,
            font=(
                "Arial",
                16,
                "bold"
            ),
            command=self.search
        )

        search_btn.pack(
            pady=20,
            padx=20,
            fill="x"
        )

    def create_slider(
            self,
            text,
            value
    ):

        frame = ctk.CTkFrame(
            self.sidebar
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        top = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=5
        )

        title = ctk.CTkLabel(
            top,
            text=text
        )

        title.pack(
            side="left"
        )

        value_label = ctk.CTkLabel(
            top,
            text=f"{value:.2f}"
        )

        value_label.pack(
            side="right"
        )

        def update_value(v):
            value_label.configure(
                text=f"{float(v):.2f}"
            )

        slider = ctk.CTkSlider(
            frame,
            from_=0,
            to=1,
            command=update_value
        )

        slider.set(value)

        slider.pack(
            fill="x",
            padx=10
        )

        return slider

    def choose_image(self):

        path = filedialog.askopenfilename(
            filetypes=[
                (
                    "Image",
                    "*.jpg *.jpeg *.png"
                )
            ]
        )

        if not path:
            return

        self.query_path = path

        image = Image.open(path)

        img = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(250, 250)
        )

        self.query_label.configure(
            image=img,
            text=""
        )

        self.query_label.image = img

    def search(self):

        if not self.query_path:
            return

        for widget in self.main_area.winfo_children():
            widget.destroy()

        self.result_images.clear()

        try:

            results = search_image(

                self.query_path,

                int(
                    self.top_k_entry.get()
                ),

                self.w_hsv.get(),
                self.w_color.get(),
                self.w_lbp.get(),
                self.w_glcm.get(),
                self.w_hog.get(),
                self.w_hu.get()
            )

            for idx, result in enumerate(results):

                self.create_result_card(
                    idx,
                    result
                )

        except Exception as e:

            print(
                "SEARCH ERROR:",
                e
            )

    def create_result_card(
        self,
        idx,
        result
    ):

        row = idx // 3
        col = idx % 3

        card = ctk.CTkFrame(
            self.main_area
        )

        card.grid(
            row=row,
            column=col,
            padx=15,
            pady=15
        )

        try:

            image = Image.open(
                result["file"]
            )

            img = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(220,220)
            )

            self.result_images.append(
                img
            )

            img_label = ctk.CTkLabel(
                card,
                image=img,
                text=""
            )

            img_label.pack(
                pady=10
            )

        except Exception as e:

            print(e)

        ctk.CTkLabel(
            card,
            text=result["animal"].upper(),
            font=(
                "Arial",
                18,
                "bold"
            )
        ).pack()

        ctk.CTkLabel(
            card,
            text=f"Similarity: {result['score']:.4f}"
        ).pack()

        detail_btn = ctk.CTkButton(
            card,
            text="View Detail",
            command=lambda r=result:
            self.show_detail(r)
        )

        detail_btn.pack(
            pady=10
        )

    def show_detail(self, result):

        try:

            if (
                    self.detail_window
                    and
                    self.detail_window.winfo_exists()
            ):
                self.detail_window.destroy()

            self.detail_window = ctk.CTkToplevel(
                self.root
            )

            win = self.detail_window

            win.title(
                f"Feature Analysis - {result['animal']}"
            )

            win.geometry(
                "1400x850"
            )

            # =========================
            # Main Frame
            # =========================

            container = ctk.CTkFrame(
                win
            )

            container.pack(
                fill="both",
                expand=True,
                padx=15,
                pady=15
            )

            # =========================
            # LEFT
            # =========================

            left = ctk.CTkFrame(
                container
            )

            left.pack(
                side="left",
                fill="y",
                padx=10
            )

            ctk.CTkLabel(
                left,
                text="Query Image",
                font=("Arial", 18, "bold")
            ).pack(pady=10)

            query_img = ctk.CTkImage(
                Image.open(self.query_path),
                size=(300, 300)
            )

            query_lbl = ctk.CTkLabel(
                left,
                image=query_img,
                text=""
            )

            query_lbl.image = query_img
            query_lbl.pack()

            ctk.CTkLabel(
                left,
                text="Matched Image",
                font=("Arial", 18, "bold")
            ).pack(pady=10)

            result_img = ctk.CTkImage(
                Image.open(result["file"]),
                size=(300, 300)
            )

            result_lbl = ctk.CTkLabel(
                left,
                image=result_img,
                text=""
            )

            result_lbl.image = result_img
            result_lbl.pack()

            # =========================
            # RIGHT
            # =========================

            right = ctk.CTkFrame(
                container
            )

            right.pack(
                side="right",
                fill="both",
                expand=True,
                padx=10
            )

            ctk.CTkLabel(
                right,
                text="Feature Similarity Analysis",
                font=("Arial", 22, "bold")
            ).pack(
                pady=10
            )

            self.draw_radar_chart(
                right,
                result
            )

            textbox = ctk.CTkTextbox(
                right,
                width=700,
                height=300
            )

            textbox.pack(
                pady=20
            )

            textbox.insert(
                "end",
                f"""
    FILE
    ---------------------------------------
    {result['file']}

    ANIMAL
    ---------------------------------------
    {result['animal']}

    FINAL SCORE
    ---------------------------------------
    {result['score']:.4f}

    FEATURE BREAKDOWN
    ---------------------------------------
    HSV Histogram      : {result['hsv']:.4f}

    Color Moments      : {result['color']:.4f}

    Local Binary Pattern
    (LBP)              : {result['lbp']:.4f}

    GLCM Texture       : {result['glcm']:.4f}

    Histogram of
    Oriented Gradient
    (HOG)              : {result['hog']:.4f}

    Hu Moments         : {result['hu']:.4f}
    """
            )

            textbox.configure(
                state="disabled"
            )

        except Exception as e:

            print(
                "DETAIL ERROR:",
                e
            )

    def draw_chart(
        self,
        parent,
        result
    ):

        fig = Figure(
            figsize=(6,4),
            dpi=100
        )

        ax = fig.add_subplot(
            111
        )

        labels = [
            "HSV",
            "Color",
            "LBP",
            "GLCM",
            "HOG",
            "HU"
        ]

        values = [

            result["hsv"],
            result["color"],
            result["lbp"],
            result["glcm"],
            result["hog"],
            result["hu"]
        ]

        ax.bar(
            labels,
            values
        )

        ax.set_ylim(
            0,
            1
        )

        ax.set_title(
            "Feature Contribution"
        )

        canvas = FigureCanvasTkAgg(
            fig,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            pady=10
        )


if __name__ == "__main__":

    root = ctk.CTk()

    app = AnimalSearchApp(
        root
    )

    root.mainloop()