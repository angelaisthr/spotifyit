# SPOTIFYIT
#### Video Demo:  <URL HERE>
#### Description:
Spotifyit is an application that takes a user's liked songs, and outputs it as a shareable playlist, with the title being a timestamp of when the program was used. I chose to do this for my final project as this was something I couldn't find someone already doing. The idea came up when I wanted to share my liked songs with my friends, but there was no official way to share liked songs, nor was there a website on the internet that converted the liked songs into a shareable playlist. Thus, this project was created. The app.py file contains the logistics behind the entire program, computing all calculations, and redirecting the user when needed. Styles.css provides the styles for the HTML files, and each HTML file (excluding layout.html, which provides the layout for all HTML files,) provides the design of each page that the user may be redirected to. I also made a .env file, containing the information needed to use the Spotify API. I went through several design choices, one of which was where I wanted to list out all the liked songs, but I wasn't able to find a way to implement it, and scrapped it as it wouldn't provide any functionality anyways. Another design choice that was made was to have the navigation bar only show the homepage, so the user wouldn't go to other pages when they may not have logged in yet. If they still somehow went to those pages via the URLs, redirect.html came into play and showed text saying that the user wasn't allowed, and a button that sent them back to the homepage. The entire website was fairly minimal, as users may be coming here for the sole purpose of just having a playlist, which was the whole idea, but I would like to implement a feature that showed analytics of the created playlist in the future. An important thing to note if the person reading this wants to use this program is that you will need to add a client_id and a client_secret, preferably in a .env file, as the steps needed to retrieve that information is already in app.py. You would also need to read the requirments.txt file to see all the things you need to install (with an exception of python-dotenv if you are not using .envs).
