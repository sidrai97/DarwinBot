import os
import sys
import json
import logging
import data_helper
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib import learn

def predict_unseen_data(userMessage):
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
	#logging.getLogger().setLevel(logging.INFO)
	"""Step 0: load trained model and parameters"""
	mainDir = "C:/Users/sid/Desktop/Darwin/DarwinBot/process_message/intentClassifier/"
	params = json.loads(open(mainDir+'parameters.json').read())
	#checkpoint_dir = mainDir+"trained_model_1519274258/"
	checkpoint_dir = mainDir+"trained_model_1522994422"
	if not checkpoint_dir.endswith('/'):
		checkpoint_dir += '/'
	checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir + 'checkpoints')
	#logging.critical('Loaded the trained model: {}'.format(checkpoint_file))

	"""Step 1: load data for prediction"""
	
	# labels.json was saved during training, and it has to be loaded during prediction
	labels = json.loads(open(mainDir+'labels.json').read())
	one_hot = np.zeros((len(labels), len(labels)), int)
	np.fill_diagonal(one_hot, 1)
	label_dict = dict(zip(labels, one_hot))

	x_raw = userMessage
	x_test = [data_helper.clean_str(x_raw)]
	#logging.info('The number of x_test: {}'.format(len(x_test)))
	
	vocab_path = os.path.join(checkpoint_dir, "vocab.pickle")
	vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
	x_test = np.array(list(vocab_processor.transform(x_test)))

	"""Step 2: compute the predictions"""
	graph = tf.Graph()
	with graph.as_default():
		session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
		sess = tf.Session(config=session_conf)

		with sess.as_default():
			saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
			saver.restore(sess, checkpoint_file)

			input_x = graph.get_operation_by_name("input_x").outputs[0]
			dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
			predictions = graph.get_operation_by_name("output/predictions").outputs[0]

			batches = data_helper.batch_iter(list(x_test), params['batch_size'], 1, shuffle=False)
			all_predictions = []
			for x_test_batch in batches:
				batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
				all_predictions = np.concatenate([all_predictions, batch_predictions])
				all_predictions = all_predictions.tolist()
	return labels[int(all_predictions[0])]

ip = input("Enter Message: ").strip()
label=predict_unseen_data(ip)
print("Label: "+label)