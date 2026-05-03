"""
arabic_resources.py — قواعد بيانات اللغة العربية والإنجليزية
يحتوي على: المرادفات، العبارات الانتقالية، التعبيرات الشخصية،
عبارات التحفظ، العلامات العاطفية، والتعبيرات العامية
"""

# ═══════════════════════════════════════════════════════════════
# 1. قاموس المرادفات العربية — لكسر نمط العلامات المائية والتوقعية
# ═══════════════════════════════════════════════════════════════
ARABIC_SYNONYMS = {
    # أفعال شائعة
    "يستخدم": ["يوظّف", "يستعمل", "يعتمد على", "يلجأ إلى", "يستثمر"],
    "يعتبر": ["يُعدّ", "يُصنَّف", "يُنظر إليه على أنه", "يُحسب"],
    "يساعد": ["يُسهم في", "يُعين", "يدعم", "يعاون", "يُيسّر"],
    "يؤدي": ["يقوم بـ", "ينفّذ", "يمارس", "يُنجز", "يباشر"],
    "يوفر": ["يُتيح", "يقدّم", "يمنح", "يُهيّئ", "يُوجِد"],
    "يتضمن": ["يشمل", "يحتوي على", "ينطوي على", "يستوعب"],
    "يحتاج": ["يستلزم", "يتطلب", "يستدعي", "لا بد له من"],
    "يمكن": ["بالإمكان", "من الممكن", "يتسنى", "بمقدور", "يُتاح"],
    "يجب": ["ينبغي", "يتعيّن", "يلزم", "من الضروري", "لا بد"],
    "يوجد": ["يتوفر", "يتواجد", "هناك", "ثمة", "يقوم"],
    "يعمل": ["يشتغل", "يُزاول", "يمارس عمله", "ينشط"],
    "يبدأ": ["يشرع في", "يباشر", "ينطلق", "يستهلّ", "يفتتح"],
    "يحدث": ["يقع", "يطرأ", "يجري", "ينشأ", "يبرز"],
    "يظهر": ["يبرز", "يتجلى", "يتبدّى", "يتضح", "ينكشف"],
    "يقول": ["يذكر", "يُفيد", "يصرّح", "يُبيّن", "يشير"],
    "يعرف": ["يدرك", "يُلمّ بـ", "يعي", "يفقه", "يستوعب"],
    "يحصل": ["ينال", "يفوز بـ", "يكتسب", "يحوز", "يظفر بـ"],
    "يزيد": ["يرتفع", "ينمو", "يتصاعد", "يتضخم", "يتعاظم"],
    "يقلل": ["يُنقص", "يُخفّض", "يحدّ من", "يتراجع"],
    "يؤثر": ["يطال", "ينعكس على", "يمسّ", "يلقي بظلاله على"],

    # أسماء وصفات شائعة
    "مهم": ["جوهري", "بالغ الأهمية", "حيوي", "أساسي", "محوري", "ركيزة"],
    "كبير": ["ضخم", "هائل", "واسع", "عظيم", "مُعتبَر"],
    "صغير": ["ضئيل", "يسير", "طفيف", "محدود", "بسيط"],
    "جديد": ["مستحدث", "حديث", "طازج", "مبتكر", "عصري"],
    "قديم": ["عتيق", "تقليدي", "كلاسيكي", "موروث", "سابق"],
    "جيد": ["حسن", "ممتاز", "رفيع", "لائق", "مُرضٍ"],
    "سيئ": ["رديء", "متدنٍّ", "مُخيّب", "دون المستوى"],
    "مختلف": ["متباين", "متنوع", "متغاير", "متعدد الأوجه"],
    "واضح": ["جليّ", "بيّن", "صريح", "لا لبس فيه", "ناصع"],
    "صعب": ["شاق", "عسير", "متعذر", "مُعقّد", "مُربك"],
    "سريع": ["عاجل", "فوري", "خاطف", "متسارع", "سريع الإيقاع"],
    "بطيء": ["متأنٍّ", "تدريجي", "رتيب", "متمهل"],
    "كثير": ["وفير", "غزير", "عديد", "لا يُحصى", "متراكم"],
    "قليل": ["شحيح", "نادر", "محدود", "معدود", "ضئيل"],
    "خاص": ["مميز", "فريد", "حصري", "منفرد", "استثنائي"],
    "عام": ["شامل", "عمومي", "كلّي", "مُطلق", "واسع النطاق"],

    # روابط وأدوات ربط
    "بالإضافة إلى": ["فضلاً عن", "علاوة على", "إلى جانب", "ناهيك عن", "ومن جهة أخرى"],
    "ومع ذلك": ["غير أن", "إلا أن", "بيد أن", "لكن", "على الرغم من ذلك"],
    "لذلك": ["من هنا", "ولهذا السبب", "تبعاً لذلك", "نتيجةً لذلك", "بناءً عليه"],
    "بسبب": ["جرّاء", "نتيجة", "بفعل", "من جرّاء", "بحكم"],
    "من أجل": ["بغية", "سعياً إلى", "بهدف", "ابتغاءَ", "توخّياً لـ"],
    "في الواقع": ["حقيقةً", "على أرض الواقع", "فعلياً", "في حقيقة الأمر"],
    "بشكل عام": ["إجمالاً", "على وجه العموم", "في المجمل", "عموماً"],
    "على سبيل المثال": ["كمثال على ذلك", "ومن ذلك", "ولنأخذ مثالاً", "فلو نظرنا إلى"],
    "وبالتالي": ["ومن ثمّ", "وعليه", "فيترتب على ذلك", "مما يفضي إلى"],
    "نظراً لـ": ["بالنظر إلى", "اعتباراً لـ", "في ضوء", "أخذاً بعين الاعتبار"],
}

