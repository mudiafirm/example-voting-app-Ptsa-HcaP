from flask import Flask, render_template, request, make_response, g, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, multiprocess
import time
from redis import Redis
import os
import socket
import random
import json
import logging

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)

app.logger.setLevel(logging.INFO)

REQUEST_COUNT = Counter(
    "vote_http_requests_total",
    "Total HTTP requests handled by the Vote application",
    ["method", "endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "vote_http_request_duration_seconds",
    "HTTP request processing duration in seconds",
    ["method", "endpoint"],
)

@app.before_request
def start_request_timer():
    g.request_start_time = time.perf_counter()

@app.after_request
def record_request_metrics(response):
    if request.path != "/metrics":
        endpoint = request.endpoint or request.path
        REQUEST_COUNT.labels(
            request.method, endpoint, str(response.status_code)
        ).inc()

        start_time = getattr(g, "request_start_time", None)
        if start_time is not None:
            REQUEST_LATENCY.labels(
                request.method, endpoint
            ).observe(time.perf_counter() - start_time)

    return response

@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return Response(
        generate_latest(registry),
        mimetype=CONTENT_TYPE_LATEST,
    )

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
