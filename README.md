# CFWebScraping
Simple project to learn webscraping techniques analyzing crossfit data.


This project was to help me learn how to use python to do webscraping.  Crossfit is a domain that I am particularly passionate about and interested in doing analytics on. 


3/18/2022
This first commit is analysis on the 2022 Crossfit Open.  It pulls all the data directly from the leaderboard.  Below are the columns that its setup to pull:
RANK,NAME,COUNTRY,REGION,AFFILIATE,AGE,HEIGHT,WEIGHT,POINTS,22.1 Rank,22.1 Result,22.2 Rank,22.2 Result,22.3 Rank,22.3 Result

The workouts in the header are pulled dynamically, this way if you are running this code, mid-open, it won't break or fail.  This also assumes the format is the same it
was during the open in spring 2022.

I am not sure if the html for earlier or later years are the different or the same yet.
