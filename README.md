What to Watch?

This project is a movie and TV recommendation application. It uses a Graphical User Interface (GUI) to take in movie and TV sorting parameters. The input user information is used in either a k nearest neighboring algorithm or a sorting algorithm to that generate the top ten suggested movies for the user

_GUI_

The GUI was developed using the tkinter package. The GUI window consists of 9 pages that ask for different user inputs such as genre, movie rating, movie length, etc. Once finished inputting parameters, the user clicks on the “Submit” button on the first or last page to end the program. When the GUI closes, the input parameters are stored in a list called movie_input.

_Database Building_

We used an API key to obtain data from the Imdb database using Omdb package on Python. The data was processed an split into two datasets - Movie and TV Shows using Pandas. 

_KNN Clustering_

KNN Clustering was performed using the sklearn module on Python. The movie title, genre, imdb rating and imdb votes were preprocessed, scaled and converted to a matrix. KNN clustering was then performed on this matrix to yield the top 10 most similar movies given a certain movie input.

_Specific Search_
The user can also tailor their search based on a number of parameters such as media format (tv/movie), genre, movie period, imdb rating, actor, director, runtime and title.

