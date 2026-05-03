"""
text_analyzer.py — محلل النصوص لقياس مؤشرات الكشف
يحسب: الحيرة التقريبية، الانفجارية، مؤشرات الأسلوب، النتيجة الإجمالية
مبني على القواعد الموثقة في: AI_Writing_Detection_القواعد_الشاملة.md
"""

import re
import math
from collections import Counter, defaultdict


class TextAnalyzer:
    """
    محلل النصوص — يقيس المؤشرات التي تستخدمها أدوات الكشف
    
    المؤشرات المقاسة:
    1. الحيرة التقريبية (Perplexity Estimate)
    2. الانفجارية (Burstiness)
    3. المؤشرات الأسلوبية (Stylometric Features)
    4. المؤشرات الإحصائية (Statistical Patterns)
    5. النتيجة الإجمالية (Overall AI Score)
    """

    def __init__(self):
        # كلمات عربية شائعة (الأكثر تكراراً في نصوص الذكاء الاصطناعي)
        self.ar_common_words = {
            "يمكن", "يجب", "بشكل", "من خلال", "بالإضافة", "ومع ذلك",
            "علاوة", "بالتالي", "يتضمن", "يوفر", "يساعد", "يعتبر",
            "بشكل عام", "في هذا السياق", "من الجدير بالذكر", "تجدر الإشارة",
            "يُعد", "يُعتبر", "بصفة عامة", "في الختام", "وبالتالي",
        }
        # كلمات إنجليزية شائعة في نصوص AI
        self.en_common_ai_words = {
            "utilize", "furthermore", "moreover", "consequently", "therefore",
            "additionally", "comprehensive", "significant", "facilitate",
            "implement", "demonstrate", "enhance", "crucial", "essential",
            "leverage", "streamline", "delve", "tapestry", "multifaceted",
            "it is important to note", "in conclusion", "in summary",
            "plays a crucial role", "it is worth noting",
        }

        # عبارات "بصمة" الذكاء الاصطناعي
        self.ai_fingerprint_ar = [
            "تجدر الإشارة إلى", "من الجدير بالذكر", "يلعب دوراً حيوياً",
            "في هذا السياق", "من المهم أن نلاحظ", "وفي الختام",
            "على صعيد آخر", "في ضوء ما سبق", "مما لا شك فيه",
            "ليس من المبالغة القول", "في نهاية المطاف",
            "يمكن القول إن", "بناءً على ما تقدم", "في هذا الإطار",
        ]
        self.ai_fingerprint_en = [
            "it is important to note that", "it is worth noting that",
            "plays a crucial role", "in today's world",
            "it's important to remember", "in conclusion",
            "this comprehensive", "delve into", "tapestry of",
            "multifaceted approach", "let's explore",
            "in the realm of", "navigating the",
        ]

    def detect_language(self, text):
        """كشف لغة النص"""
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        latin_chars = sum(1 for c in text if 'a' <= c.lower() <= 'z')
        total = arabic_chars + latin_chars
        if total == 0:
            return "ar"
        return "ar" if arabic_chars / total > 0.3 else "en"

    def split_sentences(self, text):
        """تقسيم النص إلى جمل"""
        # أنماط نهاية الجملة
        sentences = re.split(r'[.!?؟。！？]+', text)
        # تنظيف الجمل
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
        return sentences

    def get_words(self, text):
        """استخراج الكلمات من النص"""
        lang = self.detect_language(text)
        if lang == "ar":
            words = re.findall(r'[\u0600-\u06FF]+', text)
        else:
            words = re.findall(r'[a-zA-Z]+', text.lower())
        return words

    # ═══════════════════════════════════════════════════════════
    # 1. قياس الحيرة التقريبية (Perplexity Estimate)
    # ═══════════════════════════════════════════════════════════
    def _ngram_entropy(self, words, n=2):
        """حساب إنتروبيا N-gram — الأساس الرياضي للحيرة"""
        if len(words) < n + 1:
            return 0.0
        ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]
        freq = Counter(ngrams)
        total = len(ngrams)
        entropy = -sum((c / total) * math.log2(c / total) for c in freq.values())
        return entropy

    def _zipf_deviation(self, words):
        """
        انحراف عن قانون Zipf — AI يتبع Zipf بدقة مفرطة.
        البشر ينحرفون عنه أكثر.
        """
        if len(words) < 20:
            return 0.5
        freq = Counter(words)
        sorted_freqs = sorted(freq.values(), reverse=True)
        n = min(len(sorted_freqs), 30)
        if n < 3 or sorted_freqs[0] == 0:
            return 0.5
        deviations = []
        for rank in range(1, n):
            expected = sorted_freqs[0] / (rank + 1)
            actual = sorted_freqs[rank] if rank < len(sorted_freqs) else 0
            if expected > 0:
                deviations.append(abs(actual - expected) / expected)
        return sum(deviations) / len(deviations) if deviations else 0.5

    def _repetition_score(self, text):
        """
        كشف أنماط التكرار — AI يكرر بنى وعبارات بشكل منهجي.
        يقيس: تكرار بدايات الجمل، تكرار ثنائيات الكلمات، تكرار البنى.
        """
        sentences = self.split_sentences(text)
        if len(sentences) < 4:
            return 0.5
        words = self.get_words(text)
        total_words = len(words)
        if total_words < 10:
            return 0.5

        # 1. تكرار بدايات الجمل (نفس الكلمة الأولى)
        starters = [s.split()[0] for s in sentences if s.split()]
        starter_freq = Counter(starters)
        max_starter_repeat = max(starter_freq.values()) / len(starters) if starters else 0

        # 2. تكرار ثنائيات الكلمات (bigrams)
        bigrams = [tuple(words[i:i+2]) for i in range(len(words)-1)]
        bigram_freq = Counter(bigrams)
        repeated_bigrams = sum(1 for c in bigram_freq.values() if c > 2)
        bigram_repeat_ratio = repeated_bigrams / max(len(bigram_freq), 1)

        # 3. تكرار أنماط بنية الجمل (طول الجملة كبصمة)
        patterns = [len(s.split()) for s in sentences]
        pattern_freq = Counter(patterns)
        dominant_pattern = max(pattern_freq.values()) / len(patterns) if patterns else 0

        # كلما زاد التكرار = أشبه بالآلة (نتيجة أقل)
        repetition = (max_starter_repeat * 0.4 + bigram_repeat_ratio * 0.3 + dominant_pattern * 0.3)
        return round(min(repetition, 1.0), 3)

    def _sentence_uniformity(self, text):
        """
        قياس تجانس أطوال الجمل — أهم مؤشر لكشف AI.
        AI ينتج جملاً متقاربة الطول (12-18 كلمة). البشر يتذبذبون.
        القيمة: 0 (متنوع جداً = بشري) إلى 1 (متجانس = AI)
        """
        sentences = self.split_sentences(text)
        if len(sentences) < 4:
            return 0.5

        lengths = [len(s.split()) for s in sentences]
        mean_len = sum(lengths) / len(lengths)
        if mean_len == 0:
            return 0.5

        # 1. نسبة الجمل في النطاق "المريح" لـ AI (10-20 كلمة)
        in_comfort_zone = sum(1 for l in lengths if 10 <= l <= 20)
        comfort_ratio = in_comfort_zone / len(lengths)

        # 2. هل هناك جمل قصيرة جداً (< 6) أو طويلة جداً (> 25)؟
        has_extremes = sum(1 for l in lengths if l < 6 or l > 25)
        extreme_ratio = has_extremes / len(lengths)

        # 3. الانحراف المعياري النسبي (CV) — منخفض = AI
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        std_dev = math.sqrt(variance)
        cv = std_dev / mean_len if mean_len > 0 else 0

        # 4. أقصى فرق بين جملتين متتاليتين
        max_consecutive_diff = 0
        for i in range(1, len(lengths)):
            diff = abs(lengths[i] - lengths[i-1])
            max_consecutive_diff = max(max_consecutive_diff, diff)
        normalized_max_diff = min(max_consecutive_diff / 15, 1)

        # التجانس: عالٍ إذا كانت الجمل في comfort zone مع CV منخفض
        uniformity = (
            comfort_ratio * 0.35 +
            (1 - min(extreme_ratio * 3, 1)) * 0.25 +
            (1 - min(cv / 0.8, 1)) * 0.25 +
            (1 - normalized_max_diff) * 0.15
        )
        return round(min(max(uniformity, 0), 1.0), 3)

    def _transition_overuse(self, text):
        """
        قياس الإفراط في استخدام الروابط الانتقالية الرسمية.
        AI يستخدم "Furthermore", "Moreover", "Additionally" بكثرة.
        البشر يستخدمونها أقل ويربطون الجمل بشكل طبيعي أو بدون روابط.
        القيمة: 0 (استخدام طبيعي) إلى 1 (إفراط = AI)
        """
        lang = self.detect_language(text)
        sentences = self.split_sentences(text)
        if len(sentences) < 3:
            return 0.0

        if lang == "ar":
            formal_transitions = [
                "بالإضافة", "علاوة", "فضلاً", "من ناحية أخرى",
                "بالتالي", "لذلك", "وبالتالي", "ومع ذلك",
                "في هذا السياق", "من هذا المنطلق", "في ضوء",
                "تجدر الإشارة", "من الجدير بالذكر",
            ]
        else:
            formal_transitions = [
                "furthermore", "moreover", "additionally", "consequently",
                "therefore", "nevertheless", "nonetheless", "in addition",
                "in conclusion", "as a result", "on the other hand",
                "it is important", "it is worth noting", "it should be noted",
                "significantly", "subsequently", "accordingly",
            ]

        text_lower = text.lower()
        transition_count = sum(1 for t in formal_transitions if t in text_lower)
        # نسبة الروابط لكل جملة
        ratio = transition_count / len(sentences)
        # أكثر من رابط لكل 3 جمل = إفراط
        overuse = min(ratio / 0.35, 1.0)
        return round(overuse, 3)

    def estimate_perplexity(self, text):
        """
        تقدير الحيرة بناءً على N-gram entropy + مؤشرات إحصائية متعددة.
        
        القيم المرجعية (من الوثيقة):
        - نص بشري عادي: 80-100
        - نص GPT-4 غير معدل: 20-30
        - نص معدل: 35-60
        """
        words = self.get_words(text)
        if len(words) < 5:
            return 50.0

        total_words = len(words)
        unique_words = len(set(words))

        # 1. N-gram entropy (bigram + trigram)
        bigram_entropy = self._ngram_entropy(words, 2)
        trigram_entropy = self._ngram_entropy(words, 3)
        max_possible_entropy = math.log2(max(total_words, 2))
        normalized_entropy = ((bigram_entropy + trigram_entropy) / 2) / max(max_possible_entropy, 1)

        # 2. TTR مصحح (Guiraud's corrected TTR — أدق للنصوص المتفاوتة الطول)
        guiraud_ttr = unique_words / math.sqrt(total_words) if total_words > 0 else 0
        normalized_guiraud = min(guiraud_ttr / 12, 1)

        # 3. Hapax Legomena ratio
        word_freq = Counter(words)
        hapax = sum(1 for c in word_freq.values() if c == 1)
        hapax_ratio = hapax / total_words

        # 4. نسبة كلمات AI الشائعة
        lang = self.detect_language(text)
        common = self.ar_common_words if lang == "ar" else self.en_common_ai_words
        ai_word_count = sum(1 for w in words if w in common)
        ai_word_ratio = ai_word_count / total_words

        # 5. تنوع بدايات الجمل
        sentences = self.split_sentences(text)
        if sentences:
            starters = [s.split()[0] for s in sentences if s.split()]
            starter_diversity = len(set(starters)) / len(starters) if starters else 0
        else:
            starter_diversity = 0.5

        # 6. انحراف Zipf
        zipf_dev = self._zipf_deviation(words)
        normalized_zipf = min(zipf_dev / 1.5, 1)

        perplexity = (
            normalized_entropy * 25 +       # إنتروبيا N-gram (0-25)
            normalized_guiraud * 20 +        # تنوع المفردات المصحح (0-20)
            hapax_ratio * 20 +               # ندرة الكلمات (0-20)
            (1 - ai_word_ratio) * 10 +       # عدم استخدام كلمات AI (0-10)
            starter_diversity * 10 +          # تنوع بدايات الجمل (0-10)
            normalized_zipf * 15             # انحراف Zipf (0-15)
        )

        return round(min(max(perplexity, 5), 100), 1)

    # ═══════════════════════════════════════════════════════════
    # 2. قياس الانفجارية (Burstiness)
    # ═══════════════════════════════════════════════════════════
    def calculate_burstiness(self, text):
        """
        قياس الانفجارية — تباين أنماط الكتابة.
        يستخدم معامل التباين CV + تحليل الفروق المتتالية + مؤشر Gini للأطوال.
        
        القيم المرجعية (من الوثيقة):
        - كتابة بشرية: 0.6 - 1.2
        - ذكاء اصطناعي نقي: 0.2 - 0.4
        - نص معدل (هجين): 0.4 - 0.7
        """
        sentences = self.split_sentences(text)
        if len(sentences) < 3:
            return 0.3

        lengths = [len(s.split()) for s in sentences]
        n = len(lengths)
        mean_len = sum(lengths) / n
        if mean_len == 0:
            return 0.3

        # 1. معامل التباين CV — المؤشر الأساسي
        variance = sum((l - mean_len) ** 2 for l in lengths) / n
        cv_length = math.sqrt(variance) / mean_len

        # 2. مؤشر Gini لأطوال الجمل — يقيس عدم التساوي في التوزيع
        sorted_lens = sorted(lengths)
        cumulative = sum((2 * (i + 1) - n - 1) * sorted_lens[i] for i in range(n))
        gini = cumulative / (n * sum(sorted_lens)) if sum(sorted_lens) > 0 else 0

        # 3. نسبة الجمل القصيرة جداً والطويلة جداً (الذيول)
        short = sum(1 for l in lengths if l < 5)
        long_s = sum(1 for l in lengths if l > 20)
        extremes_ratio = (short + long_s) / n

        # 4. متوسط الفرق المطلق بين الجمل المتتالية
        consecutive_diffs = [abs(lengths[i] - lengths[i-1]) for i in range(1, n)]
        mean_diff = sum(consecutive_diffs) / len(consecutive_diffs) if consecutive_diffs else 0
        normalized_mean_diff = min(mean_diff / 15, 1)

        # 5. تنوع علامات الترقيم + أسئلة
        punct_types = set(re.findall(r'[.!?؟،,;:—\-…()\[\]]', text))
        punct_diversity = min(len(punct_types) / 8, 1)
        questions = text.count('?') + text.count('؟')
        exclamations = text.count('!')
        rhetorical_score = min((questions + exclamations) / max(n * 0.12, 1), 1)

        # 6. تنوع تعقيد الجمل (بناءً على عدد الفواصل والروابط)
        complexity_scores = []
        for s in sentences:
            commas = s.count('،') + s.count(',')
            depth = min(commas, 4)
            complexity_scores.append(depth)
        if complexity_scores:
            complexity_cv = (max(complexity_scores) - min(complexity_scores)) / max(mean_len, 1)
        else:
            complexity_cv = 0

        burstiness = (
            cv_length * 0.25 +
            gini * 0.20 +
            extremes_ratio * 0.15 +
            normalized_mean_diff * 0.15 +
            punct_diversity * 0.08 +
            rhetorical_score * 0.10 +
            min(complexity_cv, 0.5) * 0.07
        )

        return round(min(max(burstiness, 0.05), 1.2), 2)

    # ═══════════════════════════════════════════════════════════
    # 3. تحليل المؤشرات الأسلوبية (Stylometry)
    # ═══════════════════════════════════════════════════════════
    def analyze_stylometry(self, text):
        """
        تحليل أسلوبي شامل — يقيس مدى 'بشرية' النص
        النتيجة من 0 (آلي تماماً) إلى 100 (بشري تماماً)
        """
        lang = self.detect_language(text)
        words = self.get_words(text)
        sentences = self.split_sentences(text)
        total_words = len(words)
        
        if total_words < 10:
            return {"score": 50, "details": {}}

        scores = {}

        # 1. استخدام الضمائر الشخصية
        if lang == "ar":
            personal_pronouns = ["أنا", "نحن", "أعتقد", "رأيي", "تجربتي", "شخصياً"]
        else:
            personal_pronouns = ["i", "me", "my", "we", "our", "myself", "personally"]
        
        pronoun_count = sum(1 for w in words if w in personal_pronouns)
        scores["personal_pronouns"] = min(pronoun_count / max(total_words / 50, 1), 1) * 100

        # 2. وجود عبارات بصمة AI
        fingerprints = self.ai_fingerprint_ar if lang == "ar" else self.ai_fingerprint_en
        text_lower = text.lower()
        fp_count = sum(1 for fp in fingerprints if fp in text_lower)
        scores["ai_fingerprints"] = max(0, 100 - fp_count * 20)

        # 3. تنوع مستوى الرسمية
        if lang == "ar":
            informal_markers = ["يعني", "بصراحة", "الحقيقة", "خلاص", "طيب", "ببساطة"]
        else:
            informal_markers = ["honestly", "basically", "i mean", "well", "you know", "like"]
        
        informal_count = sum(1 for w in words if w in informal_markers)
        scores["formality_variation"] = min(informal_count / max(total_words / 100, 1), 1) * 100

        # 4. وجود أخطاء أو تصحيحات ذاتية
        self_corrections = text.count("—") + text.count("أقصد") + text.count("أعني") + text.count("I mean")
        scores["self_corrections"] = min(self_corrections / 3, 1) * 100

        # 5. تنوع بنى الجمل (بسيطة / مركبة / معقدة)
        if sentences:
            simple = sum(1 for s in sentences if len(s.split()) < 8)
            medium = sum(1 for s in sentences if 8 <= len(s.split()) <= 18)
            complex_s = sum(1 for s in sentences if len(s.split()) > 18)
            total_s = len(sentences)
            categories_present = (1 if simple > 0 else 0) + (1 if medium > 0 else 0) + (1 if complex_s > 0 else 0)
            scores["sentence_variety"] = (categories_present / 3) * 100
        else:
            scores["sentence_variety"] = 33

        # 6. وجود أسئلة
        question_marks = text.count('?') + text.count('؟')
        scores["questions"] = min(question_marks / max(len(sentences) * 0.15, 1), 1) * 100

        # 7. تفاوت طول الفقرات
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) > 1:
            para_lengths = [len(p.split()) for p in paragraphs]
            para_cv = (max(para_lengths) - min(para_lengths)) / (sum(para_lengths) / len(para_lengths)) if para_lengths else 0
            scores["paragraph_variation"] = min(para_cv / 2, 1) * 100
        else:
            scores["paragraph_variation"] = 20

        # النتيجة الإجمالية (المتوسط المرجح)
        weights = {
            "personal_pronouns": 0.18,
            "ai_fingerprints": 0.22,
            "formality_variation": 0.12,
            "self_corrections": 0.10,
            "sentence_variety": 0.15,
            "questions": 0.10,
            "paragraph_variation": 0.13,
        }

        total_score = sum(scores[k] * weights[k] for k in weights)
        
        return {
            "score": round(total_score, 1),
            "details": {k: round(v, 1) for k, v in scores.items()},
        }

    # ═══════════════════════════════════════════════════════════
    # 4. كشف بصمات الذكاء الاصطناعي
    # ═══════════════════════════════════════════════════════════
    def detect_ai_fingerprints(self, text):
        """
        كشف العبارات والأنماط المميزة للذكاء الاصطناعي
        يُرجع قائمة بالعبارات المكتشفة ومواقعها
        """
        lang = self.detect_language(text)
        fingerprints = self.ai_fingerprint_ar if lang == "ar" else self.ai_fingerprint_en
        text_lower = text.lower() if lang == "en" else text
        
        found = []
        for fp in fingerprints:
            fp_check = fp.lower() if lang == "en" else fp
            idx = text_lower.find(fp_check)
            while idx != -1:
                found.append({
                    "phrase": fp,
                    "position": idx,
                    "severity": "high"
                })
                idx = text_lower.find(fp_check, idx + 1)

        return found

    # ═══════════════════════════════════════════════════════════
    # 5. التحليل الإحصائي العام
    # ═══════════════════════════════════════════════════════════
    def statistical_analysis(self, text):
        """تحليل إحصائي شامل للنص"""
        words = self.get_words(text)
        sentences = self.split_sentences(text)
        total_words = len(words)

        if total_words < 5:
            return {}

        word_lengths = [len(w) for w in words]
        sent_lengths = [len(s.split()) for s in sentences] if sentences else [0]

        return {
            "total_words": total_words,
            "total_sentences": len(sentences),
            "unique_words": len(set(words)),
            "type_token_ratio": round(len(set(words)) / total_words, 3),
            "avg_word_length": round(sum(word_lengths) / total_words, 1),
            "avg_sentence_length": round(sum(sent_lengths) / len(sent_lengths), 1) if sent_lengths else 0,
            "min_sentence_length": min(sent_lengths) if sent_lengths else 0,
            "max_sentence_length": max(sent_lengths) if sent_lengths else 0,
            "sentence_length_std": round(
                math.sqrt(sum((l - sum(sent_lengths)/len(sent_lengths))**2 for l in sent_lengths) / len(sent_lengths)), 1
            ) if sent_lengths else 0,
        }

    # ═══════════════════════════════════════════════════════════
    # 6. التقرير الشامل
    # ═══════════════════════════════════════════════════════════
    def full_analysis(self, text):
        """
        تحليل شامل للنص — يُرجع كل المؤشرات مع تقييم إجمالي.
        
        يستخدم نظام Ensemble مرجح (كما في GPTZero) يجمع:
        - Perplexity (n-gram entropy)
        - Burstiness (CV + Gini)
        - Stylometry (12 مؤشر)
        - Repetition patterns
        - AI fingerprints
        
        النتيجة النهائية:
        - 0-30: احتمال عالٍ بأنه نص AI (سهل الكشف)
        - 30-60: منطقة رمادية
        - 60-100: يبدو بشرياً (صعب الكشف)
        """
        perplexity = self.estimate_perplexity(text)
        burstiness = self.calculate_burstiness(text)
        stylometry = self.analyze_stylometry(text)
        ai_fingerprints = self.detect_ai_fingerprints(text)
        statistics = self.statistical_analysis(text)
        repetition = self._repetition_score(text)
        uniformity = self._sentence_uniformity(text)
        transition_score = self._transition_overuse(text)

        # ═══ نظام التسجيل المُركَّب (Ensemble Scoring) — v2 ═══
        perplexity_score = min(perplexity / 100, 1) * 100
        burstiness_score = min(burstiness / 0.8, 1) * 100
        fingerprint_penalty = min(len(ai_fingerprints) * 12, 50)
        repetition_penalty = repetition * 100
        uniformity_penalty = uniformity * 100  # تجانس عالٍ = AI
        transition_penalty = transition_score * 100  # إفراط في الروابط = AI

        # المعادلة المُركَّبة مع المؤشرات الجديدة
        raw_score = (
            perplexity_score * 0.20 +
            burstiness_score * 0.18 +
            stylometry["score"] * 0.22 +
            max(0, 100 - fingerprint_penalty) * 0.10 +
            max(0, 100 - repetition_penalty) * 0.10 +
            max(0, 100 - uniformity_penalty) * 0.10 +
            max(0, 100 - transition_penalty) * 0.10
        )

        # معايرة: النصوص ذات البصمات الكثيرة تُعاقب بشدة
        if len(ai_fingerprints) >= 4:
            raw_score *= 0.7
        elif len(ai_fingerprints) >= 2:
            raw_score *= 0.85

        human_score = min(max(raw_score, 0), 100)

        # تصنيف صارم بحدود واقعية
        if human_score >= 68:
            verdict = "يبدو بشرياً — صعب الكشف"
            verdict_en = "Appears Human — Hard to Detect"
            risk = "low"
        elif human_score >= 42:
            verdict = "منطقة رمادية — قد يُكتشف"
            verdict_en = "Gray Zone — May Be Detected"
            risk = "medium"
        else:
            verdict = "يبدو آلياً — سهل الكشف"
            verdict_en = "Appears AI — Easy to Detect"
            risk = "high"

        return {
            "human_score": round(human_score, 1),
            "verdict": verdict,
            "verdict_en": verdict_en,
            "risk_level": risk,
            "perplexity": perplexity,
            "burstiness": burstiness,
            "stylometry": stylometry,
            "repetition_score": round(repetition, 3),
            "sentence_uniformity": round(uniformity, 3),
            "transition_overuse": round(transition_score, 3),
            "ai_fingerprints": len(ai_fingerprints),
            "ai_fingerprint_details": ai_fingerprints,
            "statistics": statistics,
            "language": self.detect_language(text),
        }
