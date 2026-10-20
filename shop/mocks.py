from unittest import mock

import requests

ECOSCORE_GRADE = 'd'


def mock_openfoodfact_success(*args, **kwargs):
    response = requests.Response()
    response.status_code = 200
    response.json = mock.Mock(return_value={'product': {'ecoscore_grade': ECOSCORE_GRADE}})
    return response


def mock_openfoodfact_failure(*args, **kwargs):
    response = requests.Response()
    response.status_code = 500
    return response
