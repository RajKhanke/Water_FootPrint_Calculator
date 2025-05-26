from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import base64
import json
import os
from PIL import Image
import io
import re

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY") # Use environment variable first

if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_FALLBACK_PLACEHOLDER_KEY":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        # Test the model connection
        list(model.generate_content("ping", stream=True))
        print("Gemini model loaded successfully.")
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")
        model = None # Set model to None if initialization fails
else:
    print("Error: GEMINI_API_KEY environment variable not set or is the placeholder. AI model will not be available.")
    model = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_water_footprint():
    if model is None:
         return jsonify({'success': False, 'error': 'AI model failed to initialize. Please ensure GEMINI_API_KEY is set correctly.'}), 500

    try:
        data = request.json
        image_data = data.get('image')

        if not image_data:
             return jsonify({'success': False, 'error': 'No image data provided.'}), 400

        # Remove data URL prefix if present
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Ensure image is in RGB if it's RGBA
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Prepare the prompt with explicit unit requests for string values
        prompt = """
        Analyze the agricultural product shown in this image and provide a comprehensive water footprint analysis based on global averages and regional variations.

        Provide a detailed JSON response with the following structure. Ensure the response is *only* the JSON object, wrapped in triple backticks for clarity, and is valid JSON. For any data point that cannot be confidently estimated, use the string value "N/A".

        IMPORTANT UNIT INSTRUCTIONS:
        - For water volume metrics (total, green, blue, grey, global average, regional variations, water savings), provide the value as a string INCLUDING " L/kg" at the end (e.g., "1500 L/kg").
        - For percentage values (confidence, difference), provide the value as a string INCLUDING "%" at the end (e.g., "85%", "-5%").
        - For scores out of 10, provide as a string "X/10" (e.g., "7/10").
        - For Carbon Footprint, provide as a string INCLUDING " kg CO2e/kg" (e.g., "2.5 kg CO2e/kg").
        - For Land Use, provide as a string INCLUDING " m²/kg" (e.g., "3 m²/kg").
        - For Economic Water Cost, provide as a string INCLUDING " USD/kg" (e.g., "0.5 USD/kg").
        - For chart data arrays ("values", "water_usage"), provide ONLY numeric values (e.g., 60.5, 1500). The frontend expects numbers here.
        - For qualitative values (severity, category, dependency, sensitivity, seasonal buying, impact types), provide the descriptive string or "N/A".
        - For lists (seasonal availability, tips, practices, conservation, facts), provide arrays of strings.

        ```json
        {
            "product_identification": {
                "detected_product": "product name (e.g., Apple, Tomato, Almonds, Beef)",
                "confidence": "estimated confidence level string with unit (e.g., '85%' or 'N/A')",
                "category": "product category (e.g., Fruits, Vegetables, Grains, Nuts, Meat, Dairy)",
                "scientific_name": "scientific name if applicable (e.g., Malus domestica) or 'N/A'"
            },
            "overall_severity": "Overall water footprint impact severity (e.g., Low, Medium, High, Very High, Unknown)",
            "water_footprint": {
                "total_footprint": "estimated total water footprint string with unit (e.g., '1500 L/kg' or 'N/A')",
                "green_water": "estimated green water component string with unit (e.g., '900 L/kg' or 'N/A')",
                "blue_water": "estimated blue water component string with unit (e.g., '400 L/kg' or 'N/A')",
                "grey_water": "estimated grey water component string with unit (e.g., '200 L/kg' or 'N/A')",
                "global_average": "estimated global average for this product string with unit (e.g., '1500 L/kg' or 'N/A')",
                "regional_variations": {
                    "arid_regions": "estimated value for arid regions string with unit (e.g., '2000 L/kg' or 'N/A')",
                    "temperate_regions": "estimated value for temperate regions string with unit (e.g., '1200 L/kg' or 'N/A')",
                    "tropical_regions": "estimated value for tropical regions string with unit (e.g., '1800 L/kg' or 'N/A')"
                }
            },
            "definitions": {
                "green_water": "brief definition of green water footprint",
                "blue_water": "brief definition of blue water footprint",
                "grey_water": "brief definition of grey water footprint"
            },
            "water_breakdown_chart": {
                "labels": ["Green Water", "Blue Water", "Grey Water"],
                "values": [percentage of green water (number, e.g., 60.5), percentage of blue water (number, e.g., 30), percentage of grey water (number, e.g., 9.5)],
                "colors": ["#48BB78", "#4299E1", "#A78BFA"]
            },
             "regional_comparison_chart": {
                "regions": ["Global Average", "Arid Regions", "Temperate", "Tropical"],
                "water_usage": [estimated value for global average (number, e.g., 1500), estimated value for arid (number), estimated value for temperate (number), estimated value for tropical (number)]
            },
            "environmental_impact": {
                "severity_score": "score string with unit (e.g., '7/10' or 'N/A')",
                "impact_category": "Overall impact category (e.g., Low, Medium, High, Very High, Unknown)",
                "sustainability_rating": "Sustainability rating (e.g., 'B+' or 'N/A')",
                "carbon_footprint": "estimated carbon footprint string with unit (e.g., '2.5 kg CO2e/kg' or 'N/A')",
                "land_use": "estimated land use string with unit (e.g., '3 m²/kg' or 'N/A')"
            },
            "production_insights": {
                "growing_season": "typical growing season or climate requirements (e.g., 'Year-round', 'Summer months', 'Warm climate', or 'N/A')",
                "water_efficiency": "estimated water efficiency rating string with unit (e.g., '8/10' or 'N/A')",
                "irrigation_dependency": "level of dependency on irrigation (e.g., Low, Medium, High, Unknown)",
                "climate_sensitivity": "sensitivity to climate changes (e.g., Low, Medium, High, Unknown)",
                "seasonal_availability": ["list of months when typically in season (e.g., 'June', 'July', 'August') or empty array if year-round/unknown"]
            },
            "comparisons": {
                "vs_similar_products": [
                    {"product": "name of similar product", "water_footprint": "estimated liters/kg string with unit (e.g., '1300 L/kg' or 'N/A')", "difference": "percentage difference string with unit vs detected product (e.g., '+10%', '-5%', 'Same', 'N/A')"},
                     {"product": "name of another similar product", "water_footprint": "estimated liters/kg string with unit (e.g., '1800 L/kg' or 'N/A')", "difference": "percentage difference string with unit vs detected product (e.g., '+10%', '-5%', 'Same', 'N/A')"}
                     # Add 1-3 similar products
                ],
                "vs_alternatives": [
                    {"alternative": "name of sustainable alternative", "water_savings": "estimated liters/kg saved string with unit (e.g., 'Saves ~500 L/kg' or 'N/A')", "benefit": "brief description of benefit (e.g., 'Lower water use', 'Grows in arid climates')"},
                     # Add 1-2 alternatives
                ]
            },
            "recommendations": {
                "consumer_tips": ["tip 1 for consumers", "tip 2 for consumers", "tip 3 for consumers"],
                "sustainable_practices": ["practice 1 for production/supply chain", "practice 2 for production/supply chain"],
                "water_conservation": ["method 1 for conservation related to this product", "method 2 for conservation"],
                "seasonal_buying": "best months or time period to buy for sustainability (e.g., 'Peak season is June-August', or 'Year-round', or 'N/A')"
            },
            "interesting_facts": [
                "interesting fact 1 about water usage or production",
                "interesting fact 2 about environmental impact",
                "interesting fact 3 about this product"
                # Add 2-4 facts
            ],
            "impact_metrics": {
                "water_stress_contribution": "estimated percentage contribution string with unit to local/regional water stress (e.g., 'High' or '20%' or 'N/A')",
                "biodiversity_impact": "estimated impact on biodiversity (e.g., Low, Medium, High, Very High, Unknown)",
                "soil_health_impact": "estimated impact on soil health (e.g., Positive, Neutral, Negative, Unknown)",
                "economic_water_cost": "estimated economic cost string with unit of water used per kg (e.g., '0.5 USD/kg' or 'N/A')"
                 # Add other specific metrics if relevant
            }
        }
        ```
        Provide accurate, research-based data. If exact data isn't available, provide reasonable estimates based on general knowledge. Ensure the JSON is strictly formatted as requested, contains valid JSON syntax, and is enclosed *only* by the triple backticks.
        """

        response = model.generate_content([prompt, image])
        response_text = response.text
        print("Raw Gemini Response:")
        print(response_text) # Log raw response for debugging

        try:
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)

            if not json_match:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start == -1 or json_end == -1 or json_end < json_start:
                     raise ValueError("Could not find a JSON object in the response.")
                json_str = response_text[json_start:json_end].strip()
                print("Warning: JSON not found within ```json```. Extracted based on {} bounds.")
            else:
                 json_str = json_match.group(1).strip()
                 print("JSON found within ```json```.")

            result = json.loads(json_str)

            if 'product_identification' not in result or 'water_footprint' not in result or 'overall_severity' not in result:
                 raise ValueError("Parsed JSON is missing required top-level keys.")

            return jsonify({
                'success': True,
                'data': result
            })

        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON parsing or structure error: {e}")

            fallback_data = {
                'product_identification': {'detected_product': 'Unknown Product', 'confidence': 'N/A', 'category': 'N/A', 'scientific_name': 'N/A'},
                'overall_severity': 'Unknown',
                'water_footprint': {'total_footprint': 'N/A', 'green_water': 'N/A', 'blue_water': 'N/A', 'grey_water': 'N/A', 'global_average': 'N/A', 'regional_variations': {}},
                'definitions': {}, # Include definitions key in fallback
                'environmental_impact': {'severity_score': 'N/A', 'impact_category': 'Unknown', 'sustainability_rating': 'N/A', 'carbon_footprint': 'N/A', 'land_use': 'N/A'},
                'production_insights': {'growing_season': 'N/A', 'water_efficiency': 'N/A', 'irrigation_dependency': 'Unknown', 'climate_sensitivity': 'Unknown', 'seasonal_availability': []},
                'comparisons': {'vs_similar_products': [], 'vs_alternatives': []},
                'recommendations': {'consumer_tips': [], 'sustainable_practices': [], 'water_conservation': [], 'seasonal_buying': 'N/A'},
                'interesting_facts': ["Could not retrieve detailed facts due to analysis error."],
                'water_breakdown_chart': None, # No chart data
                'regional_comparison_chart': None, # No chart data
                'impact_metrics': {'water_stress_contribution': 'N/A', 'biodiversity_impact': 'Unknown', 'soil_health_impact': 'Unknown', 'economic_water_cost': 'N/A'},
                'raw_analysis_text_fallback': response_text
            }
            return jsonify({
                'success': False,
                'error': f"Could not fully parse AI response. Reason: {e}",
                'data': fallback_data
            }), 500

    except Exception as e:
        print(f"An unexpected error occurred during content generation: {e}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred during analysis: ' + str(e),
            'data': None
        }), 500


@app.route('/health')
def health_check():
    status = 'healthy' if model is not None else 'warning (model not loaded)'
    return jsonify({'status': status})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
