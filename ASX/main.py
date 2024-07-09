from asx_crawler import ASXCrawler  


def main():
    # Initialize the crawler with the initial search parameters
    proxy = 'http://127.0.0.1:7890'  # Set up proxy if needed
    crawler = ASXCrawler(search_key='AIZ', title_keys=['Dividend', 'Distribution'], year='2024', proxy=proxy)

    tasks = [
        {'search_key': 'AIZ', 'title_keys': ['Dividend'], 'year': '2024'},
        {'search_key': 'CBA', 'title_keys': ['Report'], 'year': '2023'}
    ]

    # Execute tasks
    for task in tasks:
        # Update the crawler with new search parameters
        crawler.search_key = task['search_key']
        crawler.title_keys = task['title_keys']
        crawler.year = task['year']
        crawler.announcements_url = f'{crawler.base_url}/asx/v2/statistics/announcements.do?by=asxCode&asxCode={task["search_key"]}&timeframe=Y&year={task["year"]}'
        
        # Run the crawler
        crawler.run()

if __name__ == '__main__':
    main()
