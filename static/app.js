// ═══════════════════════════════════════════════════════════
// app.js — الواجهة الأمامية v2 (نص + رفع ملفات)
// ═══════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // ═══ عناصر النص اليدوي ═══
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
    const loadingText = document.getElementById('loadingText');
    const inputWordCount = document.getElementById('inputWordCount');
    const outputWordCount = document.getElementById('outputWordCount');
    const chips = document.querySelectorAll('.chip');

    // ═══ عناصر التبويبات ═══
    const tabText = document.getElementById('tabText');
    const tabFile = document.getElementById('tabFile');
    const textMode = document.getElementById('textMode');
    const fileMode = document.getElementById('fileMode');

    // ═══ عناصر رفع الملفات ═══
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileTypeIcon = document.getElementById('fileTypeIcon');
    const fileName = document.getElementById('fileName');
    const fileStats = document.getElementById('fileStats');
    const removeFileBtn = document.getElementById('removeFileBtn');
    const fileOverallScore = document.getElementById('fileOverallScore');
    const fileScoreRing = document.getElementById('fileScoreRing');
    const fileScoreValue = document.getElementById('fileScoreValue');
    const fileVerdict = document.getElementById('fileVerdict');
    const fileAiPercent = document.getElementById('fileAiPercent');
    const progressSection = document.getElementById('progressSection');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const fileActions = document.getElementById('fileActions');
    const bypassAllBtn = document.getElementById('bypassAllBtn');
    const bypassAiOnlyBtn = document.getElementById('bypassAiOnlyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const paragraphsPanel = document.getElementById('paragraphsPanel');
    const paragraphsList = document.getElementById('paragraphsList');

    // ═══ حالة التطبيق ═══
    let currentDocId = null;

    // ═══════════════════════════════════════
    //  تبويبات الوضع
    // ═══════════════════════════════════════
    tabText.addEventListener('click', () => {
        tabText.classList.add('active');
        tabFile.classList.remove('active');
        textMode.style.display = '';
        fileMode.style.display = 'none';
    });

    tabFile.addEventListener('click', () => {
        tabFile.classList.add('active');
        tabText.classList.remove('active');
        fileMode.style.display = '';
        textMode.style.display = 'none';
    });

    // ═══════════════════════════════════════
    //  أدوات مساعدة
    // ═══════════════════════════════════════
    function countWords(text) {
        return text.trim() ? text.trim().split(/\s+/).length : 0;
    }

    function showLoading(msg) {
        loadingText.textContent = msg || 'جارٍ المعالجة...';
        loading.style.display = 'flex';
    }
    function hideLoading() { loading.style.display = 'none'; }

    function getFileIcon(type) {
        const icons = { 'docx': '📘', 'pdf': '📕', 'txt': '📄' };
        return icons[type] || '📄';
    }

    function getStatusClass(status) {
        if (status === 'human') return 'status-human';
        if (status === 'mixed') return 'status-mixed';
        if (status === 'ai') return 'status-ai';
        return '';
    }

    function getScoreClass(score) {
        if (score >= 68) return 'score-human';
        if (score >= 42) return 'score-mixed';
        return 'score-ai';
    }

    function getVerdictText(score) {
        if (score >= 68) return 'يبدو بشرياً';
        if (score >= 42) return 'منطقة رمادية';
        return 'مكتشف كـ AI';
    }

    function getVerdictColor(score) {
        if (score >= 68) return 'var(--success)';
        if (score >= 42) return 'var(--warning)';
        return 'var(--danger)';
    }

    // ═══════════════════════════════════════
    //  وضع النص اليدوي (الأصلي بالكامل)
    // ═══════════════════════════════════════
    inputText.addEventListener('input', () => {
        inputWordCount.textContent = countWords(inputText.value) + ' كلمة';
    });

    intensitySlider.addEventListener('input', () => {
        intensityValue.textContent = intensitySlider.value + '%';
    });

    chips.forEach(chip => {
        chip.addEventListener('click', () => chip.classList.toggle('active'));
    });

    function getActiveTechniques() {
        const active = [];
        chips.forEach(c => { if (c.classList.contains('active')) active.push(c.dataset.tech); });
        return active;
    }

    // ═══ زر التحليل ═══
    analyzeBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) return;
        showLoading('جارٍ تحليل النص...');
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
        showLoading('جارٍ تطبيق التجاوز...');
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

    // ═══════════════════════════════════════
    //  وضع رفع الملفات (الجديد)
    // ═══════════════════════════════════════

    // ── Drag & Drop ──
    uploadZone.addEventListener('click', () => fileInput.click());

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) handleFileUpload(files[0]);
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) handleFileUpload(fileInput.files[0]);
    });

    // ── إزالة الملف ──
    removeFileBtn.addEventListener('click', resetFileMode);

    // ── أزرار التجاوز ──
    bypassAllBtn.addEventListener('click', () => bypassFile('all'));
    bypassAiOnlyBtn.addEventListener('click', () => bypassFile('ai_only'));

    // ── زر التحميل ──
    downloadBtn.addEventListener('click', async () => {
        if (!currentDocId) return;
        downloadBtn.disabled = true;
        downloadBtn.textContent = '⏳ جارٍ التحميل...';
        try {
            const res = await fetch(`/api/download/${currentDocId}`);
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || 'خطأ في التحميل');
            }
            const blob = await res.blob();
            // استخراج اسم الملف من Content-Disposition header
            const disposition = res.headers.get('Content-Disposition');
            let downloadName = 'bypassed_file.docx';
            if (disposition) {
                // filename*=UTF-8''name.docx or filename="name.docx"
                const utf8Match = disposition.match(/filename\*=UTF-8''(.+)/i);
                const plainMatch = disposition.match(/filename="?([^";\n]+)"?/i);
                if (utf8Match) {
                    downloadName = decodeURIComponent(utf8Match[1]);
                } else if (plainMatch) {
                    downloadName = plainMatch[1].trim();
                }
            }
            // إنشاء رابط تحميل مؤقت
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = downloadName;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (e) {
            alert('خطأ: ' + e.message);
        }
        downloadBtn.disabled = false;
        downloadBtn.textContent = '💾 تحميل الملف';
    });

    // ═══ رفع ومعالجة الملف ═══
    async function handleFileUpload(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        if (!['docx', 'pdf', 'txt'].includes(ext)) {
            alert('نوع الملف غير مدعوم. يرجى رفع ملف DOCX أو PDF أو TXT');
            return;
        }

        if (file.size > 20 * 1024 * 1024) {
            alert('حجم الملف كبير جداً. الحد الأقصى 20 ميجابايت');
            return;
        }

        // إظهار شريط التقدم
        showProgress('جارٍ رفع الملف وتحليله...', 10);
        uploadZone.style.display = 'none';
        fileInfo.style.display = '';

        // إظهار اسم الملف
        fileTypeIcon.textContent = getFileIcon(ext);
        fileName.textContent = file.name;
        fileStats.textContent = 'جارٍ التحليل...';

        try {
            showProgress('جارٍ استخراج النص والصور...', 25);

            const formData = new FormData();
            formData.append('file', file);

            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || 'خطأ غير معروف');
            }

            showProgress('جارٍ تحليل الفقرات...', 60);

            const data = await res.json();
            currentDocId = data.doc_id;

            // تحديث الإحصائيات
            let statsText = `${data.total_words} كلمة`;
            if (data.image_count > 0) {
                statsText += ` · ${data.image_count} صورة`;
            }
            statsText += ` · ${data.file_type.toUpperCase()}`;
            fileStats.textContent = statsText;

            showProgress('اكتمل التحليل!', 100);

            // عرض النتيجة الإجمالية
            setTimeout(() => {
                hideProgress();
                displayFileResults(data);
            }, 600);

        } catch (e) {
            hideProgress();
            alert('خطأ: ' + e.message);
            resetFileMode();
        }
    }

    // ═══ عرض نتائج تحليل الملف ═══
    function displayFileResults(data) {
        // النتيجة الإجمالية
        fileOverallScore.style.display = '';
        const score = data.overall_score;
        setRingValue(fileScoreRing, score);
        fileScoreValue.textContent = score;
        fileVerdict.textContent = getVerdictText(score);
        fileVerdict.style.color = getVerdictColor(score);
        fileAiPercent.textContent = `نسبة AI المقدرة: ${Math.max(0, 100 - score).toFixed(0)}%`;
        fileAiPercent.style.color = getVerdictColor(score);

        // تلوين الحلقة
        if (score >= 68) fileScoreRing.style.stroke = 'var(--success)';
        else if (score >= 42) fileScoreRing.style.stroke = 'var(--warning)';
        else fileScoreRing.style.stroke = 'var(--danger)';

        // أزرار التحكم
        fileActions.style.display = '';

        // عرض الفقرات
        displayParagraphs(data.paragraphs);
    }

    // ═══ عرض الفقرات ═══
    function displayParagraphs(paragraphs) {
        paragraphsPanel.style.display = '';
        paragraphsList.innerHTML = '';

        paragraphs.forEach((para, idx) => {
            const div = document.createElement('div');
            div.className = `paragraph-item ${getStatusClass(para.status)}`;
            div.id = `para-${para.id}`;

            let scoreHtml = '';
            if (para.analysis) {
                const sc = para.analysis.human_score;
                scoreHtml = `<span class="para-score ${getScoreClass(sc)}">${sc}%</span>`;
            } else {
                scoreHtml = `<span class="para-score" style="opacity:0.4">قصير</span>`;
            }

            div.innerHTML = `
                <div class="para-header">
                    <span class="para-number">فقرة ${idx + 1}</span>
                    ${scoreHtml}
                </div>
                <div class="para-text">${escapeHtml(para.text)}</div>
            `;
            paragraphsList.appendChild(div);
        });
    }

    // ═══ تجاوز الملف ═══
    async function bypassFile(mode) {
        if (!currentDocId) return;

        showLoading('جارٍ تطبيق التجاوز على الملف...');
        showProgress('جارٍ معالجة الفقرات...', 20);

        try {
            // إرسال التقنيات المختارة من المستخدم
            const techniques = getActiveTechniques();
            const allActive = techniques.length === 6;

            const res = await fetch('/api/bypass-file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    doc_id: currentDocId,
                    intensity: intensitySlider.value / 100,
                    mode: mode,
                    techniques: allActive ? null : techniques
                })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || 'خطأ');
            }

            showProgress('جارٍ تجميع النتائج...', 80);

            const data = await res.json();

            showProgress('اكتمل التجاوز!', 100);

            setTimeout(() => {
                hideProgress();
                hideLoading();
                displayBypassResults(data);
            }, 500);

        } catch (e) {
            hideProgress();
            hideLoading();
            alert('خطأ: ' + e.message);
        }
    }

    // ═══ عرض نتائج التجاوز ═══
    function displayBypassResults(data) {
        // تحديث النتيجة الإجمالية
        const afterScore = data.overall_after;
        setRingValue(fileScoreRing, afterScore);
        fileScoreValue.textContent = afterScore;
        fileVerdict.textContent = getVerdictText(afterScore) + ' (بعد التعديل)';
        fileVerdict.style.color = getVerdictColor(afterScore);
        fileAiPercent.textContent = `تحسن: +${data.improvement} · عُدّلت ${data.modified_count} من ${data.total_paragraphs} فقرة`;
        fileAiPercent.style.color = 'var(--accent-2)';

        if (afterScore >= 68) fileScoreRing.style.stroke = 'var(--success)';
        else if (afterScore >= 42) fileScoreRing.style.stroke = 'var(--warning)';
        else fileScoreRing.style.stroke = 'var(--danger)';

        // تحديث الفقرات بالنتائج
        data.results.forEach((result, idx) => {
            const paraDiv = document.getElementById(`para-${result.id}`);
            if (!paraDiv) return;

            if (result.status === 'modified') {
                paraDiv.className = 'paragraph-item status-modified';

                // تحديث النتيجة
                const scoreSpan = paraDiv.querySelector('.para-score');
                if (scoreSpan) {
                    scoreSpan.textContent = `${result.before_score}→${result.after_score}`;
                    scoreSpan.className = `para-score ${getScoreClass(result.after_score)}`;
                }

                // إضافة النص المعدل
                const existingModified = paraDiv.querySelector('.para-modified');
                if (!existingModified) {
                    const modDiv = document.createElement('div');
                    modDiv.className = 'para-modified';
                    modDiv.innerHTML = `
                        <div class="para-modified-label">✅ النص المعدَّل:</div>
                        <div class="para-modified-text">${escapeHtml(result.modified)}</div>
                    `;
                    paraDiv.appendChild(modDiv);
                }
            }
        });

        // إظهار زر التحميل
        downloadBtn.style.display = '';
    }

    // ═══ إعادة تعيين وضع الملف ═══
    function resetFileMode() {
        currentDocId = null;
        uploadZone.style.display = '';
        fileInfo.style.display = 'none';
        fileOverallScore.style.display = 'none';
        fileActions.style.display = 'none';
        downloadBtn.style.display = 'none';
        paragraphsPanel.style.display = 'none';
        paragraphsList.innerHTML = '';
        fileInput.value = '';
        hideProgress();
    }

    // ═══ شريط التقدم ═══
    function showProgress(text, percent) {
        progressSection.style.display = '';
        progressText.textContent = text;
        progressFill.style.width = percent + '%';
    }

    function hideProgress() {
        progressSection.style.display = 'none';
        progressFill.style.width = '0%';
    }

    // ═══════════════════════════════════════
    //  وظائف العرض المشتركة
    // ═══════════════════════════════════════

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

    function displayFullAnalysis(before, after, improvement) {
        analysisPanel.style.display = 'block';
        setRing('beforeRing', before.human_score);
        setRing('afterRing', after.human_score);
        document.getElementById('beforeScore').textContent = before.human_score;
        document.getElementById('afterScore').textContent = after.human_score;
        document.getElementById('beforeVerdict').textContent = before.verdict;
        document.getElementById('afterVerdict').textContent = after.verdict;
        document.getElementById('beforeVerdict').style.color = getRiskColor(before.risk_level);
        document.getElementById('afterVerdict').style.color = getRiskColor(after.risk_level);
        const imp = improvement.human_score;
        document.getElementById('improvementValue').textContent = (imp > 0 ? '+' : '') + imp;
        setBars(before, after);
        analysisPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function setRing(id, value) {
        const el = document.getElementById(id);
        const circumference = 2 * Math.PI * 52;
        const offset = circumference - (value / 100) * circumference;
        setTimeout(() => { el.style.strokeDashoffset = offset; }, 100);
    }

    function setRingValue(el, value) {
        const circumference = 2 * Math.PI * 52;
        const offset = circumference - (value / 100) * circumference;
        setTimeout(() => { el.style.strokeDashoffset = offset; }, 100);
    }

    function setBars(before, after) {
        setBar('perpBefore', before.perplexity);
        document.getElementById('perpBeforeVal').textContent = before.perplexity;
        if (after) {
            setBar('perpAfter', after.perplexity);
            document.getElementById('perpAfterVal').textContent = after.perplexity;
        }
        setBar('burstBefore', (before.burstiness / 1.2) * 100);
        document.getElementById('burstBeforeVal').textContent = before.burstiness;
        if (after) {
            setBar('burstAfter', (after.burstiness / 1.2) * 100);
            document.getElementById('burstAfterVal').textContent = after.burstiness;
        }
        setBar('styleBefore', before.stylometry.score);
        document.getElementById('styleBeforeVal').textContent = before.stylometry.score;
        if (after) {
            setBar('styleAfter', after.stylometry.score);
            document.getElementById('styleAfterVal').textContent = after.stylometry.score;
        }
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

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
