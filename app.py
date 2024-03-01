import os
import logging
from flask import Flask

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/apply', methods=['GET'])
def apply_changes():
    try:
        logger.debug("Attempting to apply changes")
        
        # Execute the script to update sip.conf
        os.system('python3 script.py')
        
        logger.debug("Changes applied successfully")
        return 'Changes applied successfully'

    except Exception as e:
        logger.error(f"An error occurred while applying changes: {e}")
        return 'An error occurred while applying changes', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
