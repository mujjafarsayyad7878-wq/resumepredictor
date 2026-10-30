/**
 * Smart Resume Matcher & Career Guide - Frontend Controller
 * Supports multi-page navigation (Home, Results, Roles Guide),
 * custom job role typing & preset dropdown, English and Hindi bilingual UI,
 * Chart.js score gauge & radar, drag & drop, and PDF export.
 */

let matchGaugeChart = null;
let competencyRadarChart = null;
let currentAnalysisResult = null;
let availableRoles = [];
let currentLanguage = 'en'; // 'en' or 'hi'
let currentPage = 'home';
let isCustomRoleMode = false;

// Translation Dictionary (English and Hindi - Simple, everyday language)
const I18N = {
    en: {
        nav_home: "Home & Upload",
        nav_results: "Analysis Report",
        nav_roles: "Job Roles Guide",
        status_online: "Ready",
        hero_badge: "100% Free Resume Analysis & Career Guidance",
        hero_title_1: "Check How Well Your Resume Matches",
        hero_title_2: "Any Tech Job",
        hero_desc: "Upload your resume to instantly see your match score, discover the exact missing skills employers look for, estimate your realistic salary, and get free learning courses — in simple, normal language!",
        step1_title: "1. Upload Resume",
        step1_desc: "PDF, Text or paste text. English & Hindi supported.",
        step2_title: "2. Choose Job Role",
        step2_desc: "Pick from popular tech roles or type your own custom role!",
        step3_title: "3. Get Instant Results",
        step3_desc: "See match score, missing skills, salary and free courses.",
        input_label_resume: "Upload or Paste Resume",
        dropzone_click: "Click to upload PDF / Text",
        dropzone_or: "or drag & drop here",
        dropzone_support: "Supports PDF, TXT, MD (Max 15MB)",
        resume_placeholder: "Or paste your resume text here (experience, skills, education, projects, English or Hindi)...",
        target_role_label: "Select Target Job Role",
        btn_type_custom_role: "Type custom role",
        btn_pick_preset_role: "Pick from list",
        custom_role_hint: "You can type any tech title you want.",
        custom_role_placeholder: "Type job title (e.g. Flutter Developer, Mobile Engineer, QA Tester)...",
        role_exp_needed: "Experience Needed:",
        role_salary_label: "Typical Market Salary:",
        custom_jd_toggle: "Compare against a specific Job Description",
        custom_jd_placeholder: "Paste the job posting requirements here...",
        btn_analyze: "Analyze Resume Now",
        btn_clear: "Clear Form",
        loading_title: "Analyzing Your Resume...",
        loading_steps: [
            "Reading candidate profile, experience and education...",
            "Matching skills against job requirements...",
            "Checking market salary and learning recommendations...",
            "Preparing your personalized career report..."
        ],
        empty_title: "No Analysis Results Yet",
        empty_desc: "Upload your resume on the Home page first to generate your match score, missing skills, and salary report.",
        empty_btn: "Go to Upload Resume",
        res_report_for: "Analysis Report for:",
        btn_download_pdf: "Download PDF Report",
        btn_upload_another: "Upload Another Resume",
        summary_box_title: "Quick Summary & Recommendation",
        card_exp: "Experience",
        card_level: "Level",
        card_skills_found: "Skills Found",
        metric_score_label: "Job Match Score",
        gauge_match_label: "Match",
        score_skills: "Skills Coverage",
        score_text: "Resume Quality",
        metric_salary_label: "Estimated Salary",
        salary_sublabel: "Market Baseline for your skills",
        salary_percentile: "Market Standing:",
        metric_radar_label: "Skills Balance Chart",
        radar_footer: "Your skills across core technology areas",
        skills_matrix_title: "Skills You Have vs. Skills You Need",
        skills_matrix_desc: "Clear comparison showing what you already know and what skills to learn next.",
        skills_you_have: "Skills You Have (Verified)",
        skills_to_learn: "Skills to Learn (Missing for this role)",
        skills_extra: "Extra Skills in Your Resume",
        courses_title: "Free Learning Courses & Recommendations",
        courses_desc: "Free courses, official docs, and practice projects to easily learn your missing skills.",
        courses_badge: "Actionable Steps",
        capstone_label: "Recommended Practice Project:",
        explore_resource_btn: "Explore Free Tutorial",
        alt_roles_title: "Other Jobs You Are Good For",
        alt_roles_desc: "See how well your current skills fit other in-demand tech roles.",
        roles_guide_badge: "Industry Roles Guide",
        roles_guide_title: "Tech Job Roles & Required Skills",
        roles_guide_desc: "Explore standard tech jobs to understand what skills companies look for, expected salary bands, and average experience needed.",
        footer_title: "Smart Resume Matcher & Career Guide (Production Edition)"
    },

    hi: {
        nav_home: "होम और अपलोड",
        nav_results: "रिजल्ट रिपोर्ट",
        nav_roles: "नौकरी गाइड",
        status_online: "तैयार है",
        hero_badge: "100% मुफ्त रिज्यूमे विश्लेषण व करियर सलाह",
        hero_title_1: "जानें कि आपका रिज्यूमे किसी भी नौकरी के लिए",
        hero_title_2: "कितना तैयार है",
        hero_desc: "अपना रिज्यूमे अपलोड करें और तुरंत जानें: आपका मैच स्कोर, कौन से कौशल आपको सीखने हैं, आपका अनुमानित वेतन और सीखने के लिए मुफ्त कोर्सेज — बिल्कुल सरल और आसान भाषा में!",
        step1_title: "1. रिज्यूमे अपलोड करें",
        step1_desc: "पीडीएफ या टेक्स्ट फाइल अपलोड करें या टेक्स्ट पेस्ट करें। हिंदी व अंग्रेजी दोनों समर्थित।",
        step2_title: "2. नौकरी का पद चुनें",
        step2_desc: "लिस्ट से चुनें या अपना मनपसंद पद खुद टाइप करें!",
        step3_title: "3. तुरंत रिजल्ट पाएं",
        step3_desc: "मैच स्कोर, छूटे हुए कौशल, वेतन और सीखने के मुफ्त साधन देखें।",
        input_label_resume: "रिज्यूमे अपलोड करें या पेस्ट करें",
        dropzone_click: "पीडीएफ या टेक्स्ट फाइल चुनने के लिए क्लिक करें",
        dropzone_or: "या फाइल को यहां ड्रैग व ड्रॉप करें",
        dropzone_support: "पीडीएफ (PDF), टेक्स्ट (TXT), मार्कडाउन (MD) समर्थित (अधिकतम 15MB)",
        resume_placeholder: "या अपना रिज्यूमे यहां पेस्ट करें (अनुभव, कौशल, शिक्षा, प्रोजेक्ट्स - हिंदी या अंग्रेजी में)...",
        target_role_label: "लक्षित नौकरी का पद चुनें",
        btn_type_custom_role: "खुद से लिखें",
        btn_pick_preset_role: "लिस्ट से चुनें",
        custom_role_hint: "आप कोई भी पद खुद टाइप कर सकते हैं।",
        custom_role_placeholder: "पद का नाम लिखें (जैसे Flutter Developer, Android Engineer, QA Tester)...",
        role_exp_needed: "आवश्यक अनुभव:",
        role_salary_label: "बाजार में सामान्य वेतन:",
        custom_jd_toggle: "किसी विशेष नौकरी के विवरण (JD) से तुलना करें",
        custom_jd_placeholder: "कंपनी की नौकरी का विवरण (Job Description) यहां पेस्ट करें...",
        btn_analyze: "रिज्यूमे का विश्लेषण करें",
        btn_clear: "फॉर्म साफ करें",
        loading_title: "आपके रिज्यूमे का विश्लेषण हो रहा है...",
        loading_steps: [
            "उम्मीदवार का प्रोफाइल, कुल अनुभव और शिक्षा पढ़ी जा रही है...",
            "नौकरी की आवश्यकताओं से कौशल का मिलान किया जा रहा है...",
            "बाजार वेतन और सीखने के कोर्सेज तैयार किए जा रहे हैं...",
            "आपकी व्यक्तिगत करियर रिपोर्ट तैयार हो रही है..."
        ],
        empty_title: "अभी तक कोई रिपोर्ट उपलब्ध नहीं है",
        empty_desc: "अपना मैच स्कोर, छूटे हुए कौशल और वेतन रिपोर्ट देखने के लिए पहले होम पेज पर अपना रिज्यूमे अपलोड करें।",
        empty_btn: "रिज्यूमे अपलोड करने जाएं",
        res_report_for: "विश्लेषण रिपोर्ट:",
        btn_download_pdf: "पीडीएफ रिपोर्ट डाउनलोड करें",
        btn_upload_another: "नया रिज्यूमे जांचें",
        summary_box_title: "त्वरित सारांश और सलाह",
        card_exp: "अनुभव",
        card_level: "वरिष्ठता स्तर",
        card_skills_found: "पहचाने गए कौशल",
        metric_score_label: "नौकरी मैच स्कोर",
        gauge_match_label: "मैच",
        score_skills: "कौशल मिलान",
        score_text: "रिज्यूमे गुणवत्ता",
        metric_salary_label: "अनुमानित वेतन पैकेज",
        salary_sublabel: "आपके कौशल के आधार पर बाजार दर",
        salary_percentile: "बाजार में स्थिति:",
        metric_radar_label: "कौशल संतुलन चार्ट",
        radar_footer: "प्रमुख तकनीकी क्षेत्रों में आपका ज्ञान",
        skills_matrix_title: "आपके पास मौजूद कौशल बनाम सीखने योग्य कौशल",
        skills_matrix_desc: "स्पष्ट तुलना जो दिखाती है कि आप क्या जानते हैं और आगे क्या सीखना है।",
        skills_you_have: "आपके पास मौजूद कौशल (Verified)",
        skills_to_learn: "सीखने योग्य कौशल (इस पद के लिए जरूरी)",
        skills_extra: "अतिरिक्त कौशल",
        courses_title: "सीखने के लिए मुफ्त कोर्सेज व सुझाव",
        courses_desc: "छूटे हुए कौशल को आसानी से सीखने के लिए मुफ्त ट्यूटोरियल्स, आधिकारिक डॉक्स और प्रोजेक्ट्स।",
        courses_badge: "सुझाए गए कदम",
        capstone_label: "सुझाया गया प्रैक्टिस प्रोजेक्ट:",
        explore_resource_btn: "फ्री ट्यूटोरियल देखें",
        alt_roles_title: "अन्य नौकरियां जिनके लिए आप उपयुक्त हैं",
        alt_roles_desc: "देखें कि आपके वर्तमान कौशल अन्य लोकप्रिय तकनीकी नौकरियों से कितने मेल खाते हैं।",
        roles_guide_badge: "नौकरी गाइड",
        roles_guide_title: "प्रमुख आईटी नौकरियां और आवश्यक कौशल",
        roles_guide_desc: "जानें कि अलग-अलग तकनीकी नौकरियों में कंपनियां क्या कौशल मांगती हैं और कितना वेतन मिलता है।",
        footer_title: "स्मार्ट रिज्यूमे मैच व करियर गाइड (प्रोडक्शन संस्करण)"
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    setupDragAndDrop();
    await fetchRoles();
    handleRoleChange();
    applyTranslations(currentLanguage);
}

/**
 * Switch Navigation Tab Pages (3 Core Pages)
 */
function switchPage(pageId) {
    currentPage = pageId;

    const pages = ['home', 'results', 'roles'];
    pages.forEach(p => {
        const el = document.getElementById(`page-${p}`);
        if (el) {
            if (p === pageId) {
                el.classList.remove('hidden');
            } else {
                el.classList.add('hidden');
            }
        }

        const navBtn = document.getElementById(`nav-btn-${p}`);
        if (navBtn) {
            if (p === pageId) {
                navBtn.className = 'px-3.5 py-1.5 rounded-lg bg-indigo-600 text-white transition-all flex items-center space-x-1.5 shadow-sm';
            } else {
                navBtn.className = 'px-3.5 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60 transition-all flex items-center space-x-1.5 relative';
            }
        }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Switch Language Toggle (English <-> Hindi)
 */
function toggleLanguage() {
    currentLanguage = (currentLanguage === 'en') ? 'hi' : 'en';
    applyTranslations(currentLanguage);
    
    // Update button display
    const labelEl = document.getElementById('current-lang-label');
    if (labelEl) {
        labelEl.textContent = (currentLanguage === 'en') ? 'English' : 'हिंदी';
    }

    // If analysis result is currently displayed, re-render in the active language
    if (currentAnalysisResult) {
        renderResultsDashboard(currentAnalysisResult);
    }

    // Re-render role preview and roles catalog
    handleRoleChange();
    renderRolesCatalog();
}

/**
 * Apply I18N Translations across all HTML nodes
 */
function applyTranslations(lang) {
    const dict = I18N[lang] || I18N.en;

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    // Update Placeholders
    const resumeTextarea = document.getElementById('resume-text');
    if (resumeTextarea && dict.resume_placeholder) {
        resumeTextarea.placeholder = dict.resume_placeholder;
    }

    const jdTextarea = document.getElementById('custom-jd-text');
    if (jdTextarea && dict.custom_jd_placeholder) {
        jdTextarea.placeholder = dict.custom_jd_placeholder;
    }

    const customRoleInput = document.getElementById('custom-role-input');
    if (customRoleInput && dict.custom_role_placeholder) {
        customRoleInput.placeholder = dict.custom_role_placeholder;
    }

    const langLabel = document.getElementById('current-lang-label');
    if (langLabel) {
        langLabel.textContent = (lang === 'en') ? 'English' : 'हिंदी';
    }

    // Update toggle role mode text
    const toggleBtnText = document.getElementById('toggle-role-mode-text');
    if (toggleBtnText) {
        toggleBtnText.textContent = isCustomRoleMode ? dict.btn_pick_preset_role : dict.btn_type_custom_role;
    }
}

/**
 * Toggle Between Dropdown Role Selection and Custom Input Typing
 */
function toggleCustomRoleMode(forceCustom) {
    if (typeof forceCustom === 'boolean') {
        isCustomRoleMode = forceCustom;
    } else {
        isCustomRoleMode = !isCustomRoleMode;
    }

    const selectContainer = document.getElementById('role-select-container');
    const customContainer = document.getElementById('custom-role-container');
    const toggleBtnText = document.getElementById('toggle-role-mode-text');
    const customInput = document.getElementById('custom-role-input');
    const isHi = (currentLanguage === 'hi');

    if (isCustomRoleMode) {
        if (selectContainer) selectContainer.classList.add('hidden');
        if (customContainer) customContainer.classList.remove('hidden');
        if (toggleBtnText) toggleBtnText.textContent = isHi ? 'लिस्ट से चुनें' : 'Pick from list';
        if (customInput) customInput.focus();
        handleCustomRoleInput();
    } else {
        if (selectContainer) selectContainer.classList.remove('hidden');
        if (customContainer) customContainer.classList.add('hidden');
        if (toggleBtnText) toggleBtnText.textContent = isHi ? 'खुद से लिखें' : 'Type custom role';
        
        const select = document.getElementById('target-role');
        if (select && select.value === '__custom__') {
            select.selectedIndex = 0;
        }
        handleRoleChange();
    }
}

/**
 * Handle Live Input in Custom Target Role Input Field
 */
function handleCustomRoleInput() {
    const customInput = document.getElementById('custom-role-input');
    const roleTitle = customInput ? customInput.value.trim() : '';
    const expEl = document.getElementById('preview-exp');
    const salEl = document.getElementById('preview-salary');
    const sumEl = document.getElementById('preview-summary');
    const isHi = (currentLanguage === 'hi');

    if (roleTitle) {
        if (expEl) expEl.textContent = isHi ? '2-5+ वर्ष (अनुमानित)' : '2-5+ Years (Estimated)';
        if (salEl) salEl.textContent = '$100k - $165k (~₹12 - ₹28 LPA)';
        if (sumEl) sumEl.textContent = isHi 
            ? `लक्षित पद: "${roleTitle}"। आपके रिज्यूमे का मूल्यांकन इस तकनीकी पद की आवश्यक क्षमताओं के आधार पर किया जाएगा।`
            : `Target Role: "${roleTitle}". Evaluation will benchmark your skills against industry requirements for this title.`;
    } else {
        if (expEl) expEl.textContent = isHi ? 'पद दर्ज करें' : 'Varies by role';
        if (salEl) salEl.textContent = '$95k - $160k (~₹10 - ₹25 LPA)';
        if (sumEl) sumEl.textContent = isHi 
            ? 'ऊपर अपने मनपसंद पद का नाम टाइप करें (जैसे Flutter Developer, Android Engineer, QA Tester)...'
            : 'Type your custom job title above (e.g. Flutter Developer, Mobile Engineer, QA Tester)...';
    }
}

/**
 * Fetch available roles from backend
 */
async function fetchRoles() {
    try {
        const res = await fetch('/api/roles');
        if (res.ok) {
            const data = await res.json();
            availableRoles = data.roles || [];
            populateRoleDropdown(availableRoles);
            renderRolesCatalog();
        }
    } catch (err) {
        console.warn('Could not fetch roles from API, using fallback defaults', err);
    }
}

function populateRoleDropdown(roles) {
    const select = document.getElementById('target-role');
    if (!select || !roles.length) return;
    
    const currentVal = select.value;
    select.innerHTML = '';
    roles.forEach(role => {
        const opt = document.createElement('option');
        opt.value = role.title;
        opt.textContent = (currentLanguage === 'hi' && role.title_hi) ? `${role.title_hi} (${role.title})` : role.title;
        select.appendChild(opt);
    });

    // Add custom typing option
    const customOpt = document.createElement('option');
    customOpt.value = '__custom__';
    customOpt.textContent = (currentLanguage === 'hi') ? '✏️ Custom Role (खुद से लिखें)...' : '✏️ Custom Role (Type your own title)...';
    select.appendChild(customOpt);

    if (currentVal && currentVal !== '__custom__') select.value = currentVal;
}

/**
 * Handle changing target role to update preview snapshot
 */
function handleRoleChange() {
    const select = document.getElementById('target-role');
    const selectedTitle = select ? select.value : '';

    if (selectedTitle === '__custom__') {
        toggleCustomRoleMode(true);
        return;
    }

    const role = availableRoles.find(r => r.title === selectedTitle);
    const expEl = document.getElementById('preview-exp');
    const salEl = document.getElementById('preview-salary');
    const sumEl = document.getElementById('preview-summary');

    if (role) {
        const expText = (currentLanguage === 'hi') ? `${role.min_experience_years}+ वर्ष` : `${role.min_experience_years}+ Years`;
        if (expEl) expEl.textContent = expText;

        if (salEl && role.salary_range) {
            const minK = Math.round(role.salary_range.min / 1000);
            const maxK = Math.round(role.salary_range.max / 1000);
            const inrMin = role.salary_range.inr_lpa_min || 12;
            const inrMax = role.salary_range.inr_lpa_max || 28;
            salEl.textContent = `$${minK}k - $${maxK}k (~₹${inrMin} - ₹${inrMax} LPA)`;
        }

        if (sumEl) {
            sumEl.textContent = (currentLanguage === 'hi' && role.summary_hi) ? role.summary_hi : role.summary;
        }
    } else {
        if (expEl) expEl.textContent = (currentLanguage === 'hi') ? '3+ वर्ष' : '3+ Years';
        if (salEl) salEl.textContent = '$110k - $175k (~₹12 - ₹25 LPA)';
        if (sumEl) sumEl.textContent = (currentLanguage === 'hi') ? 'मानक तकनीकी भूमिका मूल्यांकन।' : 'Industry benchmark role evaluation.';
    }
}

/**
 * Render the dedicated Job Roles Catalog on Page 3
 */
function renderRolesCatalog() {
    const grid = document.getElementById('roles-catalog-grid');
    if (!grid) return;

    grid.innerHTML = '';
    if (!availableRoles.length) return;

    availableRoles.forEach(role => {
        const isHi = (currentLanguage === 'hi');
        const title = isHi && role.title_hi ? role.title_hi : role.title;
        const category = isHi && role.category_hi ? role.category_hi : role.category;
        const summary = isHi && role.summary_hi ? role.summary_hi : role.summary;
        const minK = Math.round(role.salary_range.min / 1000);
        const maxK = Math.round(role.salary_range.max / 1000);
        const inrMin = role.salary_range.inr_lpa_min || 12;
        const inrMax = role.salary_range.inr_lpa_max || 28;

        const card = document.createElement('div');
        card.className = 'glass-panel rounded-2xl p-6 flex flex-col justify-between space-y-4 glow-border';

        const primaryChips = (role.primary_skills || []).slice(0, 6).map(s => 
            `<span class="px-2 py-0.5 rounded-md bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-[10px] font-medium">${s}</span>`
        ).join('');

        card.innerHTML = `
            <div class="space-y-3">
                <div class="flex items-center justify-between">
                    <span class="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                        ${category}
                    </span>
                    <span class="text-xs text-slate-400">
                        <i class="fa-solid fa-clock mr-1"></i>${role.min_experience_years}+ ${isHi ? 'वर्ष अनुभव' : 'Years Exp'}
                    </span>
                </div>
                <h4 class="text-lg font-bold font-heading text-white">${title}</h4>
                <p class="text-xs text-slate-300 leading-relaxed">${summary}</p>
                <div>
                    <span class="text-[10px] uppercase font-semibold text-slate-400 block mb-1.5">${isHi ? 'मुख्य कौशल (Top Skills):' : 'Key Skills Looked For:'}</span>
                    <div class="flex flex-wrap gap-1.5">
                        ${primaryChips}
                    </div>
                </div>
            </div>
            <div class="pt-4 border-t border-white/10 flex items-center justify-between text-xs">
                <div>
                    <span class="text-[10px] text-slate-400 block">${isHi ? 'अनुमानित पैकेज:' : 'Market Salary:'}</span>
                    <span class="font-bold text-emerald-400">$${minK}k - $${maxK}k <span class="text-cyan-300">(₹${inrMin}-₹${inrMax} LPA)</span></span>
                </div>
                <button type="button" onclick="selectRoleAndGoHome('${role.title}')" class="px-3 py-1.5 rounded-xl bg-indigo-600/30 hover:bg-indigo-600 text-indigo-200 hover:text-white border border-indigo-500/30 text-xs font-semibold transition-all cursor-pointer">
                    ${isHi ? 'यह पद चुनें' : 'Test This Role'} &rarr;
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

function selectRoleAndGoHome(roleTitle) {
    if (isCustomRoleMode) {
        toggleCustomRoleMode(false);
    }
    const select = document.getElementById('target-role');
    if (select) {
        select.value = roleTitle;
        handleRoleChange();
    }
    switchPage('home');
}

/**
 * Drag and Drop File Upload Setup
 */
function setupDragAndDrop() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resume-file-input');

    if (!dropzone || !fileInput) return;

    dropzone.addEventListener('click', (e) => {
        if (e.target.closest('#uploaded-file-badge button')) return;
        fileInput.click();
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dropzone-active');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dropzone-active');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleUploadedFile(files[0]);
        }
    });
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleUploadedFile(files[0]);
    }
}

async function handleUploadedFile(file) {
    if (!file) return;

    const badge = document.getElementById('uploaded-file-badge');
    const nameEl = document.getElementById('uploaded-file-name');
    if (badge && nameEl) {
        nameEl.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;
        badge.classList.remove('hidden');
    }

    const textarea = document.getElementById('resume-text');
    const waitMsg = (currentLanguage === 'hi') ? `${file.name} से टेक्स्ट निकाला जा रहा है... कृपया प्रतीक्षा करें।` : `Extracting text from ${file.name}... Please wait.`;
    if (textarea) {
        textarea.value = waitMsg;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('/api/extract-text', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Failed to extract text from file');
        }

        const data = await res.json();
        if (textarea) {
            textarea.value = data.extracted_text;
            updateCounters();
        }

        // Auto-switch to Hindi if uploaded file contains Hindi
        if (data.detected_language === 'hi' && currentLanguage !== 'hi') {
            currentLanguage = 'hi';
            applyTranslations('hi');
        }

    } catch (err) {
        alert(`File Extraction Error: ${err.message}`);
        if (textarea) textarea.value = '';
        clearUploadedFile();
    }
}

function clearUploadedFile(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    const fileInput = document.getElementById('resume-file-input');
    if (fileInput) fileInput.value = '';
    const badge = document.getElementById('uploaded-file-badge');
    if (badge) badge.classList.add('hidden');
}

/**
 * Text and word counter
 */
function updateCounters() {
    const textarea = document.getElementById('resume-text');
    const counterEl = document.getElementById('char-count');
    if (!textarea || !counterEl) return;

    const text = textarea.value.trim();
    const chars = text.length;
    const words = text ? text.split(/\s+/).length : 0;
    const wordsLabel = (currentLanguage === 'hi') ? 'शब्द' : 'words';
    const charsLabel = (currentLanguage === 'hi') ? 'अक्षर' : 'chars';
    counterEl.textContent = `${words} ${wordsLabel} | ${chars} ${charsLabel}`;

    // Auto-detect Hindi as user types or pastes
    const devChars = (text.match(/[\u0900-\u097F]/g) || []).length;
    if (devChars > 15 && currentLanguage !== 'hi') {
        currentLanguage = 'hi';
        applyTranslations('hi');
    }
}

function toggleCustomJdView() {
    const checkbox = document.getElementById('toggle-custom-jd');
    const container = document.getElementById('custom-jd-container');
    if (checkbox && container) {
        if (checkbox.checked) {
            container.classList.remove('hidden');
        } else {
            container.classList.add('hidden');
        }
    }
}

function resetForm() {
    const textarea = document.getElementById('resume-text');
    const customJd = document.getElementById('custom-jd-text');
    const customToggle = document.getElementById('toggle-custom-jd');
    const customRoleInput = document.getElementById('custom-role-input');
    if (textarea) textarea.value = '';
    if (customJd) customJd.value = '';
    if (customRoleInput) customRoleInput.value = '';
    if (customToggle) {
        customToggle.checked = false;
        toggleCustomJdView();
    }
    if (isCustomRoleMode) {
        toggleCustomRoleMode(false);
    }
    clearUploadedFile();
    updateCounters();
}

/**
 * Execute Main Analysis Pipeline
 */
async function runAnalysis() {
    const textarea = document.getElementById('resume-text');
    const resumeText = textarea ? textarea.value.trim() : '';

    if (!resumeText || resumeText.length < 25) {
        const msg = (currentLanguage === 'hi') 
            ? 'कृपया विश्लेषण के लिए कम से कम 25 अक्षरों का एक मान्य रिज्यूमे दर्ज करें या अपलोड करें।' 
            : 'Please enter or upload a valid resume with at least 25 characters to analyze.';
        alert(msg);
        if (textarea) textarea.focus();
        return;
    }

    // Determine target role (either custom typed or from preset dropdown)
    let targetRole = document.getElementById('target-role').value;
    const customRoleInput = document.getElementById('custom-role-input');
    if (isCustomRoleMode && customRoleInput && customRoleInput.value.trim()) {
        targetRole = customRoleInput.value.trim();
    } else if (targetRole === '__custom__' && customRoleInput && customRoleInput.value.trim()) {
        targetRole = customRoleInput.value.trim();
    } else if (targetRole === '__custom__') {
        targetRole = 'Senior Full Stack Developer';
    }

    const isCustomJd = document.getElementById('toggle-custom-jd').checked;
    const customJdText = isCustomJd ? document.getElementById('custom-jd-text').value.trim() : null;

    // Show loading state
    const loadingEl = document.getElementById('loading-state');
    const analyzeBtn = document.getElementById('analyze-btn');
    const stepText = document.getElementById('loading-step-text');

    if (loadingEl) loadingEl.classList.remove('hidden');
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.classList.add('opacity-50', 'cursor-not-allowed');
    }

    // Animated loading step messages
    const dict = I18N[currentLanguage] || I18N.en;
    const steps = dict.loading_steps;
    let stepIdx = 0;
    const stepInterval = setInterval(() => {
        stepIdx = (stepIdx + 1) % steps.length;
        if (stepText) stepText.textContent = steps[stepIdx];
    }, 500);

    try {
        const payload = {
            resume_text: resumeText,
            target_role: targetRole,
            custom_jd: customJdText,
            language: currentLanguage
        };

        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        clearInterval(stepInterval);

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Analysis failed. Please check inputs.');
        }

        const data = await res.json();
        currentAnalysisResult = data;

        // Auto-switch UI to Hindi if backend detected Hindi
        if (data.detected_language === 'hi' && currentLanguage !== 'hi') {
            currentLanguage = 'hi';
            applyTranslations('hi');
        }

        renderResultsDashboard(data);

        // Turn on "results ready" dot in nav
        const dot = document.getElementById('results-ready-dot');
        if (dot) dot.classList.remove('hidden');

        if (loadingEl) loadingEl.classList.add('hidden');

        // Smoothly transition directly to PAGE 2 (Results)
        switchPage('results');

    } catch (err) {
        clearInterval(stepInterval);
        if (loadingEl) loadingEl.classList.add('hidden');
        alert(`Analysis Error: ${err.message}`);
    } finally {
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    }
}

/**
 * Render complete results dashboard
 */
function renderResultsDashboard(data) {
    const isHi = (currentLanguage === 'hi');
    const profile = data.profile || {};
    const fit = data.fit_analysis || {};
    const salary = data.salary_prediction || {};
    const recs = data.recommendations || [];
    const altRoles = data.alternative_roles || [];

    // Show active container, hide empty state
    const emptyState = document.getElementById('results-empty-state');
    const activeContainer = document.getElementById('results-active-container');
    if (emptyState) emptyState.classList.add('hidden');
    if (activeContainer) activeContainer.classList.remove('hidden');

    // 1. Language Badge
    const langBadge = document.getElementById('res-lang-badge');
    if (langBadge) {
        if (data.detected_language === 'hi' || isHi) {
            langBadge.textContent = 'भाषा: हिंदी (Hindi Output)';
            langBadge.className = 'ml-2 px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-semibold';
        } else {
            langBadge.textContent = 'Language: English';
            langBadge.className = 'ml-2 px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-[10px] font-semibold';
        }
    }

    // 2. Summary Box
    const summaryTextEl = document.getElementById('res-summary-text');
    if (summaryTextEl) {
        summaryTextEl.textContent = isHi ? (fit.summary_hi || data.active_summary) : (fit.summary_en || data.active_summary);
    }

    // 3. Candidate Profile Header
    const defaultCandName = isHi ? 'उम्मीदवार प्रोफाइल' : 'Candidate Profile';
    const name = profile.candidate_name || defaultCandName;
    document.getElementById('res-candidate-name').textContent = name;
    document.getElementById('res-cand-name-title').textContent = name;

    const initials = name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase() || 'CP';
    document.getElementById('res-avatar').textContent = initials;

    const targetTitle = isHi && fit.target_role_hi ? fit.target_role_hi : fit.target_role;
    document.getElementById('res-candidate-target').textContent = `${isHi ? 'लक्षित पद:' : 'Target Job:'} ${targetTitle || 'Target Role'}`;
    
    const email = profile.contact_info?.email || (isHi ? 'ईमेल नहीं मिला' : 'Not detected');
    const phone = profile.contact_info?.phone || (isHi ? 'फोन नहीं मिला' : 'Not detected');
    document.getElementById('res-email').innerHTML = `<i class="fa-regular fa-envelope mr-1 text-slate-500"></i> ${email}`;
    document.getElementById('res-phone').innerHTML = `<i class="fa-solid fa-phone mr-1 text-slate-500"></i> ${phone}`;

    const expVal = profile.experience?.estimated_years || 0;
    document.getElementById('res-exp-years').textContent = isHi ? `${expVal} वर्ष` : `${expVal} Years`;
    
    const seniorityText = isHi ? (profile.experience?.seniority_level_hi || 'पेशेवर') : (profile.experience?.seniority_level || 'Professional');
    document.getElementById('res-seniority-level').textContent = seniorityText;
    
    const totalSkills = profile.skills?.skills_count || 0;
    document.getElementById('res-total-skills').textContent = isHi ? `${totalSkills} कौशल` : `${totalSkills} Skills`;

    // 4. Metrics & Gauge
    const score = fit.overall_match_score || 0;
    document.getElementById('res-gauge-score').textContent = `${score}%`;
    document.getElementById('res-tfidf-score').textContent = `${fit.tfidf_similarity || 0}%`;
    document.getElementById('res-skill-score').textContent = `${fit.skill_match_percentage || 0}%`;

    const tierBadge = document.getElementById('res-match-tier-badge');
    tierBadge.textContent = isHi ? (fit.match_tier_hi || fit.match_tier) : fit.match_tier;
    if (score >= 80) {
        tierBadge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
    } else if (score >= 65) {
        tierBadge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30';
    } else if (score >= 45) {
        tierBadge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30';
    } else {
        tierBadge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30';
    }

    renderMatchGaugeChart(score);

    // 5. Compensation (USD + INR)
    document.getElementById('res-salary-median').textContent = salary.formatted_median || '$145,000 / yr';
    document.getElementById('res-salary-range').textContent = `${isHi ? 'अनुमानित बैंड:' : 'Estimated Band:'} ${salary.formatted_range || '$115,000 - $185,000'}`;
    
    const inrEl = document.getElementById('res-salary-inr');
    if (inrEl) {
        const inrText = salary.formatted_inr || '₹12 - ₹28 लाख / वर्ष';
        inrEl.textContent = `${isHi ? 'भारतीय बाजार पैकेज:' : 'India Package:'} ~${inrText}`;
    }

    const percentile = salary.market_percentile || 50;
    document.getElementById('res-salary-percentile').textContent = `${percentile}th ${isHi ? 'पर्सेंटाइल' : 'Percentile'}`;
    document.getElementById('res-percentile-bar').style.width = `${percentile}%`;
    
    const expExpl = document.getElementById('res-salary-explanation');
    if (expExpl) {
        expExpl.textContent = isHi ? (salary.explanation_hi || '') : (salary.explanation_en || '');
    }

    // 6. Competency Radar Chart
    renderCompetencyRadar(profile.skills?.categorized || {});

    // 7. Skill Gap Matrix Badges
    const matchedContainer = document.getElementById('res-matched-tags');
    const missingContainer = document.getElementById('res-missing-tags');
    const extraContainer = document.getElementById('res-extra-tags');

    matchedContainer.innerHTML = '';
    missingContainer.innerHTML = '';
    extraContainer.innerHTML = '';

    const matchedList = fit.matched_skills || [];
    const missingList = fit.missing_skills || [];
    const extraList = fit.extra_skills || [];

    document.getElementById('res-matched-count').textContent = isHi ? `${matchedList.length} मौजूद हैं` : `${matchedList.length} Matched`;
    document.getElementById('res-missing-count').textContent = isHi ? `${missingList.length} सीखने हैं` : `${missingList.length} Missing`;

    if (matchedList.length > 0) {
        matchedList.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'badge-matched px-3 py-1 rounded-lg text-xs font-medium flex items-center space-x-1.5';
            span.innerHTML = `<i class="fa-solid fa-check text-[10px]"></i><span>${skill}</span>`;
            matchedContainer.appendChild(span);
        });
    } else {
        matchedContainer.innerHTML = `<span class="text-xs text-slate-500 italic">${isHi ? 'अभी तक कोई मुख्य कौशल मेल नहीं खाया' : 'No primary skills matched yet'}</span>`;
    }

    if (missingList.length > 0) {
        missingList.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'badge-missing px-3 py-1 rounded-lg text-xs font-medium flex items-center space-x-1.5';
            span.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-[10px]"></i><span>${skill}</span>`;
            missingContainer.appendChild(span);
        });
    } else {
        missingContainer.innerHTML = `<span class="text-xs text-emerald-400 italic">${isHi ? 'शानदार! कोई भी जरूरी कौशल छूटा नहीं है।' : 'No critical skill gaps identified! Complete match.'}</span>`;
    }

    if (extraList.length > 0) {
        extraList.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'badge-extra px-2.5 py-1 rounded-lg text-xs font-medium flex items-center space-x-1';
            span.innerHTML = `<i class="fa-regular fa-star text-[10px]"></i><span>${skill}</span>`;
            extraContainer.appendChild(span);
        });
    } else {
        extraContainer.innerHTML = `<span class="text-xs text-slate-500 italic">${isHi ? 'कोई अतिरिक्त कौशल नहीं मिला' : 'No additional extra skills detected.'}</span>`;
    }

    // 8. Automated Learning Recommendations Grid (with Hindi support)
    const recGrid = document.getElementById('res-recommendations-grid');
    recGrid.innerHTML = '';

    if (recs.length > 0) {
        recs.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'p-5 rounded-xl bg-slate-900/60 border border-white/10 flex flex-col justify-between hover:border-cyan-500/40 transition-all';
            
            const title = isHi && rec.title_hi ? rec.title_hi : rec.title;
            const duration = isHi && rec.duration_hi ? rec.duration_hi : rec.duration;
            const project = isHi && rec.capstone_project_hi ? rec.capstone_project_hi : rec.capstone_project;
            const btnText = isHi ? 'फ्री ट्यूटोरियल देखें' : 'Explore Free Resource';

            card.innerHTML = `
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                            ${rec.skill}
                        </span>
                        <span class="text-[11px] text-slate-400"><i class="fa-regular fa-clock mr-1"></i>${duration}</span>
                    </div>
                    <h5 class="text-sm font-bold text-white leading-snug">${title}</h5>
                    <p class="text-xs text-slate-400"><i class="fa-solid fa-chalkboard-user mr-1 text-indigo-400"></i> ${rec.provider}</p>
                    <div class="p-3 rounded-lg bg-slate-950/50 border border-white/5 text-xs text-slate-300">
                        <span class="text-[10px] uppercase font-bold text-indigo-400 tracking-wider block mb-1">
                            ${isHi ? 'प्रैक्टिस प्रोजेक्ट सुझाव:' : 'Recommended Practice Project:'}
                        </span>
                        ${project}
                    </div>
                </div>
                <div class="pt-4 mt-3 border-t border-white/5">
                    <a href="${rec.url}" target="_blank" class="w-full inline-flex items-center justify-center space-x-2 py-2 px-3 rounded-lg bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/30 text-indigo-200 text-xs font-semibold transition-all">
                        <span>${btnText}</span>
                        <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                </div>
            `;
            recGrid.appendChild(card);
        });
    } else {
        recGrid.innerHTML = `
            <div class="col-span-3 p-6 text-center text-slate-400 text-sm">
                <i class="fa-solid fa-circle-check text-emerald-400 text-2xl mb-2 block"></i>
                ${isHi ? 'बधाई हो! आपके पास इस नौकरी के लिए सभी आवश्यक कौशल पहले से हैं।' : 'Congratulations! You possess all primary requirements for this position.'}
            </div>
        `;
    }

    // 9. Alternative Career Roles Grid
    const altGrid = document.getElementById('res-alternative-roles-grid');
    altGrid.innerHTML = '';
    
    if (altRoles.length > 0) {
        altRoles.slice(0, 6).forEach(role => {
            const roleTitle = isHi && role.role_title_hi ? role.role_title_hi : role.role_title;
            const roleCat = isHi && role.category_hi ? role.category_hi : role.category;
            const seniorityFit = isHi && role.seniority_fit_hi ? role.seniority_fit_hi : role.seniority_fit;

            const card = document.createElement('div');
            card.className = 'p-4 rounded-xl bg-slate-900/50 border border-white/10 flex flex-col justify-between space-y-3';
            card.innerHTML = `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[10px] uppercase font-semibold text-slate-400">${roleCat}</span>
                        <span class="text-xs font-bold text-cyan-400">${role.match_percentage}% ${isHi ? 'मैच' : 'Match'}</span>
                    </div>
                    <h5 class="text-sm font-bold text-white">${roleTitle}</h5>
                    <div class="w-full bg-slate-800 rounded-full h-1.5 mt-2 overflow-hidden">
                        <div class="h-full bg-gradient-to-r from-indigo-500 to-cyan-400" style="width: ${role.match_percentage}%;"></div>
                    </div>
                </div>
                <div class="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-white/5">
                    <span>${seniorityFit}</span>
                    <span class="text-emerald-400 font-semibold">$${Math.round(role.salary_range.median / 1000)}k / yr</span>
                </div>
            `;
            altGrid.appendChild(card);
        });
    }
}

