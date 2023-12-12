# World Cup Best-XI Selection with ML

- This project is an attempt to use regression to predict the best XI players for the 2023 Cricket World Cup given a team and an opponent. 
- The data used for this project is ODI records of players from 2023 Cricket World Cup. 
- The data was gathered from [ESPN Cricinfo](https://www.espncricinfo.com/) using web scraping.

## Problem Statements

- How many runs will a `player` score against a particular `opposition` in a `venue`.
- What will be the economy of a `player` against an `opposition` in a `venue`.
- In the next match, how will a `player` get out (Caught behind, stumped, run out ... etc) against an `opposition` in a `venue`.
- Given a new domestic player will he be a X-Factor Bowler like Bumrah, Cummins, Strong middle-order batsman like Shreyas Iyer, K L Rahul or an explosive all rounder like Maxwell or a top class batsman like Kohli.

## Where to Start

- The `final_data` folder contains the data used for this project.
- The `predicting_runs.ipynb`, `predicting_economy.ipynb` and `predicting_Dismissal.ipynb` notebooks contain the ML models used for predicting runs, economy and predicting dismissal respectively.
- The `clustering_players.ipynb` contains the code to cluster the players into 4 groups, X-Factor Bowlers, Strong Middle Order and Wicket Keeping batsmen, Explosive All Rounders and Top Class Batsmen.
- The `post_clustering.ipynb` contains the code that classifies a new player into one of the clusters from above!

## Team

| Team |
| ---- |
|`Ashwin Narayanan S`|
|`Sreepadh`|
|`Ananya R`|
|`Arjun P`|
|`Kona Deepak`|
