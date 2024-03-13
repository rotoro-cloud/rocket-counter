import time
import random
import os
import redis
from flask import Flask, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

ROCKET_SIZE = os.environ.get('ROCKET_SIZE') or None

images = [

    "small.png",
    "average.png",
    "big.png",
    "fat.png"

]

def get_rocket_count():
    retries = 5
    while True:
        try:
            return cache.incr('rocket')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route("/getimage")
def get_img():
    count = get_rocket_count()
    if ROCKET_SIZE:
        image = ROCKET_SIZE + '.png'
    else:
        image = random.choice(images)
    return '{' + '"image": "{}", "count": "{}"'.format(image, count) + '}'

@app.route("/")
def hello():
    return render_template("img.html")
