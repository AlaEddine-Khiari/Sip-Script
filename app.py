import os
import psycopg2
import logging

from flask import Flask

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG
logger = logging.getLogger(__name__)

app = Flask(__name__)

def update_sip_conf(sip_conf_path):
        try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

        # Create a cursor
        cur = conn.cursor()

        # Execute a SELECT query to fetch data from 'internal_numbers' table
        cur.execute("SELECT extension, secret FROM internal_numbers")

        # Fetch the first row (assuming one row contains one username and password)
        row = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        conn.close()

        logger.debug(f"Fetched internals user: {row}")  # Log debug information

        return row

    except Exception as e:
        logger.error(f"Error fetching data from PostgreSQL: {e}")  # Log error
        return None
    try:
        with open(sip_conf_path, 'r') as f:
            lines = f.readlines()

        # Find the last "internals" user line
        last_internals_index = -1
        for i, line in enumerate(lines):
            if line.startswith('; Configuration for internal extensions'):
                last_internals_index = i

        if last_internals_index == -1:
            raise Exception('verify sip.conf file')

        # Remove lines after the line
        lines = lines[:last_internals_index + 1]

        # Add new user lines from the database
        new_exten, new_secret = fetch_internals_user()
        lines.append(f'[{new_exten}](COMMON)\n')
        lines.append(f'secret={new_secret}\n')
        lines.append('\n')  # Add an empty line after each user entry

        # Write the updated content back to sip.conf
        with open(sip_conf_path, 'w') as f:
            f.writelines(lines)

        logger.debug("sip.conf updated successfully")  # Log debug information

    except Exception as e:
        logger.error(f"Error updating sip.conf: {e}")  # Log error

@app.route('/apply', methods=['GET'])
def apply_changes():
    try:
        # Execute the script to update sip.conf
        sip_conf_path = os.environ.get('SIP_CONF_PATH')
        update_sip_conf(sip_conf_path)
        return 'Changes applied successfully'

    except Exception as e:
        logger.error(f"Error applying changes: {e}")  # Log error
        return 'An error occurred while applying changes', 500  # Return 500 Internal Server Error status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
