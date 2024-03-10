import oracledb

class DW_Interface:
    def __init__(self, config_dir, user, password, dsn, wallet_location, wallet_password):
        self.connection = oracledb.connect(
            config_dir=config_dir,
            user=user,
            password=password,
            dsn=dsn,
            wallet_location=wallet_location,
            wallet_password=wallet_password,
        )