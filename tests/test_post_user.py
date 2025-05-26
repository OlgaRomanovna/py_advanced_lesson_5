import copy
from http import HTTPStatus

from faker import Faker
from app.models.User import User

fake = Faker()

user_payload = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "avatar": fake.image_url()
}


class TestCreationUser:

    def test_successful_creation(self, users_api):
        response_post = users_api.post(json=user_payload)
        assert response_post.status_code == HTTPStatus.CREATED
        user = User.model_validate(response_post.json())
        response_get = users_api.get_by_id(user.id)
        assert response_get.status_code == HTTPStatus.OK
        get_user = User.model_validate(response_get.json())
        assert user.id == get_user.id

    def test_invalid_email(self, users_api):
        copy_data = copy.deepcopy(user_payload)
        copy_data["email"] = "email"
        response_post = users_api.post(json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_invalid_avatar(self, users_api):
        copy_data = copy.deepcopy(user_payload)
        copy_data["avatar"] = "avatar"
        response_post = users_api.post(json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_invalid_first_name(self, users_api):
        copy_data = copy.deepcopy(user_payload)
        copy_data["first_name"] = 12345
        response_post = users_api.post( json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_without_last_name(self, users_api):
        copy_data = copy.deepcopy(user_payload)
        copy_data.pop("last_name")
        response_post = users_api.post(json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
