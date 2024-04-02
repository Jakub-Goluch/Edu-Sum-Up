import requests
import json


class SemanticScholarScraper:
    """Class to scrape related publications from semanticscholar api."""
    @staticmethod
    def get_semanticscholar_response(
        keywords: list[str], min_year: int, max_year: int
    ) -> requests.Response:
        """Get response from semanticscholar api.

        Args:
            keywords (list[str]): list of keywords to search for.
            min_year (int): minimum year of publication.
            max_year (int): maximum year of publication.

        Returns:
            response requests.Response: response from semanticscholar api.
        """

        headers = {
            "Connection": "keep-alive",
            "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            "Cache-Control": "no-cache,no-store,must-revalidate,max-age=-1",
            "Content-Type": "application/json",
            "sec-ch-ua-mobile": "?1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36",
            "X-S2-UI-Version": "20166f1745c44b856b4f85865c96d8406e69e24f",
            "sec-ch-ua-platform": '"Android"',
            "Accept": "*/*",
            "Origin": "https://www.semanticscholar.org",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.semanticscholar.org/search?year%5B0%5D=2018&year%5B1%5D=2022&q=multi%20label%20text%20classification&sort=relevance",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }

        joined_keywords = " ".join([str(elem).lower() for elem in keywords])

        data = json.dumps(
            {
                "queryString": f"{joined_keywords}",
                "page": 1,
                "pageSize": 10,
                "sort": "relevance",
                "authors": [],
                "coAuthors": [],
                "venues": [],
                "yearFilter": {"min": min_year, "max": max_year},
                "requireViewablePdf": False,
                "fieldsOfStudy": [],
                "hydrateWithDdb": True,
                "includeTldrs": True,
                "performTitleMatch": True,
                "includeBadges": True,
                "getQuerySuggestions": False,
            }
        )

        response = requests.post(
            "https://www.semanticscholar.org/api/1/search", headers=headers, data=data
        )
        return response

    @staticmethod
    def parse_html_response(response: requests.Response) -> list[dict[str, str]]:
        """Parse response from semanticscholar api.

        Args:
            response requests.Response: response from semanticscholar api.

        Returns:
            list[dict[str, str]]: list of dictionaries containing title and link of publications.
        """

        final_result = []
        response = response.json()["results"]

        for result in response:

            publication = {"title": result["title"]["text"], "link": []}

            if "primaryPaperLink" in result:
                publication["link"] = result["primaryPaperLink"]["url"]
            elif result["alternatePaperLinks"]:
                publication["link"] = result["alternatePaperLinks"][0]["url"]
            else:
                publication["link"] = "no_link_found"

            final_result.append(publication)
        return final_result

    def get_related_publications(
        self, keywords: list[str], min_year: int = 2015, max_year: int = 2024
    ):
        """Get related publications from semanticscholar api.

        Args:
            keywords (list[str]): list of keywords to search for.
            min_year (int): minimum year of publication.
            max_year (int): maximum year of publication.

        Returns:
            list[dict[str, str]]: list of dictionaries containing title and link of publications.
        """

        semanticscholar_response = self.get_semanticscholar_response(
            keywords, min_year=min_year, max_year=max_year
        )
        parsed_response = self.parse_html_response(semanticscholar_response)

        return parsed_response


if __name__ == "__main__":
    # Example usage
    keywords = ["Zero-shot learning", "Natural Language Processing", "Machine Learning"]
    scraper = SemanticScholarScraper()
    publications = scraper.get_related_publications(keywords)
    print(publications)
