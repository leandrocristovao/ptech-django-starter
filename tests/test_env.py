import os

from core.env import load_env_file


def test_load_env_file_parses_values_and_comments(monkeypatch, tmp_path):
    monkeypatch.delenv("DJANGO_SECRET_KEY", raising=False)
    monkeypatch.delenv("DJANGO_DEBUG", raising=False)
    monkeypatch.delenv("DJANGO_ALLOWED_HOSTS", raising=False)
    monkeypatch.delenv("DJANGO_CSRF_TRUSTED_ORIGINS", raising=False)
    monkeypatch.delenv("EMPTY_VALUE", raising=False)
    monkeypatch.delenv("INLINE_HASH", raising=False)
    monkeypatch.delenv("QUOTED_HASH", raising=False)
    monkeypatch.delenv("EXPORTED_VALUE", raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "# Example file",
                "DJANGO_SECRET_KEY=from-file",
                "DJANGO_DEBUG=0",
                "DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1",
                'DJANGO_CSRF_TRUSTED_ORIGINS="http://localhost:8000 http://127.0.0.1:8000"',
                "EMPTY_VALUE=",
                "INLINE_HASH=keep-this # trailing comment",
                'QUOTED_HASH="keep # this part"',
                "export EXPORTED_VALUE=works",
            ]
        ),
        encoding="utf-8",
    )

    loaded = load_env_file(env_file)

    assert loaded == {
        "DJANGO_SECRET_KEY": "from-file",
        "DJANGO_DEBUG": "0",
        "DJANGO_ALLOWED_HOSTS": "localhost,127.0.0.1",
        "DJANGO_CSRF_TRUSTED_ORIGINS": "http://localhost:8000 http://127.0.0.1:8000",
        "EMPTY_VALUE": "",
        "INLINE_HASH": "keep-this",
        "QUOTED_HASH": "keep # this part",
        "EXPORTED_VALUE": "works",
    }

    assert env_file.exists()
    assert loaded["DJANGO_SECRET_KEY"] == "from-file"


def test_load_env_file_does_not_override_existing_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("DJANGO_SECRET_KEY", "from-shell")

    env_file = tmp_path / ".env"
    env_file.write_text("DJANGO_SECRET_KEY=from-file\n", encoding="utf-8")

    loaded = load_env_file(env_file)

    assert loaded == {}
    assert os.environ["DJANGO_SECRET_KEY"] == "from-shell"
