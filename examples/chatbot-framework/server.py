import os
import requests
import time
import json

from http.server import HTTPServer, BaseHTTPRequestHandler

CHANNEL_ID = os.getenv('HEALTH_CHECK_CHANNEL_ID')
URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
PORT = 8001


def call_api(url, method, data=None):
    headers = {
        "Authorization": f"Bot {os.getenv('DISCORD_HEALTH_CHECK_TOKEN')}",
        "Content-Type": "application/json"
    }

    if (method == "GET"):
        response = requests.get(url, headers=headers)
    elif (method == "POST"):
        response = requests.post(url, headers=headers, json=data)
    else:
        raise Exception(f"Invalid method - {method}")

    return response



def write_json_response(self,object):
    # Convert the dictionary to a JSON string
    response_json = json.dumps(object)
    # Write the JSON string to the response body
    self.wfile.write(response_json.encode('utf-8'))

def default_response(self,object):
    self.send_response(500)
    self.end_headers()
    write_json_response(self, object)

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            if CHANNEL_ID:
                send_message_response = call_api(
                    URL, "POST", {
                        "content": "ping"
                    })

                if (send_message_response.status_code == 200):
                    time.sleep(5)
                    get_message_response = call_api(
                        f"{URL}?limit=1", "GET")
                    if (get_message_response.status_code == 200):
                        content = get_message_response.json()[0]["content"]

                        if (content == "online"):
                            # Set the response status code and content type
                            self.send_response(200)
                            self.end_headers()
                            write_json_response(self,{"success":True})
                        else:
                            default_response(self, {
                                             "success": False, "error": f"Invalid response from get message API - {content}"})
                    else:
                        default_response(self, {
                            "success": False, "error": f"Got {get_message_response.status_code} status code from get_message API"})
                else:
                    default_response(self, {
                        "success": False, "error": f"Got {send_message_response.status_code} status code from send message API"})
            else:
                default_response(self, {
                    "success": False, "error": "In env, HEALTH_CHECK_CHANNEL_ID is missing"})
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')


# Set up the HTTP server
httpd = HTTPServer(('localhost', PORT), MyRequestHandler)
print(f"Server started on http://localhost:{PORT}")
httpd.serve_forever()
