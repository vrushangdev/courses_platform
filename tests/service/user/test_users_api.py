import json
import mock
import pytest

from app.domain.user import User
from app.response_objects import ResponseSuccess
from app.serializers.json_user_serializer import UserJsonEncoder


class TestUsersApi:

    @mock.patch('app.application.user.queries.get_all.GetAllUsersQuery')
    @pytest.mark.parametrize('response_val', [([User('test@gmail.com')]), ([])])
    def test_users_api_returns_list_of_users(self, mock_query, client, response_val):
        response = ResponseSuccess.build_response_success(response_val)
        mock_query().execute.return_value = response

        http_response = client.get('/api/users')
        users_data = json.dumps(response_val, cls=UserJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(users_data)
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('app.application.user.commands.create.CreateUserCommand')
    def test_users_api_creates_new_user(self, mock_command, client, user):
        response = ResponseSuccess.build_response_resource_created(user)
        mock_command().execute.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = json.dumps(dict(email='test@gmail.com'))

        http_response = client.post('/api/users', data=data, headers=headers)
        user_data = json.dumps(user, cls=UserJsonEncoder)

        _, kwargs = mock_command().execute.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(user_data)
        mock_command().execute.assert_called()
        assert kwargs['request'].email == 'test@gmail.com'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
