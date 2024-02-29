from flask import Flask

app = Flask(__name__)

@app.route('/apply', methods=['GET'])
def apply_changes():
    # Execute the script to update sip.conf
    os.system('python script.py')
    return 'Changes applied successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
