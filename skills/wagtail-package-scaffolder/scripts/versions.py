"""Fetch and validate compatibility data without language-model extraction."""

import json
import re
from datetime import date
from html.parser import HTMLParser
from urllib.request import Request, urlopen

RELEASE_URL = "https://github.com/wagtail/wagtail/wiki/Release-schedule"
COMPATIBILITY_URL = "https://docs.wagtail.org/en/stable/releases/upgrading.html"
MONTHS = dict(
    zip(
        "January February March April May June July August September October November December".split(),
        range(1, 13),
        strict=False,
    )
)


def version_key(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+", value):
        raise ValueError(f"Invalid major.minor version: {value!r}")
    return tuple(map(int, value.split(".")))


def sorted_versions(values):
    return sorted(set(values), key=version_key)


class TableParser(HTMLParser):
    """Extract table cells, including text nested in links and footnotes."""

    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = self.row = self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("th", "td") and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def fetch(url):
    request = Request(url, headers={"User-Agent": "wagtail-package-scaffolder/1"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def find_table(html, headers):
    parser = TableParser()
    parser.feed(html)
    matches = [table for table in parser.tables if table and table[0] == headers]
    if len(matches) != 1:
        raise ValueError(f"Expected one table with headers {headers!r}")
    return matches[0][1:]


def parse_date(value):
    parts = value.split()
    if len(parts) != 3 or parts[1] not in MONTHS:
        raise ValueError(f"Unexpected release date: {value!r}")
    return date(int(parts[2]), MONTHS[parts[1]], int(parts[0])).isoformat()


def parse_version_list(value):
    result = []
    for token in value.split(","):
        match = re.fullmatch(r"\s*(\d+\.\d+)(?:\[\d+\]|\s*\([^)]*\))*\s*", token)
        if not match:
            raise ValueError(f"Unexpected compatibility cell: {value!r}")
        result.append(match[1])
    return sorted_versions(result)


def parse_releases(html, today):
    rows = find_table(
        html,
        [
            "Version",
            "Release date",
            "Active support [1]",
            "Security support [2]",
        ],
    )
    result = []
    for row in rows:
        if len(row) != 4:
            raise ValueError("Unexpected release table row")
        match = re.fullmatch(r"(\d+\.\d+)( LTS|\*)?", row[0])
        if not match:
            raise ValueError(f"Unexpected Wagtail release: {row[0]!r}")
        released, end = parse_date(row[1]), parse_date(row[3])
        if released <= today <= end and match[2] != "*":
            result.append(
                {
                    "version": match[1],
                    "is_lts": match[2] == " LTS",
                    "release_date": released,
                    "support_end": end,
                }
            )
    if not result or not any(row["is_lts"] for row in result):
        raise ValueError("No supported Wagtail LTS release found")
    return sorted(result, key=lambda row: version_key(row["version"]))


def parse_compatibility(html):
    rows = find_table(
        html,
        [
            "Wagtail release",
            "Compatible Django versions",
            "Compatible Python versions",
        ],
    )
    result = {}
    for row in rows:
        if len(row) != 3:
            raise ValueError("Unexpected compatibility table row")
        match = re.fullmatch(r"(\d+\.\d+)(?: LTS)?", row[0])
        if not match or match[1] in result:
            raise ValueError(f"Unexpected/duplicate compatibility release: {row[0]!r}")
        result[match[1]] = {
            "django_versions": parse_version_list(row[1]),
            "python_versions": parse_version_list(row[2]),
        }
    return result


def parse_django(html):
    rows = find_table(html, ["Django version", "Python versions"])
    result = {}
    for row in rows:
        if len(row) != 2:
            raise ValueError("Unexpected Django compatibility row")
        version_key(row[0])
        result[row[0]] = parse_version_list(row[1])
    return result


def validate_data(data, today):
    """Normalize saved or fetched data and reject missing/inconsistent fields."""
    if not isinstance(data, dict) or set(data) != {
        "supported_wagtail_versions",
        "django_python",
        "sources",
    }:
        raise ValueError(
            "Version data must contain supported_wagtail_versions, django_python, sources"
        )
    rows = data["supported_wagtail_versions"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("Wagtail release list is empty")
    normalized = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "version",
            "is_lts",
            "release_date",
            "support_end",
            "django_versions",
            "python_versions",
        }:
            raise ValueError("Invalid Wagtail release fields")
        version_key(row["version"])
        if row["version"] in seen or type(row["is_lts"]) is not bool:
            raise ValueError("Duplicate Wagtail release or invalid LTS flag")
        seen.add(row["version"])
        for field in ("release_date", "support_end"):
            if date.fromisoformat(row[field]).isoformat() != row[field]:
                raise ValueError("Dates must use YYYY-MM-DD")
        if not row["release_date"] <= today <= row["support_end"]:
            raise ValueError(f"Wagtail {row['version']} is not supported on {today}")
        item = dict(row)
        for field in ("django_versions", "python_versions"):
            if not isinstance(row[field], list) or not row[field]:
                raise ValueError(f"Empty or invalid {field}")
            item[field] = sorted_versions(row[field])
        normalized.append(item)
    if not any(row["is_lts"] for row in normalized):
        raise ValueError("No supported LTS release")
    django = data["django_python"]
    if not isinstance(django, dict):
        raise ValueError("Invalid Django/Python map")
    required = sorted_versions(v for row in normalized for v in row["django_versions"])
    if set(django) != set(required):
        raise ValueError(
            "Django/Python map must cover exactly the retained Django releases"
        )
    for version in required:
        if not isinstance(django[version], list) or not django[version]:
            raise ValueError(f"Missing Python compatibility for Django {version}")
    sources = data["sources"]
    if (
        not isinstance(sources, list)
        or not sources
        or any(
            not isinstance(url, str) or not url.startswith("https://")
            for url in sources
        )
    ):
        raise ValueError("Version sources must be HTTPS URLs")
    return {
        "supported_wagtail_versions": sorted(
            normalized, key=lambda row: version_key(row["version"])
        ),
        "django_python": {v: sorted_versions(django[v]) for v in required},
        "sources": list(dict.fromkeys(sources)),
    }


def fetch_data(today):
    sources = [RELEASE_URL, COMPATIBILITY_URL]
    rows = parse_releases(fetch(RELEASE_URL), today)
    compatibility = parse_compatibility(fetch(COMPATIBILITY_URL))
    for row in rows:
        if row["version"] not in compatibility:
            raise ValueError(f"Missing compatibility for Wagtail {row['version']}")
        row.update(compatibility[row["version"]])
    # Wagtail docs may list compatibility with a forthcoming Django series.
    # Include only series with a stable, non-yanked release published on PyPI.
    pypi_url = "https://pypi.org/pypi/Django/json"
    sources.append(pypi_url)
    releases = json.loads(fetch(pypi_url))["releases"]
    published = set()
    for release, files in releases.items():
        match = re.fullmatch(r"(\d+\.\d+)(?:\.\d+)?", release)
        if match and any(not file.get("yanked", False) for file in files):
            published.add(match[1])
    for row in rows:
        row["django_versions"] = [v for v in row["django_versions"] if v in published]
    required = sorted_versions(v for row in rows for v in row["django_versions"])
    django = {}
    for version in reversed(required):
        if version in django:
            continue
        url = f"https://docs.djangoproject.com/en/{version}/faq/install/"
        sources.append(url)
        django.update(parse_django(fetch(url)))
    return validate_data(
        {
            "supported_wagtail_versions": rows,
            "django_python": {v: django[v] for v in required},
            "sources": sources,
        },
        today,
    )


def defaults(data):
    # Prefer the latest supported LTS for new projects, rather than an older
    # LTS that remains in its security-support overlap period.
    row = max(
        (row for row in data["supported_wagtail_versions"] if row["is_lts"]),
        key=lambda row: version_key(row["version"]),
    )
    pairs = [
        (p, d)
        for p in row["python_versions"]
        for d in row["django_versions"]
        if p in data["django_python"][d]
    ]
    if not pairs:
        raise ValueError("No compatible default combination")
    python, django = min(
        pairs, key=lambda pair: (version_key(pair[1]), version_key(pair[0]))
    )
    return {"wagtail_min": row["version"], "django_min": django, "python_min": python}


def combinations(data, config):
    result = []
    for row in data["supported_wagtail_versions"]:
        if version_key(row["version"]) < version_key(config["wagtail_min"]):
            continue
        for django in row["django_versions"]:
            if version_key(django) < version_key(config["django_min"]):
                continue
            for python in row["python_versions"]:
                if (
                    version_key(python) >= version_key(config["python_min"])
                    and python in data["django_python"][django]
                ):
                    result.append((python, django, row["version"]))
    result.sort(key=lambda triple: tuple(version_key(v) for v in triple))
    if not result:
        raise ValueError("Version constraints leave no compatible test combinations")
    # Each selected minimum must occur in the resulting supported matrix.
    for index, field in enumerate(("python_min", "django_min", "wagtail_min")):
        if not any(triple[index] == config[field] for triple in result):
            raise ValueError(f"{field} is unsupported under the selected constraints")
    return result
