# Loyalty Lines

In an age of political contention, having transparent and accessible political data is essential to hold Members of the European Parliament accountable regarding their voting actions. Our application aims to visualize MEP party loyalty, identify frequent dissenters, and provide recommendations for party changes and civilian votes.

Due to the high volume of votes that Parliament holds, it can be difficult for both party leaders and members to keep track of cohesion within the group. Currently, there is no interactive system that visualizes and predicts MEP voting patterns and party loyalties.

Our application will provide an interface to view how cohesive a given political party is based on the percentage of MEPs within the party that vote together. It will visualize the hemicycle through the lens of party loyalty and also provide information for the MEPs themselves, specifically by computing a loyalty score for each. This will allow the application to predict future party changes, offer potential recommendations for party changes, and corroborate rhetoric with actual votes. It can also inform citizens how closely their MEP is in alignment with their party’s values so they can make an informed decision on whether to vote for that person again.

With our app, we hope to streamline MEP data by providing clear insights for our user personas. By creating interactive visualizations, predictions, and loyalty scores, we hope to increase transparency and civic engagement across the EU.


## In-Depth UI Breakdown

### Party Leader

The party leader has access to two functionality screens, **Party Recqruitment** and **Party Cohesion** 

#### Party Recruitment
- This screen makes user of our recommender model to inform the party leader of MEP's that statistically vote alongside their party frequently. 

#### Party Cohesion
- This screen provides the party leader with an in depth look into their own party's cohesion. Specifically they can see their party's cohesion over time, as well as compare their party to others. 

### Political Journalist

