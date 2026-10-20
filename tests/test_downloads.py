"""Exercise the installed gdown API, replacing only its HTTP transport."""

import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch

from backend.download.download_manager import DownloadManager
from tests.support import BackendCase


@unittest.skipUnless(importlib.util.find_spec("gdown"), "Requer requirements/backend.txt.")
class GoogleDriveDownloadTests(BackendCase):
    file_id = "1u6Uj5ro5HLFOXxsgIwWBnmmEyrnfq8H4"

    def response(self, payload):
        import requests

        response = requests.Response()
        response.status_code = 200
        response.url = f"https://drive.google.com/uc?id={self.file_id}"
        response.headers.update(
            {
                "Content-Type": "application/zip",
                "Content-Disposition": 'attachment; filename="game.zip"',
                "Content-Length": str(len(payload)),
            }
        )
        response.raw = io.BytesIO(payload)
        return response

    def transport(self, payload):
        import requests

        session = requests.Session()
        session.get = unittest.mock.Mock(return_value=self.response(payload))
        factory = patch(
            "gdown.download._get_session",
            return_value=(session, str(self.home / "gdown-cookies.txt")),
        )
        return factory, session

    def test_direct_and_shared_links_use_the_real_gdown_function(self):
        payload = self.archive().read_bytes()
        urls = (
            f"https://drive.google.com/uc?export=download&id={self.file_id}",
            f"https://drive.google.com/file/d/{self.file_id}/view?usp=sharing",
        )
        for index, url in enumerate(urls):
            with self.subTest(url=url):
                factory, session = self.transport(payload)
                destination = self.home / f"download-{index}.zip"
                with factory:
                    result = DownloadManager().download(url, destination)
                self.assertEqual(result, destination)
                self.assertEqual(destination.read_bytes(), payload)
                self.assertFalse(destination.with_name(destination.name + ".part").exists())
                session.get.assert_called_once_with(
                    f"https://drive.google.com/uc?id={self.file_id}", stream=True, verify=True
                )

    def test_native_install_uses_real_gdown_and_updates_the_library(self):
        payload = self.archive().read_bytes()
        self.add_game(download_url=f"https://drive.google.com/uc?export=download&id={self.file_id}")
        factory, session = self.transport(payload)
        with factory:
            result = self.service.install_game("demo")
        executable = Path(result.executable_path)
        self.assertTrue(executable.is_file())
        self.assertEqual(executable.read_text(), "print('hello')")
        self.assertEqual([game.id for game in self.service.list_games("installed")], ["demo"])
        session.get.assert_called_once()
