import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from src.order.application.get_sales_report import GetSalesReportQuery
from src.shared.domain.value_objects import DateTimeRange

class TestGetSalesReportQuery:
    @pytest.fixture
    def date_range(self):
        return DateTimeRange(
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now()
        )

    @pytest.fixture
    def mock_report(self):
        return [
            {
                "product_name": "Test Product",
                "total_quantity": 5,
                "total_price": Decimal("50.00")
            }
        ]

    def test_execute_success(self, mocker, date_range, mock_report):
        # Given
        mock_service = mocker.Mock()
        mock_service.get_product_sales_report.return_value = mock_report
        
        query = GetSalesReportQuery(mock_service)
        
        # When
        result = query.execute(date_range)
        
        # Then
        assert len(result) == 1
        assert result[0].product_name == mock_report[0]["product_name"]
        assert result[0].total_quantity == mock_report[0]["total_quantity"]
        assert result[0].total_price == mock_report[0]["total_price"]
        mock_service.get_product_sales_report.assert_called_once_with(
            start_date=date_range.start_date,
            end_date=date_range.end_date
        ) 