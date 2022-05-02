from unittest.mock import MagicMock

import pytest
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_dao.get_one = MagicMock(return_value={"id": 1, "title": "Tom", "discription": "описание"})
    movie_dao.get_all = MagicMock(return_value=[{"id": 1, "name": "Tom"}, {"id": 2, "name": "Klaus"}])
    movie_dao.create = MagicMock(return_value={"id": 3, "name": "Marsel"})
    movie_dao.update = MagicMock(return_value={"id": 3, "name": "Tomas"})
    #    director_dao.partially_update = MagicMock(return_value={"id": 1, "name": "Klaus"})
    movie_dao.delete = MagicMock()

    return movie_dao


class TestMovieServise:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie["title"] == 'Tom'

    def test_get_all(self):
        movie = self.movie_service.get_all()

        assert movie is not None
        assert isinstance(movie, list)
        assert len(movie) == 2

    def test_create(self):
        movie = self.movie_service.create("Marsel")

        assert movie is not None
        assert movie["id"] == 3

    def test_update(self):
        movie = self.movie_service.update(3)

        assert movie is not None
        assert movie["name"] == 'Tomas'

    #    @pytest.mark.parametrize(('new_data', {"id": 1, "name": "Klaus"},))

    # def test_partially_update(self):
    #     director = self.director_service.get_one(1)
    #     assert director is not None
    #     # self.director_service.partially_update({"id": 1, "name": "Klaus"})
    #     # print(new_data)
    #     self.director_service.dao.update.assert_called_once_with({"id": 1, "name": "Klaus"})

    def test_delete(self):
        self.movie_service.delete(1)
        self.movie_service.dao.delete.assert_called_once_with(1)
