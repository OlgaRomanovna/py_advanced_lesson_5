from http import HTTPStatus

import pytest
from app.models.User import User
from tests.conftest import users_api


class TestGetUserById:

    def test_user(self, users_api):
        response_users = users_api.get_all()
        user = User.model_validate(response_users.json()["items"][0])
        response = users_api.get_by_id(user.id)
        assert response.status_code == HTTPStatus.OK

        User.model_validate(response.json())

    @pytest.mark.parametrize("user_id", [35])
    def test_user_nonexistent_values(self, users_api, user_id):
        response = users_api.get_by_id(user_id)
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
    def test_user_invalid_values(self, users_api, user_id):
        response = users_api.get_by_id(user_id)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", [35])
    def test_method_not_allowed(self, users_api, user_id):
        response = users_api.post(user_id)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
