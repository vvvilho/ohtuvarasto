"""Flask web interface for managing warehouses."""
# pylint: disable=too-many-statements
import math
from itertools import count

from flask import Flask, flash, redirect, render_template, request, url_for

from varasto import Varasto


def create_app(test_config=None):
    """Create the warehouse application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="warehouse-development-key",
        WAREHOUSES={},
        WAREHOUSE_IDS=count(1),
    )
    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        """Show all warehouses and their current balances."""
        return render_template(
            "index.html", warehouses=app.config["WAREHOUSES"].values()
        )

    @app.post("/warehouses")
    def create_warehouse():
        """Create a warehouse from the submitted name and capacity."""
        name = request.form.get("name", "").strip()
        capacity = parse_positive_number(request.form.get("capacity", ""))
        if not name:
            flash("Enter a name for the warehouse.", "error")
        elif capacity is None:
            flash("Capacity must be a positive number.", "error")
        else:
            warehouse_id = next(app.config["WAREHOUSE_IDS"])
            app.config["WAREHOUSES"][warehouse_id] = {
                "id": warehouse_id,
                "name": name,
                "inventory": Varasto(capacity),
            }
            flash(f"Warehouse ‘{name}’ created.", "success")
        return redirect(url_for("index"))

    @app.post("/warehouses/<int:warehouse_id>/items")
    def add_items(warehouse_id):
        """Add the requested quantity to a warehouse."""
        warehouse = app.config["WAREHOUSES"].get(warehouse_id)
        quantity = parse_positive_number(request.form.get("quantity", ""))
        if warehouse is None:
            flash("Warehouse not found.", "error")
        elif quantity is None:
            flash("Quantity must be a positive number.", "error")
        elif quantity > warehouse["inventory"].paljonko_mahtuu():
            flash("Not enough capacity for that quantity.", "error")
        else:
            warehouse["inventory"].lisaa_varastoon(quantity)
            message = f"Added {quantity:g} items to {warehouse['name']}."
            flash(message, "success")
        return redirect(url_for("index"))

    @app.post("/warehouses/<int:warehouse_id>/items/take")
    def take_items(warehouse_id):
        """Remove the requested quantity from a warehouse."""
        warehouse = app.config["WAREHOUSES"].get(warehouse_id)
        quantity = parse_positive_number(request.form.get("quantity", ""))
        if warehouse is None:
            flash("Warehouse not found.", "error")
        elif quantity is None:
            flash("Quantity must be a positive number.", "error")
        elif quantity > warehouse["inventory"].saldo:
            flash("Not enough items in the warehouse.", "error")
        else:
            warehouse["inventory"].ota_varastosta(quantity)
            message = f"Removed {quantity:g} items from {warehouse['name']}."
            flash(message, "success")
        return redirect(url_for("index"))

    return app


def parse_positive_number(value):
    """Return a finite positive number, or None for invalid input."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


application = create_app()


if __name__ == "__main__":
    application.run(debug=True)
