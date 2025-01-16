import asyncio
import httpx
from bs4 import BeautifulSoup


async def fetch_url(client, url):
    """Функция для загрузки содержимого страницы."""
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
    except httpx.RequestError as exc:
        print(f"Не удалось загрузить {url}: {exc}")
        return None


async def extract_h1(html, url):
    """Функция для извлечения заголовков <h1> из HTML."""
    if html:
        soup = BeautifulSoup(html, "html.parser")
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
        return {"url": url, "h1": h1_tags}
    return {"url": url, "h1": []}


async def process_urls(urls, output_file):
    """Основная функция для обработки списка URL."""
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        responses = await asyncio.gather(*tasks)

        # Извлечение заголовков h1
        extract_tasks = [
            extract_h1(html, url) for html, url in zip(responses, urls)
        ]
        results = await asyncio.gather(*extract_tasks)

    # Сохранение результата в файл
    with open(output_file, "w", encoding="utf-8") as file:
        for result in results:
            file.write(f"URL: {result['url']}\n")
            file.write("H1 tags:\n")
            for h1 in result["h1"]:
                file.write(f"  - {h1}\n")
            file.write("\n")


if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://www.wikipedia.org",
        "https://www.python.org"
    ]
    output_file = "h1_results.txt"

    asyncio.run(process_urls(urls, output_file))
    print(f"Результаты сохранены в файл: {output_file}")