# ship_scraper
 
The Oceanic Steam Navigation Company—also known as the White Star Line (WSL)—was one of the premier British shipping companies during the golden age of steamships, transporting passengers and cargo from 1845 to 1934. After suffering several disasters at sea throughout its history, the company's infamous reputation was sealed with the loss of the RMS <i>Titanic</i> in 1912. Nevertheless, the WSL endeavored to provide high-quality service to its passengers, and the line's towering vessels amazed the world. Using Python's BeautifulSoup library, I collected data from the <a href="https://en.wikipedia.org/wiki/Category:Ships_of_the_White_Star_Line">Wikipedia category page</a> about the ships of the White Star Line and stored the data in a Pandas DataFrame.

After filtering out unnecessary pages—namely the Wikipedia template and list pages, as well as a redundant article about a group of ships called the "Big Four"—the program stores the data scraped from each of the remaining 85 articles under a key in a dictionary. Since the pages for the SS <i>Bardic</i> and SS <i>Germanic</i> (1874) did not include the same data labels as any of the other pages in the category, I manually reentered the data for those ships. Now that the labels were consistent across the data entries, I converted the whole dictionary into a Pandas DataFrame. Primarily using regular expressions (regexes), I cleaned and standardized data concerning the ships' manufacturer, tonnage, speed, dimensions, class, type, and dates of their completion and maiden voyage. For numerical variables, NA's were filled with 0.0 as needed (except for speed, since no unit conversion was necessary). Due to the varying degree of completeness of the entries related to the ships' passenger and cargo capacities, crew, and fate, I chose to not include those variables in the final dataset. If such data were required for an analysis, it would be better, in my opinion, to enter and format the individual entries by hand using software such as Microsoft Excel. The other variables, however, are fully cleaned and are well-suited for further analysis (e.g., the tonnage of WSL vessels).

| Ship Name | Builder | Class/type | Length (ft) | Beam (ft) | Depth (ft) | Tonnage (GRT) | Speed (kn) | Launched | Completed | Maiden voyage |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| SS Adriatic (1871) | Harland & Wolff, Belfast | Oceanic-class ocean liner | 452.0 | 40.9 | 31.0 | 3888 | 14.5 | 17 Oct 1871 | 31 Mar 1872 | 11 Apr 1872 |
| RMS Adriatic (1906) | Harland & Wolff, Belfast | Big Four ocean liner | 729.0 | 75.6 | 52.6 | 24679 | 16 | 20 Sep 1906 | 25 Apr 1907 | 8 May 1907 |
| SS Afric | Harland & Wolff, Belfast | Jubilee-class ocean liner | 550.0 | 63.3 | 0.0 | 11948 | 13.5 | 16 Nov 1898 |  | 8 Feb 1899 |
| SS Albertic | AG Weser | Ocean liner | 590.7 | 72.0 | 0.0 | 18940 |  | 23 Mar 1920 |  |  |
| SS American (1895) | Harland & Wolff, Belfast |  | 475.0 | 55.2 | 0.0 | 8249 | 11 | 8 Aug 1895 |  | 9 Oct 1895 |

The full dataset can be found in the file <i>ships.csv</i>.


### References
In writing my program, I took inspiration from code solutions provided by the following two users:

Vlad Siv – <a href="https://stackoverflow.com/questions/70233801/python-scraping-of-wikipedia-category-page">"Python scraping of Wikipedia category page"</a><p>
baduker – <a href="http://5.9.10.113/64256790/how-do-i-web-scrape-a-wikipedia-infobox-table">"How do I Web Scrape a Wikipedia Infobox Table?"</a>
