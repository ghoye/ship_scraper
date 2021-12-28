# ship_scraper
 
The Oceanic Steam Navigation Company—better known as the White Star Line (WSL)—was one of the premier British shipping companies of the 1800's and early 1900's, transporting passengers and cargo for almost a century (1845-1934). After suffering several disasters at sea throughout its lifetime, the company's infamous reputation in popular culture was sealed with the loss of the RMS <i>Titanic</i> in 1912. Nevertheless, the line prided itself on providing high-quality service to its passengers, and its towering ocean liners amazed the world. By using Python's BeautifulSoup library, one can collect data from the <a href="https://en.wikipedia.org/wiki/Category:Ships_of_the_White_Star_Line">Wikipedia category page</a> about the ships that served the White Star Line and store the data in a Pandas DataFrame.

After filtering out Wikipedia template and list pages—leaving 86 instances ready for analysis—this program initially stores the data scraped from each page in the category under a key in a dictionary. Since the Wikipedia articles for the SS <i>Bardic</i>, <i>Big Four</i>, and SS <i>Germanic</i> (1874) did not include the same data labels as any of the other pages in the category, I manually reentered the data for those ships. Since the labels were now consistent across the data entries, I converted the whole dictionary into a Pandas DataFrame. Using mostly regular expressions (regexes), I cleaned and standardized variables related to the ships' manufacturer, tonnage, speed, dimensions, class, and type. Due to the general lack of uniformity across the Wikipedia articles, I did not believe it to be efficient to take this same approach for columns concerning the ships' alternate names, operators, ports of registry, capacity, and crew. Many of the values in those columns contained issues that were exclusive to that particular entry: For example, the page for the SS <i>Cevic</i> listed the United Kingdom as its port of registry multiple times, but no other page had that mistake. Therefore, it would be better, in my opinion, to edit individual entries by hand in Microsoft Excel, rather than hard-coding solutions for each and every error in the dataset. That being said, there are other variables that are well-suited for further analysis (e.g., the tonnage of WSL vessels) and are fully cleaned. The full dataset can be found in the file <i>ships.csv</i>.

In the future, I will likely return to this project and update the techniques used as I continue to develop my knowledge of the various libraries and functions in Python.

### References
I modified the code provided by the following two users as part of my program:

Vlad Siv – <a href="https://stackoverflow.com/questions/70233801/python-scraping-of-wikipedia-category-page">"Python scraping of Wikipedia category page"</a><p>
baduker – <a href="http://5.9.10.113/64256790/how-do-i-web-scrape-a-wikipedia-infobox-table">"How do I Web Scrape a Wikipedia Infobox Table?"</a>
