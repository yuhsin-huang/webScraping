# CLOSESPIDER_PAGECOUNT = 20

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

class ImdbSpider(Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt1375666/']

    def parse(self,response):
        """
        parse(self, response) should assume that you start on a movie page, and then navigate to
        the Cast & Crew page. Remember that this page has url <movie_url>fullcredits. Once there, 
        the parse_full_credits(self,response) should be called, by specifying this method in the 
        callback argument to a yielded scrapy.Request. The parse() method does not return any data. 
        This method should be no more than 5 lines of code, excluding comments and docstrings.
        """
        next_page = response.urljoin('fullcredits')

        if next_page:
            yield Request(next_page, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        """
        should assume that you start on the Cast & Crew page. Its purpose is to yield a scrapy.
        Request for the page of each actor listed on the page. Crew members are not included. 
        The yielded request should specify the method parse_actor_page(self, response) should 
        be called when the actor’s page is reached. The parse_full_credits() method does not 
        return any data. This method should be no more than 5 lines of code, excluding comments 
        and docstrings.
        """
        actor_pages = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        if actor_pages:
            for i in actor_pages:
                actor_page = 'https://www.imdb.com'+i
                yield Request(actor_page, callback = self.parse_actor_page)

    
    def parse_actor_page(self, response):
        """
        parse_actor_page(self, response) should assume that you start on the page of an actor. 
        It should yield a dictionary with two key-value pairs, of the form {"actor" : actor_name, 
        "movie_or_TV_name" : movie_or_TV_name}. The method should yield one such dictionary for each of the movies 
        or TV shows on which that actor has worked. Note that you will need to determine both the name of the actor and 
        the name of each movie or TV show. This method should be no more than 15 lines of code, excluding comments and 
        docstrings.
        """
        actor_name = response.css("span.itemprop::text").get()

        for quote in response.css("div.filmo-row"):    
            movie_or_TV_name = quote.css("a::text").getall()
            
            yield {
                "actor" : actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }





 
    