import requests
from lxml import html

clean = lambda x: x[0].strip() if x else ""


def get_music(name: str, page: int = 1):
    try:
        url = "http://muztv.net/index.php?do=search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }

        response = requests.post(url, data={
            "do": "search",
            "subaction": "search",
            "search_start": page,
            "full_search": "0",
            "result_from": "1",
            "story": name
        }, headers=headers)

        tree = html.fromstring(response.content)
        items = tree.xpath('//div[contains(@class, "play-item")]')

        data = []

        for idx, item in enumerate(items, start=1):
            title = clean(item.xpath('./@data-title'))
            artist = clean(item.xpath('./@data-artist'))
            url = clean(item.xpath('./@data-track'))

            result = {
                "id": idx,
                "title": title,
                "artist": artist,
                "url": url
            }

            if all(result.values()):
                data.append(result)

        return data if data else None

    except Exception:
        return None