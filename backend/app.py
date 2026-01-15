from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.parsers.pmm_parser import PMMParser
from backend.models.llm_client import LLMClient
from backend.utils.excel_generator import ExcelGenerator

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'data/uploads'
EXPORT_FOLDER = 'data/exports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Parse file
    parser = PMMParser()
    items = parser.parse(file_path)

    return jsonify({
        'success': True,
        'file_path': file_path,
        'item_count': len(items),
        'preview': items[:5]
    })

@app.route('/api/process', methods=['POST'])
def process_file():
    """Process uploaded file with LLM categorization"""
    data = request.json
    file_path = data.get('file_path')

    # Parse file
    parser = PMMParser()
    items = parser.parse(file_path)

    # Categorize with LLM
    llm_client = LLMClient()
    categorized_items = []

    for item in items:
        # Use OpenAI for MVP (add Claude in Phase 2)
        llm_result = llm_client.categorize_with_openai(item)

        if llm_result['success']:
            # Merge LLM results into item
            item['Product Category'] = llm_result.get('product_category', '')
            item['Product Category - LLM Reasoning'] = llm_result.get('product_category_reasoning', '')

            item['Product Area'] = llm_result.get('product_area', '')
            item['Product Area - LLM Reasoning'] = llm_result.get('product_area_reasoning', '')

            item['Request type'] = llm_result.get('request_type', '')
            item['Request type - LLM Reasoning'] = llm_result.get('request_type_reasoning', '')

            item['Personas'] = ', '.join(llm_result.get('personas', []))
            item['Personas - LLM Reasoning'] = llm_result.get('personas_reasoning', '')

            item['UXR Needs Based Segmentation'] = ', '.join(llm_result.get('uxr_segments', []))
            item['UXR Needs Based Segmentation - LLM Reasoning'] = llm_result.get('uxr_segments_reasoning', '')

            item['Vertical'] = ', '.join(llm_result.get('vertical', []))
            item['Vertical - LLM Reasoning'] = llm_result.get('vertical_reasoning', '')

            item['User Touchpoint'] = llm_result.get('user_touchpoint', '')
            item['User Touchpoint - LLM Reasoning'] = llm_result.get('user_touchpoint_reasoning', '')

            item['Severity [T-Shirt Size]'] = llm_result.get('severity', '')
            item['Severity [T-Shirt Size] - LLM Reasoning'] = llm_result.get('severity_reasoning', '')

            item['Revenue [Tshirt Size]'] = llm_result.get('revenue_tshirt', '')
            item['Revenue [Tshirt Size] - LLM Reasoning'] = llm_result.get('revenue_tshirt_reasoning', '')
            item['Revenue Sizing Needed'] = 'Yes' if llm_result.get('revenue_sizing_needed') else 'No'

            item['Reach [T-Shirt Size]'] = llm_result.get('reach_tshirt', '')
            item['Reach [T-Shirt Size] - LLM Reasoning'] = llm_result.get('reach_tshirt_reasoning', '')

            if llm_result.get('refined_customer_need'):
                item['Customer need'] = llm_result['refined_customer_need']
                item['Customer need - LLM Reasoning'] = llm_result.get('customer_need_reasoning', '')

            item['llm_confidence'] = llm_result.get('confidence_scores', {})

        categorized_items.append(item)

    # Generate Excel
    generator = ExcelGenerator()
    output_path = os.path.join(EXPORT_FOLDER, f"categorized_{os.path.basename(file_path)}")
    generator.generate(categorized_items, output_path)

    return jsonify({
        'success': True,
        'processed_count': len(categorized_items),
        'export_path': output_path
    })

@app.route('/api/export/<filename>', methods=['GET'])
def download_export(filename):
    """Download exported Excel file"""
    file_path = os.path.join(EXPORT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
