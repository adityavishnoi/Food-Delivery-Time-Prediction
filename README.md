# 🚀 SwiftETA: AI-Powered Food Delivery Time Predictor

An immersive, machine learning-driven web application that estimates end-to-end food delivery times based on real-world logistics constraints. 

This project utilizes a **Random Forest Regressor** to predict delivery ETAs and features a highly vibrant, custom-styled **Streamlit** frontend complete with glassmorphism effects, CSS animations, and a neon-glowing interactive UI.

## ✨ Features
* **Real-Time Predictions**: Calculates estimated delivery times instantly based on 7 distinct logistical factors.
* **Advanced ML Model**: Powered by a finely tuned Random Forest Regressor for high-accuracy predictions.
* **Immersive UI/UX**: Breaks the standard Streamlit mold with a custom animated mesh gradient background, frosted glass containers, and neon hover effects.
* **ETA Breakdown**: Automatically separates food preparation time from actual transit time for clearer logistical insights.

## 🛠️ Tech Stack
* **Machine Learning**: Scikit-Learn (Random Forest Regressor)
* **Frontend**: Streamlit, Custom CSS (Glassmorphism, Keyframe Animations)
* **Data Manipulation**: Pandas, NumPy
* **Deployment/Environment**: Python 3.x

## 📊 Model Features Used
The prediction engine factors in the following independent variables to output the `Delivery_Time_min`:
1. **Distance (km)**: Total route distance.
2. **Weather Condition**: Clear, Foggy, Rainy, Snowy, Windy.
3. **Traffic Density**: Low, Medium, High.
4. **Time of Day**: Morning, Afternoon, Evening, Night.
5. **Vehicle Type**: Bike, Scooter, Car.
6. **Preparation Time**: Time required by the restaurant to prepare the food (minutes).
7. **Courier Experience**: Driver's experience level (years).

Live Link - https://food-delivery-time-prediction-xsuud8upe6hgkd2ztcz3xs.streamlit.app/
