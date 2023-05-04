def parse_page_range(pages: str) -> set[int]:
    page_ranges = []
    for page_range in pages.split(","):
        if "-" in page_range:
            start, end = map(int, page_range.split("-"))
            page_ranges.append(set(range(start, end + 1)))
        else:
            page_ranges.append({int(page_range)})

    pages_set = set()
    for page_set in page_ranges:
        pages_set |= page_set

    return pages_set
