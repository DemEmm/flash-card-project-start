import pandas as pd
import tkinter as tk

# ---------------------------- DATA LOAD ------------------------------- #

prototype_df = pd.read_csv("data/words_data.csv")

# ---------------------------- BUTTONS ------------------------------- #
word = []
user_name = "NaN"
reveal_timer = []
word_id = 0


def on_green():
    global word, reveal_timer, word_id
    print("green")

    word = prototype_df.sample(1).copy()
    if prototype_df[user_name + "Count"].min() < 3:
        while word[user_name + "Count"].squeeze() >= 3:
            word = prototype_df.sample(1).copy()
        main_wind_my.after_cancel(reveal_timer)
        # Change functionality of green_button to yes I know
        green_button.config(text="green", image=green_button_image, command=i_know)
        word_id = word.index

        bg_canvas_my.itemconfig(foreign_word_text, text=f"English")
        bg_canvas_my.itemconfig(translated_word_text, text=f"{word["Word"].squeeze()}")
        reveal_timer = main_wind_my.after(3000, reveal)
        bg_canvas_my.itemconfig(canv_image, image=image_file_front)
    else:
        bg_canvas_my.itemconfig(translated_word_text, text=f"No more available words sorry")


def on_red():
    print("Red")
    global reveal_timer
    main_wind_my.after_cancel(reveal_timer)
    on_green()


def reveal():
    global word
    green_button.config(text="green", image=green_button_image, command=on_green)
    bg_canvas_my.itemconfig(foreign_word_text, text=f"Greek")
    bg_canvas_my.itemconfig(translated_word_text, text=f"{word["Word"].squeeze()}: {word["Translation"].squeeze()}")
    bg_canvas_my.itemconfig(canv_image, image=image_file_back)


def on_submit():
    global user_name, reveal_timer
    user_name = user_name_box.get()
    if user_name != "":
        if not (user_name + "Count" in prototype_df.columns):
            prototype_df[user_name + "Count"] = 0
        reveal_timer = main_wind_my.after(3000, do_nothing)
        green_button.config(text="green", image=green_button_image, command=on_green)
        bg_canvas_my.itemconfig(foreign_word_text, text=f"Hello {user_name}")
        bg_canvas_my.itemconfig(translated_word_text, text=f"Press Green to get new word")
        print(user_name)


def i_know():
    print("yes i know")
    global word_id
    prototype_df.loc[word_id, user_name + "Count"] += 1
    prototype_df.to_csv("data/words_data.csv", index=False)
    on_green()


def do_nothing():
    print("")


# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
# main wind
main_wind_my = tk.Tk()
main_wind_my.config(bg=BACKGROUND_COLOR, pady=100, padx=100)
main_wind_my.wm_title("English Teacher")
wind_wid = 1000
wind_hei = 800
main_wind_my.wm_minsize(wind_wid, wind_hei)
main_wind_my.wm_maxsize(wind_wid, wind_hei)

# meddle page
image_file_back = tk.PhotoImage(file="./images/card_red.png")
image_file_front = tk.PhotoImage(file="./images/card_back.png")
bg_canvas_my = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canv_image = bg_canvas_my.create_image(400, 526 / 2, image=image_file_front)
bg_canvas_my.grid(row=0, column=0, columnspan=3)

foreign_word_text = bg_canvas_my.create_text(800 / 2, (526 / 2) - 30, font=('Ariel', '30', 'bold'))
translated_word_text = bg_canvas_my.create_text(800 / 2, (526 / 2) + 30, font=('Ariel', '30', 'italic'))

bg_canvas_my.itemconfig(foreign_word_text, text=f"Hello")
bg_canvas_my.itemconfig(translated_word_text, text=f"Please give me a username")
bg_canvas_my.itemconfig(canv_image, image=image_file_front)

# bot page

red_button = tk.Button()
red_button_image = tk.PhotoImage(file="images/wrong.png")
red_button.config(text="red", image=red_button_image, command=on_red)
red_button.grid(row=1, column=0)

user_name_box = tk.Entry(width=50)
user_name_box.grid(row=1, column=1)
user_name_box.focus()

green_button = tk.Button()
green_button_image = tk.PhotoImage(file="images/right.png")
green_button.grid(row=1, column=2)

green_button.config(text="green", image=green_button_image, command=on_submit)

main_wind_my.mainloop()
