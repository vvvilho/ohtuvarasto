"""Tests for the warehouse web interface."""
import unittest

from app import create_app


class TestWarehouseWebApp(unittest.TestCase):
    """Exercise warehouse creation and inventory actions through HTTP."""

    def setUp(self):
        self.app = create_app({"TESTING": True, "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def test_home_page_shows_empty_state(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No warehouses yet", response.data)

    def test_create_warehouse_and_manage_inventory(self):
        response = self.client.post(
            "/warehouses", data={"name": "Main storage", "capacity": "10"}
        )

        self.assertEqual(response.status_code, 302)
        warehouse = self.app.config["WAREHOUSES"][1]
        self.assertEqual(warehouse["name"], "Main storage")

        self.client.post("/warehouses/1/items", data={"quantity": "6"})
        self.assertEqual(warehouse["inventory"].saldo, 6)

        self.client.post("/warehouses/1/items/take", data={"quantity": "2"})
        self.assertEqual(warehouse["inventory"].saldo, 4)

        page = self.client.get("/")
        self.assertIn(b"Main storage", page.data)
        self.assertIn(b"4.0", page.data)

    def test_rejects_invalid_warehouse_and_inventory_inputs(self):
        response = self.client.post(
            "/warehouses", data={"name": " ", "capacity": "nan"}, follow_redirects=True
        )
        self.assertIn(b"Enter a name for the warehouse", response.data)
        self.assertEqual(self.app.config["WAREHOUSES"], {})

        self.client.post("/warehouses", data={"name": "Small", "capacity": "5"})
        response = self.client.post(
            "/warehouses/1/items", data={"quantity": "6"}, follow_redirects=True
        )
        self.assertIn(b"Not enough capacity", response.data)
        self.assertEqual(self.app.config["WAREHOUSES"][1]["inventory"].saldo, 0)

        response = self.client.post(
            "/warehouses/1/items/take", data={"quantity": "1"}, follow_redirects=True
        )
        self.assertIn(b"Not enough items", response.data)
        self.assertEqual(self.app.config["WAREHOUSES"][1]["inventory"].saldo, 0)


if __name__ == "__main__":
    unittest.main()
