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
## MVP Selection Criteria

This project predicts the **NBA Most Valuable Player (MVP)** based on key statistical metrics that capture scoring ability, efficiency, playmaking, defense, and overall impact on winning. The following categories explain the significance of each stat in determining the MVP:

### Per Game Stats (Basic Counting Stats)
- **PPG (Points Per Game)** – MVPs are typically elite scorers who can carry their team's offense.  
- **APG (Assists Per Game)** – Playmaking ability is crucial, as MVPs often elevate their teammates.  
- **RPG (Rebounds Per Game)** – Rebounding is essential for both big men and versatile players.  
- **BPG (Blocks Per Game)** – Defensive presence matters, and high block numbers indicate rim protection.  
- **EffFG% (Effective Field Goal Percentage)** – Measures shooting efficiency by weighting three-pointers higher. MVPs should score efficiently, not just in volume.  
- **FT% (Free Throw Percentage)** – High FT% indicates reliability in crucial moments and efficiency in scoring easy points.  
- **SPG (Steals Per Game)** – Strong defensive instincts are important for two-way MVP candidates.  

### Advanced Stats (Efficiency & Impact Metrics)
- **USG% (Usage Percentage)** – MVPs are high-usage players who drive their team’s offense.  
- **AST% (Assist Percentage)** – Shows how much a player contributes to team ball movement and playmaking.  
- **TRB% (Total Rebound Percentage)** – Measures rebounding impact relative to playing time.  
- **PER (Player Efficiency Rating)** – A composite stat that highlights overall productivity.  
- **WS (Win Shares)** – Estimates how many wins a player contributes to their team’s success.  
- **WS/48 (Win Shares Per 48 Minutes)** – Adjusts WS for playing time to show impact per minute.  
- **BPM (Box Plus-Minus)** – Measures overall impact per 100 possessions, indicating dominance.  
- **OBPM (Offensive Box Plus-Minus)** – Highlights offensive contributions beyond raw scoring.  
- **DBPM (Defensive Box Plus-Minus)** – Measures defensive impact and effectiveness.  
- **VORP (Value Over Replacement Player)** – Quantifies how much better a player is compared to a league-average replacement.  
- **STL% (Steal Percentage)** – Highlights defensive playmaking ability.  
- **BLK% (Block Percentage)** – Indicates shot-blocking and rim protection ability.  
- **TOV% (Turnover Percentage)** – Measures ball security; lower values indicate efficiency in possession.  

### How These Stats Determine MVP
- **Scoring dominance** (PPG, EffFG%, USG%) is a key factor.  
- **Playmaking ability** (APG, AST%) differentiates elite offensive players.  
- **Two-way impact** (BPG, SPG, DBPM, STL%, BLK%) boosts an MVP case.  
- **Winning contribution** (WS, WS/48, VORP) helps identify players leading successful teams.  
- **Efficiency** (PER, EffFG%, FT%) separates volume scorers from true MVP-caliber players.  

MVP candidates typically excel in multiple categories, showcasing a balance of scoring, efficiency, defense, and team impact.  


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

