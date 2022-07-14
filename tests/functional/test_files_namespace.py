from flask import url_for
import mock
import os

from csv_poc.database.models import File
from csv_poc.utils.exc import DatabaseOpsException

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, "..", os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


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

    def test_upload_file_success(self, app, db, client):
        data = {}
        file_path = os.path.join(PROJECT_ROOT, "sample.csv")
        with open(file_path, "rb") as file:
            data["file"] = file
            response = client.post(
                url_for("api_v1.get_file_list"),
                data=data,
                follow_redirects=True,
                content_type="multipart/form-data",
            )
            resp_json = response.get_json()
            assert "sample.csv" in resp_json["name"]

    def test_upload_file_bad_ext(self, app, db, client):
        data = {}
        file_path = os.path.join(PROJECT_ROOT, "README.md")
        with open(file_path, "rb") as file:
            data["file"] = file
            response = client.post(
                url_for("api_v1.get_file_list"),
                data=data,
                follow_redirects=True,
                content_type="multipart/form-data",
            )
            resp_json = response.get_json()
            assert response.status_code == 400
            assert resp_json["message"] is not None
