# rss_reader

> A pure Python command-line RSS reader that fetches and displays news feeds from any valid RSS URL.

## Overview

`rss_reader` is a CLI tool that parses RSS feeds and prints them in a human-readable or JSON format. It's useful for developers, news aggregators, or anyone who prefers consuming news from the terminal.

## Features

- Parses standard RSS feeds using built-in libraries (`xml.etree.ElementTree`)
- Outputs news items with title, description, date, link, author, and categories
- Optional `--json` flag to pretty-print feed content in structured JSON
- Supports limiting the number of displayed items with `--limit`
- Simple, dependency-light design — no third-party RSS parsers required

## Usage

```bash
python rss_reader.py <rss_url> [--limit N] [--json]

