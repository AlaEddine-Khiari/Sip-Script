import os
import psycopg2

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

        # Execute a SELECT query to fetch data from 'internals_numbers' table
        cur.execute("SELECT extension, secret FROM internals_numbers")

        # Fetch the first row (assuming one row contains one username and password)
        row = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        conn.close()

        return row

    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return None
# Get the file path from environment variable
        sip_conf_path = os.environ.get('SIP_CONF_PATH')
def update_sip_conf(sip_conf_path):
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

        # Remove lines after the last "internals" user line
        lines = lines[:last_internals_index + 1]

        # Add new user lines from the database
        new_exten, new_secret = fetch_internals_user()
        lines.append(f'[{new_exten}](COMMON)\n')
        lines.append(f'secret={new_secret}\n')
        lines.append('\n')  # Add an empty line after each user entry

        # Write the updated content back to sip.conf
        with open(sip_conf_path, 'w') as f:
            f.writelines(lines)

        print("sip.conf updated successfully")

    except Exception as e:
        print(f"Error updating sip.conf: {e}")

if __name__ == "__main__":
    # Call function to update sip.conf with user from the database
    update_sip_conf()
