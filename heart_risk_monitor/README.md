# Heart Risk Monitoring Dashboard

An interactive dashboard application for monitoring heart attack risk levels and providing healthcare insights based on patient data.

## Project Overview

This application provides two specialized dashboards for healthcare professionals:

1. **Analytical Dashboard** - Designed for healthcare providers and clinicians, focusing on:
   - Real-time patient risk monitoring
   - Critical metrics visualization
   - Interactive patient search and filtering
   - Visual representation of vital signs, lab results, and risk factors

2. **Managerial Dashboard** - Designed for hospital administrators and public health officials, focusing on:
   - Population-level health trends
   - Risk factor analysis across demographics
   - Resource allocation insights
   - Strategic decision-making support

## Features

- **Real-time Risk Monitoring**: Track and visualize patient risk levels with intuitive metrics
- **Interactive Visualizations**: Multiple chart types (line, bar, radar, pie, heatmap) for comprehensive data analysis
- **Patient Records Management**: Search, filter, and view detailed patient information
- **Population Health Analytics**: Analyze trends and patterns across different demographic groups
- **Report Generation**: Create printable reports for patients and population segments
- **Responsive Design**: Optimized for both desktop and mobile devices

## Data Structure

The application uses a heart attack prediction dataset with the following key components:

- Patient demographics (age, gender, income)
- Vital signs (blood pressure, heart rate, BMI)
- Lab results (cholesterol, blood sugar, triglycerides)
- Risk assessment (stress levels, heart attack risk)
- Lifestyle factors (smoking, alcohol, exercise)
- Medical history (diabetes, family history, previous heart problems)

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Bootstrap 5
- **Visualization Libraries**: Chart.js, D3.js
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite (with option to scale to larger databases)

## Project Structure

```
heart_risk_monitor/
│
├── app/                     # Application package
│   ├── routes/              # Route blueprints for different sections
│   ├── static/              # Static assets (CSS, JS, images)
│   ├── templates/           # HTML templates
│   ├── models/              # Data models and database utilities
│   ├── services/            # Business logic and services
│   └── utils/               # Helper utilities
│
├── data/                    # Data files and scripts
├── notebooks/               # Jupyter notebooks for analysis
├── tests/                   # Test files
├── config.py                # Configuration settings
├── run.py                   # Application entry point
└── requirements.txt         # Project dependencies
```

## Setup Instructions

1. Clone the repository:
```
git clone <repository-url>
cd heart_risk_monitor
```

2. Create and activate a virtual environment:
```
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the application:
```
python run.py
```

5. Access the application in a web browser:
```
http://localhost:5000
```

## Dashboard Usage

### Analytical Dashboard
- Use the filters on the left to focus on specific patient segments
- Search for individual patients by ID
- View risk distribution and vital sign trends
- Examine lab results and patient metrics compared to population averages
- Monitor high-risk patients requiring immediate attention

### Managerial Dashboard
- Select departments, time periods, and demographic segments using filters
- Analyze risk distribution across different age groups
- Track risk trends over time
- Understand the impact of lifestyle factors on risk levels
- Export data for further analysis or reporting

## Development Roadmap

- Integration with electronic health record (EHR) systems
- Machine learning model for improved risk prediction
- Mobile application for on-the-go monitoring
- Alerts and notification system for critical risk changes
- Additional visualization techniques for deeper insights

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Name - Initial development
