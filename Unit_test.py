import os

from pip._vendor import requests

from  main import app
import unittest

class FlaskrTestCase(unittest.TestCase):
    def test_no_file(self):
        response = app.test_client().get('/openfile')
        assert response.status_code == 400
    def test_file_correct(self):
        url = "http://127.0.0.1:5000/openfile"
        payload = {'person': 'False',
                   'start_date': '01-01-2020',
                   'end_date': '01-01-2020'}
        files = [('file', ('33.xml', open('33.xml', 'rb'), 'text/xml'))]
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        assert response.status_code == 200
        files[0][1][1].close()
    def test_file_correct_data_in_file(self):
        url = "http://127.0.0.1:5000/openfile"
        payload = {'person': 'False'}
        files = [('file', ('33.xml', open('33.xml', 'rb'), 'text/xml'))]
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        assert response.status_code == 200
        files[0][1][1].close()
    def test_file_correct_data_in_file_and_person_True(self):
        url = "http://127.0.0.1:5000/openfile"
        payload = {'person': 'True'}
        files = [('file', ('33.xml', open('33.xml', 'rb'), 'text/xml'))]
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        assert response.status_code == 200
        files[0][1][1].close()
    def test_file_incorrect(self):
        url = "http://127.0.0.1:5000/openfile"
        payload = {'person': 'False',
                   'start_date': '01-01-2020',
                   'end_date': '01-01-2020'}
        files = [('file', ('', open('33.xml', 'rb'), 'text/xml'))]
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        assert response.status_code == 200
        self.assertRegex(response.text.encode().decode('unicode_escape'),"Файл не найден")
        files[0][1][1].close()
    def test_path_incorrect(self):
        url = "http://127.0.0.1:5000/op3enfile"
        payload = {'person': 'False',
                   'start_date': '01-01-2020',
                   'end_date': '01-01-2020'}
        files = [('file', ('', open('33.xml', 'rb'), 'text/xml'))]
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        assert response.status_code == 404
        self.assertRegex(response.text.encode().decode('unicode_escape'), "Not found")
        files[0][1][1].close()
    def test_date_start_incorrect(self):
        def test_path_incorrect(self):
            url = "http://127.0.0.1:5000/op3enfile"
            payload = {'person': 'False',
                       'start_date': '01-01-2020',
                       'end_date': '01-01-1990'}
            files = [('file', ('', open('33.xml', 'rb'), 'text/xml'))]
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            assert response.status_code == 404
            self.assertRegex(response.text.encode().decode('unicode_escape'), "Дата начала больше даты окончания")
            files[0][1][1].close()


if __name__ == '__main__':
    unittest.main()