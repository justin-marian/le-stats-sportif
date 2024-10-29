import os
import json
import logging
from flask import request, jsonify
from logging.handlers import RotatingFileHandler
from app import webserver

handler = RotatingFileHandler("webserver.log", maxBytes=2000, backupCount=5)
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def create_job(data, request_type):
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))
    logger.info(f"Job created with ID: {job_id}, request type: {request_type}")
    return jsonify({'job_id': job_id}), 200


def read_job_result(job_id):
    file_path = f"results/{job_id}.json"
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, mode="r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            logger.info(f"Job result retrieved for ID: {job_id}")
            return jsonify({'status': 'done', 'data': data}), 200
    logger.info(f"Job result still running for ID: {job_id}")
    return jsonify({'status': 'running'}), 200


@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    data = request.json
    logger.info("POST request received on /api/post_endpoint with data: %s", data)
    return jsonify({"message": "Received data successfully", "data": data}), 200


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    try:
        job_number = int(job_id.replace("job_id_", ""))
    except ValueError:
        logger.error("Invalid job_id: %s", job_id)
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'}), 500

    if job_number < 1 or job_number >= webserver.job_counter:
        logger.error("Job ID out of range: %s", job_id)
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'}), 500

    logger.info("GET request received on /api/get_results with job_id: %s", job_id)
    return read_job_result(job_number)


@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    running_jobs = sum(1 for i in range(1, webserver.job_counter)
                       if not os.path.isfile(f"results/{i}.json"))
    logger.info("GET request on /api/num_jobs. Running jobs count: %d", running_jobs)
    return jsonify({'num_jobs': running_jobs}), 200


@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = {f"job_id_{i}": "done" if os.path.isfile(f"results/{i}.json") else "running"
            for i in range(1, webserver.job_counter)}
    logger.info("GET request on /api/jobs. Jobs status: %s", jobs)
    return jsonify({'status': 'done', 'data': jobs}), 200


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def stop_server():
    webserver.tasks_runner.stop()
    logger.info("GET request on /api/graceful_shutdown. Shutting down server gracefully.")
    return jsonify({'status': 'done'}), 200


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    logger.info("POST request on /api/states_mean")
    return create_job(request.json, "states_mean")

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    logger.info("POST request on /api/state_mean")
    return create_job(request.json, "state_mean")

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    logger.info("POST request on /api/best5")
    return create_job(request.json, "best5")

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    logger.info("POST request on /api/worst5")
    return create_job(request.json, "worst5")

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    logger.info("POST request on /api/global_mean")
    return create_job(request.json, "global_mean")

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    logger.info("POST request on /api/diff_from_mean")
    return create_job(request.json, "diff_from_mean")

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    logger.info("POST request on /api/state_diff_from_mean")
    return create_job(request.json, "state_diff_from_mean")

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    logger.info("POST request on /api/mean_by_category")
    return create_job(request.json, "mean_by_category")

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    logger.info("POST request on /api/state_mean_by_category")
    return create_job(request.json, "state_mean_by_category")


def get_defined_routes():
    return [f"Endpoint: \"{rule}\" Methods: \"{', '.join(rule.methods)}\""
            for rule in webserver.url_map.iter_rules()]


@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    logger.info("GET request on /index")
    return "Home Route!\n" + \
           "Interact with the webserver using one of the defined routes:\n" + \
           ''.join(f"<p>{route}</p>" for route in routes)
