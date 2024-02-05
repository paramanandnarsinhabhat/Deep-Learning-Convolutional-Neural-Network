
# Deep Learning Convolutional Neural Network for Auto-Tagging

This repository contains a machine learning project that uses a Convolutional Neural Network (CNN) to automatically tag Stack Overflow questions.

## Getting Started

### Prerequisites

Before running the project, ensure that you have the following prerequisites installed:

- Python 3.x
- pip (Python package installer)

### Installation

Clone the repository to your local machine and navigate to the cloned directory. Set up a virtual environment and activate it:

```bash
python3 -m venv myenv
source myenv/bin/activate  # On macOS and Linux
myenv\Scripts\activate     # On Windows
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Data

The datasets are compressed in a zip file within the `data` folder. To unzip and access the files, run the provided code in the `autotaggingsystemcnn.py` script, which will extract the contents for use.

### Usage

After setting up the environment and data, you can run the Python script or Jupyter notebook to train the model and make predictions.

```bash
python source/autotaggingsystemcnn.py
# or
jupyter notebook notebook/autotaggingsystemcnn.ipynb
```

### Steps to Follow

1. **Load Data and Import Libraries**: Load the necessary libraries and the Stack Overflow dataset.
2. **Text Cleaning**: Preprocess the text data to remove HTML tags and non-alphabetic characters.
3. **Merge Tags with Questions**: Combine the question and tag data for model training.
4. **Dataset Preparation**: Prepare the dataset by selecting the most frequent tags.
5. **Text Representation**: Convert text data into a numerical format that can be fed into the CNN.
6. **Model Building**: 
   - Define the CNN model architecture.
   - Train the model on the prepared dataset.
7. **Model Predictions**: Use the trained model to predict tags for new questions.
8. **Model Evaluation**: Evaluate the model's performance using metrics like F1 score.
9. **Inference**: Predict tags for new data inputs.

### Project Structure

- `data/`: Contains the datasets and the zip file.
- `myenv/`: Recommended directory for the Python virtual environment.
- `notebook/`: Contains the Jupyter notebook for the project.
- `source/`: Contains the Python script for the project.
- `weights.best.hdf5`: Model weights saved during training.
- `requirements.txt`: Required Python packages for the project.
- `README.md`: Documentation for the project.

### Contributing

We welcome contributions to improve this project. Please feel free to fork the repository and submit pull requests.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


