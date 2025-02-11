from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import update
from src.product.domain.model.product import Product
from src.product.domain.repository.product_repository import ProductRepository
from src.product.infrastructure.persistence.models import ProductModel
from src.shared.domain.value_objects import Money

class PostgresqlProductRepository(ProductRepository):
    """PostgreSQL implementation of ProductRepository"""

    def __init__(self, session: Session):
        self._session = session

    def save(self, product: Product) -> Product:
        """Saves a product and returns the saved entity"""
        product_model = ProductModel(
            name=product.name,
            current_price=product.current_price.amount
        )
        
        self._session.add(product_model)
        self._session.commit()
        self._session.refresh(product_model)
        
        return self._product_model_to_entity(product_model)

    def find_by_name(self, name: str) -> Optional[Product]:
        """Finds a product by name"""
        product_model = self._session.query(ProductModel).filter(
            ProductModel.name == name
        ).first()
        
        return self._product_model_to_entity(product_model) if product_model else None

    def find_all(self) -> List[Product]:
        """Returns all products ordered by name"""
        product_models = self._session.query(ProductModel).order_by(ProductModel.name).all()
        return [self._product_model_to_entity(pm) for pm in product_models]

    def update_price(self, product_id: int, new_price: Decimal) -> Product:
        """Updates product price"""
        try:
            product_model = self._session.query(ProductModel).filter(
                ProductModel.id == product_id
            ).first()
            
            if not product_model:
                raise ValueError(f"Product with id {product_id} not found")
            
            product_model.current_price = new_price
            self._session.commit()
            
            return self._product_model_to_entity(product_model)
        except Exception:
            self._session.rollback()
            raise

    def _product_model_to_entity(self, product_model: ProductModel) -> Product:
        """Converts ProductModel to Product domain entity"""
        return Product(
            id=product_model.id,
            name=product_model.name,
            current_price=Money(amount=product_model.current_price),
            created_at=product_model.created_at,
            updated_at=product_model.updated_at
        ) 