# ═══════════════════════════════════════════════════════════════
# 2. قاموس المرادفات الإنجليزية
# ═══════════════════════════════════════════════════════════════
ENGLISH_SYNONYMS = {
    # Common verbs
    "use": ["utilize", "employ", "leverage", "rely on", "make use of"],
    "help": ["assist", "aid", "support", "facilitate", "contribute to"],
    "show": ["demonstrate", "illustrate", "reveal", "indicate", "display"],
    "make": ["create", "produce", "generate", "craft", "construct"],
    "get": ["obtain", "acquire", "receive", "gain", "secure"],
    "give": ["provide", "offer", "supply", "grant", "deliver"],
    "think": ["believe", "consider", "reckon", "suppose", "maintain"],
    "need": ["require", "demand", "necessitate", "call for"],
    "find": ["discover", "uncover", "identify", "detect", "locate"],
    "start": ["begin", "commence", "initiate", "launch", "kick off"],
    "improve": ["enhance", "refine", "boost", "elevate", "upgrade"],
    "increase": ["grow", "expand", "rise", "surge", "escalate"],
    "decrease": ["decline", "reduce", "diminish", "drop", "shrink"],
    "change": ["modify", "alter", "transform", "shift", "adjust"],
    "develop": ["evolve", "progress", "advance", "mature", "build"],
    "provide": ["supply", "furnish", "deliver", "offer", "yield"],
    "include": ["encompass", "comprise", "incorporate", "contain"],
    "suggest": ["propose", "recommend", "imply", "indicate", "hint"],
    "achieve": ["accomplish", "attain", "reach", "realize", "fulfill"],
    "maintain": ["preserve", "sustain", "uphold", "keep", "retain"],

    # Common adjectives
    "important": ["crucial", "vital", "essential", "significant", "pivotal"],
    "different": ["diverse", "distinct", "varied", "unique", "disparate"],
    "large": ["substantial", "considerable", "extensive", "massive", "vast"],
    "small": ["minor", "modest", "slight", "limited", "marginal"],
    "good": ["excellent", "outstanding", "favorable", "solid", "strong"],
    "bad": ["poor", "inadequate", "subpar", "deficient", "flawed"],
    "new": ["novel", "fresh", "innovative", "modern", "cutting-edge"],
    "old": ["traditional", "established", "longstanding", "classic", "dated"],
    "clear": ["evident", "obvious", "apparent", "transparent", "unambiguous"],
    "hard": ["difficult", "challenging", "tough", "demanding", "arduous"],
    "easy": ["simple", "straightforward", "effortless", "manageable"],
    "fast": ["rapid", "swift", "quick", "speedy", "prompt"],
    "big": ["major", "enormous", "tremendous", "significant", "immense"],

    # Common transitions
    "however": ["nevertheless", "nonetheless", "yet", "still", "though", "that said", "on the other hand"],
    "therefore": ["consequently", "thus", "hence", "as a result", "accordingly", "for this reason"],
    "also": ["additionally", "moreover", "furthermore", "besides", "likewise", "on top of that"],
    "for example": ["for instance", "such as", "to illustrate", "as in", "like", "take for example"],
    "in addition": ["furthermore", "moreover", "on top of that", "what's more", "not to mention"],
    "because": ["since", "as", "given that", "due to the fact that", "owing to", "seeing that"],
    "although": ["even though", "despite the fact that", "while", "whereas", "granted that"],
    "in conclusion": ["to sum up", "ultimately", "all things considered", "in the end", "wrapping up"],

    # Phrase-level replacements (most effective against AI detectors)
    "it is important to": ["what really matters is to", "the key thing is to", "we should make sure to"],
    "a wide range of": ["all sorts of", "many different", "a variety of", "quite a few"],
    "in order to": ["so as to", "to", "with the aim of", "for the purpose of"],
    "on the other hand": ["then again", "at the same time", "conversely", "but looking at it differently"],
    "as a result": ["because of this", "so", "this led to", "which meant that"],
    "plays a role": ["comes into play", "is a factor", "has an influence", "makes a difference"],
    "refers to": ["means", "is about", "describes", "points to"],
    "such as": ["like", "for instance", "including", "to name a few"],
    "is considered": ["is seen as", "is thought of as", "is regarded as", "is viewed as"],
    "contributes to": ["adds to", "helps with", "feeds into", "plays a part in"],
    "leads to": ["results in", "brings about", "causes", "ends up in"],
    "in terms of": ["when it comes to", "regarding", "as far as", "with respect to"],
    "it can be": ["it might be", "it could be", "it's possible that it is", "one could say it is"],
    "on a personal level": ["speaking for myself", "from where I stand", "in my own experience"],
    "the ability to": ["the capacity to", "being able to", "the skill to"],
    "is essential": ["is key", "is critical", "really matters", "cannot be overlooked"],
    "positive and negative": ["good and bad", "pros and cons", "upsides and downsides"],
    "interact with": ["engage with", "connect with", "deal with", "relate to"],
    "exposed to": ["faced with", "confronted by", "presented with", "encountering"],
    "encouraged to": ["motivated to", "inspired to", "pushed to", "driven to"],
    "strengthen": ["reinforce", "bolster", "solidify", "build up"],
    "gradually": ["step by step", "over time", "little by little", "slowly but surely"],
    "promotes": ["encourages", "supports", "fosters", "drives"],
    "fosters": ["nurtures", "builds", "cultivates", "supports"],
    "enabling": ["allowing", "making it possible for", "helping", "letting"],
    "dismantles": ["breaks down", "tears apart", "removes", "chips away at"],
}

