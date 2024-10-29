import os
import json
import pandas as pd


class DataIngestor:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.required_columns = [
            'LocationDesc', 'Question',
            'StratificationCategory1', 
            'Stratification1', 'Data_Value'
        ]
        self.df = pd.read_csv(self.csv_path, usecols=self.required_columns)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]
        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity '
            'and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity '
            'or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        ]

    def write_to_file(self, job_id, data):
        if not os.path.exists('results'):
            os.makedirs('results')
        with open(f"results/{job_id}.json", mode="w", encoding="utf-8") as json_file:
            json.dump(data, json_file, separators=(', ', ': '))

    def _filter_by_question(self, question):
        return self.df[self.df['Question'] == question]

    def average_each_state(self, question):
        df_filtered = self._filter_by_question(question)
        return df_filtered.groupby('LocationDesc')['Data_Value'].mean().sort_values().to_dict()

    def states_mean(self, job_id, question):
        self.write_to_file(job_id, self.average_each_state(question))

    def state_mean(self, job_id, question, state):
        state_average = self._filter_by_question(question).loc[self.df['LocationDesc'] == state, 'Data_Value'].mean()
        self.write_to_file(job_id, {state: state_average})

    def top_or_bottom_five(self, job_id, question, top=True):
        sorted_states = self.average_each_state(question)
        if (top and question in self.questions_best_is_min) or (not top and question in self.questions_best_is_max):
            selected_states = dict(list(sorted_states.items())[:5])
        else:
            selected_states = dict(list(sorted_states.items())[-5:])
            selected_states = dict(reversed(selected_states.items()))
        self.write_to_file(job_id, selected_states)

    def best_five(self, job_id, question):
        self.top_or_bottom_five(job_id, question, top=True)

    def worst_five(self, job_id, question):
        self.top_or_bottom_five(job_id, question, top=False)

    def global_mean(self, job_id, question):
        global_mean = self._filter_by_question(question)['Data_Value'].mean()
        self.write_to_file(job_id, {"global_mean": global_mean})

    def state_diff_from_mean(self, job_id, question, state):
        global_mean = self._filter_by_question(question)['Data_Value'].mean()
        state_mean = self._filter_by_question(question).loc[self.df['LocationDesc'] == state, 'Data_Value'].mean()
        self.write_to_file(job_id, {state: global_mean - state_mean})

    def diff_from_mean(self, job_id, question):
        global_mean = self._filter_by_question(question)['Data_Value'].mean()
        state_diffs = {
            state: global_mean - mean
            for state, mean in self.average_each_state(question).items()
        }
        self.write_to_file(job_id, state_diffs)

    def compute_state_averages(self, state, question, all_states=False):
        df_state = self._filter_by_question(question).loc[self.df['LocationDesc'] == state]
        state_averages = {}

        for category, group in df_state.groupby('StratificationCategory1'):
            subcategory_averages = group.groupby('Stratification1')['Data_Value'].mean().to_dict()
            formatted = {
                (f"('{state}', '{category}', '{subcategory}')"
                 if all_states else f"('{category}', '{subcategory}')"): value
                for subcategory, value in subcategory_averages.items()
            }
            state_averages.update(formatted)
        return state_averages

    def state_mean_by_category(self, job_id, question, state):
        state_averages = self.compute_state_averages(state, question, all_states=False)
        self.write_to_file(job_id, {state: state_averages})

    def mean_by_category(self, job_id, question):
        all_states_averages = {}
        for state in self.df['LocationDesc'].unique():
            state_averages = self.compute_state_averages(state, question, all_states=True)
            all_states_averages.update(state_averages)
        self.write_to_file(job_id, all_states_averages)
