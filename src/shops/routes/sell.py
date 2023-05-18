"""Module with all routes to manage Sells table"""
import re
from typing import Any, Dict, List, Optional
from flask import Blueprint, Response, request, make_response
from sqlalchemy.exc import SQLAlchemyError
from src.shops.database.database import Product, Sell, session
from src.shops.auth.authentication import authenticate

blp_sells = Blueprint("sells", __name__)


@blp_sells.route("", methods=["POST"])
@authenticate()
def add_sell() -> Response:
    """Post one sell route"""
    data: Optional[Any]
    sell: Sell
    product: Optional[Product]
    product_name: str
    res: Response
    try:
        data = request.json
        if data is not None:
            if "product_name" in data.keys() and not "product_id" in data.keys():
                product_name = re.sub(r"\s+", " ", data["product_name"]).strip().lower()
                product = (
                    session.query(Product).filter_by(id=product_name).first()
                )
                if product is not None:
                    data["product_id"] = product.id
                else:
                    res = make_response(
                        "The product name does not exists in product table. \
                        Create product before add new sell"
                    )
            sell = Sell(
                shop=re.sub(r"\s+", " ", data["shop"]).strip().lower(),
                product_id=data["product_id"],
                sell_date=data["sell_date"],
                price=data["price"],
            )
            session.add(sell)
            session.commit()
            res = make_response("Sell added successfully", 200)
        else:
            res = make_response("No data in input", 412)
        return res
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during add sell", 400)


@blp_sells.route("", methods=["GET"])
def get_sells() -> Response:
    """Get all sells route"""
    limit: int
    offset: int
    sells: List[Sell]
    results: List[Dict] = []
    try:
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        sells = list(session.query(Sell).all())
        for sell in sells[offset : offset + limit]:
            results.append(sell.to_dict())
        return make_response(results, 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during get sells", 400)


@blp_sells.route("/<int:sell_id>", methods=["GET"])
def get_sell(sell_id: int) -> Response:
    """Get one sell route"""
    sell: Optional[Sell]
    try:
        sell = session.query(Sell).filter_by(id=sell_id).first()
        if not sell:
            return make_response("Sell not found", 404)
        return make_response(sell.to_dict(), 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during get sell " + str(sell_id), 400)


@blp_sells.route("/<int:sell_id>", methods=["PUT"])
@authenticate()
def update_sell(sell_id: int) -> Response:
    """Update one sell route"""
    data: Optional[Any]
    sell: Optional[Sell]
    try:
        data = request.json
        sell = session.query(Sell).filter_by(id=sell_id).first()
        if not sell:
            return make_response("Sell not found", 404)
        sell.update_line(data)
        session.commit()
        return make_response("Sell updated successfully", 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during update sell " + str(sell_id), 400)


@blp_sells.route("/<int:sell_id>", methods=["DELETE"])
@authenticate()
def delete_sell(sell_id: int):
    """Delete one sell route"""
    sell: Optional[Sell]
    try:
        sell = session.query(Sell).filter_by(id=sell_id).first()
        if not sell:
            return make_response("Sell not found", 404)
        session.delete(sell)
        session.commit()
        return make_response("Sell deleted successfully", 200)
    except SQLAlchemyError as sqlalce:
        session.rollback()
        print(str(sqlalce))
        return make_response("Error during delete sell " + str(sell_id), 400)
