"""
app.py — تطبيق Flask الرئيسي
نظام تجاوز كشف الذكاء الاصطناعي
"""

from flask import Flask, render_template, request, jsonify
from engine.bypass_engine import BypassEngine
from engine.text_analyzer import TextAnalyzer

app = Flask(__name__)
engine = BypassEngine()
analyzer = TextAnalyzer()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """تحليل النص وإرجاع المؤشرات"""
    data = request.get_json()
    text = data.get('text', '')
    if not text.strip():
        return jsonify({"error": "النص فارغ"}), 400
    result = analyzer.full_analysis(text)
    return jsonify(result)


@app.route('/api/bypass', methods=['POST'])
def bypass():
    """تطبيق تجاوز شامل على النص"""
    data = request.get_json()
    text = data.get('text', '')
    intensity = float(data.get('intensity', 0.5))
    techniques = data.get('techniques', None)

    if not text.strip():
        return jsonify({"error": "النص فارغ"}), 400

    intensity = max(0.1, min(1.0, intensity))

    if techniques:
        result = engine.selective_bypass(text, techniques, intensity)
    else:
        result = engine.full_bypass(text, intensity)

    return jsonify(result)


@app.route('/api/fingerprints', methods=['POST'])
def fingerprints():
    """كشف بصمات AI في النص"""
    data = request.get_json()
    text = data.get('text', '')
    if not text.strip():
        return jsonify({"error": "النص فارغ"}), 400
    result = analyzer.detect_ai_fingerprints(text)
    return jsonify({"fingerprints": result, "count": len(result)})


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  AI Detection Bypass System")
    print("=" * 60)
    print("  Server running at: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)
