import json
import unittest
from flask import Flask
from backend.controllers.supplier import supplier_blueprint


class SupplierControllerTests(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(supplier_blueprint)
        self.client = self.app.test_client()

    def test_find_all_suppliers(self):
        response = self.client.get('/supplier/find_all_suppliers')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_create_supplier(self):
        supplier_data = {
            "name": "TestSupplier",
            "address": "TestAddress",
            "cep": "54321-876",
            "cnpj": "98765432109876"
        }

        response = self.client.post('/supplier/create_supplier', data=json.dumps(supplier_data),
                                    content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_update_supplier(self):
        supplier_data = {
            "name": "UpdatedName",
            "address": "UpdatedAddress"
        }

        response = self.client.put('/supplier/update_supplier/1', data=json.dumps(supplier_data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_delete_supplier(self):
        response = self.client.delete('/supplier/delete_supplier/1')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
