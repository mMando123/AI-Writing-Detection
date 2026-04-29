"""
bypass_engine.py — محرك التجاوز الرئيسي
يطبق 6 تقنيات لتجاوز كشف الذكاء الاصطناعي:
1. رفع الحيرة (Perplexity) — استبدال المرادفات وكسر التوقعية
2. رفع الانفجارية (Burstiness) — تنويع أطوال الجمل
3. أنسنة الأسلوب (Stylometry) — إضافة لمسات بشرية
4. إزالة العلامات المائية (Watermark) — استبدال منهجي للكلمات
5. كسر الأنماط الإحصائية — تعديل التوزيعات
6. إزالة بصمات AI — حذف العبارات المميزة
"""

import re
import random
import math
from engine.arabic_resources import (
    detect_language, get_resources, get_synonyms,
    ARABIC_SYNONYMS, ENGLISH_SYNONYMS,
    ARABIC_NATURAL_IMPERFECTIONS, ENGLISH_NATURAL_IMPERFECTIONS,
)
from engine.text_analyzer import TextAnalyzer


class BypassEngine:
    def __init__(self):
        self.analyzer = TextAnalyzer()
        # بصمات AI التي يجب إزالتها
        self.ai_fingerprints_ar = [
            ("تجدر الإشارة إلى أن", "واللافت أن"), ("من الجدير بالذكر أن", "ومما يُلفت النظر"),
            ("يلعب دوراً حيوياً في", "له أثر واضح في"), ("في هذا السياق", "وفي هذا الشأن"),
            ("من المهم أن نلاحظ", "ومما ينبغي الانتباه إليه"), ("وفي الختام", "وختاماً"),
            ("على صعيد آخر", "ومن ناحية أخرى"), ("في ضوء ما سبق", "بالنظر إلى ما تقدم"),
            ("مما لا شك فيه", "من الواضح"), ("ليس من المبالغة القول", "يمكن القول بثقة"),
            ("في نهاية المطاف", "في المحصلة"), ("يمكن القول إن", "أرى أن"),
            ("بناءً على ما تقدم", "واستناداً إلى ذلك"), ("في هذا الإطار", "وضمن هذا المنحى"),
            ("بشكل عام", "إجمالاً"), ("بشكل خاص", "وتحديداً"),
            ("من خلال", "عبر"), ("بالإضافة إلى ذلك", "فضلاً عن ذلك"),
        ]
        self.ai_fingerprints_en = [
            ("it is important to note that", "what stands out here is"),
            ("it is worth noting that", "notably"), ("plays a crucial role", "has a real impact"),
            ("in today's world", "these days"), ("it's important to remember", "we shouldn't forget"),
            ("in conclusion", "to wrap things up"), ("this comprehensive", "this thorough"),
            ("delve into", "dig into"), ("tapestry of", "mix of"),
            ("multifaceted approach", "layered approach"), ("let's explore", "let's look at"),
            ("in the realm of", "in the world of"), ("navigating the", "working through the"),
            ("it is essential", "it really matters"), ("furthermore", "on top of that"),
            ("moreover", "and also"), ("consequently", "so"), ("therefore", "that's why"),
            ("additionally", "plus"), ("facilitate", "make easier"),
        ]

    def split_sentences(self, text):
        parts = re.split(r'(?<=[.!?؟])\s+', text)
        return [p.strip() for p in parts if p.strip()]

    def join_sentences(self, sentences):
        return ' '.join(sentences)

    # ═══════════════════════════════════════════════════════════
    # 1. رفع الحيرة — Perplexity Boost
    # ═══════════════════════════════════════════════════════════
    def boost_perplexity(self, text, intensity=0.5):
        """استبدال كلمات متوقعة بمرادفات أقل شيوعاً مع حساسية للسياق"""
        lang = detect_language(text)
        synonyms = ARABIC_SYNONYMS if lang == "ar" else ENGLISH_SYNONYMS
        result = text
        replacements = 0
        max_replacements = max(3, int(len(text.split()) * intensity * 0.18))

        # ترتيب عشوائي مع تفضيل العبارات الأطول أولاً (أكثر تأثيراً)
        keys = sorted(synonyms.keys(), key=len, reverse=True)
        random.shuffle(keys)
        keys.sort(key=len, reverse=True)

        for word in keys:
            if replacements >= max_replacements:
                break
            if word in result:
                # اختيار المرادف الأقل شيوعاً (الأخير في القائمة عادةً)
                syns = synonyms[word]
                if intensity > 0.6:
                    chosen = random.choice(syns[-2:]) if len(syns) > 2 else random.choice(syns)
                else:
                    chosen = random.choice(syns)
                result = result.replace(word, chosen, 1)
                replacements += 1
        return result

    # ═══════════════════════════════════════════════════════════
    # 2. رفع الانفجارية — Burstiness Enhancement
    # ═══════════════════════════════════════════════════════════
    def enhance_burstiness(self, text, intensity=0.5):
        """تنويع أطوال الجمل وإضافة تقطعات مع استهداف رياضي"""
        lang = detect_language(text)
        res = get_resources(lang)
        sentences = self.split_sentences(text)
        if len(sentences) < 3:
            return text

        # تحليل الوضع الحالي
        lengths = [len(s.split()) for s in sentences]
        mean_len = sum(lengths) / len(lengths) if lengths else 10

        result = []
        for i, sent in enumerate(sentences):
            words = sent.split()
            wc = len(words)
            r = random.random()

            # تقسيم الجمل الطويلة (> 15 كلمة) عند أقرب رابط
            if wc > 15 and r < intensity * 0.7:
                # البحث عن نقطة قطع طبيعية (عند رابط أو فاصلة)
                if lang == "ar":
                    cut_markers = ["و", "لكن", "ثم", "أو", "إذ", "حيث", "كما", "بينما"]
                else:
                    cut_markers = ["and", "but", "then", "or", "while", "since", "although"]
                
                best_cut = wc // 2
                for j in range(wc // 3, 2 * wc // 3):
                    if j < len(words) and words[j] in cut_markers:
                        best_cut = j
                        break
                
                part1 = ' '.join(words[:best_cut])
                part2 = ' '.join(words[best_cut:])
                # حرف أول كبير للإنجليزية
                if lang == "en" and part2:
                    part2 = part2[0].upper() + part2[1:]
                result.append(part1 + '.')
                result.append(part2)

            # إضافة جملة قصيرة مفاجئة
            elif wc > 8 and r < intensity * 0.25 and i > 0:
                short = random.choice(res["short_sentences"])
                result.append(short)
                result.append(sent)

            # إضافة سؤال بلاغي بعد جملة تقريرية
            elif r < intensity * 0.12 and i > 0 and not sent.endswith(('?', '؟')):
                result.append(sent)
                result.append(random.choice(res["rhetorical"]))

            else:
                result.append(sent)

        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # 3. أنسنة الأسلوب — Style Humanization
    # ═══════════════════════════════════════════════════════════
    def humanize_style(self, text, intensity=0.5):
        """إضافة لمسات بشرية: ضمائر، عواطف، تحفظات"""
        lang = detect_language(text)
        res = get_resources(lang)
        sentences = self.split_sentences(text)
        if len(sentences) < 2:
            return text

        result = []
        total = len(sentences)
        insertions = max(1, int(total * intensity * 0.25))

        # مواقع عشوائية للإدراج
        insert_positions = sorted(random.sample(range(total), min(insertions, total)))
        insert_types = ["hedging", "personal", "emotional", "parenthetical", "informal", "transition"]

        for i, sent in enumerate(sentences):
            if i in insert_positions:
                itype = random.choice(insert_types)
                if itype == "hedging":
                    hedge = random.choice(res["hedging"])
                    if lang == "ar":
                        sent = hedge + "، " + sent[0].lower() + sent[1:] if sent else sent
                    else:
                        sent = hedge + ", " + sent[0].lower() + sent[1:] if sent else sent
                elif itype == "personal":
                    result.append(random.choice(res["personal"]) + ".")
                elif itype == "emotional":
                    emotional = random.choice(res["emotional"])
                    sent = emotional + "، " + sent if lang == "ar" else emotional + ", " + sent
                elif itype == "parenthetical":
                    paren = random.choice(res["parenthetical"])
                    sent = sent.rstrip('.!?؟') + " " + paren + "."
                elif itype == "informal":
                    inf = random.choice(res["informal"])
                    sent = inf + "، " + sent if lang == "ar" else inf + ", " + sent
                elif itype == "transition":
                    result.append(random.choice(res["transitions"]))
            result.append(sent)
        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # 4. إزالة العلامات المائية — Watermark Removal
    # ═══════════════════════════════════════════════════════════
    def remove_watermarks(self, text, intensity=0.5):
        """استبدال منهجي للكلمات لكسر أنماط العلامات المائية"""
        lang = detect_language(text)
        synonyms = ARABIC_SYNONYMS if lang == "ar" else ENGLISH_SYNONYMS
        result = text
        # استبدال نسبة من الكلمات بمرادفاتها
        for word, syns in synonyms.items():
            if word in result and random.random() < intensity * 0.7:
                result = result.replace(word, random.choice(syns), 1)
        return result

    # ═══════════════════════════════════════════════════════════
    # 5. إزالة بصمات AI
    # ═══════════════════════════════════════════════════════════
    def remove_ai_fingerprints(self, text):
        """إزالة العبارات المميزة للذكاء الاصطناعي"""
        lang = detect_language(text)
        fps = self.ai_fingerprints_ar if lang == "ar" else self.ai_fingerprints_en
        result = text
        for original, replacement in fps:
            if lang == "en":
                result = re.sub(re.escape(original), replacement, result, flags=re.IGNORECASE)
            else:
                result = result.replace(original, replacement)
        return result

    # ═══════════════════════════════════════════════════════════
    # 6. إضافة عيوب طبيعية — Natural Imperfections
    # ═══════════════════════════════════════════════════════════
    def add_imperfections(self, text, intensity=0.3):
        """إضافة عيوب طبيعية تحاكي الكتابة البشرية"""
        lang = detect_language(text)
        sentences = self.split_sentences(text)
        if len(sentences) < 4:
            return text

        result = []
        corrections = ARABIC_NATURAL_IMPERFECTIONS if lang == "ar" else ENGLISH_NATURAL_IMPERFECTIONS
        correction_strings = [c for c in corrections if isinstance(c, str)]

        for i, sent in enumerate(sentences):
            if random.random() < intensity * 0.15 and correction_strings:
                corr = random.choice(correction_strings)
                words = sent.split()
                if len(words) > 6:
                    pos = random.randint(2, len(words) - 2)
                    words.insert(pos, corr)
                    sent = ' '.join(words)
            result.append(sent)
        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # المعالجة الشاملة — Full Bypass Pipeline
    # ═══════════════════════════════════════════════════════════
    def full_bypass(self, text, intensity=0.5):
        """
        معالجة شاملة متعددة المراحل مع تقارب.
        
        يطبق التقنيات بالتسلسل الأمثل ثم يعيد المعالجة
        إذا لم تصل النتيجة إلى الحد المقبول (multi-pass convergence).
        
        الحد الأقصى: 3 تمريرات لتجنب الإفراط في التعديل.
        """
        before = self.analyzer.full_analysis(text)
        result = text
        best_result = text
        best_score = before["human_score"]
        passes_done = 0

        # الهدف: دائماً أعلى من النتيجة الحالية بنسبة مناسبة
        target_score = min(85, best_score + 15 + (intensity * 15))
        max_passes = 2 if intensity < 0.5 else 3

        for pass_num in range(max_passes):
            passes_done += 1
            result = self.remove_ai_fingerprints(result)
            result = self.boost_perplexity(result, intensity)
            result = self.remove_watermarks(result, intensity * 0.8)
            result = self.enhance_burstiness(result, intensity)
            result = self.humanize_style(result, intensity * (0.7 if pass_num > 0 else 1.0))
            if intensity > 0.3:
                result = self.add_imperfections(result, intensity * 0.5)

            # تنظيف
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\s+([.!?؟،,])', r'\1', result)

            # فحص التقارب
            current = self.analyzer.full_analysis(result)
            if current["human_score"] > best_score:
                best_score = current["human_score"]
                best_result = result

            # التوقف فقط إذا تجاوزنا الهدف وأكملنا تمريرة واحدة على الأقل
            if current["human_score"] >= target_score and passes_done >= 1:
                break

            # تقليل الشدة في التمريرات اللاحقة لتجنب التشويه
            intensity *= 0.7

        after = self.analyzer.full_analysis(best_result)

        return {
            "original_text": text,
            "bypassed_text": best_result,
            "before_analysis": before,
            "after_analysis": after,
            "passes_used": passes_done,
            "improvement": {
                "human_score": round(after["human_score"] - before["human_score"], 1),
                "perplexity": round(after["perplexity"] - before["perplexity"], 1),
                "burstiness": round(after["burstiness"] - before["burstiness"], 2),
            }
        }

    def selective_bypass(self, text, techniques, intensity=0.5):
        """تطبيق تقنيات مختارة فقط"""
        result = text
        if "fingerprints" in techniques:
            result = self.remove_ai_fingerprints(result)
        if "perplexity" in techniques:
            result = self.boost_perplexity(result, intensity)
        if "watermark" in techniques:
            result = self.remove_watermarks(result, intensity)
        if "burstiness" in techniques:
            result = self.enhance_burstiness(result, intensity)
        if "stylometry" in techniques:
            result = self.humanize_style(result, intensity)
        if "imperfections" in techniques:
            result = self.add_imperfections(result, intensity)

        result = re.sub(r'\s+', ' ', result).strip()
        result = re.sub(r'\s+([.!?؟،,])', r'\1', result)

        before = self.analyzer.full_analysis(text)
        after = self.analyzer.full_analysis(result)

        return {
            "original_text": text,
            "bypassed_text": result,
            "techniques_applied": techniques,
            "before_analysis": before,
            "after_analysis": after,
            "improvement": {
                "human_score": round(after["human_score"] - before["human_score"], 1),
                "perplexity": round(after["perplexity"] - before["perplexity"], 1),
                "burstiness": round(after["burstiness"] - before["burstiness"], 2),
            }
        }
