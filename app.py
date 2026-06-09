import tkinter as tk

from tkinter import filedialog
from PIL import Image, ImageTk

from search import search_image

root = tk.Tk()

root.title("Animal Search")

root.geometry("1200x700")

query_label = tk.Label(root)
query_label.pack()

result_frame = tk.Frame(root)
result_frame.pack(pady=20)

def choose_image():

    path = filedialog.askopenfilename(
        filetypes=[
            ("Image", "*.jpg *.png *.jpeg")
        ]
    )

    if not path:
        return

    img = Image.open(path)
    img.thumbnail((300, 300))

    photo = ImageTk.PhotoImage(img)

    query_label.config(image=photo)
    query_label.image = photo

    results = search_image(path)

    for widget in result_frame.winfo_children():
        widget.destroy()

    for idx, (img_path, score) in enumerate(results):

        frame = tk.Frame(result_frame)
        frame.grid(row=0, column=idx, padx=10)

        rimg = Image.open(img_path)
        rimg.thumbnail((180,180))

        rphoto = ImageTk.PhotoImage(rimg)

        lbl = tk.Label(
            frame,
            image=rphoto
        )

        lbl.image = rphoto
        lbl.pack()

        tk.Label(
            frame,
            text=f"{score:.2%}"
        ).pack()

btn = tk.Button(
    root,
    text="Chọn ảnh",
    command=choose_image
)

btn.pack(pady=10)

root.mainloop()