from app.products import models, schemas
from sqlalchemy.orm import Session


def create_new_product(
    product: schemas.ProductIn, database: Session
) -> schemas.ProductOut:

    new_product = models.Product(**product.dict())
    database.add(new_product)
    database.commit()
    database.refresh(new_product)

    return schemas.ProductOut.from_orm(new_product)


def delete_existing_product(product_id: str, database: Session) -> None:
    result = (
        database.query(models.Product).filter(models.Product.id == product_id).delete()
    )
    if not result:
        raise ValueError("Product not found")

    database.commit()


def get_existing_product(product_id: str, database: Session) -> schemas.ProductOut:
    product = database.query(models.Product).get(product_id)
    if not product:
        raise ValueError("Product not found")

    return schemas.ProductOut.from_orm(product)


def get_all_products(database: Session) -> schemas.ProductsOutCollection:
    products = database.query(models.Product)

    return schemas.ProductsOutCollection(
        products=[schemas.ProductOut.from_orm(product) for product in products]
    )


def update_a_product(
    product_id: str, product: schemas.ProductIn, database: Session
) -> schemas.ProductOut:
    product_to_update = database.query(models.Product).get(product_id)
    if not product_to_update:
        raise ValueError("Product not found")

    for key, value in product.dict().items():
        setattr(product_to_update, key, value)

    database.commit()

    return schemas.ProductOut.from_orm(product_to_update)
