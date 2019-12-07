# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 16:38:47 2019
This file creates a GUI application that allows for user input of movie
paramteres on mupltiple pages
@author: bento
"""

import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk


class Genre_Button():
    '''
    This class creates allows for the creation of a checkbutton to be put onto
    the genre page
    
    inputs: frame- the page frame that the button will be added to
            image_file - image to added too checkbutton
            text - text describing button
            font - font of text
            row - row # on genre page
            col - column # on genre page
            hg - highlight background color of button
            padx - horizantal spacing around button
            pady - vertical spacing around button
            bg - button background color
            w - width of image on button
            h - height if image on button
            cs - column span of button
            
    outputs: checkbutton added to page
    '''
    def __init__(self, frame, image_file, text, font, row, col, hg,
                 padx, pady, bg, w, h, cs):
        # resize the original input image
        image_resize(image_file, w, h)
        self.text = text
        self.image = Image.open(image_file)
        self.image = ImageTk.PhotoImage(self.image)
        # define var to store 0 or 1 for if button is checked or not
        self.var = tk.IntVar()
        # generate checkbutton
        self.gen_button = tk.Checkbutton(frame, text=text, image=self.image,
                        font=font, compound=tk.TOP, variable=self.var, 
                        highlightbackground=hg, borderwidth=2, bg=bg)
        # specify button position on page
        self.gen_button.grid(row=row, column=col, padx=padx, pady=pady,
                             columnspan=cs)


def image_resize(image, new_width, new_height):
    '''
    this function takes in an image and resizes to the specified
    width and height
    '''
    # open image as object and assign to var img
    img = Image.open(image)
    # set resize ratios based on the new width and height
    width, height = img.size
    a = width/new_width
    b = height/new_height
    # resize image based on resize ratios
    img = img.resize((int(width/a), int(height/b)))
    # save image under its original file_name
    img.save(image)



class Movie_GUI(tk.Tk):
    '''
    this class runs sets up the GUI window and stack page frames
    so that the user may move from page to page
    '''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("What to Watch")
        self.title_font = tkfont.Font(family='Helvetica', size=24,
                                      weight="bold", slant="italic")
        # page fonts
        self.gen_font = tkfont.Font(size=12)
        self.entry_font = tkfont.Font(size=12)
        self.decade_font = tkfont.Font(size=15)
        #self.attributes('-fullscreen', True)
        self.configure(background='white')
        self.start_page_font = tkfont.Font(size=15)

        # stack page frames in container and raise the frame being used
        # to the top of the stack
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFive,
                  PageSix, PageSeven, PageEight, PageNine):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''raise the page_name frame to the top
        of the container
        '''
        frame = self.frames[page_name]
        frame.tkraise()

    def close(self):
        '''
        close the GUI window
        '''
        self.destroy()


class StartPage(tk.Frame):
    '''
    this class defines the first page of the GUI and allows
    the user to visit all other pages by clicking on their page name
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Sorting Categories", bg="white",
                         font=controller.title_font)
        label.grid(row=0, column=1)
        self.configure(background='white')

        w = 40
        h = 6
        bg = "dark grey"
        sticky = None
        font = controller.start_page_font
        
        # creat button  for each page and set command to show page

        button1 = tk.Button(self, text="Movie/TV", width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageOne"))
        button1.grid(row=1, column=0, pady=30, padx=40, sticky=sticky)

        button2 = tk.Button(self, text="Genre", width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row=1, column=1, pady=20, sticky=sticky)

        button3 = tk.Button(self, text="Time Span",width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageThree"))
        button3.grid(row=1, column=2, pady=20, padx=40, sticky=sticky)

        button5 = tk.Button(self, text="Movies/TV Match", width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageFive"))
        button5.grid(row=2, column=0, pady=20, sticky=sticky)

        button6 = tk.Button(self, text="Actor Match", width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageSix"))
        button6.grid(row=2, column=1, pady=20, padx=40, sticky=sticky)

        button7 = tk.Button(self, text="Director Match", width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageSeven"))
        button7.grid(row=2, column=2, pady=20, padx=40, sticky=sticky)

        button8 = tk.Button(self, text="Rating", width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageEight"))
        button8.grid(row=3, column=0, columnspan=2, pady=20, sticky=sticky)

        button9 = tk.Button(self, text="Movie/TV Length", width=w, height=h, font=font, bg=bg,
                            command=lambda: controller.show_frame("PageNine"))
        button9.grid(row=3, column=1, columnspan=2, pady=20, padx=40, sticky=sticky)

        button10 = tk.Button(self, text="Submit", width=25, height=3, font=font, bg=bg,
                             command=controller.close)
        button10.grid(row=4, column=1, padx=10, pady=20, sticky=sticky)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)


class PageOne(tk.Frame):
    '''
    this class defines the first input page where the user checks
    a box for Movie or TV, and each box input is stored in two variables
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        label = tk.Label(self, text="Movie or TV?", font=controller.title_font, bg="white")
        label.grid(row=0, column=0, columnspan=2)
        
        bg = "dark gray"

        button = tk.Button(self, text="Back to HomePage", width=30, height=3, bg=bg,
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=0, columnspan=2)

        next_button = tk.Button(self, text="Next Page>", width=30, height=3, bg=bg,
                                command=lambda: controller.show_frame("PageTwo"))
        next_button.grid(row=2, column=1, pady=10)

        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3, bg=bg,
                           command=lambda: controller.show_frame("StartPage"))
        prev_button.grid(row=2, column=0, pady=10)
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
    '''
    This class allows the user input of genre and stores the results
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')

        bg = "dark gray"

        label = tk.Label(self, text="Genres", font=controller.title_font,
                         bg="white").grid(row=0, column=3)

        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           bg=bg, command=lambda: controller.show_frame("StartPage"))
        button.grid(row=5, column=3, pady=10)

        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageOne"))
        prev_button.grid(row=5, column=1, pady=10, columnspan=2)

        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageThree"))
        next_button.grid(row=5, column=4, pady=10, columnspan=2)

        w = 118
        h = 79
        hg = "black"
        padx = 40
        pady = 20
        bg = "white"

        global genre_var
        genre_var = [0]*27

        row = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,
               4, 4, 4, 4, 4, 4]
        col = [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6,
               0, 1, 2, 3, 4, 5]
        cs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
        genre_pic = ['Documentary', 'Short', 'Animation', 'Comedy', 'Romance',
                     'Sport', 'Action', 'News', 'Drama', 'Fantasy', 'Horror',
                     'Music', 'War', 'Crime', 'Western', 'Sci-Fi', 'Family',
                     'Adventure', 'History', 'Biography', 'Mystery',
                     'Thriller', 'Musical', 'Film Noir', 'Game Show',
                     'Talk Show', 'Reality TV']

        font = controller.gen_font

        for i in range(len(genre_var)):
            genre_var[i] = Genre_Button(self, genre_pic[i]+'.png',
                             genre_pic[i], font=font, row=row[i], col=col[i],
                                     padx=padx, pady=pady, bg=bg, w=w, h=h, hg=hg, cs=cs[i])

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


class PageThree(tk.Frame):
    '''
    This class allows the user to input a time preiod for the movies to
    be recommended
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        bg = "dark gray"
        label = tk.Label(self, text="Movie/TV Time Period", bg="white",
                         font=controller.title_font)
        label.pack(pady=20)
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           bg=bg, command=lambda: controller.show_frame("StartPage"))
        button.pack(side=tk.BOTTOM, pady=40)
        
        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageTwo"))
        prev_button.pack(side=tk.LEFT)
        
        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageFive"))
        next_button.pack(side=tk.RIGHT)

        self.time = []

        start_label = tk.Label(self, text="Start Date", font=8, bg="white")
        start_label.pack()

        self.start = tk.Entry(self, width=25, font=14)
        self.start.pack(pady=20)

        end_label = tk.Label(self, text="End Date", font=8, bg="white")
        end_label.pack()
        self.end = tk.Entry(self, width=25, font=14)
        self.end.pack(pady=20)

        submit = tk.Button(self, text='Add', command=self.show_entry,
                           font=controller.entry_font)
        submit.pack()


    def show_entry(self):
        self.time.append(self.start.get())
        self.time.append(self.end.get())
        message = tk.Message(self, text=self.start.get()+'-'+self.end.get(), font=12)
        message.pack(side=tk.LEFT, padx=20)

        self.start.delete(0, tk.END)
        self.end.delete(0, tk.END)


class PageFive(tk.Frame):
    '''
    This class allows the input of movie or TV titles that will be
    used to generate similar movies or TV shows
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        bg = "dark gray"
        label = tk.Label(self, text="Movie Match", bg="white",
                         font=controller.title_font)
        label.pack()
        label1 = tk.Label(self, text="(Enter previously watched movie titles)",
                          font=8, bg="white")
        label1.pack()

        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           bg=bg, command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=40)

        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageThree"))
        prev_button.pack(side='left')

        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageSix"))
        next_button.pack(side='right')

        self.photo = []

        self.t = tk.Entry(self, width=50, font=12)
        self.t.pack(pady=50)

        self.movies = []

        submit = tk.Button(self, text='Add', command=self.show_entry, bg=bg,
                           font=controller.entry_font)
        submit.pack()


    def show_entry(self):
        self.movies.append(self.t.get())        
        size = 120, 120
        file_name = self.t.get() + ".jpg"
        image = Image.open(file_name)
        image.thumbnail(size)

        self.photo.append(ImageTk.PhotoImage(image))

        im = tk.Button(self, text=self.t.get(), image=self.photo[-1], bg="white",
                       borderwidth=0, compound=tk.TOP)
        im.pack(side=tk.LEFT, padx=10)

        self.t.delete(0, tk.END)


class PageSix(tk.Frame):
    '''
    This class allows input of actors the user would like to see
    in the recommended movies
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        label = tk.Label(self, text="Actor Match", bg="white",
                         font=controller.title_font)
        label.pack()
        label1 = tk.Label(self, text="(Enter actor names you would like to see)",
                          bg="white", font=8)
        label1.pack()

        bg = "dark gray"

        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           bg=bg, command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=40)

        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageFive"))
        prev_button.pack(side='left')

        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageSeven"))
        next_button.pack(side='right')

        self.actors = []

        self.t = tk.Entry(self, width=50, font=12)
        self.t.pack(pady=50)

        submit = tk.Button(self, text='Add', command=self.show_entry, bg=bg,
                           font=controller.entry_font)
        submit.pack()

    def show_entry(self):
        self.actors.append(self.t.get())
        message = tk.Message(self, text=self.t.get(), bg="white", font=8)
        message.pack(side=tk.LEFT)

        self.t.delete(0, tk.END)


class PageSeven(tk.Frame):
    '''
    This class allows input of directors the user would like to see
    in the recommended movies
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        label = tk.Label(self, text="Director Match", bg="white",
                         font=controller.title_font)
        label.pack()
        label1 = tk.Label(self, text="(Enter director names you would like to see)",
                          bg="white", font=8)
        label1.pack()

        bg = "dark gray"

        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           bg=bg, command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=40)

        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3, bg=bg,
                           command=lambda: controller.show_frame("PageSix"))
        prev_button.pack(side='left')

        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageEight"))
        next_button.pack(side='right')

        self.directors = []

        self.t = tk.Entry(self, width=50, font=12)
        self.t.pack(pady=50)

        submit = tk.Button(self, text='Add', command=self.show_entry, bg=bg,
                           font=controller.entry_font)
        submit.pack()

    def show_entry(self):
        self.directors.append(self.t.get())
        message = tk.Message(self, text=self.t.get(), bg="white", font=8)
        message.pack(side=tk.LEFT)

        self.t.delete(0, tk.END)


class PageEight(tk.Frame):
    '''
    This class allows for the user to input a rating threshold
    for the movies to be recommended
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        label = tk.Label(self, text="Movie Rating", bg="white",
                         font=controller.title_font)
        label.grid(row=0, column=1)

        bg = "dark gray"
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           bg=bg, command=lambda: controller.show_frame("StartPage"))
        button.grid(row=5, column=1, pady=20)

        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageSeven"))
        prev_button.grid(row=5, column=0, pady=20)

        next_button = tk.Button(self, text="Next Page>", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageNine"))
        next_button.grid(row=5, column=2, pady=20)
        bg = "white"
        global min_rating, max_rating

        label_min = tk.Label(self, text="Set Minimum Acceptable Rating",
                             bg="white", font=9).grid(row=1, column=1)

        min_rating = tk.IntVar()
        min_scale = tk.Scale(self, from_=0, to=10, variable=min_rating, bg=bg,
                         borderwidth=0, length=610, width=25,
                             orient=tk.HORIZONTAL, font=controller.gen_font)
        min_scale.grid(row=2, column=1)

        label_max = tk.Label(self, text="Set Maximum Acceptable Rating", bg="white", font=9).grid(row=3, column=1)

        max_rating = tk.IntVar()
        max_scale = tk.Scale(self, from_=0, to=10, variable=max_rating, bg=bg, 
                         borderwidth=0, length=610, width=25,
                             orient=tk.HORIZONTAL, font=controller.gen_font)
        max_scale.grid(row=4, column=1)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)


class PageNine(tk.Frame):
    '''
    This class allows the input of a desired time length for the
    movie or TV show
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        label = tk.Label(self, text="Movie/TV Length", bg="white",
                         font=controller.title_font)
        label.grid(row=0, column=1, columnspan=2)

        bg = "dark gray"
        button = tk.Button(self, text="Back to HomePage", width=30, height=3,
                           bg=bg, command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=1, columnspan=2)

        prev_button = tk.Button(self, text="<Previous Page", width=30, height=3,
                                bg=bg, command=lambda: controller.show_frame("PageEight"))
        prev_button.grid(row=2, column=0, columnspan=2)
        
        next_button = tk.Button(self, text="Finish", width=30, height=3, bg=bg,
                           command=controller.close)
        next_button.grid(row=2, column=2, columnspan=2)
        w = 40
        h = 4
        bg = "white"
        ab = None

        global time1, time2, time3, time4

        time1 = tk.IntVar()
        t1 = tk.Checkbutton(self, text="Under 1 Hour", width=w, height=h,
                            font=controller.decade_font, bg=bg,
                                activebackground=ab, variable=time1)
        t1.grid(row=1, column=0)

        time2 = tk.IntVar()
        t2 = tk.Checkbutton(self, text="1-2 Hours", width=w, height=h,
                            font=controller.decade_font, bg=bg,
                                activebackground=ab, variable=time2)
        t2.grid(row=1, column=1)

        time3 = tk.IntVar()
        t3 = tk.Checkbutton(self, text="2-3 Hours", width=w, height=h,
                            font=controller.decade_font, bg=bg,
                                activebackground=ab, variable=time3)
        t3.grid(row=1, column=2)
        
        time4 = tk.IntVar()
        t4 = tk.Checkbutton(self, text="Over 3 Hours", width=w, height=h,
                            font=controller.decade_font, bg=bg,
                                activebackground=ab, variable=time4)
        t4.grid(row=1, column=3)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


def GUI_Movie():
    '''
    This function runs the GUI and loads its value into movie_input variable
    '''
    app = Movie_GUI()
    app.mainloop()
    genres = []
    for i in range(len(genre_var)):
        genres.append(genre_var[i].var.get())

    e_type = [movie_var.get(), TV_var.get()]

    movies = app.frames['PageFive'].movies
    actors = app.frames['PageSix'].actors
    directors = app.frames['PageSeven'].directors

    time_period = app.frames['PageThree'].time

    rating_threshold = [min_rating.get(), max_rating.get()]

    movie_length = [time1.get(), time2.get(), time3.get(), time4.get()]

    movie_input = [e_type, genres, movies, actors, directors,
                   time_period, rating_threshold, movie_length]

    return movie_input


if __name__ == "__main__":
    movie_input = GUI_Movie()
    print(movie_input)


# references: https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter




