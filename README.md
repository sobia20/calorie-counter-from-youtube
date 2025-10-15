# Calorie Counter from YouTube (Food Fusion)
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"><img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white">



A tool that estimates the calorie content of a dish from **Food Fusion** YouTube videos.


## 🧾 Table of Contents

- [About](#about)  
- [Features](#features)   
- [Installation](#installation)  
- [Usage](#usage)   



## About

This project is designed to parse a recipe video (specifically from the *Food Fusion* YouTube channel) and compute an approximate total number of calories of the dish. The core idea is:

1. Extract ingredient data (quantities, types) from the video or associated metadata.  
2. Map ingredients to calorie values (via nutritionix database).  
3. Sum up to present an estimate of the total calories.

The tool is still experimental and meant for rough estimates—not clinical accuracy.



## Features

- Parses recipe information (ingredients & quantities) from YouTube videos  
- Uses nutritionix database to assign calorie values  
- Calculates a total calorie estimate   
- Clean, modular Python code  
- Easy to extend or integrate with other data sources



## Installation

Clone the repository and install dependencies.

```bash
git clone https://github.com/sobia20/calorie-counter-from-youtube.git
cd calorie-counter-from-youtube
```
## Usage
You would need keys for Youtube, Gemini and Nutritionix API.

```bash
poetry install
poetry run python total_calories.py