# ═══════════════════════════════════════════════════════════════
# 3. عبارات التحفظ — لإضفاء الطابع البشري (Hedging)
# ═══════════════════════════════════════════════════════════════
ARABIC_HEDGING = [
    "ربما", "على الأرجح", "يبدو أن", "من المحتمل",
    "في ظني", "أعتقد أن", "قد يكون", "ليس من المؤكد لكن",
    "على حد علمي", "فيما أظن", "إن لم أكن مخطئاً",
    "من وجهة نظري", "حسب تقديري", "أميل إلى الاعتقاد بأن",
    "لست متأكداً تماماً لكن", "يخيّل إليّ أن",
    "على ما يبدو", "قد", "لعل", "أظن",
]

ENGLISH_HEDGING = [
    "perhaps", "probably", "it seems", "I think",
    "in my view", "arguably", "it appears that",
    "I believe", "it could be", "one might argue",
    "from my perspective", "if I'm not mistaken",
    "as far as I can tell", "to my understanding",
    "I'd say", "it strikes me that", "my sense is that",
    "I have a feeling that", "it's likely that",
]

# ═══════════════════════════════════════════════════════════════
# 4. عبارات شخصية — لمحاكاة الأسلوب البشري
# ═══════════════════════════════════════════════════════════════
ARABIC_PERSONAL = [
    "من تجربتي الشخصية",
    "أذكر أنني",
    "مررت بموقف مشابه حين",
    "لطالما شعرت أن",
    "ما لفت انتباهي هو",
    "أعترف أنني",
    "الحقيقة أنني",
    "صراحةً",
    "بصراحة",
    "في تجربة سابقة لي",
    "أتذكر جيداً عندما",
    "شخصياً",
    "لن أنسى كيف",
    "ما زلت أفكر في",
    "علّمتني التجربة أن",
    "وأنا أكتب هذا",
    "خطر لي للتو أن",
]

