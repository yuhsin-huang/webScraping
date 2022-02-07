# CLOSESPIDER_PAGECOUNT = 20

from scrapy.spiders import Spider
from scrapy.http import Request

class ImdbSpider(Spider):
    """
    A simple spider class that navigate from a movie website to its full cast. Then scrapt all the works each actors have 
    worked on.

    This spider works as follows. 
    - The parse method handles the navigation to the full credit of the movie.
    - The parse_full_credits method scrapts the links of all the actor profiles, and navigate through all of them.
    - The parse_actor_page method returns a dictionary that contains all the works each actors has worked on. 
    
    The spider will then create a dictionary called results.csv in the directory.
    """

    # the name of the spider
    name = 'imdb_spider'

    # the movie page we want to navigate
    start_urls = ['https://www.imdb.com/title/tt1375666/']

    def parse(self,response):
        """
        This function starts on a movie page, in this case the starts_urls we set. Then, it navigates to
        the Cast & Crew page. Next, it calls the parse_full_credits(self,response) to scrpat the full cast of the movie.
        This method does not return anything.
        """

        # the page containing the full cast of the movie has url <movie_url>fullcredits
        next_page = response.urljoin('fullcredits')

        # if there is a cast page, use the generator and callback to call the parse_full_credits method
        if next_page:
            # call parse_full_credits once we reach next_page
            yield Request(next_page, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        """
        This function starts on the full credit page. Then, it requests urls for the page of each actor listed 
        on the page (crew members excluded). Lastly, it yields the method parse_actor_page(self, response) once it 
        reaches the actor pages. 
        This method does not return anything.
        """

        # create a list of relative paths, one for each actor
        actor_pages = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        if actor_pages:
            # loop through each actor pages
            for i in actor_pages:
                # the absolute path for the actor page is 'https://www.imdb.com'+ the relative path we retrieved
                actor_page = 'https://www.imdb.com'+i
                # call parse_actor_page once we reach actor_page
                yield Request(actor_page, callback = self.parse_actor_page)

    
    def parse_actor_page(self, response):
        """
        This function starts on the page of an actor. It will yield one dictionary containing all the movie or TV shows 
        the actor has worked on. The dictionary will have two key-value pairs, of the form {"actor" : actor_name, 
        "movie_or_TV_name" : movie_or_TV_name}. 
        """
        # scrapt the actor name using CSS selector: it is the text in span.itemprop
        actor_name = response.css("span.itemprop::text").get()

        # scrapt all the movie or TV name the actors has worked on 
        # each filmo_row division contains one work, so we loop through all the divisions
        for quote in response.css("div.filmo-row"): 
            # get the first text in the division, which is the title of the movie or TV
            movie_or_TV_name = quote.css("a::text").get()
            
            # yield the dictionary
            yield {
                "actor" : actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }





 
    