/**
 * Render Chart.js Semi-Doughnut Match Score Gauge
 */
function renderMatchGaugeChart(score) {
    const ctx = document.getElementById('matchGaugeCanvas');
    if (!ctx) return;

    if (matchGaugeChart) {
        matchGaugeChart.destroy();
    }

    let fillColor = '#10B981'; // Emerald
    if (score < 45) fillColor = '#F43F5E'; // Rose
    else if (score < 65) fillColor = '#F59E0B'; // Amber
    else if (score < 80) fillColor = '#3B82F6'; // Blue

    matchGaugeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [fillColor, 'rgba(255, 255, 255, 0.05)'],
                borderWidth: 0,
                circumference: 240,
                rotation: 240
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '78%',
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false }
            },
            animation: {
                animateRotate: true,
                duration: 1000
            }
        }
    });
}

/**
 * Render Multi-Dimensional Competency Radar Chart
 */
function renderCompetencyRadar(categorizedSkills) {
    const ctx = document.getElementById('competencyRadarCanvas');
    if (!ctx) return;

    if (competencyRadarChart) {
        competencyRadarChart.destroy();
    }

    const categories = [
        'Programming Languages',
        'Frontend Development',
        'Backend & APIs',
        'AI, ML & Data Science',
        'Cloud & DevOps',
        'Databases & Storage'
    ];

    const isHi = (currentLanguage === 'hi');
    const shortLabels = isHi 
        ? ['प्रोग्रामिंग', 'फ्रंटएंड', 'बैकएंड', 'एआई/डेटा', 'क्लाउड', 'डेटाबेस']
        : ['Languages', 'Frontend', 'Backend', 'AI & ML', 'Cloud/DevOps', 'Databases'];

    const counts = categories.map(cat => (categorizedSkills[cat] || []).length);
    const values = counts.map(c => Math.min(100, Math.max(15, c * 25)));

    competencyRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: shortLabels,
            datasets: [{
                label: isHi ? 'कौशल स्तर' : 'Candidate Competency',
                data: values,
                backgroundColor: 'rgba(99, 102, 241, 0.25)',
                borderColor: '#6366F1',
                pointBackgroundColor: '#06B6D4',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#06B6D4',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
                    grid: { color: 'rgba(255, 255, 255, 0.08)' },
                    pointLabels: {
                        color: '#94A3B8',
                        font: { size: 10, family: 'Inter' }
                    },
                    ticks: { display: false, maxTicksLimit: 4 },
                    min: 0,
                    max: 100
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

/**
 * Export Assessment Report as PDF
 */
async function exportPdfReport() {
    if (!currentAnalysisResult) {
        alert(currentLanguage === 'hi' ? 'कृपया पहले रिज्यूमे का विश्लेषण करें।' : 'Please run an analysis first before exporting the report.');
        return;
    }

    try {
        const response = await fetch('/api/export-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentAnalysisResult)
        });

        if (response.ok) {
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            const candidateName = currentAnalysisResult.profile?.candidate_name || 'Candidate';
            const safeName = candidateName.replace(/[^a-zA-Z0-9\u0900-\u097F]/g, '_');
            a.href = downloadUrl;
            a.download = `Career_Report_${safeName}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(downloadUrl);
            return;
        }
    } catch (serverErr) {
        console.warn('Server PDF generation failed, falling back to client-side html2pdf', serverErr);
    }

    // Strategy 2: Client-side html2pdf fallback
    const reportElement = document.getElementById('report-printable-area');
    if (!reportElement || typeof html2pdf === 'undefined') {
        window.print();
        return;
    }

    const opt = {
        margin: [10, 10, 10, 10],
        filename: 'Career_Assessment_Report.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, backgroundColor: '#080C15' },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(reportElement).save();
}
