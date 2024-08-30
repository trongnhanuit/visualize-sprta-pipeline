import argparse
import re
import matplotlib.pyplot as plt

def extract_SPRTA_scores(input_file_path):
	# Read the content of the text file
	with open(input_file_path, 'r') as file:
		input_string = file.read()

	# Regular expression pattern to find all pairs of support and IQsupport values
	pattern = r'support=(\d+\.\d+).*?IQsupport=(\d+\.\d+)'

	# Find all matches in the input string
	matches = re.findall(pattern, input_string)

	# Initialize arrays to store MAPLE and CMAPLE scores
	MAPLE_scores = []
	CMAPLE_scores = []

	# Process and store each pair of values in the respective arrays
	for match in matches:
		MAPLE_score, CMAPLE_score = match
		MAPLE_scores.append(float(support))
		CMAPLE_scores.append(float(iqsupport))
	
	return MAPLE_scores, CMAPLE_scores


def plot_SPRTA_scores(MAPLE_scores, CMAPLE_scores, output_file_path):
	# Draw a scatter plot
	plt.scatter(MAPLE_scores, CMAPLE_scores, color='blue', marker='o')
	# Labeling the axes
	plt.xlabel('MAPLE')
	plt.ylabel('CMAPLE')
	# Set the range for the axes (0 to 1 for both axes)
	plt.xlim(0, 1)
	plt.ylim(0, 1)
	# Title of the plot
	plt.title('Scatter Plot of SPRTA computed by MAPLE and CMAPLE')
	# Save the plot to the output file
	plt.savefig(output_file_path)
	# Optional: Clear the current plot if you plan to create another plot
	plt.clf()
	print(f"Scatter plot saved to {output_file_path}")

def main():
	# input params
	parser = argparse.ArgumentParser(description='Extract and visualize SPRTA scores computed by CMAPLE and MAPLE.')
	parser.add_argument('--input', default="", help='The treefile with SPRTA scores')
	parser.add_argument('--output', default="", help='The output file path')

	# parse params
	args = parser.parse_args()
	input_path = args.input
	output_path = args.output

	# extract SPRTA scores
	MAPLE_scores, CMAPLE_scores = extract_SPRTA_scores(input_path)

	# visualize the results
	plot_SPRTA_scores(MAPLE_scores, CMAPLE_scores, output_path)

# Call the main function
if __name__ == "__main__":
	main()















