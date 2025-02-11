import pytest
from decimal import Decimal
from datetime import datetime
from src.product.application.get_products import GetProductsQuery
from src.product.domain.model.product import Product
from src.shared.domain.value_objects import Money

class TestGetProductsQuery:
    @pytest.fixture
    def mock_product(self):
        now = datetime.utcnow()
        return Product(
            id=1,
            name="Test Product",
            current_price=Money(amount=Decimal("10.00")),
            created_at=now,
            updated_at=now
        )

    def test_execute_success(self, mocker, mock_product):
        # Given
        mock_service = mocker.Mock()
        mock_service.get_all_products.return_value = [mock_product]
        
        query = GetProductsQuery(mock_service)
        
        # When
        result = query.execute()
        
        # Then
        assert len(result) == 1
        assert result[0].id == mock_product.id
        assert result[0].name == mock_product.name
        assert result[0].current_price == mock_product.current_price.amount
        assert result[0].created_at == mock_product.created_at
        assert result[0].updated_at == mock_product.updated_at
        mock_service.get_all_products.assert_called_once() 