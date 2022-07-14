from flask import url_for
import pytest
import mock

from csv_poc.database.models import File
from csv_poc.utils.exc import DatabaseOpsException


class TestFileNamespace:
    def test_get_file_list(self, app, db, client):
        response = client.get(url_for("api_v1.get_file_list"))
        data = response.get_json()
        assert response.status_code == 200
        assert isinstance(data, list)

    @mock.patch(
        "csv_poc.api.v1.files_dao.FileDAO.list_files",
        side_effect=DatabaseOpsException(message="test message", data=None),
    )
    def test_get_file_list_database_error(self, app, db, client):
        file = File.create(name="testing", path="testing")
        response = client.get(url_for("api_v1.get_file_list"))
        data = response.get_json()
        print(data)
        assert response.status_code == 500
        assert data["message"] == "test message"
        assert data["data"] is None

    def test_get_missing_file(self, app, db, client):
        response = client.get(url_for("api_v1.get_file", file_id=100))
        data = response.get_json()
        assert response.status_code == 404
        assert data["message"] is not None
        assert data["data"] is None

    def test_get_file(self, app, db, client):
        file = File.create(name="testing", path="testing")
        response = client.get(url_for("api_v1.get_file", file_id=file.id))
        data = response.get_json()
        assert response.status_code == 200
        assert data["name"] == file.name
        assert data["path"] == file.path
        assert len(data["columns"]) == 0

    @mock.patch(
        "csv_poc.api.v1.files_dao.FileDAO.get_file",
        side_effect=DatabaseOpsException(message="test message", data=None),
    )
    def test_get_file_database_error(self, app, db, client):

        file = File.create(name="testing", path="testing")
        response = client.get(url_for("api_v1.get_file", file_id=file.id))
        data = response.get_json()
        assert response.status_code == 500
        assert data["message"] == "test message"
        assert data["data"] is None
