# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 16:38:47 2019

@author: bento
"""
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk


class Genre_Button():
    def __init__(self, frame, image_file, text, font, row, col,
                 padx, pady, bg, w, h):
        image_resize(image_file, w, h)
        self.text = text
        self.image = Image.open(image_file)
        self.image = ImageTk.PhotoImage(self.image)
        self.var = tk.IntVar()
        self.gen_button = tk.Checkbutton(frame, text=text, image=self.image,
                        font=font, compound=tk.TOP, variable=self.var,
                            bg=bg).grid(row=row, column=col, padx=padx, pady=pady)


def image_resize(image, new_width, new_height):
    try:
        img = Image.open(image)
        width, height = img.size
        a = width/new_width
        b = height/new_height

        img = img.resize((int(width/a), int(height/b)))

        img.save(image)
    except IOError:
        pass


class Movie_GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("What to Watch")
        self.title_font = tkfont.Font(family='Helvetica', size=24,
                                      weight="bold", slant="italic")
        self.gen_font = tkfont.Font(size=12)
        self.entry_font = tkfont.Font(size=12)
        self.decade_font = tkfont.Font(size=15)
        self.attributes('-fullscreen', True)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive,
                  PageSix, PageSeven, PageEight, PageNine):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def close(self):
        self.destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Sorting Categories",
                         font=controller.title_font)
        label.grid(row=0, column=1)

        w = 60
        h = 9
        af = 'blue'
        sticky = None

        button1 = tk.Button(self, text="Movie/TV", width=w, height=h,
                            command=lambda: controller.show_frame("PageOne"))
        button1.grid(row=1, column=0, pady=30, padx=40, sticky=sticky)

        button2 = tk.Button(self, text="Genre", width=w, height=h,
                            command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row=1, column=1, pady=20, sticky=sticky)

        button3 = tk.Button(self, text="Movie Time Period",width=w, height=h,
                            command=lambda: controller.show_frame("PageThree"))
        button3.grid(row=1, column=2, pady=20, padx=40, sticky=sticky)

        button4 = tk.Button(self, text="Movie Mood", width=w, height=h,
                            command=lambda: controller.show_frame("PageFour"))
        button4.grid(row=2, column=0, pady=20, padx=40, sticky=sticky)

        button5 = tk.Button(self, text="Movie Input", width=w, height=h,
                            command=lambda: controller.show_frame("PageFive"))
        button5.grid(row=2, column=1, pady=20, sticky=sticky)

        button6 = tk.Button(self, text="Actor", width=w, height=h,
                            command=lambda: controller.show_frame("PageSix"))
        button6.grid(row=2, column=2, pady=20, padx=40, sticky=sticky)

        button7 = tk.Button(self, text="Director", width=w, height=h,
                            command=lambda: controller.show_frame("PageSeven"))
        button7.grid(row=3, column=0, pady=20, padx=40, sticky=sticky)

        button8 = tk.Button(self, text="Rating", width=w, height=h,
                            command=lambda: controller.show_frame("PageEight"))
        button8.grid(row=3, column=1, pady=20, padx=40, sticky=sticky)

        button9 = tk.Button(self, text="Movie Length", width=w, height=h,
                            command=lambda: controller.show_frame("PageNine"))
        button9.grid(row=3, column=2, pady=20, padx=40, sticky=sticky)

        button10 = tk.Button(self, text="Submit", width=25, height=3,
                             command=controller.close)
        button10.grid(row=4, column=1, padx=10, pady=20, sticky=sticky)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Movie or TV?", font=controller.title_font)
        label.grid(row=0, column=0, columnspan=2)

        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=0, columnspan=2)

        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                command=lambda: controller.show_frame("PageTwo"))
        next_button.grid(row=2, column=1, pady=10)

        w = 380
        h = 300

        image_resize("Movie.jpg", w, h)
        movie_image = Image.open("Movie.jpg")
        self.moviephoto = ImageTk.PhotoImage(movie_image)

        bg = 'white'
        global movie_var, TV_var
        movie_var = tk.IntVar()
        movie = tk.Checkbutton(self, text='Movie', variable=movie_var,
                               image=self.moviephoto, padx=35, bg=bg, borderwidth=2)
        movie.grid(row=1, column=0, padx=20, pady=10)

        image_resize("TV.png", w, h)
        TVimage = Image.open("TV.png")
        self.TVphoto = ImageTk.PhotoImage(TVimage)

        TV_var = tk.IntVar()
        tv = tk.Checkbutton(self, text='TV', variable=TV_var,
                            image=self.TVphoto, padx=35, bg=bg, borderwidth=2)
        tv.grid(row=1, column=1, padx=20, pady=10)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Genres", font=controller.title_font)
        label.grid(row=0, column=3)

        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=5, column=3, pady=10)
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                                command=lambda: controller.show_frame("PageOne"))
        prev_button.grid(row=5, column=2, pady=10)

        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                command=lambda: controller.show_frame("PageThree"))
        next_button.grid(row=5, column=4, pady=10)

        w = 118
        h = 79
        bg = "grey"
        sticky = None
        padx = 40
        pady = 20

        global genre_var
        genre_var = [0]*28

        row = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,
               4, 4, 4, 4, 4, 4, 4]
        col = [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6,
               0, 1, 2, 3, 4, 5, 6]
        genre_pic = ['Documentary', 'Short', 'Animation', 'Comedy', 'Romance',
                     'Sport', 'Action', 'News', 'Drama', 'Fantasy', 'Horror',
                     'Music', 'War', 'Crime', 'Western', 'Sci-Fi', 'Family',
                     'Adventure', 'History', 'Biography', 'Mystery',
                     'Thriller', 'Musical', 'Film Noir', 'Game Show',
                     'Talk Show', 'Reality TV', 'Adult']

        font = controller.gen_font

        for i in range(len(genre_var)):
            genre_var[i] = Genre_Button(self, genre_pic[i]+'.png',
                             genre_pic[i], font=font, row=row[i], col=col[i],
                                     padx=padx, pady=pady, bg=bg, w=w, h=h)

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Movie Time Period",
                         font=controller.title_font)
        label.pack(pady=20)
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side=tk.BOTTOM)
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                           command=lambda: controller.show_frame("PageTwo"))
        prev_button.pack(side=tk.LEFT)
        
        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                           command=lambda: controller.show_frame("PageFour"))
        next_button.pack(side=tk.RIGHT)        
        self.time = []
        
        start_label = tk.Label(self, text="Start Date", font=8)
        start_label.pack()
        
        self.start = tk.Entry(self, width=25, font=14)
        self.start.pack(pady=20)
       
        end_label = tk.Label(self, text="End Date", font=8)
        end_label.pack()
        self.end = tk.Entry(self, width=25, font=14)
        self.end.pack(pady=20)
        
        submit = tk.Button(self, text='Add', command=self.show_entry, font=controller.entry_font)
        submit.pack()
        

    
    def show_entry(self):
        self.time.append((self.start.get(), self.end.get()))
        message = tk.Message(self, text=self.start.get()+'-'+self.end.get(), font=12)
        message.pack(side=tk.LEFT, padx=20)
      
        
        self.start.delete(0, tk.END)
        self.end.delete(0, tk.END)
        
class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Movie Mood", font=controller.title_font).grid(row=0, column=1)
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage")).grid(row=2, column=1)
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                           command=lambda: controller.show_frame("PageThree")).grid(row=2, column=0)
        
        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                           command=lambda: controller.show_frame("PageFive")).grid(row=2, column=2)
        
        
        
        bg="light grey"
        size = 100, 100
        sad_image = Image.open("sad.png")
        sad_image.thumbnail(size)
        self.sad_photo = ImageTk.PhotoImage(sad_image)
        
        sad_im = tk.Button(self, image=self.sad_photo, borderwidth=0, bg=bg).grid(row=1, column=0)
        
        happy_image = Image.open("happy.png")
        happy_image.thumbnail(size)
        self.happy_photo = ImageTk.PhotoImage(happy_image)
        
        happy_im = tk.Button(self, image=self.happy_photo, borderwidth=0, bg=bg).grid(row=1, column=2)
        
        global sentiment
        
        sentiment = tk.IntVar()
        scale = tk.Scale(self, from_=0, to=10, variable=sentiment, bg=bg, 
                         borderwidth=0, length=610, width=25, orient=tk.HORIZONTAL, font=controller.gen_font).grid(row=1, column=1)
        
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        
        
        
class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Similar Movies", font=controller.title_font)
        label.pack()
        label1 = tk.Label(self, text="(Enter previously watched movie titles)", font=8)
        label1.pack()
        
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom")
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                           command=lambda: controller.show_frame("PageFour"))
        prev_button.pack(side='left')
        
        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                           command=lambda: controller.show_frame("PageSix"))
        next_button.pack(side='right')
        
        
        self.photo = []
        
        self.t = tk.Entry(self, width=50, font=12)
        self.t.pack(pady=50)
        
        
        self.movies = []
        
        submit = tk.Button(self, text='Add', command=self.show_entry, font=controller.entry_font)
        submit.pack()

    
    def show_entry(self):
        self.movies.append(self.t.get())
        #entry_font = tkFont.Font(size=9)
        #message = tk.Message(self.root, text=self.t.get(), font=entry_font)
        #message.pack(side=tk.RIGHT)
        
        size = 100, 100
        file_name = self.t.get() + ".jpg"
        image = Image.open(file_name)
        image.thumbnail(size)
        
        self.photo.append(ImageTk.PhotoImage(image))
        
        im = tk.Button(self, text=self.t.get(), image=self.photo[-1], borderwidth=0, compound=tk.TOP)
        im.pack(side=tk.RIGHT, padx=10)
        
        
        self.t.delete(0, tk.END)
        
        
class PageSix(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Actor", font=controller.title_font)
        label.pack()
        label1 = tk.Label(self, text="(Enter actor names you would like to see)", font=8)
        label1.pack()
        
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom")
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                           command=lambda: controller.show_frame("PageFive"))
        prev_button.pack(side='left')
        
        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                           command=lambda: controller.show_frame("PageSeven"))
        next_button.pack(side='right')
        
        self.actors = []
        
        self.t = tk.Entry(self, width=50, font=12)
        self.t.pack(pady=50)
        
        
        submit = tk.Button(self, text='Add', command=self.show_entry, font=controller.entry_font)
        submit.pack()

    
    def show_entry(self):
        self.actors.append(self.t.get())
        message = tk.Message(self, text=self.t.get())
        message.pack(side=tk.RIGHT)
        
   
        
        self.t.delete(0, tk.END)
        
class PageSeven(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Director", font=controller.title_font)
        label.pack()
        label1 = tk.Label(self, text="(Enter director names you would like to see)", font=8)
        label1.pack()
        
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom")
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                           command=lambda: controller.show_frame("PageSix"))
        prev_button.pack(side='left')
        
        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                           command=lambda: controller.show_frame("PageEight"))
        next_button.pack(side='right')
        
        self.directors = []
        
        self.t = tk.Entry(self, width=50, font=12)
        self.t.pack(pady=50)
        
        
        submit = tk.Button(self, text='Add', command=self.show_entry, font=controller.entry_font)
        submit.pack()

    
    def show_entry(self):
        self.directors.append(self.t.get())
        message = tk.Message(self, text=self.t.get())
        message.pack(side=tk.RIGHT)
        
   
        
        self.t.delete(0, tk.END)
        
class PageEight(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Movie Rating", font=controller.title_font).grid(row=0, column=1)
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage")).grid(row=5, column=1)
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                           command=lambda: controller.show_frame("PageSeven")).grid(row=5, column=0)
        
        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                           command=lambda: controller.show_frame("PageNine")).grid(row=5, column=2)
        bg=None
        global min_rating, max_rating
        
        label_min = tk.Label(self, text="Set Minimum Acceptable Rating", font=9).grid(row=1, column=1)

        min_rating = tk.IntVar()
        min_scale = tk.Scale(self, from_=0, to=10, variable=min_rating, bg=bg, 
                         borderwidth=0, length=610, width=25, orient=tk.HORIZONTAL, font=controller.gen_font).grid(row=2, column=1)
        
        label_max = tk.Label(self, text="Set Maximum Acceptable Rating", font=9).grid(row=3, column=1)
    
        max_rating = tk.IntVar()
        max_scale = tk.Scale(self, from_=0, to=10, variable=max_rating, bg=bg, 
                         borderwidth=0, length=610, width=25, orient=tk.HORIZONTAL, font=controller.gen_font).grid(row=4, column=1)
        
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)
    
    
    
class PageNine(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Movie Length", font=controller.title_font).grid(row=0, column=1)
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           command=lambda: controller.show_frame("StartPage")).grid(row=2, column=1)
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                           command=lambda: controller.show_frame("PageEight")).grid(row=2, column=0)
        
        next_button = tk.Button(self, text="Finish", width=30, height=3,
                           command=controller.close).grid(row=2, column=2)
        w=40
        h=4
        bg=None
        ab=None
        
        global time1, time2, time3
        
        time1 = tk.IntVar()
        t1 = tk.Checkbutton(self, text="Under 90 min", width=w, height=h, font=controller.decade_font, bg=bg, activebackground=ab,
                                       variable=time1).grid(row=1, column=0)
        
        time2 = tk.IntVar()
        t2 = tk.Checkbutton(self, text="90-150 min", width=w, height=h, font=controller.decade_font, bg=bg, activebackground=ab,
                                       variable=time2).grid(row=1, column=1)
        
        time3 = tk.IntVar()
        t3 = tk.Checkbutton(self, text="Over 150 min", width=w, height=h, font=controller.decade_font, bg=bg, activebackground=ab,
                                       variable=time3).grid(row=1, column=2)
        
        
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        
def GUI_Movie():
    app = Movie_GUI()
    app.mainloop()
    genres = []
    for i in range(len(genre_var)):
        genres.append((genre_var[i].text, genre_var[i].var.get()))
        
    e_type = {'Movie': movie_var.get(), 'TV': TV_var.get()}

    sent_num = sentiment.get()
    #decades = {'Pre-1950s': d.get(), '1950s': d1.get(), '1960s': d2.get(),
               #'1970s': d3.get(), '1980s': d4.get(), '1990s': d5.get(), '2000s': d6.get(), '2010s': d7.get()}
    
    movies = app.frames['PageFive'].movies
    actors = app.frames['PageSix'].actors
    directors = app.frames['PageSeven'].directors

    time_period = app.frames['PageThree'].time
    
    rating_threshold = {'Min Threshold': min_rating.get(), 'Max Threshold': max_rating.get()}

    movie_length = {'Under 90 min': time1.get(), '90-150 min': time2.get(), 'Over 150 min': time3.get()}
    
    return e_type, genres, sent_num, time_period, movies, actors, directors, rating_threshold, movie_length

 


if __name__ == "__main__":
    e_type, genres, sent_num, time_period, movies, actors, directors, rating_threshold, movie_length = GUI_Movie()
    print(e_type, genres, sent_num, time_period, movies, actors, directors, rating_threshold, movie_length)
    
    








