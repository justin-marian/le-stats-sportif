import os
import json
import requests
import unittest
import time


class TestWebserver(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:5000/api/"

    def test_states_mean(self):
        self.helper_test_endpoint("states_mean")

    def test_state_mean(self):
        self.helper_test_endpoint("state_mean")

    def test_best5(self):
        self.helper_test_endpoint("best5")

    def test_worst5(self):
        self.helper_test_endpoint("worst5")

    def test_global_mean(self):
        self.helper_test_endpoint("global_mean")

    def test_diff_from_mean(self):
        self.helper_test_endpoint("diff_from_mean")

    def test_state_diff_from_mean(self):
        self.helper_test_endpoint("state_diff_from_mean")

    def test_mean_by_category(self):
        self.helper_test_endpoint("mean_by_category")

    def test_state_mean_by_category(self):
        self.helper_test_endpoint("state_mean_by_category")

    def helper_test_endpoint(self, endpoint):
        output_dir = f"tests/{endpoint}/output/"
        input_dir = f"tests/{endpoint}/input/"
        input_file = "in-1.json" # CHOOSE OTHER IN FILE in-<1-9>.json
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, f"out-1.json") # RENAME OUT FILE out-<1-9>.json

        with open(input_path, "r") as fin:
            req_data = json.load(fin)

        with open(output_path, "r") as fout:
            ref_result = json.load(fout)

        res = requests.post(f"{self.BASE_URL}{endpoint}", json=req_data)
        self.assertEqual(res.status_code, 200, f"Failed to create job for {endpoint}")
        job_id = res.json().get("job_id")

        for _ in range(5):
            result_res = requests.get(f"{self.BASE_URL}get_results/{job_id}")
            if result_res.status_code == 200 and result_res.json().get("status") == "done":
                received_result = result_res.json().get("data")
                break
            time.sleep(1)
        else:
            self.fail(f"Timeout waiting for job result for {endpoint}")

        self.assertEqual(received_result, ref_result, f"Test failed for: {endpoint}")
        print(f"Test passed for: {endpoint}")


if __name__ == "__main__":
    unittest.main()
