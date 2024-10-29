# Le Stats Sportif

## Objective

- **Familiarize** with classes, threads, synchronization, and Python modules for multithreading.
- **Efficiently utilize** synchronization elements and processes in a client-server `app`.

## Project Description

This project implements a **Flask-based service** that processes data requests from a set of questions, leveraging a CSV file, `nutrition_activity_obesity_usa_subset.csv`, to provide statistical insights.

### Dataset

Access the dataset [here](https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system), containing information on **nutrition, physical activity, and obesity in the United States (2011–2022)** collected by the U.S. Department of Health & Human Services.

### Questions Set

The service can respond to the following predefined questions:

#### Minimum Desired Values

For these questions, the goal is to minimize the `Data_Value`.

- *Percent of adults aged 18 years and older who have an overweight classification*
- *Percent of adults aged 18 years and older who have obesity*
- *Percent of adults who engage in no leisure-time physical activity*
- *Percent of adults who report consuming fruit less than one time daily*
- *Percent of adults who report consuming vegetables less than one time daily*

#### Maximum Desired Values

For these questions, the goal is to maximize the `Data_Value`.

- *Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)*
- *Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week*
- *Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)*
- *Percent of adults who engage in muscle-strengthening activities on 2 or more days a week*

The service calculates results based on the above questions, applying minimum or maximum criteria as specified.

## Multithreaded Service

The service is **multithreaded** and processes requests using a job queue managed by a **Thread Pool**.

### Request Mechanics

| Endpoint                                                              | Description                                                                                       |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [/api/states_mean](http://127.0.0.1:5000/api/states_mean)             | Calculates the average `Data_Value` for each state for a specific question and sorts the results. |
| [/api/state_mean](http://127.0.0.1:5000/api/state_mean)               | Calculates the average `Data_Value` for a specific state and question.                            |
| [/api/best5](http://127.0.0.1:5000/api/best5)                         | Returns the top 5 states for a question (best scores).                                            |
| [/api/worst5](http://127.0.0.1:5000/api/worst5)                       | Returns the last 5 states for a question (worst scores).                                          |
| [/api/global_mean](http://127.0.0.1:5000/api/global_mean)             | Calculates the global average of `Data_Value` for a question.                                     |
| [/api/diff_from_mean](http://127.0.0.1:5000/api/diff_from_mean)       | Calculates the difference between `global_mean` and `state_mean` for all states.                  |
| [/api/state_diff_from_mean](http://127.0.0.1:5000/api/state_diff_from_mean) | Calculates the difference between `global_mean` and `state_mean` for a specific state.      |
| [/api/mean_by_category](http://127.0.0.1:5000/api/mean_by_category)   | Calculates the average `Data_Value` by category (`Stratification1`) for each state.               |
| [/api/state_mean_by_category](http://127.0.0.1:5000/api/state_mean_by_category) | Calculates the average `Data_Value` by category for a specific state.                   |
| [/api/graceful_shutdown](http://127.0.0.1:5000/api/graceful_shutdown) | Allows the service to shut down after completing all current jobs.                                |
| [/api/jobs](http://127.0.0.1:5000/api/jobs)                           | Returns the status of all jobs.                                                                   |
| [/api/num_jobs](http://127.0.0.1:5000/api/num_jobs)                   | Returns the number of remaining jobs.                                                             |
| [/api/get_results/<job_id>](http://127.0.0.1:5000/api/get_results/<job_id>) | Returns the results for a specific job.                                                     |

## Input/Output Structure

The input and output formats can be observed in the `tests` folder.
The server response format is determined by the queried API endpoint (e.g., `/api/states_mean`, `/api/best5`).

| Type   | Description                                                                                                     |
|--------|-----------------------------------------------------------------------------------------------------------------|
| Input  | The input follows the format of one of the predefined questions.                                                |
| Output | The output format varies based on the specific API endpoint queried.                                            |

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
