from http import HTTPStatus

import pytest
from faker import Faker
from app.models.User import User

fake = Faker()

user_payload = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "avatar": fake.image_url()
}

@pytest.fixture(scope="function")
def create_user(envs, users_api):
    response_post = users_api.post(json=user_payload)
    user = User.model_validate(response_post.json())
    return user.id


class TestDeletionUser:

    def test_successful_removal(self, envs, users_api, create_user):
        response_delete = users_api.delete(create_user)
        assert response_delete.status_code == HTTPStatus.OK
        response_get = users_api.get(create_user)
        assert response_get.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
    def test_invalid_user_id(self, users_api, user_id):
        response_delete = users_api.delete(user_id)
        assert response_delete.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_double_removal(self, users_api, create_user):
        response_delete = users_api.delete(create_user)
        assert response_delete.status_code == HTTPStatus.OK
        response_delete_2 = users_api.delete(create_user)
        assert response_delete_2.status_code == HTTPStatus.NOT_FOUND