ENGLISH_PERSONAL = [
    "from my own experience",
    "I remember when",
    "I've always felt that",
    "what struck me was",
    "I have to admit",
    "honestly",
    "to be frank",
    "in a previous experience of mine",
    "I distinctly remember",
    "personally",
    "I'll never forget how",
    "I still think about",
    "experience has taught me that",
    "as I write this",
    "it just occurred to me that",
    "looking back",
    "I once had",
]

# ═══════════════════════════════════════════════════════════════
# 5. علامات عاطفية — لكسر الرتابة الآلية
# ═══════════════════════════════════════════════════════════════
ARABIC_EMOTIONAL = [
    "والمدهش في الأمر", "ومن المثير للاهتمام", "لكن المفاجأة هي",
    "وهنا تكمن المفارقة", "والأمر الذي لا يُصدَّق", "ما أدهشني حقاً",
    "وللأسف", "لحسن الحظ", "ويا للعجب", "والغريب أن",
    "ومما يبعث على التفاؤل", "ومما يثير القلق", "والمحزن في الأمر",
    "وبكل أمانة", "ومن باب الإنصاف", "وهذا ما يحيّرني",
    "ولعل أجمل ما في الأمر", "والمقلق فعلاً",
]

ENGLISH_EMOTIONAL = [
    "what's surprising is", "interestingly enough", "but here's the thing",
    "and here's where it gets tricky", "unbelievably", "what really amazed me",
    "unfortunately", "fortunately", "oddly enough", "strangely",
    "what gives me hope", "what concerns me", "sadly",
    "to be completely honest", "in all fairness", "what puzzles me",
    "the beautiful part is", "what's truly worrying",
]

# ═══════════════════════════════════════════════════════════════
# 6. عبارات انتقالية متنوعة — لكسر التسلسل المتوقع
# ═══════════════════════════════════════════════════════════════
ARABIC_TRANSITIONS = [
    # انتقالات مفاجئة
    "لكن دعني أتوقف هنا لحظة.",
    "وقبل أن أكمل، لا بد من الإشارة إلى شيء.",
    "لنعد خطوة إلى الوراء.",
    "هناك نقطة لم أتطرق لها بعد.",
    "الموضوع أعقد مما يبدو للوهلة الأولى.",
    "لنتأمل الصورة من زاوية مختلفة.",
    "وهنا تحديداً يتعقد الأمر.",
    "لكن انتظر — هناك جانب آخر.",
    "قد يتساءل أحدكم...",
    "والسؤال الذي يطرح نفسه:",
    "دعوني أوضح ما أعنيه.",
    "وللتوضيح أكثر...",
    "الآن، هنا بيت القصيد.",
]

