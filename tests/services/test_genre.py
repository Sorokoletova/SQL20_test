from unittest.mock import MagicMock

import pytest
from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    genre_dao.get_one = MagicMock(return_value=Genre(id=1, name="драма"))
    genre_dao.get_all = MagicMock(return_value=["Драма", "комедия"])
    genre_dao.create = MagicMock(return_value=Genre(id=3, name="фантастика"))
    genre_dao.update = MagicMock(return_value=Genre(id=1, name="фантастика"))
    genre_dao.delete = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.name == 'драма'

    def test_get_all(self):
        genre = self.genre_service.get_all()

        assert genre is not None
        assert isinstance(genre, list)
        assert len(genre) == 2

    def test_create(self):
        genre = self.genre_service.create("фантастика")

        assert genre is not None
        assert genre.id == 3

    def test_update(self):
        genre = self.genre_service.update(3)

        assert genre is not None
        assert genre.name == 'фантастика'

    def test_delete(self):
        self.genre_service.delete(1)
        self.genre_service.dao.delete.assert_called_once_with(1)
