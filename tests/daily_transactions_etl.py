import unittest
from unittest.mock import Mock, patch
from oracle.connection import DW_Interface
from scripts.ETL.utils.daily_transactions import Daily_Transactions_ETL


class TestGetDateId(unittest.TestCase):
    def test_get_date_id(self):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [1]
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_dw_interface = Mock()
        mock_dw_interface.connection = mock_connection
        test_class = Daily_Transactions_ETL(mock_dw_interface)
        test_date = '89-01-13'
        result = test_class.get_date_id(test_date)
        print(result)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
