import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://www.amazon.com/Meta-Sunglasses-Graphite-Transitions-Regular/dp/B0DD65YPJV/")
        print(result.fit_markdown[:500])  # Print first 500 characters

if __name__ == "__main__":
    asyncio.run(main())
