from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool


webserver = Flask(__name__)
webserver.data_ingestor = DataIngestor("./dataset.csv")
webserver.tasks_runner = ThreadPool(webserver.data_ingestor)
webserver.job_counter = 1


# if __name__ == "__main__":
#     webserver.run(debug=True)
