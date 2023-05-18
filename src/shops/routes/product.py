"""Module with all routes to manage Products table"""
import re
from typing import Any, Dict, List, Optional
from flask import Blueprint, Response, request, make_response
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.shops.database.database import Product, session
from src.shops.auth.authentication import authenticate


blp_products: Blueprint = Blueprint("product", __name__)


@blp_products.route("", methods=["POST"])
@authenticate()
def add_product() -> Response:
    """Post one product route"""
    data: Optional[Any]
    product: Product
    res: Response
    try:
        data = request.json
        if data is not None:
            product = Product(name=re.sub(r"\s+", " ", data["name"]).strip().lower())
            session.add(product)
            session.commit()
            res = make_response("Product added successfully", 200)
        else:
            res = make_response("No data in input", 412)
        return res
    except IntegrityError as intege:
        session.rollback()
        print(str(intege))
        return make_response("Product already exists", 409)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during add product", 400)


@blp_products.route("", methods=["GET"])
def get_products() -> Response:
    """Get all products route"""
    products: List[Product]
    results: List[Dict] = []
    limit: int
    offset: int
    try:
        products = list(session.query(Product).all())
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        for product in products[offset : offset + limit]:
            results.append(product.to_dict())
        return make_response(results, 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during get product", 400)


@blp_products.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> Response:
    """Get one product route"""
    product: Optional[Product]
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            return make_response("Product not found", 404)
        return make_response(product.to_dict(), 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during get product " + str(product_id), 400)


@blp_products.route("/<int:product_id>", methods=["PUT"])
@authenticate()
def update_product(product_id: int) -> Response:
    """Update one product route"""
    product: Optional[Product]
    data: Optional[Any]
    try:
        data = request.json
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            return make_response("Product not found", 404)
        product.update_line(data)
        session.commit()
        return make_response("Product updated successfully", 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during updated product " + str(id), 400)


@blp_products.route("/<int:product_id>", methods=["DELETE"])
@authenticate()
def delete_product(product_id: int) -> Response:
    """Delete one product route"""
    product: Optional[Product]
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            return make_response("Product not found", 404)
        session.delete(product)
        session.commit()
        return make_response("Product deleted successfully", 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during delete product " + str(product_id), 400)
