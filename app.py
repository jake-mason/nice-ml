'''
python3 app.py
'''

import os
import time
import argparse
from functools import reduce

from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, ParameterGrid, cross_validate
from sklearn import metrics

import pandas as pd
import numpy as np

from xgboost import XGBClassifier

print('pid: {}'.format(os.getpid()))
print('Current niceness: {}'.format(os.nice(0)))

RANDOM_STATE = 100

parser = argparse.ArgumentParser()
parser.add_argument('--n_samples', default=1000000, type=int)
parser.add_argument('--n_features', default=75, type=int)
parser.add_argument('--n_informative', default=50, type=int)
parser.add_argument('--n_jobs', default=1, type=int)
parser.add_argument('--cross_validate', default=False, type=bool)
parser.add_argument('--filename', type=str)
args = parser.parse_args()

print(args.__dict__)

def calculate_performance(ytrue, ypred, yproba):
	return {
		'f1': metrics.f1_score(ytrue, ypred),
		'precision': metrics.precision_score(ytrue, ypred),
		'recall': metrics.recall_score(ytrue, ypred),
		'accuracy': metrics.accuracy_score(ytrue, ypred),
		'roc_auc': metrics.roc_auc_score(ytrue, yproba)
	}

def summarize_performance(results):
	mean_s = pd.DataFrame.from_records(results).mean().rename('mean').to_frame()
	std_s = pd.DataFrame.from_records(results).std().rename('std').to_frame()
	max_s = pd.DataFrame.from_records(results).max().rename('max').to_frame()
	min_s = pd.DataFrame.from_records(results).min().rename('min').to_frame()
	result_df = reduce(lambda x, y: x.join(y), [mean_s, std_s, max_s, min_s])
	return result_df.reset_index()

X, y = make_classification(
	n_samples=args.n_samples,
	n_features=args.n_features,
	n_informative=args.n_informative,
	random_state=RANDOM_STATE
)

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, random_state=RANDOM_STATE)

param_grid = {
	'n_estimators': [100, 200, 300],
	'learning_rate': [0.05, 0.10],
	'max_depth': [6, 8],
	'min_samples_leaf': [5]
}

n_configs_to_test = reduce(lambda x, y: x * y, map(len, param_grid.values()))
print('Number of configs to test: {}'.format(n_configs_to_test))

param_grid = ParameterGrid(param_grid)
results = []

for i, param in enumerate(param_grid):
	t0 = time.time()

	# Add number of jobs/processes to param config
	param.update({'n_jobs': args.n_jobs, 'verbose': True})
	print(param)

	model = XGBClassifier(**param)
	model.fit(Xtrain, ytrain)

	t1 = time.time()
	diff = t1 - t0

	ypred = model.predict(Xtest)
	yproba = model.predict_proba(Xtest)[:, 1]

	perf = calculate_performance(ytest, ypred, yproba)
	results.append({**perf, **{'time': diff}})

	print('{} configs left to test'.format(n_configs_to_test - (i+1)))

result_df = summarize_performance(results)
result_df.to_csv(args.filename, index=False)

if args.cross_validate:
	print('Beginning cross-validation')
	t0 = time.time()
	
	cv = cross_validate(
		model, X, y,
		cv=3, scoring=['f1', 'precision', 'recall', 'accuracy'],
		verbose=4, n_jobs=args.n_jobs
	)
	
	t1 = time.time()
	print('Start time: {}, end time: {}, duration: {}'.format(t0, t1, t1-t0))