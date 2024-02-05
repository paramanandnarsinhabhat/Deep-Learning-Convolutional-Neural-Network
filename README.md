## Deep Learning Advanced Sequence Models

This project is a deep learning system designed to automatically tag content using a Convolutional Neural Network (CNN). It processes text data, specifically questions from Stack Overflow, to predict associated tags.

### Project Structure

- `data/`: This directory contains the datasets `Questions.csv` and `Tags.csv` necessary for the model.
- `source/`: Contains the Python script `autotaggingsystemcnn.py` and Jupyter notebook `autotaggingsystemcnn.ipynb` for the tagging system.
- `weights.best.hdf5`: The saved model weights after training.
- `myenv/`: Suggested directory for a Python virtual environment.
- `README.md`: This file, containing information about the project.
- `LICENSE`: The license file for the project.
- `.gitignore`: Specifies intentionally untracked files to ignore.


### Installation

To set up the project environment:

1. Clone this repository.
2. Create a virtual environment:
   ```
   python3 -m venv myenv
   ```
3. Activate the virtual environment:
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```
   - On Windows:
     ```
     myenv\Scripts\activate
     ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

# requirements.txt

```
pandas
numpy
beautifulsoup4
matplotlib
scikit-learn
tensorflow
```

### Usage

Execute the script using Python:

```
python source/autotaggingsystemcnn.py
```

Or open the Jupyter notebook:

```
jupyter notebook source/autotaggingsystemcnn.ipynb
```

### Steps to Follow in the Script

1. Load Data and Import Libraries.
2. Perform Text Cleaning on the dataset.
3. Merge Tags with Questions for combined processing.
4. Prepare the Dataset for the neural network.
5. Create Text Representations suitable for input into the model.
6. Build the Model with CNN architecture.
7. Train the Model on the data.
8. Predict tags for new data.
9. Evaluate the Model's performance.
10. Perform Inference to tag new questions.

### Requirements

The project requires Python 3 and the following libraries:

- `re` (built-in)
- `pandas`
- `numpy`
- `BeautifulSoup` from `bs4`
- `matplotlib`
- `sklearn`
- `keras` from `tensorflow`

### Contributing

Contributions to this project are welcome. Please ensure you follow the guidelines in the `LICENSE`.

### License

This project is licensed under the [MIT License](LICENSE).

---


