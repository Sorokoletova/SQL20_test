from unittest.mock import MagicMock

import pytest
from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    director_dao.get_one = MagicMock(return_value=Director(id=1, name="Tom"))
    director_dao.get_all = MagicMock(return_value=["Tom", "Klaus"])
    director_dao.create = MagicMock(return_value=Director(id=3, name="Marsel"))
    director_dao.update = MagicMock(return_value=Director(id=1, name="Tomas"))
    director_dao.partially_update = MagicMock(return_value=Director(id=1, name="Tom"))
    director_dao.delete = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def durector_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.name == 'Tom'

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert directors is not None
        assert isinstance(directors, list)
        assert len(directors) == 2

    def test_create(self):
        director = self.director_service.create("Marsel")

        assert director is not None
        assert director.id == 3

    def test_update(self):
        director = self.director_service.update(3)

        assert director is not None
        assert director.name == 'Tomas'

    def test_partially_update(self):
        director = self.director_service.get_one(1)
        assert director is not None
        self.director_service.partially_update({"id": 1, "name": "Klaus"})
        self.director_service.dao.update.assert_called_once_with(director)

    def test_delete(self):
        self.director_service.delete(1)
        self.director_service.dao.delete.assert_called_once_with(1)
