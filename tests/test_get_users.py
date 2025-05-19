from http import HTTPStatus

import pytest

from app.models.User import ListUserPaginationModel


class TestGetUsers:


    def test_users(self, users_api) -> None:
        response = users_api.get_all()
        assert response.status_code == HTTPStatus.OK
        users_data = ListUserPaginationModel.model_validate(response.json())

        assert isinstance(users_data.items, list)
        assert len(users_data.items) > 0


    def test_users_no_duplicates(self, users_api) -> None:
        users = users_api.get_all()
        users_ids = [user.id for user in users.items]
        assert len(users_ids) == len(set(users_ids))


    @pytest.mark.parametrize("size", [2, 4, 7])
    def test_pagination_size(self, users_api, size: int) -> None:
        response = users_api.get_paginated(size)
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        assert len(data.items) == size


    @pytest.mark.parametrize("size", [1, 2, 3])
    def test_pagination_total_pages(self, users_api, users: ListUserPaginationModel, size: int) -> None:
        response = users_api.get_paginated(size)
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        expected_pages = (users.total + size - 1) // size
        assert data.pages == expected_pages


    @pytest.mark.parametrize("page_one, page_two", [(1, 2)])
    @pytest.mark.parametrize("size", [5])
    def test_pagination_different_pages(self, users_api, page_one: int, page_two: int, size: int) -> None:

        response_page_1 = users_api.get_paginated(page_one, size)
        response_page_2 = users_api.get_paginated(page_two, size)

        assert response_page_1.status_code == HTTPStatus.OK
        assert response_page_2.status_code == HTTPStatus.OK

        data_page_1 = ListUserPaginationModel.model_validate(response_page_1.json())
        data_page_2 = ListUserPaginationModel.model_validate(response_page_2.json())

        ids_page_1 = {user.id for user in data_page_1.items}
        ids_page_2 = {user.id for user in data_page_2.items}

        assert ids_page_1, "Список пользователей на странице 1 пуст!"
        assert ids_page_2, "Список пользователей на странице 2 пуст!"
        assert ids_page_1.isdisjoint(ids_page_2), "Данные на страницах не должны пересекаться!"

        assert len(data_page_1.items) == size, f"Ожидалось {size} объектов на странице 1, получено {len(data_page_1.items)}"
        assert len(data_page_2.items) <= size, f"Ожидалось не более {size} объектов на странице 2, получено {len(data_page_2.items)}"


    @pytest.mark.parametrize("page, size", [(1, 2), (1, 5), (2, 3)])
    def test_pagination_correct_pages(self, users_api, page: int, size: int) -> None:
        response = users_api.get_paginated(page, size)
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        expected_pages = (data.total + size - 1) // size
        assert data.pages == expected_pages, f"Ожидалось {expected_pages} страниц, получено {data.pages}"


    @pytest.mark.parametrize("size", [3, 5, 10])
    def test_pagination_response_fields(self, users_api, size: int) -> None:
        response = users_api.get_paginated(size)
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        assert isinstance(data.page, int)
        assert isinstance(data.size, int)
        assert isinstance(data.total, int)
        assert isinstance(data.pages, int)
        assert isinstance(data.items, list)
