from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import xml.etree.ElementTree as ET
import html
import json


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
    """
    root = ET.fromstring(xml)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("Invalid RSS feed: missing channel.")

    def get_text(elem, default=""):
        return html.unescape(elem.text.strip()) if elem is not None and elem.text else default

    # Parse channel info
    feed_data = {
        "title": get_text(channel.find("title")),
        "link": get_text(channel.find("link")),
        "lastBuildDate": get_text(channel.find("lastBuildDate")),
        "pubDate": get_text(channel.find("pubDate")),
        "language": get_text(channel.find("language")),
        "categories": [get_text(cat) for cat in channel.findall("category")],
        "managingEditor": get_text(channel.find("managingEditor")),
        "description": get_text(channel.find("description")),  # Ensure description is included
        "items": [],
    }

    # Parse items
    items = []
    for item in channel.findall("item"):
        item_data = {
            "title": get_text(item.find("title")),
            "author": get_text(item.find("author")),
            "pubDate": get_text(item.find("pubDate")),
            "link": get_text(item.find("link")),
            "categories": [get_text(cat) for cat in item.findall("category")],
            "description": get_text(item.find("description")),
        }
        if not item_data["title"] and not item_data["description"]:
            continue
        items.append(item_data)

    if limit is not None:
        items = items[:limit]
    feed_data["items"] = items

    if json:
        return [json_dumps_pretty(feed_data)]

    # Console Output Formatting
    output = []
    output.append(f"Feed: {feed_data['title']}")
    output.append(f"Link: {feed_data['link']}")
    if feed_data["lastBuildDate"]:
        output.append(f"Last Build Date: {feed_data['lastBuildDate']}")
    if feed_data["pubDate"]:
        output.append(f"Publish Date: {feed_data['pubDate']}")
    if feed_data["language"]:
        output.append(f"Language: {feed_data['language']}")
    if feed_data["categories"]:
        output.append(f"Categories: {', '.join(feed_data['categories'])}")
    if feed_data["managingEditor"]:
        output.append(f"Editor: {feed_data['managingEditor']}")
    if feed_data["description"]:
        output.append(f"Description: {feed_data['description']}")

    if feed_data["items"]:
        output.append("")  # Space between channel info and items

    for item in feed_data["items"]:
        output.append(f"Title: {item['title']}")
        if item["author"]:
            output.append(f"Author: {item['author']}")
        if item["pubDate"]:
            output.append(f"Published: {item['pubDate']}")
        if item["link"]:
            output.append(f"Link: {item['link']}")
        if item["categories"]:
            output.append(f"Categories: {', '.join(item['categories'])}")
        if item["description"]:
            output.append("")  # separate description
            output.append(item["description"])
        output.append("")  # separator between items

    return output[:-1]  # remove last empty string


def json_dumps_pretty(data):
    return json.dumps(data, ensure_ascii=False, indent=2)


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    print(xml[:500])

    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
