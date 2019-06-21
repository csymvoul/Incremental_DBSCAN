from flask import Flask, send_file

app = Flask(__name__)


@app.route('/get_cluster_limits')
def get_cluster_limits():
    try:
        return send_file('../json_exports/cluster_limits.json')
    except:
        return "Clusters not created yet"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
