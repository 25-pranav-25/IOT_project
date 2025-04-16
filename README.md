# IoT-Based Energy Monitoring and Anomaly Detection System

## Overview

This project presents an IoT-based solution for real-time energy monitoring and anomaly detection across multiple buildings. Utilizing ESP32 microcontrollers, the system simulates hourly power consumption data for 20 distinct buildings. The data is transmitted via MQTT to a Flask-based web server, which processes, stores, and visualizes the information. An integrated machine learning model, specifically a Random Forest classifier, analyzes the data to detect anomalies in energy usage.

## Features

- **Synthetic Data Generation**: Simulates realistic hourly power consumption data for 20 buildings, accounting for variations due to building type and weekend effects.
- **MQTT Communication**: Employs the MQTT protocol for efficient and lightweight data transmission from ESP32 devices to the server.
- **Web Interface**: A user-friendly Flask web application that displays energy consumption plots and anomaly reports for each building.
- **Anomaly Detection**: Implements a Random Forest classifier to identify unusual patterns in energy usage, providing precision and recall metrics for performance evaluation.


- `IOT_project_modelling.ipynb`: Contains scripts for generating synthetic energy consumption data.
- `main.py`: MicroPython code for ESP32 devices to publish data via MQTT.
- `app.py`: Flask application handling data reception, storage, and visualization.
- `models/`: Pre-trained machine learning models for anomaly detection.
- `scalers/`: Pre-trained scalers for scaling inputs.
- `templates/`: Contains index.html frontend page for the website.

## Getting Started

### Prerequisites

- Python
- Flask
- pandas
- numpy
- scikit-learn
- paho-mqtt
- matplotlib
- MicroPython firmware for ESP32

### Data Generation and modelling

Navigate to the `IOT_project_modelling.ipynb` and run the script to generate synthetic data and get models and scalers:

This will create a CSV file containing the simulated energy consumption data.

### Deploying the Flask Server

```bash
python app.py
```

The web interface will be accessible at `http://localhost:5000`.

### Starting Mosquitto Server

```bash
mosquitto.exe -v -c mosquitto.conf
```

### Configuring ESP32 Devices

Flash the MicroPython firmware onto your ESP32 devices. Upload the `main.py` script to each device. Ensure that the devices are connected to the same network as the Flask server and are configured to publish data to the correct MQTT broker address.

## Usage

1. **Select a Building**: Use the sidebar in the web interface to choose a building.
2. **View Energy Consumption**: Observe the hourly energy consumption plot for the selected building.
3. **Analyze Anomalies**: Review the anomaly table to identify any unusual energy usage patterns detected by the Random Forest model.

## Machine Learning Model

The Random Forest classifier is trained on the synthetic dataset to detect anomalies in energy consumption. The model evaluates each data point and flags it as anomalous based on learned patterns. Performance metrics such as accuracy, precision, recall, and F1-score are computed to assess the model's effectiveness.
