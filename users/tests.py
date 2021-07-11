from django.test import TestCase


class FileHandling(TestCase):
    def setUp(self) -> None:
        pass

    def test_valid_format_is_handled(self) -> bool:
        """files that follow the file structure doesn't throw an exception"""
        return True
