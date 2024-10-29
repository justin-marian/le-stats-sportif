# Le Stats Sportif

## Objective

- Familiarization with classes, threads, synchronization, and Python modules for multithreading.
- Efficient use of synchronization elements threads and processes in a client-server `app`.

## Project Description

The project involves implementing a service that processes data requests based on a set of questions in `Flask`, using a CSV file, `nutrition_activity_obesity_usa_subset.csv`, to provide statistical insights.

### Dataset

The dataset can be accessed [here](https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system) and contains information on nutrition, physical activity, and obesity in the United States (2011–2022), collected by the U.S. Department of Health & Human Services.

#### Questions Set

The service should be able to respond to the following questions:

| Question                                                                                                                    |
|-----------------------------------------------------------------------------------------------------------------------------|
| Percentage of adults who engage in no leisure-time physical activity                                                        |
| Percentage of adults aged 18 years and older who are classified as obese                                                    |
| Percentage of adults aged 18 years and older classified as overweight                                                       |
| Percentage of adults achieving at least 300 minutes of moderate or 150 minutes of vigorous aerobic physical activity weekly |
| Other questions related to fruit and vegetable consumption, physical activity, etc.                                         |

The values required for calculations are in the `Data_Value` column.

## Multithread service

The service is multithreaded and will process requests in a job queue managed by a `Thread Pool`.

### Request Mechanics

| Endpoint                        | Description                                                                                       |
|---------------------------------|---------------------------------------------------------------------------------------------------|
| **/api/states_mean**            | Calculates the average `Data_Value` for each state for a specific question and sorts the results. |
| **/api/state_mean**             | Calculates the average `Data_Value` for a specific state and question.                            |
| **/api/best5**                  | Returns the top 5 states for a question (best scores).                                            |
| **/api/worst5**                 | Returns the last 5 states for a question (worst scores).                                          |
| **/api/global_mean**            | Calculates the global average of `Data_Value` for a question.                                     |
| **/api/diff_from_mean**         | Calculates the difference between `global_mean` and `state_mean` for all states.                  |
| **/api/state_diff_from_mean**   | Calculates the difference between `global_mean` and `state_mean` for a specific state.            |
| **/api/mean_by_category**       | Calculates the average `Data_Value` by category (`Stratification1`) for each state.               |
| **/api/state_mean_by_category** | Calculates the average `Data_Value` by category for a specific state.                             |
| **/api/graceful_shutdown**      | Allows the service to shut down after completing all current jobs.                                |
| **/api/jobs**                   | Returns the status of all jobs.                                                                   |
| **/api/num_jobs**               | Returns the number of remaining jobs.                                                             |
| **/api/get_results/<job_id>**   | Returns the results for a specific job.                                                           |

## Input/Output Structure

| Type   | Example                                                                                                        |
|--------|----------------------------------------------------------------------------------------------------------------|
| Input  | `{"question": "Percent of adults aged 18 years and older who have an overweight classification"}`              |
| Output | `{"status": "done", "data": <calculated_result>}`                                                              |

## Logging

To monitor service activity, implement logging with the `logging` module:

- **Log File**: Name the log file `webserver.log`, and use the `info` level to record all entries and exits for each route.
- **Rotating File Handler**: Use `RotatingFileHandler` to handle the log file rotation and set a maximum file size to keep log history.
- **Timestamps**: Set timestamps to UTC/GMT rather than local time for consistency across different time zones. Use `formatTime` to set this format.

### Example Logging Setup

The following is an example of setting up logging in Python:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler("webserver.log", maxBytes=2000, backupCount=5)
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Example log entry
logging.info("Service started")
```
