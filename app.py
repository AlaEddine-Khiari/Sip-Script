import os
import logging
import psycopg2
from flask import Flask

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_internals_user():
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

        # Fetch the data
        rows = cur.fetchall()

        # Close the cursor and connection
        cur.close()
        conn.close()

        return rows

    except Exception as e:
        logger.error(f"Error fetching data from PostgreSQL: {e}")
        raise  # Raise the exception to be caught in the caller function

def find_last_internals_index(lines):
    """Find the line index"""
    last_internals_index = -1
    for i, line in enumerate(lines):
        if line.startswith('; Configuration for internal extensions'):
            last_internals_index = i
    return last_internals_index

def update_sip_conf(sip_conf_path):
    try:
        with open(sip_conf_path, 'r') as f:
            lines = f.readlines()

        last_internals_index = find_last_internals_index(lines)

        if last_internals_index == -1:
            raise Exception('Verify sip.conf file')

        # Remove lines after the line
        lines = lines[:last_internals_index + 1]

        # Fetch all users from the database
        users = fetch_internals_user()
        
        # Add new user lines from the database
        for user in users:
            exten, secret = user
            lines.append(f'[{exten}](COMMON)\n')
            lines.append(f'secret={secret}\n')
            lines.append('\n')  # Add an empty line after each user entry

        # Write the updated content back to sip.conf
        with open(sip_conf_path, 'w') as f:
            f.writelines(lines)

        logger.info("sip.conf updated successfully")

    except Exception as e:
        logger.error(f"Error updating sip.conf: {e}")
        raise  # Raise the exception to be caught in the caller function

def update_voicemail_conf(voicemail_conf_path):
    try:
        with open(voicemail_conf_path, 'r') as f:
            lines = f.readlines()

        last_internals_index = find_last_internals_index(lines)

        if last_internals_index == -1:
            raise Exception('Verify voicemail.conf file')

        # Remove lines after the line
        lines = lines[:last_internals_index + 1]

        # Fetch all users from the database
        users = fetch_internals_user()

        # Add new user lines from the database
        for user in users:
            exten, _ = user
            lines.append(f'{exten} => {exten}\n')
            lines.append('\n')  # Add an empty line after each user entry

        # Write the updated content back to voicemail.conf
        with open(voicemail_conf_path, 'w') as f:
            f.writelines(lines)

        logger.info("voicemail.conf updated successfully")

    except Exception as e:
        logger.error(f"Error updating voicemail.conf: {e}")
        raise  # Raise the exception to be caught in the caller function

@app.route('/apply', methods=['GET'])
def apply_changes():
    sip_path = '/app/sip.conf'
    voicemail_path = '/app/voicemail.conf'
    try:
        update_sip_conf(sip_path)
        update_voicemail_conf(voicemail_path)
        return 'Changes applied successfully'
    except Exception as e:
        return f'An error occurred while applying changes: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
