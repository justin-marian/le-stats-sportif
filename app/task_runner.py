import os
import time
import multiprocessing
from queue import Queue, Empty
from threading import Thread, Event


class ThreadPool:
    def __init__(self, data_ingestor):
        self.data_ingestor = data_ingestor
        self.task_queue = Queue()
        self.accept_tasks = Event()
        self.accept_tasks.set()
        self.thread_list = []
        self.nr_threads = int(os.getenv('TP_NUM_OF_THREADS', multiprocessing.cpu_count()))

        for i in range(self.nr_threads):
            t = TaskRunner(self.task_queue, i, self.data_ingestor, self.accept_tasks)
            t.start()
            self.thread_list.append(t)


    def add_task(self, task):
        if self.accept_tasks.is_set():
            self.task_queue.put(task)


    def stop(self):
        self.accept_tasks.clear()
        for t in self.thread_list:
            t.join()


class TaskRunner(Thread):
    def __init__(self, task_queue, index, data_ingestor, accept_tasks):
        super().__init__()
        self.index = index
        self.task_queue = task_queue
        self.data_ingestor = data_ingestor
        self.accept_tasks = accept_tasks

        self.task_map = {
            "states_mean": self.data_ingestor.states_mean,
            "state_mean": self.data_ingestor.state_mean,
            "best5": self.data_ingestor.best_five,
            "worst5": self.data_ingestor.worst_five,
            "global_mean": self.data_ingestor.global_mean,
            "state_diff_from_mean": self.data_ingestor.state_diff_from_mean,
            "diff_from_mean": self.data_ingestor.diff_from_mean,
            "state_mean_by_category": self.data_ingestor.state_mean_by_category,
            "mean_by_category": self.data_ingestor.mean_by_category,
        }


    def execute_task(self, job_id, request_type, task_data):
        function = self.task_map.get(request_type)
        if function:
            state_name = task_data.get('state')
            question = task_data.get('question')
            if state_name:
                function(job_id, question, state_name)
            else:
                function(job_id, question)


    def run(self):
        while self.accept_tasks.is_set():
            try:
                job_id, request_type, task_data = self.task_queue.get(timeout=1)
                self.execute_task(job_id, request_type, task_data)
            except Empty:
                if not self.accept_tasks.is_set():
                    break
                time.sleep(1)
