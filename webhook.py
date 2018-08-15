"""local usage"""

from flask import Flask, request
from controller import handle_request

webhook = Flask(__name__)

@webhook.route("/", methods=['GET', 'POST'])
def main():
    return handle_request(request)

if __name__ == "__main__":
    webhook.run(debug=True, host="0.0.0.0", port=8080)