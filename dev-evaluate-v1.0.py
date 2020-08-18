from scipy import stats
import argparse
import json

def load_data(load_file):
	ranks = []
	while True:
		one_line = load_file.readline()
		if not one_line:
			break
		rank = [int(i.strip()) for i in one_line.strip().split(" ")]
		ranks.append(rank)
		
	return ranks


def evaluate(answers, predictions):
	if len(answers) != len(predictions):
		raise Exception("Invalid Answers or Predictions!")

	rank_crr = 0
	for i in range(len(answers)):
		answer = answers[i]
		prediction = predictions[i]
		if len(prediction) != 3 or not (1 in prediction) or not (2 in prediction) or not (0 in prediction):
			raise Exception("Invalid Prediction! %s" % prediction)

		wkt = stats.weightedtau(answer, prediction)[0]

		rank_crr += wkt

	sum_wkt = rank_crr
	avg_wkt = rank_crr / len(answers)

	return { "sum_wkt": sum_wkt, "avg_wkt": avg_wkt }


if __name__ == '__main__':
	expected_version = 'FashionHow_v1.0'
	parser = argparse.ArgumentParser(
			description = 'Evaluation for FashionHow ' + expected_version)
	parser.add_argument('answer_file', help='Answer File')
	parser.add_argument('prediction_file', help='Prediction file')
	args = parser.parse_args()
	with open(args.answer_file) as answer_file:
		answers = load_data(answer_file)
		
	with open(args.prediction_file) as prediction_file:
		predictions = load_data(prediction_file)

	print(json.dumps(evaluate(answers, predictions)))
