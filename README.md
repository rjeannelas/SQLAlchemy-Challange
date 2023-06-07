# SQLAlchemy-Challange

 You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area.
 
  Do a basic climate analysis and data exploration of your climate database then perform a precipitation analysis and a station analysis.
  
      Tools to use: Python, SQLAlchemy queries, Pandas, Matplotlib
       
## Part 1: Analyze and Explore the Climate Data
  
  - With the provided files use SQLAlchemy functions to connect to your SQLite database and reflect your tables into classes, and then save references.
  - Link Python to the database by creating a SQLAlchemy session

#### Perform a precipitation analysis and then a station analysis by completing the steps into two subsections:
##### Precipitation Analysis
 - Find the most recent date in the dataset, get the previous 12 months of precipitation data by querying the previous 12 months of data
 - Select only the "date" and "prcp" values
 - Load the query results into a Pandas DataFrame -explicitly set the column names
 - Sort the DataFrame values by "date".
 - Plot the results by using the DataFrame plot method
##### Station Analysis: Design a query to calculate the total number of stations in the dataset
 - Design a query to find the most-active stations by listing the stations and observation counts in descending order

Which station id has the greatest number of observations?

 - Calculate the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query
 - Design a query to get the previous 12 months of temperature observation (TOBS) data

## Part 2: Design Your Climate App:
#### Design a Flask API based on the queries that you just developed
 - Join the station and measurement tables for some of the queries
 - Use the Flask jsonify function to convert your API data to a valid JSON response object.
