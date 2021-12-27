# ship_scraper

The Oceanic Steam Navigation Company—better known as the White Star Line (WSL)—was one of the premier British shipping companies, transporting passengers and cargo for almost a century (1845-1934). Made infamous in popular culture by the loss of the RMS <i>Titanic</i> in 1912—which was, in fact, only one of several disasters that the line suffered in the late nineteenth and early twentieth centuries—the company nevertheless prided itself on providing high-quality service to its passengers, and its towering ocean liners amazed the world. By using Python's BeautifulSoup library, one can collect data from the <a href="https://en.wikipedia.org/wiki/Category:Ships_of_the_White_Star_Line">Wikipedia category page</a> about the ships that served the White Star Line and store the data in a Pandas DataFrame.

After filtering out individual Wikipedia pages such as the template for WSL ship articles, the program stores the data scraped from each page in the category under a key in a dictionary. Since the Wikipedia articles for the SS <i>Bardic</i>, <i>Big Four</i>, and SS <i>Germanic</i> (1874) did not include the same data labels as any of the other pages in the Wikipedia category, I manually reentered the data for those ships, which then allowed me to convert the whole dictionary into a Pandas DataFrame. Using mostly regular expressions (regexes), I cleaned and standardized variables related to the ships' manufacturer, tonnage, speed, dimensions, class, and type. Due to the general lack of uniformity across the Wikipedia articles, I did not believe it efficient to take this same approach to columns concerning the ship's additional names, operators, ports of registry, capacity, and crew. Many of the entries presented issues that were exclusive to that particular entry (e.g., the page for the SS <i>Cevic</i> listed the United Kingdom as its port of registry multiple times, but no other page showed that error). Therefore, it would be better, in my opinion, to edit individual entries by hand in Microsoft Excel, rather than writing code to address each and every error in the datset. Fortunately, 


### References
 