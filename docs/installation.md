# Installation Instructions

## Virtual Environment Setup

It is recommended to use a virtual environment to install the required packages for this project. To create a virtual environment, run the following command in the terminal:

```bash
python3 -m venv venv
```

To activate the virtual environment, run the following command in the terminal:

```bash
. venv/Scripts/activate
```

### Install Required Packages

To install the required packages, run the following command in the terminal:

```bash
pip install -r requirements.txt
```

**Note:** Make sure to activate the virtual enviroment before running the above command.

## Database Connection Setup

To connect to the database, create a `.env` file in the root directory of the project and add the values from our database connection values.

Example `.env` file:

```
CONFIG_DIR="C:\\opt\\OracleCloud\\<wallet_dir>"
USER=""
PASSWORD=""
DSN="<wallet_name>_low"
WALLET_LOCATION="C:\\opt\\OracleCloud\\<wallet_name>"
WALLET_PASSWORD=""
ALPHA_ADVANTAGE_API_KEY=""
```

Add the wallet files from Oracle into this directory on your computer.

```bash
C:\opt\OracleCloud\JSX031OXSTSUSO9D
```

## Running the Application

To run the application, run the following command in the terminal:

```bash
python3 main.py
```
