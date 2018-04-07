import unittest
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        super().setUp()

    def test_api_logs_without_params(self):
        response = self.app.get('/logs')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_api_logs_all_get_params(self):
        params = {
            'from': 1.383253541E12,
            'to': 1.383334735E12,
            'page': 1,
            'items': 20
        }
        response = self.app.get('/logs', query_string=params)
        self.assertTrue(len(response.data) > 0)

    def test_prepare_sql_query_log(self):
        pass

    def extract_ids_from_logs(self):
        pass

    def extract_enrich_logs(self):
        pass