from tkinter import *
from tkinter import messagebox
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
timer = None
random_word_pair = {}

#Flash Card Words
try:
    with open("data/words_to_learn.csv") as file:
        all_words_data = pandas.read_csv(file)
except FileNotFoundError:
    with open("data/french_words.csv") as file:
        all_words_data = pandas.read_csv(file)
except pandas.errors.EmptyDataError:
    messagebox.showinfo(title="No More Flashcards", message="All flashcards answered correctly! "
                                                            "\nClose the program to refresh all flashcards.")


translation_dict_list = all_words_data.to_dict(orient="records")


def next_card():
    global random_word_pair, flip_timer
    window.after_cancel(flip_timer)
    random_word_pair = random.choice(translation_dict_list)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=random_word_pair["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global random_word_pair
    global timer
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=random_word_pair["English"], fill="white")


def correct_answer():
    global random_word_pair, translation_dict_list
    translation_dict_list.remove(random_word_pair)

    if len(translation_dict_list) == 0:
        messagebox.showinfo(title="No More Flashcards", message="All flashcards answered correctly! "
                                                            "\nClose the program to refresh all flashcards.")
        os.remove("data/words_to_learn.csv")
    else:
        df = pandas.DataFrame(translation_dict_list)
        df.to_csv("data/words_to_learn.csv", index=False)
        next_card()



#Main window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

#Flash Card Image
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
language_text = canvas.create_text(400, 150, text="Title", fill="black", font=("Ariel", 30, "italic"))
word_text = canvas.create_text(400, 253, text="Word", fill="black", font=("Ariel", 45, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

#Right/Wrong buttons
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=correct_answer)
right_button.grid(column=1, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()
print(random_word_pair)
window.mainloop()
