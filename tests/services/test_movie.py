from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_dao.get_one = MagicMock(
        return_value=Movie(id=1, title="Йеллоустоун", description="описание",
                           trailer="описание", year="2010", rating=7,
                           genre_id=10, director_id=18))
    movie_dao.get_all = MagicMock(return_value=["Йеллоустоун", "Рокетмен"])
    movie_dao.create = MagicMock(return_value=Movie(id=3, title="Дюна", description="описание",
                                                    trailer="описание", year="2010", rating=7,
                                                    genre_id=10, director_id=18))
    movie_dao.update = MagicMock(return_value=Movie(id=3, title="Tomas"))
    movie_dao.partially_update = MagicMock()
    movie_dao.delete = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.title == 'Йеллоустоун'

    def test_get_all(self):
        movie = self.movie_service.get_all()

        assert movie is not None
        assert isinstance(movie, list)
        assert len(movie) == 2

    def test_create(self):
        movie = self.movie_service.create("Дюна")

        assert movie is not None
        assert movie.id == 3

    def test_update(self):
        movie = self.movie_service.update(3)

        assert movie is not None
        assert movie.title == 'Tomas'

    def test_partially_update(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        self.movie_service.partially_update({"id": 1, "title": "Йеллоустоун", "description": "описание",
                                             "trailer": "описание", "year": "2013", "rating": "7", "genre_id": "9",
                                             "director_id": "18"}),

        self.movie_service.dao.update.assert_called_once_with(movie)

    def test_delete(self):
        self.movie_service.delete(1)
        self.movie_service.dao.delete.assert_called_once_with(1)
