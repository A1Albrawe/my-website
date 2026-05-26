from flask import Blueprint, jsonify

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/cloud_submit_report', methods=['GET', 'POST'])
def cloud_submit_report():
    return jsonify({"status": "forbidden", "message": "This API has been permanently disabled by Admin."}), 403

@api_blueprint.route('/api/cloud_submit_analytics', methods=['POST'])
def cloud_submit_analytics():
    return jsonify({"status": "disabled"}), 200

@api_blueprint.route('/api/admin_get_all_data', methods=['GET'])
def admin_get_all_data():
    return jsonify({"status": "terminated"}), 410

@api_blueprint.route('/api/admin_clear_data', methods=['POST'])
def admin_clear_data():
    return jsonify({"status": "terminated"}), 410

@api_blueprint.route('/PASS', methods=['GET', 'POST'])
def admin_page(): 
    return "404 Not Found", 404
