// ═══════════════════════════════════════════════════════════
// app.js — الواجهة الأمامية لنظام تجاوز كشف الذكاء الاصطناعي
// ═══════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const bypassBtn = document.getElementById('bypassBtn');
    const copyBtn = document.getElementById('copyBtn');
    const reprocessBtn = document.getElementById('reprocessBtn');
    const intensitySlider = document.getElementById('intensity');
    const intensityValue = document.getElementById('intensityValue');
    const analysisPanel = document.getElementById('analysisPanel');
    const loading = document.getElementById('loading');
    const inputWordCount = document.getElementById('inputWordCount');
    const outputWordCount = document.getElementById('outputWordCount');
    const chips = document.querySelectorAll('.chip');

    // عداد الكلمات
    function countWords(text) {
        return text.trim() ? text.trim().split(/\s+/).length : 0;
    }

    inputText.addEventListener('input', () => {
        inputWordCount.textContent = countWords(inputText.value) + ' كلمة';
    });

    // شريط التمرير
    intensitySlider.addEventListener('input', () => {
        intensityValue.textContent = intensitySlider.value + '%';
    });

    // أزرار التقنيات
    chips.forEach(chip => {
        chip.addEventListener('click', () => chip.classList.toggle('active'));
    });

    // الحصول على التقنيات المفعلة
    function getActiveTechniques() {
        const active = [];
        chips.forEach(c => { if (c.classList.contains('active')) active.push(c.dataset.tech); });
        return active;
    }

    function showLoading() { loading.style.display = 'flex'; }
    function hideLoading() { loading.style.display = 'none'; }

    // ═══ زر التحليل ═══
    analyzeBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) return;
        showLoading();
        try {
            const res = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            displayAnalysisOnly(data);
        } catch (e) { alert('خطأ في الاتصال بالخادم'); }
        hideLoading();
    });

    // ═══ زر التجاوز ═══
    bypassBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) return;
        showLoading();
        try {
            const techniques = getActiveTechniques();
            const allActive = techniques.length === 6;
            const body = {
                text,
                intensity: intensitySlider.value / 100,
                techniques: allActive ? null : techniques
            };
            const res = await fetch('/api/bypass', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await res.json();
            outputText.value = data.bypassed_text;
            outputWordCount.textContent = countWords(data.bypassed_text) + ' كلمة';
            copyBtn.disabled = false;
            reprocessBtn.disabled = false;
            displayFullAnalysis(data.before_analysis, data.after_analysis, data.improvement);
        } catch (e) { alert('خطأ في الاتصال بالخادم'); }
        hideLoading();
    });

    // ═══ زر النسخ ═══
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(outputText.value).then(() => {
            copyBtn.querySelector('.btn-icon').textContent = '✅';
            setTimeout(() => { copyBtn.querySelector('.btn-icon').textContent = '📋'; }, 2000);
        });
    });

    // ═══ زر إعادة المعالجة ═══
    reprocessBtn.addEventListener('click', () => {
        inputText.value = outputText.value;
        inputWordCount.textContent = countWords(inputText.value) + ' كلمة';
        outputText.value = '';
        outputWordCount.textContent = '0 كلمة';
        bypassBtn.click();
    });

    // ═══ عرض تحليل فقط ═══
    function displayAnalysisOnly(data) {
        analysisPanel.style.display = 'block';
        setRing('beforeRing', data.human_score);
        document.getElementById('beforeScore').textContent = data.human_score;
        document.getElementById('beforeVerdict').textContent = data.verdict;
        document.getElementById('beforeVerdict').style.color = getRiskColor(data.risk_level);
        setRing('afterRing', 0);
        document.getElementById('afterScore').textContent = '—';
        document.getElementById('afterVerdict').textContent = 'لم يُعدَّل بعد';
        document.getElementById('improvementValue').textContent = '—';
        setBars(data, null);
        analysisPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // ═══ عرض التحليل الكامل ═══
    function displayFullAnalysis(before, after, improvement) {
        analysisPanel.style.display = 'block';
        // الحلقات
        setRing('beforeRing', before.human_score);
        setRing('afterRing', after.human_score);
        document.getElementById('beforeScore').textContent = before.human_score;
        document.getElementById('afterScore').textContent = after.human_score;
        document.getElementById('beforeVerdict').textContent = before.verdict;
        document.getElementById('afterVerdict').textContent = after.verdict;
        document.getElementById('beforeVerdict').style.color = getRiskColor(before.risk_level);
        document.getElementById('afterVerdict').style.color = getRiskColor(after.risk_level);
        // التحسن
        const imp = improvement.human_score;
        document.getElementById('improvementValue').textContent = (imp > 0 ? '+' : '') + imp;
        setBars(before, after);
        analysisPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function setRing(id, value) {
        const el = document.getElementById(id);
        const circumference = 2 * Math.PI * 52; // r=52
        const offset = circumference - (value / 100) * circumference;
        setTimeout(() => { el.style.strokeDashoffset = offset; }, 100);
    }

    function setBars(before, after) {
        // Perplexity (0-100)
        setBar('perpBefore', before.perplexity);
        document.getElementById('perpBeforeVal').textContent = before.perplexity;
        if (after) {
            setBar('perpAfter', after.perplexity);
            document.getElementById('perpAfterVal').textContent = after.perplexity;
        }
        // Burstiness (0-1.2 → scale to 100)
        setBar('burstBefore', (before.burstiness / 1.2) * 100);
        document.getElementById('burstBeforeVal').textContent = before.burstiness;
        if (after) {
            setBar('burstAfter', (after.burstiness / 1.2) * 100);
            document.getElementById('burstAfterVal').textContent = after.burstiness;
        }
        // Stylometry (0-100)
        setBar('styleBefore', before.stylometry.score);
        document.getElementById('styleBeforeVal').textContent = before.stylometry.score;
        if (after) {
            setBar('styleAfter', after.stylometry.score);
            document.getElementById('styleAfterVal').textContent = after.stylometry.score;
        }
        // Fingerprints (inverted: less = better)
        const maxFp = 10;
        setBar('fpBefore', Math.min(before.ai_fingerprints / maxFp * 100, 100));
        document.getElementById('fpBeforeVal').textContent = before.ai_fingerprints;
        if (after) {
            setBar('fpAfter', Math.min(after.ai_fingerprints / maxFp * 100, 100));
            document.getElementById('fpAfterVal').textContent = after.ai_fingerprints;
        }
    }

    function setBar(id, percent) {
        const el = document.getElementById(id);
        setTimeout(() => { el.style.width = Math.min(percent, 100) + '%'; }, 200);
    }

    function getRiskColor(risk) {
        return risk === 'low' ? 'var(--success)' : risk === 'medium' ? 'var(--warning)' : 'var(--danger)';
    }
});
