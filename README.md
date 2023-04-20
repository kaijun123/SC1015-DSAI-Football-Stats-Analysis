# SC1015 Data Science and Analytics

# Table of Content
- [Repo Structure](#Repo-Structure)
- [Problem Statement](#Problem-Statement)
- [Approach](#Approach)
- [Introduction to code](#Introduction-to-code)
  * [Anomaly_Detection](#Anomaly_Detection)
  * [Player Reflection](#Player_Valuation)
  * [Video Presentation](#Video-Presentation)
  * [Slides](#Slides)
- [Contributors](#Contributors)

# Repo Structure
```bash
.
├── README.md
├── Anomaly_Detection
│   ├── fbref_data                      # Data from Fbref
│   ├── sofifa_data                     # Data from Sofifa
│   ├── FbRef Data Scraping.ipynb       # Notebook to scrape data from FbRef
│   ├── FbRef Data Processing.ipynb     # Notebook to process FbRef data
│   └── 
│
├── Player_Valuation
│   ├── 
│   ├── 
│   ├── 
│   ├── 
│   └── 
│
├── Video Presentation
└── Slides
```
# Problem Statement


# Approach


# Introduction to code base

## Anomaly_Detection
- This segment contains code to identify the worst performing players within the team per season.
- Data used is obtained from scraping [FbRef]('https://fbref.com/en/') and [Sofifa](https://sofifa.com/)
- Using data from FbRef, we calculated the `Plus-Minus Per Min`. The formula is given as follows: 
`Plus-Minus Per Min = (Goals scored by own team - Goals scored by opponent team) / Playing Time per player`
- Using the data from Sofifa, we obtained the `Player Rankings`.
- Using these 2 metrics, we trained our model using these 2 metrics: `Plus-Minus Per Min` and `Player Rankings`, to identify the worst performing player in the team in a particular season.

## Player_Valuation
- This segment contains code to predict a player's valuation.
- Data used include players' stats, such as height, age, etc, and players' past transaction values.

## Video Presentation
- This contains our video presentation.

## Slides
- This contains our slides for our project.

# Contributors
- Ang Kai Jun
- Chay Hui Xiang
- Ivan Loke Zhi Hao
