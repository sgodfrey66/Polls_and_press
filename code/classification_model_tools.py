# Python utilities
import pandas as pd
import numpy as np
from scipy import interp

# Base sklearn
from sklearn.base import TransformerMixin

# Models
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# Preprocessing tools
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import label_binarize
from sklearn.feature_extraction.text import CountVectorizer

# Modeling processors
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline

# Evaluation tools
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


# Return a dense matrix
class DenseTransformer(TransformerMixin):
	"""
	A class object in the structure of sklearn modeling classes to transform a sparse array
	to a dense array.  This is designed to be incorporated into pipe objects in which there
	is a vectorizer producing a sparse matrix and a model that requires a dense matrix input.

	Reference
	---------
	# see https://stackoverflow.com/questions/28384680/
	# scikit-learns-pipeline-a-sparse-matrix-was-passed-but-dense-data-is-required

	libraries
	---------
	from sklearn.base import TransformerMixin

	Methods
	-------
	fit(self, X, y=None, **fit_params)
		Return self
	transform(self, X, y=None, **fit_params)
		Return a dense array from the X input
		output : dense array

	"""

	def fit(self, X, y=None, **fit_params):
		return self
	def transform(self, X, y=None, **fit_params):
		return X.todense()



class ClassModels:
	"""
	Evaluate any number of several classification models over a specified X and y dataset.  The models
	can be GaussianNB, KNeighborsClassifier or RandomForestClassifier and the feature set can include
	numeric variables or text fields that require vectorization.

	Libraries and uses
	------------------
	# Python utilities
	import pandas as pd
	import numpy as np
	from scipy import interp

	# Base sklearn
	from sklearn.base import TransformerMixin

	# Models
	from sklearn.naive_bayes import GaussianNB
	from sklearn.neighbors import KNeighborsClassifier
	from sklearn.ensemble import RandomForestClassifier

	# Preprocessing tools
	from sklearn.model_selection import StratifiedShuffleSplit
	from sklearn.preprocessing import StandardScaler
	from sklearn.preprocessing import label_binarize
	from sklearn.feature_extraction.text import CountVectorizer

	# Modeling processors
	from sklearn.model_selection import train_test_split, GridSearchCV
	from sklearn.pipeline import Pipeline

	# Evaluation tools
	from sklearn.metrics import roc_curve, auc
	from sklearn.metrics import confusion_matrix
	from sklearn.metrics import accuracy_score
	

	Parameters
	----------
	vectorizer : sklearn vectorizing class
		A class object speficiying the vectorizer to be used on every x column.  If set to None,
		no vectorizing is applied.  Only CountVectorizer() is supported at this time.
	model : sklearn model class
		A class object specifying the model to be used. GaussianNB(), KNeighborsClassifier() and
		RandomForestClassifier() are supported at this stage.
	pipe : sklearn pipeline object
		A sklearn pipeline object defining the steps in the processing and modeling pipeline.  This 
		is defined by the define_pipe method.
	pipe_params : dictionary
		Parameters for the pipe to be employed in a grid search.
	n_splits : integer
		Number of splits for the cross-validation grid search.
	random_state : integer
		Random seed for the cross-validation grid search.

	methods
	----------
	__init__(self, vectorizer = None, model = None, n_splits = 3, random_state = 223)
		Initialize the class object.
	fit_model(self, df, x_cols, y_col)
		Fit model using the relevant pipe, pipe_params in gridsearchcv().
		output : dictionary with fitted model outputs including predictions and evaluation metrics

	"""

	vectorizer = None
	model = None
	description = ''
	pipe = None
	pipe_params = None
	n_splits = 3
	random_state = 223
	
	def __init__(self, vectorizer = None, model = None, 
				n_splits = 3, random_state = 223):
		# set the variable description and use that in the object
		if vectorizer == None and isinstance(model,GaussianNB):
			self.description = 'Naive Bayes without vectorization'

		elif vectorizer == None and isinstance(model,KNeighborsClassifier):
			self.description = 'K Nearest Neighbors without vectorization'
			
		elif vectorizer == None and isinstance(model,RandomForestClassifier):
			self.description = 'Random Forest without vectorization'
			
		elif isinstance(vectorizer, CountVectorizer) and isinstance(model,GaussianNB):
			self.description = 'Naive Bayes with Count Vectorization'
			
		elif isinstance(vectorizer, CountVectorizer) and isinstance(model,KNeighborsClassifier):
			self.description = 'K Nearest Neighbors with Count Vectorization'
			
		elif isinstance(vectorizer, CountVectorizer) and isinstance(model,RandomForestClassifier):
			self.description = 'Random Forest with Count Vectorization'       
		else:
			self.description = 'Configuration not supported'
		
		# Assign the self model and vectorizer
		self.n_splits = n_splits
		self.model = model
		self.vectorizer = vectorizer
		self.random_state = random_state
	 
	# Define the pipes
	def define_pipe(self):

		if self.description != 'Configuration not supported':
			# Set up the pipeline based on the model and vectorizer inputs
			if self.vectorizer == None and isinstance(self.model,GaussianNB):
				self.pipe = Pipeline([('scale', StandardScaler()),
									  ('mod', self.model)])
				self.pipe_params = {}

			elif self.vectorizer == None and isinstance(self.model,KNeighborsClassifier):
				self.pipe = Pipeline([('scale', StandardScaler()),
									   ('mod', self.model)])
				self.pipe_params = {}

			elif self.vectorizer == None and isinstance(self.model,RandomForestClassifier):
				self.pipe = Pipeline([('scale', StandardScaler()),
									  ('mod', self.model)])
				self.pipe_params = {}

			elif isinstance(self.vectorizer, CountVectorizer) and isinstance(self.model,GaussianNB):
				self.pipe = Pipeline([('vec',  self.vectorizer),
								 ('to_array', DenseTransformer()),
								 ('mod', self.model)])
				self.pipe_params = {'vec__max_features': [None],
								'vec__min_df': [0.0],
								'vec__max_df': [1.0],
								'vec__ngram_range': [(1,1)]
								}
								
			elif isinstance(self.vectorizer, CountVectorizer) and isinstance(self.model,KNeighborsClassifier):
				self.pipe = Pipeline([('vec',  self.vectorizer),
								 ('to_array', DenseTransformer()),
								 ('mod', self.model)])
				self.pipe_params = {'vec__max_features': [None],
								'vec__min_df': [0.0],
								'vec__max_df': [1.0],
								'vec__ngram_range': [(1,1)]
								}
				
			elif isinstance(self.vectorizer, CountVectorizer) and isinstance(self.model,RandomForestClassifier):
				self.pipe = Pipeline([('vec',  self.vectorizer),
								 ('to_array', DenseTransformer()),
								 ('mod', self.model)])
				self.pipe_params = {'vec__max_features': [None],
								'vec__min_df': [0.0],
								'vec__max_df': [1.0],
								'vec__ngram_range': [(1,1)]
								}

	 # Define the pipes
	def fit_model(self, df, x_cols, y_col):
		
		# Attempt modeling only if configuration supported
		if self.description != 'Configuration not supported':

			# Set description
			if self.vectorizer == None:
				# Assign X and y variable
				X = df[x_cols].astype('float64')
				y = df[y_col]
			else:
				# Assign X and y variable
				X = df[x_cols]
				y = df[y_col]

			# Define the pipe and pipe params
			self.define_pipe()

			# Determine the number of classes
			classes = list(y.value_counts(normalize = True).index)
			n_classes = y.value_counts(normalize = True).shape[0]

			# Declare a dictionary to hold model parameters and results
			mod_out = {}

			# Split the testing data into n_splits treain/test periods
			cv = StratifiedShuffleSplit(n_splits = self.n_splits, random_state = self.random_state)
			gs = GridSearchCV(estimator = self.pipe, 
							  param_grid = self.pipe_params, 
							  cv = cv,
							  scoring = 'accuracy')

			# fit the model
			gs.fit(X, y)

			# Get the X,y split of the best test score
			max_sc = 0
			for i in range(self.n_splits):
				key = 'split' + str(i) + '_test_score'
				if gs.cv_results_[key] >= max_sc:
					max_sc  = gs.cv_results_[key]
					index = i

			# Set the values of train and test based on these indices
			tt_split = list(cv.split(X,y))[index]
			X_train= X.iloc[tt_split[0]]
			X_test = X.iloc[tt_split[1]]
			y_train = y.iloc[tt_split[0]]
			y_test = y.iloc[tt_split[1]]

			# If vectorizer is present in pipe, set X to vectorized models
			if self.vectorizer != None:
				# Re-vectorize X
				X_train = gs.best_estimator_.named_steps['vec'].fit_transform(X_train)
				X_train = gs.best_estimator_.named_steps['to_array'].transform(X_train)
				X_test = gs.best_estimator_.named_steps['vec'].transform(X_test)
				X_test = gs.best_estimator_.named_steps['to_array'].transform(X_test)

				# Create predictions using vectorized X
				y_predict = gs.best_estimator_.named_steps['mod'].fit(X_train,y_train).predict(X_test)
			else:
				# Create predictions using the unvectorized X
				y_predict = gs.best_estimator_.named_steps['mod'].predict(X_test)

			
			# To create ROC curve - create a dataframe of predictions
			y_test.name = 'actual'
			df_y_test = pd.DataFrame(y_test)
			df_y_test['predicted'] = y_predict
			df_y_test.head()

			# Compute ROC curve and ROC area for each class
			fpr = dict()
			tpr = dict()
			roc_auc = dict()
			# For each class, determine the tpr, fpr and AUC
			for cls in classes:
				y_actual = df_y_test['actual'].apply(lambda x: 1 if x == cls else 0)
				y_pred = df_y_test['predicted'].apply(lambda x: 1 if x == cls else 0)
				fpr[cls], tpr[cls], _ = \
					roc_curve(y_actual,y_pred)
				roc_auc[cls] = auc(fpr[cls], tpr[cls])

			# Create aggreggate functions
			# Aggregate all false positive rates
			all_fpr = np.unique(np.concatenate([fpr[cls] for cls in classes]))
			# Interpolate all ROC curves at these points
			mean_tpr = np.zeros_like(all_fpr)
			for cls in classes:
				mean_tpr += interp(all_fpr, fpr[cls], tpr[cls])
			# Average it and compute AUC
			mean_tpr /= n_classes
			# Add these elements to the dictionaries
			fpr['all'] = all_fpr
			tpr['all'] = mean_tpr
			roc_auc['all'] = auc(fpr['all'], tpr['all'])

			# Return model parameters
			mod_out['description'] = self.description
			mod_out['x_column'] = x_cols                                      
			mod_out['test_size'] = len(y_test)
			mod_out['train_size'] = len(y_train)   
			mod_out['class_balance'] = df[y_col].value_counts(normalize = True)

			# Return training and test scores
			mod_out['train_score_mean'] = float(gs.cv_results_['mean_train_score'])
			mod_out['test_score_mean'] = float(gs.cv_results_['mean_test_score'])
			mod_out['best_accuracy'] = float(accuracy_score(y_true = y_test, y_pred = y_predict))
			mod_out['conf_matrix'] = confusion_matrix(y_test,y_predict)

			# Return data for the ROC curve
			mod_out['fpr'] = fpr
			mod_out['tpr'] = tpr
			mod_out['roc_auc'] = roc_auc
			mod_out['roc_auc_all'] = float(roc_auc['all'])

			# Return vectorizer data
			if self.vectorizer != None:
				mod_out['vocabulary'] = gs.best_estimator_.named_steps['vec'].vocabulary_
				mod_out['features'] = gs.best_estimator_.named_steps['vec'].get_feature_names()
				mod_out['vector_matrix'] = gs.best_estimator_.named_steps['vec'].transform(X)
			else:
				mod_out['vocabulary'] = np.NaN
				mod_out['features'] = np.NaN
				mod_out['vector_matrix'] = np.NaN

			return mod_out
