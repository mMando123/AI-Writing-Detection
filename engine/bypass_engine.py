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
            ("تلعب دوراً محورياً", "لها أثر ملموس"), ("من منظور شامل", "إذا نظرنا للأمر"),
            ("يُعد من أبرز", "يبرز كواحد من"), ("لا يمكن إنكار أن", "الواضح أن"),
            ("تشير الدراسات إلى", "لوحظ أن"), ("وفقاً للبيانات المتاحة", "كما يتضح"),
            ("يتسم بالتعقيد", "فيه تشعّب"), ("ثمة حاجة ماسة", "نحتاج فعلاً"),
            ("في سياق متصل", "وعلى صلة بذلك"), ("تبرز أهمية", "يتّضح دور"),
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
            ("it should be noted", "worth mentioning"), ("a key aspect", "one thing that matters"),
            ("significantly", "quite a bit"), ("demonstrates", "shows"),
            ("enhances", "improves"), ("leveraging", "using"), ("streamline", "simplify"),
            ("paramount", "really important"), ("underpinning", "behind"),
            ("holistic approach", "full picture"), ("paradigm shift", "big change"),
            ("synergy", "teamwork"), ("ecosystem", "environment"),
        ]
        # أنماط بنيوية للتحويل (active ↔ passive)
        self.voice_patterns_ar = [
            (r'يتم (\S+)', r'\1'),  # يتم استخدام → استخدام
            (r'تم (\S+)', r'\1'),
        ]
        self.voice_patterns_en = [
            (r'is being (\w+ed)', r'gets \1'),
            (r'has been (\w+ed)', r'was \1'),
            (r'can be (\w+ed)', r'we can \1'),
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
        """استبدال كلمات وعبارات متوقعة بمرادفات أقل شيوعاً — نسخة محسّنة"""
        lang = detect_language(text)
        synonyms = ARABIC_SYNONYMS if lang == "ar" else ENGLISH_SYNONYMS
        result = text
        replacements = 0
        # رفع الحد الأقصى بشكل كبير
        max_replacements = max(5, int(len(text.split()) * intensity * 0.35))

        # ترتيب: العبارات الأطول أولاً (أكثر تأثيراً)
        keys = sorted(synonyms.keys(), key=len, reverse=True)

        for word in keys:
            if replacements >= max_replacements:
                break
            if lang == "en":
                # بحث بحدود الكلمة لمنع استبدال أجزاء من كلمات أخرى
                # مثلاً: لا نستبدل "change" داخل "exchange"
                pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                if pattern.search(result):
                    syns = synonyms[word]
                    chosen = random.choice(syns)
                    result = pattern.sub(chosen, result, count=1)
                    replacements += 1
            else:
                if word in result:
                    syns = synonyms[word]
                    chosen = random.choice(syns)
                    result = result.replace(word, chosen, 1)
                    replacements += 1
        return result

    # ═══════════════════════════════════════════════════════════
    # 2. رفع الانفجارية — Burstiness Enhancement
    # ═══════════════════════════════════════════════════════════
    def enhance_burstiness(self, text, intensity=0.5):
        """تنويع أطوال الجمل — تقسيم ودمج وتنويع بنية أكثر عدوانية"""
        lang = detect_language(text)
        res = get_resources(lang)
        sentences = self.split_sentences(text)
        if len(sentences) < 3:
            return text

        lengths = [len(s.split()) for s in sentences]
        mean_len = sum(lengths) / len(lengths) if lengths else 10

        result = []
        short_added = 0
        max_short = max(2, int(len(sentences) * 0.20))  # 20% من الجمل
        i = 0

        while i < len(sentences):
            sent = sentences[i]
            words = sent.split()
            wc = len(words)
            r = random.random()

            # دمج جملتين قصيرتين متتاليتين في جملة واحدة
            if wc < 10 and i + 1 < len(sentences) and len(sentences[i+1].split()) < 10 and r < intensity * 0.5:
                next_sent = sentences[i+1]
                if lang == "ar":
                    connectors = ["، وبالتالي ", "، كما أن ", "، إذ ", "، وهذا يعني أن ", "، و"]
                else:
                    connectors = [", and this means that ", ", which also ", "; in fact, ", " — and ", ", and "]
                connector = random.choice(connectors)
                merged = sent.rstrip('.!?؟') + connector + next_sent
                result.append(merged)
                i += 2
                continue

            # تقسيم الجمل الطويلة (> 15 كلمة) عند أقرب رابط
            if wc > 15 and r < intensity * 0.6:
                if lang == "ar":
                    cut_markers = ["و", "لكن", "ثم", "أو", "إذ", "حيث", "كما", "بينما", "مما", "حتى"]
                else:
                    # إزالة "as" و "which" لأنها تظهر في عبارات مثل "such as"
                    cut_markers = ["and", "but", "then", "or", "while", "since", "although", "where", "when"]
                
                best_cut = -1
                for j in range(wc // 3, min(2 * wc // 3 + 1, len(words))):
                    if words[j].lower().strip(',') in cut_markers:
                        best_cut = j
                        break
                
                # التأكد أن كلا الجزأين طويلان كفاية (4 كلمات على الأقل)
                if best_cut > 3 and (wc - best_cut) > 3:
                    part1 = ' '.join(words[:best_cut])
                    part2 = ' '.join(words[best_cut:])
                    # إزالة الرابط من بداية الجزء الثاني وتكبير الحرف
                    if lang == "en" and part2:
                        part2_words = part2.split()
                        if part2_words and part2_words[0].lower().strip(',') in cut_markers:
                            part2 = ' '.join(part2_words[1:])
                        if part2 and part2[0].isalpha():
                            part2 = part2[0].upper() + part2[1:]
                    result.append(part1 + '.')
                    result.append(part2)
                else:
                    result.append(sent)

            # إضافة جملة قصيرة مفاجئة
            elif wc > 8 and r < intensity * 0.25 and i > 0 and short_added < max_short:
                short = random.choice(res["short_sentences"])
                result.append(short)
                result.append(sent)
                short_added += 1

            # إضافة سؤال بلاغي
            elif r < intensity * 0.12 and i > 1 and not sent.endswith(('?', '؟')) and short_added < max_short:
                result.append(sent)
                result.append(random.choice(res["rhetorical"]))
                short_added += 1

            else:
                result.append(sent)

            i += 1

        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # 3. أنسنة الأسلوب — Style Humanization
    # ═══════════════════════════════════════════════════════════
    def humanize_style(self, text, intensity=0.5):
        """إضافة لمسات بشرية: ضمائر، عواطف، تحفظات — نسخة أقوى"""
        lang = detect_language(text)
        res = get_resources(lang)
        sentences = self.split_sentences(text)
        if len(sentences) < 2:
            return text

        result = []
        total = len(sentences)
        # زيادة عدد الإدراجات — 35% من الجمل
        insertions = max(2, int(total * intensity * 0.35))
        insertions = min(insertions, max(2, total // 3))

        # مواقع عشوائية للإدراج
        available = list(range(1, max(2, total)))
        insert_positions = sorted(random.sample(available, min(insertions, len(available))))
        insert_types = ["hedging", "personal", "emotional", "parenthetical",
                        "informal", "transition", "hedging", "personal"]

        for i, sent in enumerate(sentences):
            if i in insert_positions:
                itype = random.choice(insert_types)
                if itype == "hedging":
                    hedge = random.choice(res["hedging"])
                    if lang == "ar":
                        sent = hedge + "، " + sent
                    else:
                        if sent and sent[0].isalpha():
                            sent = hedge + ", " + sent[0].lower() + sent[1:]
                        else:
                            sent = hedge + ", " + sent
                elif itype == "personal":
                    personal = random.choice(res["personal"])
                    if lang == "ar":
                        sent = personal + "، " + sent
                    else:
                        if sent and sent[0].isalpha():
                            sent = personal + ", " + sent[0].lower() + sent[1:]
                        else:
                            sent = personal + ", " + sent
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
        """استبدال منهجي للكلمات لكسر أنماط العلامات المائية — نسخة أقوى"""
        lang = detect_language(text)
        synonyms = ARABIC_SYNONYMS if lang == "ar" else ENGLISH_SYNONYMS
        result = text
        # رفع نسبة الاستبدال بشكل كبير
        for word, syns in synonyms.items():
            if lang == "en":
                # حدود الكلمة لمنع استبدال أجزاء من كلمات أخرى
                pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                if pattern.search(result) and random.random() < intensity * 0.9:
                    result = pattern.sub(random.choice(syns), result, count=1)
            else:
                if word in result and random.random() < intensity * 0.9:
                    result = result.replace(word, random.choice(syns), 1)
        return result

    # ═══════════════════════════════════════════════════════════
    # 5. إزالة بصمات AI
    # ═══════════════════════════════════════════════════════════
    def remove_ai_fingerprints(self, text):
        """إزالة العبارات المميزة للذكاء الاصطناعي + إعادة صياغة البنية"""
        lang = detect_language(text)
        fps = self.ai_fingerprints_ar if lang == "ar" else self.ai_fingerprints_en
        result = text
        for original, replacement in fps:
            if lang == "en":
                result = re.sub(re.escape(original), replacement, result, flags=re.IGNORECASE)
            else:
                result = result.replace(original, replacement)
        
        # إعادة صياغة إضافية: تغيير بنية الجمل التي تبدأ بنفس الطريقة
        sentences = self.split_sentences(result)
        if len(sentences) > 3:
            starters = {}
            new_sentences = []
            for sent in sentences:
                words = sent.split()
                if not words:
                    new_sentences.append(sent)
                    continue
                starter = words[0].lower() if lang == "en" else words[0]
                starters[starter] = starters.get(starter, 0) + 1
                # إذا تكررت بداية الجملة، أعد صياغتها
                if starters[starter] > 1 and len(words) > 5:
                    if lang == "en":
                        prefixes = ["What stands out is that", "It's worth noting that", "One key point is that", "Looking at this closely,", "From my perspective,"]
                    else:
                        prefixes = ["واللافت هنا أن", "ومما يستحق الذكر", "والملاحظ أن", "ومن زاوية أخرى"]
                    prefix = random.choice(prefixes)
                    if lang == "en" and sent[0].isupper():
                        sent = prefix + " " + sent[0].lower() + sent[1:]
                    else:
                        sent = prefix + " " + sent
                new_sentences.append(sent)
            result = ' '.join(new_sentences)
        
        return result

    # ═══════════════════════════════════════════════════════════
    # 6. إضافة عيوب طبيعية — Natural Imperfections
    # ═══════════════════════════════════════════════════════════
    def add_imperfections(self, text, intensity=0.3):
        """إضافة عيوب طبيعية تحاكي الكتابة البشرية — محدودة العدد"""
        lang = detect_language(text)
        sentences = self.split_sentences(text)
        if len(sentences) < 5:
            return text

        result = []
        corrections = ARABIC_NATURAL_IMPERFECTIONS if lang == "ar" else ENGLISH_NATURAL_IMPERFECTIONS
        correction_strings = [c for c in corrections if isinstance(c, str)]

        # حد أقصى: تصحيح ذاتي واحد لكل 8 جمل
        max_corrections = max(1, len(sentences) // 8)
        corrections_added = 0

        for i, sent in enumerate(sentences):
            if (random.random() < intensity * 0.10
                    and correction_strings
                    and corrections_added < max_corrections
                    and i > 1):  # لا نضيف في أول جملتين
                corr = random.choice(correction_strings)
                words = sent.split()
                if len(words) > 8:  # فقط في الجمل الطويلة كفاية
                    pos = random.randint(3, len(words) - 3)
                    words.insert(pos, corr)
                    sent = ' '.join(words)
                    corrections_added += 1
            result.append(sent)
        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # 7. إعادة هيكلة الجمل — Sentence Restructuring (NEW)
    # ═══════════════════════════════════════════════════════════
    def restructure_sentences(self, text, intensity=0.5):
        """تغيير بنية الجمل بشكل جذري: تبديل الأجزاء + تغيير الصوت + إعادة ترتيب"""
        lang = detect_language(text)
        result = text
        
        # تحويل أنماط الصوت (active/passive)
        patterns = self.voice_patterns_ar if lang == "ar" else self.voice_patterns_en
        for pattern, replacement in patterns:
            if random.random() < intensity * 0.8:
                result = re.sub(pattern, replacement, result, count=2)

        # تبديل ترتيب الجُمَل الفرعية عند الفواصل
        sentences = self.split_sentences(result)
        rebuilt = []
        for sent in sentences:
            words = sent.split()
            
            # تخطي الجمل القصيرة (عناوين، أسئلة) — لا نعدلها
            if len(words) < 12:
                rebuilt.append(sent)
                continue
            
            # تخطي الجمل التي تحتوي على نقطتين (أسئلة وعناوين)
            if ':' in sent or '؟' in sent:
                rebuilt.append(sent)
                continue

            if lang == "ar":
                parts = sent.split('،')
            else:
                parts = sent.split(',')
            
            # تبديل أجزاء الجملة — فقط إذا كان كل جزء طويلاً كفاية
            if (len(parts) >= 2 
                    and random.random() < intensity * 0.5
                    and len(parts[0].split()) > 4 
                    and len(parts[1].split()) > 4):
                parts[0], parts[1] = parts[1].strip(), parts[0].strip()
                sep = '، ' if lang == "ar" else ', '
                rebuilt.append(sep.join(parts))
            # تحويل "X because Y" إلى "Since Y, X" — فقط مع because
            elif lang == "en" and random.random() < intensity * 0.3:
                if 'because ' in sent.lower():
                    idx = sent.lower().find('because ')
                    part_before = sent[:idx].rstrip(', ')
                    part_after = sent[idx + 8:]  # len('because ') = 8
                    if part_before and part_after and len(part_before.split()) > 3:
                        sent = "Since " + part_after.rstrip('.') + ", " + part_before[0].lower() + part_before[1:] + "."
                rebuilt.append(sent)
            else:
                rebuilt.append(sent)
        return ' '.join(rebuilt)

    # ═══════════════════════════════════════════════════════════
    # 8. تعطيل أنماط الخطاب — Discourse Disruption (NEW)
    # ═══════════════════════════════════════════════════════════
    def disrupt_discourse(self, text, intensity=0.5):
        """كسر البنية المتوقعة — نسخة محافظة تنقل جملاً متجاورة فقط"""
        sentences = self.split_sentences(text)
        if len(sentences) < 7:
            return text

        result = list(sentences)
        n = len(result)
        # حد أقصى: تبديل واحد فقط لكل 10 جمل
        swaps = max(1, int(n * intensity * 0.06))

        for _ in range(swaps):
            # فقط تبديل جمل متجاورة (لا نقفز) — لحماية السياق
            i = random.randint(2, n - 3)  # تجنب الأولى والأخيرتين
            j = i + 1
            # فقط إذا كانت الجملتان بأطوال متشابهة (لتجنب تشويه البنية)
            len_i = len(result[i].split())
            len_j = len(result[j].split())
            if abs(len_i - len_j) < 8:
                result[i], result[j] = result[j], result[i]

        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # 9. حقن الإنتروبيا — Entropy Injection (NEW)
    # ═══════════════════════════════════════════════════════════
    def inject_entropy(self, text, intensity=0.5):
        """إدخال ظروف في بداية الجمل لرفع الحيرة — محدود وطبيعي"""
        lang = detect_language(text)
        sentences = self.split_sentences(text)
        if len(sentences) < 4:
            return text

        # ظروف طبيعية تُضاف في بداية الجملة فقط (أكثر طبيعية)
        if lang == "ar":
            adverbs = ["حقاً", "تحديداً", "واقعياً", "فعلاً", "بالتأكيد"]
        else:
            adverbs = ["frankly", "realistically", "interestingly",
                       "truthfully", "notably", "admittedly"]

        result = []
        max_inserts = max(1, len(sentences) // 6)  # حد أقصى: 1 لكل 6 جمل
        inserts_done = 0

        for i, sent in enumerate(sentences):
            words = sent.split()
            if (len(words) > 8
                    and random.random() < intensity * 0.12
                    and inserts_done < max_inserts
                    and i > 1):  # تجنب الجملة الأولى
                adv = random.choice(adverbs)
                sep = "، " if lang == "ar" else ", "
                # إضافة الظرف في بداية الجملة (أكثر طبيعية من الوسط)
                result.append(adv + sep + sent)
                inserts_done += 1
            else:
                result.append(sent)
        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # 10. إزالة الروابط الانتقالية الزائدة — Transition Cleanup
    # ═══════════════════════════════════════════════════════════
    def remove_transition_overuse(self, text, intensity=0.5):
        """إزالة أو استبدال الروابط الانتقالية الرسمية الزائدة بأسلوب طبيعي"""
        lang = detect_language(text)
        sentences = self.split_sentences(text)
        if len(sentences) < 3:
            return text

        if lang == "en":
            # روابط رسمية → بدائل طبيعية أو حذف
            transition_map = {
                "furthermore, ": ["", "also, ", "and "],
                "moreover, ": ["", "plus, ", "and "],
                "additionally, ": ["", "also, ", "on top of that, "],
                "consequently, ": ["so, ", "as a result, ", ""],
                "nevertheless, ": ["still, ", "but ", "yet "],
                "nonetheless, ": ["still, ", "even so, ", ""],
                "subsequently, ": ["then, ", "after that, ", ""],
                "accordingly, ": ["so, ", "", "that's why "],
                "in addition, ": ["also, ", "", "plus, "],
                "it is important to note that ": ["", "notably, ", "one thing — "],
                "it is worth noting that ": ["", "notably, ", ""],
                "it should be noted that ": ["", "", "worth mentioning, "],
            }
        else:
            transition_map = {
                "بالإضافة إلى ذلك، ": ["", "كما أن ", "وأيضاً "],
                "علاوة على ذلك، ": ["", "وكذلك ", ""],
                "فضلاً عن ذلك، ": ["", "وأيضاً ", ""],
                "وبالتالي، ": ["لذا ", "", "فـ"],
                "ومع ذلك، ": ["لكن ", "إلا أن ", ""],
                "من ناحية أخرى، ": ["", "أما ", ""],
                "تجدر الإشارة إلى أن ": ["", "واللافت أن ", ""],
                "من الجدير بالذكر أن ": ["", "ومما يُلاحظ ", ""],
            }

        result = text
        removals = 0
        max_removals = max(2, int(len(sentences) * intensity * 0.4))

        for formal, alternatives in transition_map.items():
            if removals >= max_removals:
                break
            if lang == "en":
                pattern = re.compile(re.escape(formal), re.IGNORECASE)
            else:
                pattern = re.compile(re.escape(formal))

            if pattern.search(result) and random.random() < intensity * 0.7:
                replacement = random.choice(alternatives)
                result = pattern.sub(replacement, result, count=1)
                removals += 1

        return result

    # ═══════════════════════════════════════════════════════════
    # 11. كسر تجانس أطوال الجمل — Break Uniformity
    # ═══════════════════════════════════════════════════════════
    def break_uniformity(self, text, intensity=0.5):
        """كسر تجانس أطوال الجمل — إذا كانت 3+ جمل متتالية بنفس الطول"""
        lang = detect_language(text)
        sentences = self.split_sentences(text)
        if len(sentences) < 5:
            return text

        lengths = [len(s.split()) for s in sentences]
        result = list(sentences)
        changes = 0
        max_changes = max(1, int(len(sentences) * intensity * 0.3))

        i = 0
        while i < len(result) - 2 and changes < max_changes:
            l1 = len(result[i].split())
            l2 = len(result[i+1].split())
            l3 = len(result[i+2].split())

            # إذا كانت 3 جمل متتالية متقاربة الطول (± 4 كلمات)
            if abs(l1 - l2) <= 4 and abs(l2 - l3) <= 4 and l2 > 8:
                action = random.choice(["split", "shorten", "extend"])

                if action == "split" and l2 > 12:
                    # تقسيم الجملة الوسطى
                    words = result[i+1].split()
                    mid = len(words) // 2
                    # البحث عن نقطة قطع طبيعية قريبة من المنتصف
                    cut = mid
                    if lang == "en":
                        connectors = {"and", "but", "or", "while", "when", "since", "although"}
                    else:
                        connectors = {"و", "لكن", "أو", "حيث", "إذ", "بينما"}
                    for j in range(max(3, mid - 3), min(len(words) - 3, mid + 4)):
                        if words[j].lower().strip(',') in connectors:
                            cut = j
                            break
                    part1 = ' '.join(words[:cut]).rstrip(',') + '.'
                    part2_words = words[cut:]
                    # إزالة الرابط من بداية الجزء الثاني
                    if part2_words and part2_words[0].lower().strip(',') in connectors:
                        part2_words = part2_words[1:]
                    if part2_words:
                        part2_words[0] = part2_words[0].capitalize() if lang == "en" else part2_words[0]
                    part2 = ' '.join(part2_words)
                    if part2:
                        result[i+1] = part1
                        result.insert(i+2, part2)
                        changes += 1

                elif action == "shorten" and l2 > 10:
                    # تقصير الجملة بحذف عبارة وصفية
                    words = result[i+1].split()
                    # حذف آخر 3-5 كلمات إذا لم تنتهي بنقطة
                    cut_amount = random.randint(2, min(4, len(words) // 3))
                    result[i+1] = ' '.join(words[:-cut_amount]).rstrip(',') + '.'
                    changes += 1

                elif action == "extend" and i + 1 < len(result):
                    # إضافة عبارة قصيرة بعد الجملة
                    if lang == "en":
                        extras = [
                            "This matters.", "That's key.", "It's worth thinking about.",
                            "The impact is real.", "And it shows.",
                        ]
                    else:
                        extras = [
                            "وهذا مهم.", "وهو أمر لافت.", "والأثر واضح.",
                            "وهذا جوهري.", "ولا يمكن تجاهله.",
                        ]
                    result.insert(i+2, random.choice(extras))
                    changes += 1
                i += 3
            else:
                i += 1

        return ' '.join(result)

    # ═══════════════════════════════════════════════════════════
    # المعالجة الشاملة — Full Bypass Pipeline
    # ═══════════════════════════════════════════════════════════
    def full_bypass(self, text, intensity=0.5):
        """
        معالجة شاملة 9 تقنيات مع تقارب ذكي.
        الترتيب الأمثل: إزالة البصمات → إعادة الهيكلة → رفع الحيرة →
        إزالة العلامات → حقن الإنتروبيا → الانفجارية → الأنسنة →
        تعطيل الخطاب → العيوب
        """
        before = self.analyzer.full_analysis(text)
        result = text
        best_result = text
        best_score = before["human_score"]
        passes_done = 0

        target_score = min(88, best_score + 15 + (intensity * 18))
        max_passes = 2 if intensity < 0.5 else 3

        for pass_num in range(max_passes):
            passes_done += 1
            p_int = intensity * (0.65 if pass_num > 0 else 1.0)

            # المرحلة 1: تنظيف البصمات (الأهم)
            result = self.remove_ai_fingerprints(result)
            # المرحلة 2: إعادة هيكلة الجمل
            result = self.restructure_sentences(result, p_int)
            # المرحلة 3: رفع الحيرة
            result = self.boost_perplexity(result, p_int)
            # المرحلة 4: إزالة العلامات المائية
            result = self.remove_watermarks(result, p_int * 0.8)
            # المرحلة 5: حقن الإنتروبيا
            result = self.inject_entropy(result, p_int * 0.7)
            # المرحلة 6: رفع الانفجارية
            result = self.enhance_burstiness(result, p_int)
            # المرحلة 7: أنسنة الأسلوب
            result = self.humanize_style(result, p_int)
            # المرحلة 8: تعطيل أنماط الخطاب
            if pass_num == 0:
                result = self.disrupt_discourse(result, p_int * 0.5)
            # المرحلة 9: عيوب طبيعية
            if intensity > 0.3:
                result = self.add_imperfections(result, p_int * 0.4)

            # تنظيف
            result = re.sub(r'\s+', ' ', result).strip()
            result = re.sub(r'\s+([.!?؟،,])', r'\1', result)

            current = self.analyzer.full_analysis(result)
            if current["human_score"] > best_score:
                best_score = current["human_score"]
                best_result = result

            if current["human_score"] >= target_score and passes_done >= 1:
                break
            intensity *= 0.65

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
