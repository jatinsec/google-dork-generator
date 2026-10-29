# 🔎 Google Dork Generator

A simple security-research utility for generating Google search queries (Google Dorks) that can help security researchers identify publicly indexed information.

## ⚠️ Responsible Use

This tool is intended for:

- Security research
- OSINT
- Bug bounty reconnaissance
- Authorised penetration testing
- Educational purposes

Only use generated queries against websites and organisations you are authorised to assess.

## 🚀 Features

- Generate commonly used Google Dork queries
- Quickly construct targeted search queries
- Useful for reconnaissance and OSINT workflows
- Lightweight and easy to use

## 🛠️ Use Cases

Example categories include:

- Exposed files
- Login pages
- Public documents
- Directory listings
- Publicly indexed configuration information
- Technology discovery

## 📚 Example Dorks

```text
site:example.com
site:example.com inurl:login
site:example.com filetype:pdf
site:example.com intitle:"index of"
site:example.com inurl:api
```

## 📦 Installation

Python 3.10+. No third-party dependencies for the tool itself.

```bash
git clone https://github.com/jatinpatel-hacker33/google-dork-generator.git
cd google-dork-generator
pip install -r requirements-dev.txt   # only needed to run the tests
```

## ▶️ Usage

```bash
# List available categories
python3 dorkgen.py --list-categories

# Generate one category for a domain you're authorized to assess
python3 dorkgen.py --domain example.com --category login_pages

# Generate every category and save to a file
python3 dorkgen.py --domain example.com --all --out dorks.txt
```

Example output (`--category directory_listings`):

```text
# Directory listings
site:example.com intitle:"index of"
site:example.com intitle:"index of" "parent directory"
```

`dorkgen.py` only builds the query strings above — it never sends a request to Google or any
other search engine itself. You paste the output into a search engine (or an authorized search
API) yourself, against a target you're actually allowed to assess.

## ✅ Tests

```bash
pytest test_dorkgen.py -v
```

11 tests cover domain normalization/validation, every category's templates, and the CLI
end-to-end (including error handling for a missing/invalid domain).

## Limitations (honest)

- Templates are a curated starting set per category (4–7 queries each), not an exhaustive dork
  database — combine with your own additions for a real engagement.
- No network code at all: this tool cannot and does not query Google for you.
- Domain validation is syntactic only; it doesn't check that the domain actually resolves or that
  you're authorized against it — that's on you, per the Responsible Use section above.
