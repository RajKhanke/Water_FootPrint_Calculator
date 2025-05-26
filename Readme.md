# 💧🌱 Water Footprint Calculator - Agricultural Products

Welcome to the Water Footprint Calculator! This web application allows users to upload an image of an agricultural product and receive a detailed analysis of its water footprint, environmental impact, production insights, and more, powered by AIML Techniques.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![Google Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?logo=google)](https://ai.google.dev/models/gemini)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.0%2B-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-3.9%2B-FF6384?logo=chartdotjs)](https://www.chartjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

*   **Image Upload:** Easily upload agricultural product images via drag-and-drop or file browsing.
*   **AI Identification:** Utilizes Google Gemini AI to identify the product from the image.
*   **Water Footprint Analysis:** Calculates and displays the total, green, blue, and grey water footprints (estimated based on global averages and AI knowledge).
*   **Overall Severity:** Provides an overall assessment of the water footprint impact severity.
*   **Detailed Metrics:** Offers insights into environmental impact (carbon footprint, land use), production factors, and additional metrics (water stress contribution, biodiversity impact, etc.).
*   **Visualizations:** Presents water breakdown and regional comparisons using interactive charts.
*   **Comparisons & Recommendations:** Suggests sustainable alternatives and provides tips for consumers and producers.
*   **Interesting Facts:** Shares engaging facts related to the product's water usage and impact.
*   **Responsive UI:** A modern, clean green-white-teal themed interface built with Tailwind CSS, featuring subtle animations and hover effects.
*   **Error Handling:** Gracefully handles API errors and displays fallback messages or partial data when available.

## 🚀 Technologies Used

*   **Backend:** Python, Flask
*   **Frontend:** HTML, CSS (Tailwind CSS via CDN), JavaScript (Vanilla JS, Chart.js via CDN, Font Awesome via CDN)
*   **AI Model:** Google Gemini (specifically `gemini-1.5-flash-latest`)

## 🛠️ Setup and Installation

Follow these steps to get the project running on your local machine:

### Prerequisites

*   Python 3.8+ installed.
*   pip (Python package installer) installed.
*   Git installed.
*   A Google Cloud or MakerSuite account to obtain a **Google Gemini API Key**. You can get one [here](https://aistudio.google.com/app/apikey).

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/water-footprint-calculator.git
    cd water-footprint-calculator
    ```
    *(Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username)*

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up your Google Gemini API Key:**

    **🚨 Security Warning:** Never hardcode your API key directly in your code. Use environment variables.

    Create a file named `.env` in the root directory of the project (where `app.py` is).
    ```env
    GEMINI_API_KEY='YOUR_ACTUAL_GEMINI_API_KEY'
    ```
    *(Replace `'YOUR_ACTUAL_GEMINI_API_KEY'` with the API key you obtained from Google).*

    **Note:** The included `.gitignore` file is configured to ignore `.env` files, ensuring your key is not accidentally committed to your repository.

### Running the Application

1.  **Ensure your virtual environment is activated.**
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  The application will start, typically on `http://127.0.0.1:5000/`. Open this URL in your web browser.

*(Press `Ctrl + C` in your terminal to stop the Flask server).*

## 💡 Usage

1.  Navigate to the application URL in your browser.
2.  Click the "Drop your image here or click to browse" area, or drag and drop an image file onto it.
3.  Once the image is loaded, the "Analyze Water Footprint" button will become active.
4.  Click the button to send the image to the AI for analysis.
5.  Wait for the loading indicator to finish.
6.  Explore the detailed results displayed below the upload section, including product identification, water footprint metrics, definitions, charts, and detailed analysis tabs.

## 📁 Project Structure
Use code with caution.
```bash
├── app.py # Flask backend application
├── requirements.txt # Python dependencies
├── .gitignore # Files ignored by Git
└── templates/
└── index.html # Frontend HTML with CSS and JavaScript
```

## 🤖 AI Model

This project uses the `gemini-1.5-flash-latest` model from the Google Gemini API. The Flask backend sends the uploaded image and a detailed prompt to the model, requesting a structured JSON response containing all the water footprint and environmental data. The backend then parses this JSON to display the information in the frontend.

The prompt is carefully designed to extract specific information, including units for measurements, to ensure the frontend can display the data accurately. A fallback mechanism is included to handle potential JSON parsing errors, providing raw AI output if structured data extraction fails.

## 👋 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add your feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to the project's styling and includes necessary tests if applicable.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (You'll need to create this file if you don't have one).
