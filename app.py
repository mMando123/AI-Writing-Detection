"""
app.py — تطبيق Flask الرئيسي v4
نظام تجاوز كشف الذكاء الاصطناعي — معالجة ملفات محسّنة
"""

import os
import sys
import io

# ═══ إصلاح ترميز Windows — يجب أن يكون قبل أي import آخر ═══
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

import builtins

_original_print = builtins.print

def safe_print(*args, **kwargs):
    """دالة طباعة آمنة تتجاهل أخطاء الترميز (UnicodeEncodeError) على Windows"""
    try:
        _original_print(*args, **kwargs)
    except UnicodeEncodeError:
        pass
    except Exception:
        pass

builtins.print = safe_print

import uuid
import time
import re
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
from engine.bypass_engine import BypassEngine
from engine.text_analyzer import TextAnalyzer
from engine.file_parser import FileParser
from engine.file_exporter import FileExporter

app = Flask(__name__)
engine = BypassEngine()
analyzer = TextAnalyzer()
file_parser = FileParser()
file_exporter = FileExporter()

# مخزن مؤقت للملفات المُحلَّلة
parsed_docs = {}

# مجلد الرفع المؤقت
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


# ═══════════════════════════════════════════════════════════
#  APIs النص المباشر
# ═══════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════
#  APIs رفع الملفات
# ═══════════════════════════════════════════════════════════

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    رفع ملف واستخراج النص والصور + تحليل سريع.
    """
    if 'file' not in request.files:
        return jsonify({"error": "لم يتم رفع أي ملف"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "اسم الملف فارغ"}), 400

    try:
        t0 = time.time()
        print(f"[UPLOAD] بدأ تحليل: {file.filename}")

        # استخراج النص والصور
        parsed_doc = file_parser.parse(
            file_stream=file.stream,
            filename=file.filename
        )

        doc_id = str(uuid.uuid4())[:12]
        parsed_docs[doc_id] = parsed_doc

        t1 = time.time()
        print(f"[UPLOAD] استخراج: {t1-t0:.1f}s — {len(parsed_doc.paragraphs)} فقرة, {parsed_doc.get_image_count()} صورة")

        # تحليل النص الكامل مرة واحدة
        overall_score = 0
        if parsed_doc.raw_text.strip():
            overall_analysis = analyzer.full_analysis(parsed_doc.raw_text)
            overall_score = overall_analysis['human_score']

        t2 = time.time()
        print(f"[UPLOAD] تحليل: {t2-t1:.1f}s — score={overall_score}")

        # تقدير سريع لكل فقرة
        paragraph_analyses = []
        for para in parsed_doc.paragraphs:
            if para['word_count'] < 3:
                paragraph_analyses.append({
                    'id': para['id'],
                    'text': para['text'],
                    'word_count': para['word_count'],
                    'analysis': None,
                    'status': 'too_short'
                })
                continue

            fp = analyzer.detect_ai_fingerprints(para['text'])
            fp_count = len(fp)

            if fp_count == 0:
                est_score = min(overall_score + 10, 95)
            elif fp_count <= 2:
                est_score = overall_score
            else:
                est_score = max(overall_score - (fp_count * 5), 15)

            status = 'human' if est_score >= 68 else \
                     'mixed' if est_score >= 42 else 'ai'

            paragraph_analyses.append({
                'id': para['id'],
                'text': para['text'],
                'word_count': para['word_count'],
                'analysis': {'human_score': round(est_score, 1)},
                'status': status
            })

        overall_status = 'human' if overall_score >= 68 else \
                         'mixed' if overall_score >= 42 else 'ai'

        print(f"[UPLOAD] اكتمل في {time.time()-t0:.1f}s")

        return jsonify({
            "doc_id": doc_id,
            "filename": parsed_doc.filename,
            "file_type": parsed_doc.file_type,
            "total_words": len(parsed_doc.raw_text.split()),
            "image_count": parsed_doc.get_image_count(),
            "paragraphs": paragraph_analyses,
            "overall_score": overall_score,
            "overall_status": overall_status
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ImportError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"خطأ أثناء معالجة الملف: {str(e)}"}), 500


@app.route('/api/bypass-file', methods=['POST'])
def bypass_file():
    """
    تطبيق التجاوز على ملف مُحلَّل — خط أنابيب محسّن v4.
    
    التحسينات:
    - يحترم التقنيات المختارة من المستخدم
    - ترتيب تطبيق ذكي يمنع التكرار والتضارب
    - تقارب مع تتبع أفضل نتيجة
    - حماية المعنى والسياق الأصلي
    """
    data = request.get_json()
    doc_id = data.get('doc_id', '')
    intensity = float(data.get('intensity', 0.5))
    mode = data.get('mode', 'ai_only')
    techniques = data.get('techniques', None)  # ← جديد: التقنيات المختارة

    if doc_id not in parsed_docs:
        return jsonify({"error": "المستند غير موجود. يرجى رفع الملف مرة أخرى."}), 404

    parsed_doc = parsed_docs[doc_id]
    intensity = max(0.1, min(1.0, intensity))

    # إذا لم يرسل المستخدم تقنيات = استخدام الكل
    if not techniques:
        techniques = ["fingerprints", "perplexity", "burstiness",
                      "watermark", "stylometry", "imperfections"]

    t0 = time.time()
    print(f"[BYPASS] بدأ التجاوز: {len(parsed_doc.paragraphs)} فقرة, mode={mode}, techniques={techniques}")

    modified_paragraphs = {}
    results = []
    total_before = 0
    total_after = 0
    total_words = 0

    for i, para in enumerate(parsed_doc.paragraphs):
        # تخطي الفقرات القصيرة جداً (أقل من 5 كلمات)
        if para['word_count'] < 5:
            results.append({
                'id': para['id'],
                'original': para['text'],
                'modified': para['text'],
                'status': 'skipped',
                'before_score': None,
                'after_score': None
            })
            continue

        # تحليل قبل التجاوز
        before = analyzer.full_analysis(para['text'])
        should_bypass = (mode == 'all') or (before['human_score'] < 68)

        if should_bypass:
            # ═══ خط أنابيب محسّن — تطبيق متدرج مع تقارب ═══
            modified_text = _apply_balanced_bypass(
                para['text'], intensity, techniques, before['human_score']
            )

            after = analyzer.full_analysis(modified_text)

            # حماية: إذا ساءت النتيجة، نحتفظ بالنص الأصلي
            if after['human_score'] < before['human_score'] - 5:
                print(f"  [BYPASS] فقرة {i}: تراجع {before['human_score']}→{after['human_score']}, استخدام الأصلي")
                modified_text = para['text']
                after = before

            modified_paragraphs[para['id']] = modified_text
            results.append({
                'id': para['id'],
                'original': para['text'],
                'modified': modified_text,
                'status': 'modified',
                'before_score': before['human_score'],
                'after_score': after['human_score']
            })
            total_before += before['human_score'] * para['word_count']
            total_after += after['human_score'] * para['word_count']
            print(f"  [BYPASS] فقرة {i}: {before['human_score']}→{after['human_score']} ({para['word_count']} كلمة)")
        else:
            results.append({
                'id': para['id'],
                'original': para['text'],
                'modified': para['text'],
                'status': 'kept',
                'before_score': before['human_score'],
                'after_score': before['human_score']
            })
            total_before += before['human_score'] * para['word_count']
            total_after += before['human_score'] * para['word_count']

        total_words += para['word_count']

    # حفظ التعديلات
    parsed_docs[doc_id + '_modified'] = modified_paragraphs

    overall_before = round(total_before / total_words, 1) if total_words > 0 else 0
    overall_after = round(total_after / total_words, 1) if total_words > 0 else 0

    elapsed = time.time() - t0
    mod_count = sum(1 for r in results if r['status'] == 'modified')
    print(f"[BYPASS] اكتمل في {elapsed:.1f}s — عُدّلت {mod_count}/{len(results)} فقرة, {overall_before}→{overall_after}")

    return jsonify({
        "doc_id": doc_id,
        "results": results,
        "overall_before": overall_before,
        "overall_after": overall_after,
        "improvement": round(overall_after - overall_before, 1),
        "modified_count": mod_count,
        "total_paragraphs": len(results)
    })


def _apply_balanced_bypass(text, intensity, techniques, current_score):
    """
    خط أنابيب تجاوز محسّن v5 — تعديلات أقوى بكثير.
    
    التحسينات:
    - شدة أعلى لكل تقنية (80-100% بدلاً من 50-70%)
    - إضافة إعادة هيكلة الجمل للخط
    - عدم التوقف المبكر
    - تمرير ثانٍ للتعديل الإضافي
    """
    result = text
    
    # ═══ التمرير الأول: التعديلات الأساسية ═══
    
    # المرحلة 1: إزالة البصمات (الأهم — تنظيف أولاً)
    if "fingerprints" in techniques:
        result = engine.remove_ai_fingerprints(result)

    # المرحلة 2: إعادة هيكلة الجمل (تغيير البنية — مهم جداً!)
    result = engine.restructure_sentences(result, intensity * 0.9)

    # المرحلة 3: إزالة العلامات المائية — شدة عالية
    if "watermark" in techniques:
        result = engine.remove_watermarks(result, intensity * 0.85)

    # المرحلة 4: رفع الحيرة — شدة عالية
    if "perplexity" in techniques:
        result = engine.boost_perplexity(result, intensity * 0.9)

    # المرحلة 5: أنسنة الأسلوب — شدة عالية
    if "stylometry" in techniques:
        result = engine.humanize_style(result, intensity * 0.9)

    # المرحلة 6: رفع الانفجارية — شدة عالية
    if "burstiness" in techniques:
        result = engine.enhance_burstiness(result, intensity * 0.8)

    # المرحلة 7: حقن الإنتروبيا
    result = engine.inject_entropy(result, intensity * 0.6)

    # المرحلة 8: عيوب طبيعية
    if "imperfections" in techniques and intensity > 0.2:
        result = engine.add_imperfections(result, intensity * 0.3)

    # ═══ التمرير الثاني: تعديلات إضافية إذا كانت الشدة عالية ═══
    if intensity >= 0.4:
        # تمرير ثانٍ خفيف لاستبدال المزيد من الكلمات
        if "perplexity" in techniques:
            result = engine.boost_perplexity(result, intensity * 0.5)
        if "watermark" in techniques:
            result = engine.remove_watermarks(result, intensity * 0.4)

    # تنظيف نهائي
    result = _clean_text(result)

    return result


def _clean_text(text):
    """تنظيف النص بعد المعالجة — إزالة المسافات الزائدة فقط"""
    # تنظيف مسافات متعددة (لكن الحفاظ على الأسطر الجديدة)
    text = re.sub(r'[^\S\n]+', ' ', text).strip()
    # إزالة المسافات قبل علامات الترقيم
    text = re.sub(r'\s+([.!?؟،,;:])', r'\1', text)
    # إزالة مسافات مزدوجة متبقية
    text = re.sub(r'  +', ' ', text)
    return text


@app.route('/api/download/<doc_id>', methods=['GET'])
def download_file(doc_id):
    """تحميل الملف المُعدَّل مع الصور في أماكنها."""
    if doc_id not in parsed_docs:
        return jsonify({"error": "المستند غير موجود"}), 404

    modified_key = doc_id + '_modified'
    if modified_key not in parsed_docs:
        return jsonify({"error": "لم يتم تطبيق التجاوز بعد"}), 400

    parsed_doc = parsed_docs[doc_id]
    modified_paragraphs = parsed_docs[modified_key]

    print(f"[DOWNLOAD] doc_id={doc_id}, فقرات معدلة: {len(modified_paragraphs)}")

    try:
        file_data, output_type = file_exporter.export(parsed_doc, modified_paragraphs)
        output_filename = file_exporter.get_output_filename(
            parsed_doc.filename, output_type
        )

        print(f"[DOWNLOAD] تم تصدير: {output_filename} ({len(file_data)} bytes)")

        return send_file(
            BytesIO(file_data),
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            if output_type == 'docx' else 'text/plain'
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"خطأ في التصدير: {str(e)}"}), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  AI Detection Bypass System v4")
    print("=" * 60)
    print("  Server running at: http://localhost:5000")
    print("  Supported files: DOCX, PDF, TXT")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)
