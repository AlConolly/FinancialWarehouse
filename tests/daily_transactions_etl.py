# import unittest, os
# from dotenv import load_dotenv
# from oracle.connection import DW_Interface
# from scripts.ETL.utils.daily_transactions import Daily_Transactions_ETL

# class DailyTransactionsTests(unittest.TestCase):
#     def setUp(self):
#         load_dotenv()
#         config_dir = os.getenv('CONFIG_DIR')
#         user = os.getenv('USER')
#         password = os.getenv('PASSWORD')
#         dsn = os.getenv('DSN')
#         wallet_location = os.getenv('WALLET_LOCATION')
#         wallet_password = os.getenv('WALLET_PASSWORD')
#         self.mock_dw_interface = DW_Interface(
#             config_dir, user, password, dsn, wallet_location, wallet_password)

#     def test_get_date_id(self):
#         test_class = Daily_Transactions_ETL(self.mock_dw_interface)
#         first_date = '2001-01-01'
#         second_date = '2022-02-01'
#         valid_result = test_class.get_date_id(first_date)
#         invalid_result = test_class.get_date_id(second_date)
#         self.assertEqual(valid_result, 4019)
#         self.assertNotEqual(invalid_result, 1)

# if __name__ == '__main__':
#     unittest.main()


# OLD TESTS
# TODO: Remove these tests once the new tests are working
