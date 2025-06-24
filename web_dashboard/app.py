# web_dashboard/app.py
# Wannan fayil din zai zama backend na web dashboard (misali, Flask ko FastAPI).
# Zai kula da database, API endpoints, da kuma serving na frontend files.

from flask import Flask, render_template, request, jsonify
import os
import json
import asyncio
from datetime import datetime

# Import daga core module
from core.checker import check_token_details
# Daga config/settings.py
from config.settings import FLASK_SECRET_KEY

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# Database (misali: SQLite mai sauki don demo)
# A ainihin aikin, zaka yi amfani da PostgreSQL ko MySQL
DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'database.json')

def load_data():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'w') as f:
            json.dump({"checks": []}, f)
    with open(DATABASE_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    """Babban shafin dashboard."""
    return render_template('index.html')

@app.route('/api/check_token', methods=['POST'])
async def api_check_token():
    """API endpoint don binciken token daga dashboard."""
    data = request.get_json()
    contract_address = data.get('contract_address')

    if not contract_address:
        return jsonify({'error': 'Missing contract_address'}), 400

    try:
        # Kira async function daga core
        result = await check_token_details(contract_address)
        if result:
            db_data = load_data()
            result['timestamp'] = datetime.now().isoformat()
            db_data['checks'].append(result)
            save_data(db_data)
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Could not retrieve token details. Check contract address or API status.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def api_history():
    """API endpoint don samun tarihin bincike."""
    db_data = load_data()
    # Koda yaushe a dawo da sabbin bayanan farko
    sorted_checks = sorted(db_data['checks'], key=lambda x: x.get('timestamp', ''), reverse=True)
    return jsonify(sorted_checks), 200

if __name__ == '__main__':
    # Fara database idan bata nan
    load_data()
    # Gudanar da Flask app. Zaka iya canza port ko host
    app.run(debug=True, host='0.0.0.0', port=5000)
