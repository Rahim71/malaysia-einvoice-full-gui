from flask import Flask, request

app = Flask(__name__)

@app.route("/api/invoice", methods=["POST"])
def receive_invoice():
    xml = request.data.decode()
    print("✅ Received Invoice XML:")
    print(xml)
    return "Invoice received", 200

if __name__ == "__main__":
    app.run(port=5000)
