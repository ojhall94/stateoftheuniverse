"""
Get a list of astronomers whose birthday is on a given day.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

from datetime import datetime as dt
from dateutil.parser import parse as parse_date
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Optional

from stateoftheuniverse.widgets.prototypes import WidgetPrototype


# -----------------------------------------------------------------------------
# AUXILIARY FUNCTION DEFINITIONS
# -----------------------------------------------------------------------------

# TODO: In case we want to add more widgets that make use of Wikidata, maybe
#       this function should be in a more general utils file?

def query_wikidata(query: str,
                   url: str = "https://query.wikidata.org/sparql") -> dict:
    """
    Use a SPARQLWrapper to send a given `query` to the specified `url`,
    get the result in JSON format, and cast the result to a dictionary.

    Args:
        query: The query (using the SPARQL language) to send to `url`.
        url: The "endpoint URL" of the server that will take our `query`
            and gather the requested data from the data base.

    Returns:
        A dictionary containing the information requested in `query`.
    """

    sparql = SPARQLWrapper(url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    return sparql.query().convert()


# -----------------------------------------------------------------------------
# CLASS DEFINITIONS
# -----------------------------------------------------------------------------

class AstronomerBirthdays(WidgetPrototype):

    def __init__(self,
                 longitude: Optional[float] = None,
                 latitude: Optional[float] = None,
                 datetime: Optional[dt] = None):

        super().__init__(longitude=longitude,
                         latitude=latitude,
                         datetime=datetime)

    def get_data(self):
        """
        Send a query to Wikidata to get the names and basic information
        of astronomers whose birthday coincides with the `datetime` of
        the class, essentially answering the question: "Who's birthday
        is it today?".

        The result is a list of dictionaries with the following keys:
        `{"name", "description", "wikipedia_url", "birthdate",
          "deathdate"}`.
        """

        # Get the month and date for the datetime variable of the widget
        day = self.datetime.day
        month = self.datetime.month

        # Define the query that will be sent to Wikidata
        query = \
            """SELECT ?entity ?entityLabel ?entityDescription ?article
            ?birthdate ?deathdate
            WHERE {
            ?entity wdt:P106 wd:Q11063 .
            ?entity wdt:P569 ?birthdate .
            OPTIONAL { ?entity wdt:P570 ?deathdate . }
            FILTER (MONTH(?birthdate) = DT_MONTH && DAY(?birthdate) = DT_DAY)
            ?article schema:about ?entity .
            ?article schema:inLanguage "en" .
            FILTER (SUBSTR(str(?article), 1, 25) = "https://en.wikipedia.org/")
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
            }""".replace('DT_MONTH', str(month)).replace('DT_DAY', str(day))

        # Send the query and get the results
        results = query_wikidata(query=query)['results']['bindings']

        # Loop over the results and extract only the parts that we want to keep
        data = list()
        for result in sorted(results, key=lambda x: x['entityLabel']['value']):

            # Get all values that should always be present
            item = dict(name=result['entityLabel']['value'],
                        description=result['entityDescription']['value'],
                        wikipedia_url=result['article']['value'],
                        birthdate=parse_date(result['birthdate']['value']),
                        deathdate=None)

            # The death date needs special attention, because some people are
            # still alive, meaning that the field is not present in the result
            if 'deathdate' in result.keys():
                item['deathdate'] = parse_date(result['deathdate']['value'])

            # Store the item we've just collected
            data.append(item)

        # Store away the data retrieved by this method
        self.data = data

    def get_string(self):

        string = ''
        string += '\n' + 80 * '-' + '\n'
        string += 'BIRTHDAY CHILDS FROM ASTRONOMY'.center(80) + '\n'
        string += 80 * '-' + '\n\n'

        for item in self.data:
            birthdate = f'{item["birthdate"].strftime("%B %d, %Y")}'
            deathdate = ('today' if item["deathdate"] is None else
                         f'{item["deathdate"].strftime("%B %d, %Y")}')
            string += item['name'] + f' ({birthdate} - {deathdate})' + '\n'
            string += item['description'] + '\n'
            string += item['wikipedia_url'] + '\n\n'

        string += 80 * '-' + '\n'

        return string
