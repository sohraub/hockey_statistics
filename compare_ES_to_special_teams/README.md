# Introduction

The purpose of the scripts in this folder will be to determine the relationship between player performance at
Even-Strength vs player performance on the Power Play and on the Penalty Kill. This will be accomplished by comparing,
for each player we have data for, the Even-Strength xGF/xGA rates to their PP xGF/SH xGA, respectively, where
applicable.

The metrics I will be using to compare performance are the RAPM xGF/xGA values from evolving-hockey. Thus all data
has been downloaded from www.evolving-hockey.com. I have downloaded every player season since 2009, with a
500 minute cutoff for ES and 100 minute cutoff for special teams, per season.

# Methodology

For every player season that passes the TOI cutoffs outlined above, I will calculate the percentiles of xGF/xGA RAPM at
ES, and compare these to the percentiles for PP xGF/SG xGA. I would expect the relationship between the two to be quite
linear, but I am curious to what degree and which players show the biggest discrepancies between their ES and special
teams results.at
