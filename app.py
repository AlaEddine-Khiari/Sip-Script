import os
import logging
from flask import Flask, jsonify

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/apply', methods=['GET'])
def apply_changes():
    try:
        # Execute the script to update sip.conf
        os.system('python3 script.py')
        return 'Changes applied successfully'
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 'File not found', 404
    except Exception as e:
        logger.error(f"Error applying changes: {e}")
        return 'An error occurred while applying changes', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
