# NBA Award Prediction using Deep Learning

## Project Overview
This project aims to predict NBA award winners, such as Most Valuable Player (MVP), Defensive Player of the Year (DPOY), and Rookie of the Year (ROY), using deep learning models built with PyTorch. The models are trained on historical NBA player data, including advanced metrics, team performance, and individual player statistics.

## Features
- **Data Collection:** Automated retrieval of player statistics using `nba_api`.
- **Feature Engineering:** Aggregation of key performance indicators and advanced metrics.
- **Model Training:** Separate deep learning models for each award using PyTorch.
- **Evaluation & Predictions:** Model validation using historical award winners and real-time predictions for current seasons.

## Installation
### Prerequisites
Ensure you have Python 3.8+ installed. Then, install the required dependencies:
```sh
pip install -r requirements.txt
```

### Required Libraries
- `torch`, `torchvision`, `torchaudio` (Deep Learning)
- `pandas`, `numpy` (Data Processing)
- `nba_api` (Data Retrieval)
- `scikit-learn` (Feature Engineering & Metrics)
- `matplotlib`, `seaborn` (Visualization)

## File Structure
```
NBA_Award_Prediction/
│── data/			  # Raw and processed datasets
│   ├── raw/		  # Unprocessed data
│   ├── processed/	  # Cleaned and feature-engineered data
│── models/		  # Trained models and checkpoints
│── src/			  # Source code
│   ├── data_collection.py	# Fetch data using nba_api
│   ├── preprocessing.py	  # Clean and process data
│   ├── feature_engineering.py # Compute advanced metrics
│   ├── train_mvp.py		  # Train MVP model
│   ├── train_dpoy.py		  # Train DPOY model
│   ├── train_roy.py		  # Train ROY model
│   ├── predict.py		  # Make predictions using trained models
│── tests/		  # Unit tests
│── config/		  # Configuration files (e.g., hyperparameters)
│── scripts/		  # Utility scripts for training and evaluation
│── README.md		  # Project documentation
│── requirements.txt	  # Dependencies
│── main.py		  # Entry point for running predictions
```

## Usage
### Data Collection
Run the following script to collect and preprocess data:
```sh
python src/data_collection.py
python src/preprocessing.py
python src/feature_engineering.py
```

### Training Models
Train models for each award:
```sh
python src/train_mvp.py
python src/train_dpoy.py
python src/train_roy.py
```

### Making Predictions
Once models are trained, you can make predictions for the current NBA season:
```sh
python main.py
```

## Future Improvements
- Add ensemble models to improve prediction accuracy.
- Incorporate real-time data for live predictions.
- Experiment with attention mechanisms to enhance model interpretability.

## Contributors
[Your Name]

## License
This project is licensed under the MIT License.

