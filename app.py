from flask import Flask
from src.pipeline.process_pipeline import ProcessPipeline

application = Flask(__name__)

app = application


@app.route('/')
def index():
    return 'Home'


@app.route('/process-data', methods=['GET'])
def process_candidate_data():
    data_processing = ProcessPipeline()
    data_processing.initiate_data_processing()
    return 'Data Processing Completed'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
