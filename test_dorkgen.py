"""Tests for the Google Dork Generator. Run with: pytest test_dorkgen.py -v"""

import pytest

import dorkgen


def test_normalize_domain_strips_scheme_and_path():
    assert dorkgen.normalize_domain("https://Example.COM/some/path") == "example.com"


def test_normalize_domain_rejects_garbage():
    with pytest.raises(ValueError):
        dorkgen.normalize_domain("not a domain")


def test_all_categories_have_templates_with_domain_placeholder():
    for cat, meta in dorkgen.CATEGORIES.items():
        assert meta["templates"], f"{cat} has no templates"
        for t in meta["templates"]:
            assert "{domain}" in t, f"{cat} template missing domain placeholder: {t!r}"


def test_generate_dorks_substitutes_domain():
    dorks = dorkgen.generate_dorks("example.com", "login_pages")
    assert all("example.com" in d for d in dorks)
    assert any("inurl:login" in d for d in dorks)


def test_generate_dorks_unknown_category_raises():
    with pytest.raises(ValueError):
        dorkgen.generate_dorks("example.com", "not-a-category")


def test_generate_all_covers_every_category():
    result = dorkgen.generate_all("example.com")
    assert set(result) == set(dorkgen.CATEGORIES)
    for dorks in result.values():
        assert dorks


def test_cli_single_category(capsys):
    rc = dorkgen.main(["--domain", "example.com", "--category", "directory_listings"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "index of" in out
    assert "example.com" in out


def test_cli_all_categories_writes_file(tmp_path):
    out_file = tmp_path / "dorks.txt"
    rc = dorkgen.main(["--domain", "example.com", "--all", "--out", str(out_file)])
    assert rc == 0
    content = out_file.read_text()
    for meta in dorkgen.CATEGORIES.values():
        assert meta["label"] in content


def test_cli_requires_domain(capsys):
    rc = dorkgen.main(["--category", "login_pages"])
    assert rc == 1


def test_cli_rejects_invalid_domain(capsys):
    rc = dorkgen.main(["--domain", "not a domain", "--category", "login_pages"])
    assert rc == 1


def test_cli_list_categories(capsys):
    rc = dorkgen.main(["--list-categories"])
    assert rc == 0
    out = capsys.readouterr().out
    for cat in dorkgen.CATEGORIES:
        assert cat in out
