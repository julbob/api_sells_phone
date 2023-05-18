"""This script permit to insert a CSV file in the database.
To simplify the execution, this script delete all datas 
in table before starting the upload"""

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy
from sqlalchemy import Table
from src.shops.database.database import session, metadata, Product, Sell

products: Table = Table("products", metadata)
df: pd.DataFrame = pd.read_csv("data.csv")
df_by_product: DataFrameGroupBy
product: Product
sell: Sell

session.execute(products.delete())

df[["nom_produit", "nom_magasin"]] = (
    df[["nom_produit", "nom_magasin"]]
    .replace(r"\s+", " ", regex=True)
    .applymap(str.strip)
    .applymap(str.lower)
)
df_by_product = df.groupby(["nom_produit"])
for product, sells in df_by_product:
    product = Product(name=product[0])
    session.add(product)
    session.flush()  # Get the id of new product
    for _, df_sell in sells.iterrows():
        sell = Sell(
            shop=df_sell["nom_magasin"],
            product_id=product.id,
            sell_date=df_sell["date_vente"],
            price=float(df_sell["prix_vente"]),
        )
        session.add(sell)

session.commit()