ENGLISH_TRANSITIONS = [
    "but let me pause here for a moment.",
    "before I continue, I should point something out.",
    "let's take a step back.",
    "there's a point I haven't addressed yet.",
    "it's more complex than it first appears.",
    "let's look at this from a different angle.",
    "and this is precisely where things get complicated.",
    "but wait — there's another side to this.",
    "one might wonder...",
    "the question that comes to mind is:",
    "let me clarify what I mean.",
    "to elaborate further...",
    "now, here's the crux of the matter.",
]

# ═══════════════════════════════════════════════════════════════
# 7. أسئلة بلاغية — لرفع الانفجارية
# ═══════════════════════════════════════════════════════════════
ARABIC_RHETORICAL = [
    "ألا يبدو ذلك غريباً بعض الشيء؟",
    "لكن هل هذا يكفي حقاً؟",
    "والسؤال: ما البديل؟",
    "أليس هذا ما نعنيه تماماً؟",
    "لكن ماذا لو كان العكس هو الصحيح؟",
    "هل فكرت في ذلك من قبل؟",
    "أتساءل أحياناً: هل نحن على الطريق الصحيح؟",
    "وهل يمكننا فعلاً تجاهل ذلك؟",
    "ما الذي يمنعنا من المحاولة؟",
    "ألسنا جميعاً ندرك ذلك في قرارة أنفسنا؟",
]

ENGLISH_RHETORICAL = [
    "doesn't that seem a bit odd?",
    "but is that really enough?",
    "the question is: what's the alternative?",
    "isn't that exactly what we mean?",
    "but what if the opposite is true?",
    "have you ever thought about that?",
    "I sometimes wonder: are we on the right track?",
    "can we really ignore that?",
    "what's stopping us from trying?",
    "don't we all know this deep down?",
]

# ═══════════════════════════════════════════════════════════════
# 8. عبارات غير رسمية / عامية — لتنويع مستوى الرسمية
# ═══════════════════════════════════════════════════════════════
ARABIC_INFORMAL = [
    "يعني", "بمعنى آخر", "ببساطة", "الخلاصة إن",
    "المهم", "الفكرة إن", "بالعربي الفصيح",
    "خلينا نقول إن", "الموضوع ببساطة",
    "باختصار شديد", "لو تبسّطنا في الشرح",
    "دعنا لا نعقّد الأمور",
]

ENGLISH_INFORMAL = [
    "I mean", "in other words", "simply put", "the bottom line is",
    "the thing is", "the idea is", "to put it plainly",
    "let's just say", "basically", "in a nutshell",
    "long story short", "let's not overcomplicate things",
]

# ═══════════════════════════════════════════════════════════════
# 9. أنماط الجمل القصيرة — لرفع الانفجارية
# ═══════════════════════════════════════════════════════════════
ARABIC_SHORT_SENTENCES = [
    "هذا مهم.", "لا شك في ذلك.", "فعلاً.", "تماماً.",
    "والنتيجة؟", "هذه هي الحقيقة.", "ببساطة.", "لا مفر.",
    "هذا هو الواقع.", "بلا مبالغة.", "وهذا ليس كل شيء.",
    "لنكن صريحين.", "الأمر واضح.", "وكفى.", "نقطة.",
    "هكذا هو الحال.", "وللأسف.", "والمفاجأة؟",
]

ENGLISH_SHORT_SENTENCES = [
    "This matters.", "No doubt about it.", "Indeed.", "Exactly.",
    "And the result?", "That's the reality.", "Simply put.", "No way around it.",
    "That's just how it is.", "No exaggeration.", "And that's not all.",
    "Let's be honest.", "It's clear.", "Enough said.", "Period.",
    "That's the situation.", "Unfortunately.", "The surprise?",
]

