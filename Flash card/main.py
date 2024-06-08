BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from tkinter import messagebox
import pandas
import random
import os

file_dict={}
#............................adding TEXTS........................................
try:
    file = pandas.read_csv("left_cards.csv")
except FileNotFoundError :
    original_file = pandas.read_csv("french_words.csv")
    file_dict = original_file.to_dict(orient ="records")
else:
    file_dict=file.to_dict(orient="records")

#...........................button function............................................

selected = {}
def next_card():
    global selected,flip_timer
    screen.after_cancel(flip_timer)
    selected = random.choice(file_dict)
    french_word = selected["French"]
    flashcard.itemconfig(card_word,text= french_word,fill="black")
    flashcard.itemconfig(card_title,text="french",fill="black")
    flashcard.itemconfig(card_img, image=front_image)
    flip_timer= screen.after(3000, flip)

def flip():
    english_word = selected["English"]
    flashcard.itemconfig(card_img,image=back_image)
    flashcard.itemconfig(card_word, text=english_word,fill="white")
    flashcard.itemconfig(card_title, text="English",fill="white")

def is_known():
    if len(file_dict)>1:
        file_dict.remove(selected)
        next_card()
        left_card = pandas.DataFrame(file_dict)
        left_card.to_csv("left_cards.csv",index = False)
    else:
        messagebox.showinfo(title="There's no word to learn",
                            message="Congratulation! You've review all the words!\nGood job, keep up the good work!")
        os.remove("left_cards.csv")



#...........................GUI SETUP............................................

screen = Tk()
screen.title("Flash Crd Game")
screen.config(pady=50,padx=50,bg=BACKGROUND_COLOR)
flip_timer = screen.after(3000,flip)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image, highlightthickness=0,command=next_card)
cross_button.grid(row=1,column=0)

tick_image = PhotoImage(file="images/right.png")
tick_button = Button(image=tick_image,highlightthickness=0,command=is_known)
tick_button.grid(row=1,column=1)

front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

flashcard = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_img = flashcard.create_image(400, 263, image= front_image)
flashcard.grid(row = 0, column = 0, columnspan=2)
card_title = flashcard.create_text(400, 150, text="", fill="black", font=("Ariel", 30, "italic"))
card_word = flashcard.create_text(400, 300, text="", fill="black", font=("Ariel", 50, "bold"))

next_card()


screen.mainloop()