# ═══════════════════════════════════════════════════════════════
# 10. إضافات بين قوسين — لمحاكاة التفكير البشري
# ═══════════════════════════════════════════════════════════════
ARABIC_PARENTHETICAL = [
    "(وهذا رأيي الشخصي)",
    "(وقد يختلف معي البعض في ذلك)",
    "(على أقل تقدير)",
    "(إن صح التعبير)",
    "(بتحفظ)",
    "(وهذا أمر لافت)",
    "(لا أبالغ هنا)",
    "(وأقولها بكل ثقة)",
    "(رغم أنني لست خبيراً)",
    "(وأرجو ألا أكون مخطئاً)",
    "(ربما أُفرط في التبسيط)",
    "(وهذا موضوع يستحق التوسع فيه لاحقاً)",
]

ENGLISH_PARENTHETICAL = [
    "(and this is just my take)",
    "(some might disagree)",
    "(at the very least)",
    "(if I may say so)",
    "(with some reservation)",
    "(and this is noteworthy)",
    "(I'm not exaggerating here)",
    "(and I say this with confidence)",
    "(though I'm no expert)",
    "(I hope I'm not wrong about this)",
    "(I may be oversimplifying)",
    "(and this deserves its own discussion)",
]

# ═══════════════════════════════════════════════════════════════
# 11. أنماط الأخطاء الطبيعية — لمحاكاة العيوب البشرية
# ═══════════════════════════════════════════════════════════════
ARABIC_NATURAL_IMPERFECTIONS = [
    # تكرار طبيعي
    ("أن أن", "أن"),  # تكرار يُصحَّح
    # تصحيح ذاتي
    " — أقصد — ",
    " — أو بالأحرى — ",
    " — لا، دعني أعيد الصياغة — ",
    " — وأعني بذلك — ",
]

ENGLISH_NATURAL_IMPERFECTIONS = [
    " — I mean — ",
    " — or rather — ",
    " — no, let me rephrase that — ",
    " — what I'm trying to say is — ",
    " — well, actually — ",
]


def detect_language(text):
    """كشف لغة النص (عربي أو إنجليزي)"""
    arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    latin_chars = sum(1 for c in text if 'a' <= c.lower() <= 'z')
    total = arabic_chars + latin_chars
    if total == 0:
        return "ar"
    return "ar" if arabic_chars / total > 0.3 else "en"


def get_synonyms(word, lang="ar"):
    """الحصول على مرادفات كلمة"""
    source = ARABIC_SYNONYMS if lang == "ar" else ENGLISH_SYNONYMS
    return source.get(word, [])


def get_resources(lang="ar"):
    """الحصول على كل موارد اللغة المحددة"""
    if lang == "ar":
        return {
            "synonyms": ARABIC_SYNONYMS,
            "hedging": ARABIC_HEDGING,
            "personal": ARABIC_PERSONAL,
            "emotional": ARABIC_EMOTIONAL,
            "transitions": ARABIC_TRANSITIONS,
            "rhetorical": ARABIC_RHETORICAL,
            "informal": ARABIC_INFORMAL,
            "short_sentences": ARABIC_SHORT_SENTENCES,
            "parenthetical": ARABIC_PARENTHETICAL,
        }
    else:
        return {
            "synonyms": ENGLISH_SYNONYMS,
            "hedging": ENGLISH_HEDGING,
            "personal": ENGLISH_PERSONAL,
            "emotional": ENGLISH_EMOTIONAL,
            "transitions": ENGLISH_TRANSITIONS,
            "rhetorical": ENGLISH_RHETORICAL,
            "informal": ENGLISH_INFORMAL,
            "short_sentences": ENGLISH_SHORT_SENTENCES,
            "parenthetical": ENGLISH_PARENTHETICAL,
        }
