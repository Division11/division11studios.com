#!/usr/bin/env python3
"""Generates the division11studios.com static site into ./_site.

Run `python3 build.py` (no dependencies). GitHub Actions runs this on every
push to main and deploys _site to GitHub Pages.

Languages
---------
Every piece of visible text lives in the `T` (site strings) and `APPS`
(per-app text) tables below, keyed by language code. To add a language:
  1. add it to LANGS (code, URL prefix, text direction, name in that language)
  2. add a block for it in T and in each app's "text"
Any string missing for a language falls back to English, so a language can be
added incrementally. English is served at /, every other language at /<code>/.
"""
import os, re, shutil, json, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")
SITE = "https://www.division11studios.com"
UPDATED = "29 October 2026"
CSS_VER = hashlib.sha1(open(os.path.join(ROOT, "site.css"), "rb").read()).hexdigest()[:10]

LANGS = [
    {"code": "en", "prefix": "",    "dir": "ltr", "name": "English", "short": "EN"},
    {"code": "ar", "prefix": "/ar", "dir": "rtl", "name": "العربية", "short": "ع"},
]
DEFAULT = "en"

CO = {
    "phone": "+965 9008 5898",
    "phone_href": "+96590085898",
    "support": "support@division11studios.com",
    "dev": "dev@division11studios.com",
    "instagram": "https://www.instagram.com/division11studios/",
    "tiktok": "https://www.tiktok.com/@division11studios",
}

# ---------------------------------------------------------------- site strings
T = {
"en": {
    "brand": "Division 11 Studios",
    "legal": "Division Eleven Studios – Custom Software Design and Development",
    "legal_note": "“Division 11 Studios” is the trading name of Division Eleven Studios S.P.C.",
    "addr": ["Building 9, Street 133", "Block 1, Al Nahda", "Kuwait City, Kuwait"],
    "nav_home": "Home", "nav_apps": "Apps", "nav_about": "About", "nav_support": "Support",
    "skip": "Skip to content", "menu": "Menu", "language": "Language",
    "theme": "Switch theme (system, light, dark)",
    "tagline_footer": "Mobile apps and games, designed and built in Kuwait.",
    "f_company": "Company", "f_address": "Address", "f_contact": "Contact",
    "privacy": "Privacy", "terms": "Terms",
    "rights": "All rights reserved.",
    "ios_small": "Download on the", "ios_big": "App Store",
    "gp_small": "Get it on", "gp_big": "Google Play",
    "arrow": "→",
    # home
    "home_title": "Division 11 Studios — Mobile apps & games from Kuwait",
    "home_desc": "Division 11 Studios is an independent mobile app and game studio in Kuwait, makers of Scorey and ArtNest.",
    "hero_eyebrow": "Independent app studio · Kuwait",
    "hero_h1": "We design and build mobile apps and games people actually use.",
    "hero_lead": "Division 11 Studios designs, develops and publishes apps and games — from everyday utilities to creative tools for families — and builds custom software and websites for clients.",
    "cta_apps": "See our apps", "cta_about": "About the studio",
    "apps_eyebrow": "Published apps", "apps_h2": "Available to download now",
    "what_eyebrow": "What we do", "what_h2": "Software design and development",
    "what": [
        ("Apps", "Apps for phones, tablets and beyond, from first prototype to release, updates and support."),
        ("Games & interactive", "Casual and creative games, with attention to performance, accessibility and family-safe design."),
        ("Websites & maintenance", "Website design, development and ongoing software maintenance for businesses in Kuwait and the region."),
    ],
    "contact_eyebrow": "Get in touch", "contact_h2": "Have a question or a project in mind?",
    "contact_p": "Write to us about our apps, partnerships or custom software work. We usually reply within two business days.",
    "contact_link": "Support & contact",
    "office": "Office",
    # apps
    "apps_title": "Apps", "apps_desc": "Apps and games published by Division 11 Studios.",
    "apps_head_eyebrow": "Our apps", "apps_head_h1": "Apps by Division 11 Studios",
    "apps_head_lead": "Every app and game we publish.",
    "rated": "Rated", "details": "Details", "privacy_policy": "Privacy policy", "support": "Support",
    "more_coming": "More titles are in development, including a multiplayer trivia game.",
    "features": "Features", "f_platforms": "Platforms", "f_price": "Price", "f_age": "Age rating", "f_dev": "Developer",
    "terms_of_use": "Terms of use", "get_support": "Get support", "policy_suffix": "privacy policy",
    # about
    "about_title": "About", "about_desc": "About Division 11 Studios, an independent software studio in Kuwait City.",
    "about_eyebrow": "About", "about_h1": "About Division 11 Studios",
    "about_lead": "Division 11 Studios is an independent software studio based in Kuwait City. We design, build and publish apps and games, and we develop custom software and websites for clients.",
    "about_p": "The studio was founded in 2026. We pick the tools and platforms that fit each project, and publish wherever our users are. Our first titles are {scorey}, a scorekeeper for traditional and modern card games, and {artnest}, a creative coloring and drawing app for the whole family.",
    "values_h2": "What we care about",
    "values": [
        ("Fast and reliable", "Apps that open quickly, work offline where they can and stay out of your way."),
        ("Private by default", "No accounts required. Game history and artwork stay on your device."),
        ("Made for many languages", "Our apps and this site are built to support multiple languages, starting with English and Arabic."),
    ],
    # support
    "support_title": "Support", "support_desc": "Support and contact for Division 11 Studios apps.",
    "support_eyebrow": "Support", "support_h1": "How can we help?", "support_lead": "We usually reply within two business days.",
    "contact_support": "Contact support",
    "support_p1": "Email {email} and include the app name, your device model and what happened. Screenshots help.",
    "support_p2": "For business enquiries, partnerships or client projects, write to {dev} or call {phone}.",
    "faq_h2": "Common questions",
    "faq": [
        ("I bought “Remove Ads” but still see ads.", "Open the app’s settings and tap Restore purchases while signed in with the same Apple ID or Google account you used to buy it. If that doesn’t work, email us with your order receipt."),
        ("How do I get a refund?", "Purchases are processed by Apple or Google. Request a refund at <a href='https://reportaproblem.apple.com'>reportaproblem.apple.com</a> (App Store) or through your Google Play order history."),
        ("Where is my data stored? Can I delete it?", "Scorey game history and ArtNest artwork are stored only on your device. Delete them in the app, clear the app’s data, or uninstall the app. See each app’s privacy policy for details."),
        ("Is ArtNest safe for children?", "ArtNest needs no account and places external links behind a parental gate."),
    ],
    "app_resources": "App resources", "about_app": "About the app",
    # terms
    "terms_title": "Terms of Use", "terms_desc": "Terms of use for Division 11 Studios apps and website.",
    "legal_eyebrow": "Legal", "last_updated": "Last updated: " + UPDATED,
    "terms_intro": "These terms apply to the apps published by Division 11 Studios (“we”, “us”) and to this website. By downloading or using our apps you agree to them.",
    "terms_body": [
        ("1. Licence", "We grant you a personal, non-exclusive, non-transferable licence to use our apps on devices you own or control, subject to these terms and to the Apple Media Services Terms or Google Play Terms of Service, as applicable. Apps downloaded from the App Store are also licensed under Apple’s Standard Licensed Application End User License Agreement."),
        ("2. Purchases", "In-app purchases are sold and processed by Apple or Google. Prices, payment, refunds and restoration of purchases are handled under the store’s terms."),
        ("3. Acceptable use", "You may not copy, modify, reverse-engineer, redistribute or tamper with our apps, bypass their security or advertising systems, or use them for any unlawful purpose."),
        ("4. Advertising", "Some apps show advertisements provided by third-party networks. Their handling of data is described in each app’s privacy policy."),
        ("5. Privacy", "How we handle information is described in each app’s privacy policy and in our website privacy notice."),
        ("6. Intellectual property", "The apps, their content, names and logos are owned by Division 11 Studios or its licensors and are protected by law."),
        ("7. Disclaimer and liability", "Our apps are provided “as is”. Scores, results and content are for entertainment and convenience. To the extent permitted by law, we are not liable for indirect or consequential loss arising from use of the apps."),
        ("8. Changes", "We may update these terms. The current version is always published on this page."),
        ("9. Governing law", "These terms are governed by the laws of the State of Kuwait."),
        ("10. Contact", "Questions about these terms: {email}."),
    ],
    "translation_note": "",
    # privacy
    "privacy_title": "Privacy", "privacy_desc": "Privacy information for Division 11 Studios apps and website.",
    "privacy_apps_h2": "App privacy policies",
    "privacy_site_h2": "This website",
    "privacy_site_p": "This website doesn’t use cookies or analytics and doesn’t collect personal information.",
    "privacy_email_p": "If you email us, we use your message and address only to reply.",
    "privacy_contact_h2": "Contact",
    # 404
    "policy_en_only": "",
    "nf_title": "Page not found", "nf_lead": "The page you’re looking for doesn’t exist.", "nf_home": "Go to the home page",
},
"ar": {
    "brand": "ديفيجن 11 ستوديوز",
    "legal": "شركة ديفيجن إيليفن ستوديوز لتصميم وبرمجة البرمجيات الخاصة ش.ش.و.",
    "legal_note": "«ديفيجن 11 ستوديوز» هو الاسم التجاري لشركة ديفيجن إيليفن ستوديوز ش.ش.و.",
    "addr": ["مبنى 9، شارع 133", "قطعة 1، النهضة", "مدينة الكويت، الكويت"],
    "nav_home": "الرئيسية", "nav_apps": "التطبيقات", "nav_about": "من نحن", "nav_support": "الدعم",
    "skip": "انتقل إلى المحتوى", "menu": "القائمة", "language": "اللغة",
    "theme": "تبديل المظهر (النظام، فاتح، داكن)",
    "tagline_footer": "تطبيقات وألعاب للأجهزة المحمولة، صُممت وطُوّرت في الكويت.",
    "f_company": "الشركة", "f_address": "العنوان", "f_contact": "التواصل",
    "privacy": "الخصوصية", "terms": "الشروط",
    "rights": "جميع الحقوق محفوظة.",
    "arrow": "←",
    # home
    "home_title": "ديفيجن 11 ستوديوز — تطبيقات وألعاب من الكويت",
    "home_desc": "ديفيجن 11 ستوديوز استوديو مستقل لتطوير تطبيقات وألعاب الأجهزة المحمولة في الكويت، ومطوّر تطبيقي Scorey وArtNest.",
    "hero_eyebrow": "استوديو تطبيقات مستقل · الكويت",
    "hero_h1": "نصمم ونطوّر تطبيقات وألعاب يستخدمها الناس فعلاً.",
    "hero_lead": "يصمم استوديو ديفيجن 11 ويطوّر وينشر تطبيقات وألعاباً — من أدوات الاستخدام اليومي إلى تطبيقات إبداعية للعائلة — كما ينفّذ برمجيات ومواقع إلكترونية حسب الطلب للعملاء.",
    "cta_apps": "تطبيقاتنا", "cta_about": "عن الاستوديو",
    "apps_eyebrow": "تطبيقات منشورة", "apps_h2": "متوفرة للتنزيل الآن",
    "what_eyebrow": "ماذا نقدّم", "what_h2": "تصميم البرمجيات وتطويرها",
    "what": [
        ("التطبيقات", "تطبيقات للهواتف والأجهزة اللوحية وغيرها، من النموذج الأولي حتى الإطلاق والتحديثات والدعم."),
        ("ألعاب وتجارب تفاعلية", "ألعاب خفيفة وإبداعية، مع اهتمام بالأداء وسهولة الاستخدام وملاءمتها للعائلة."),
        ("المواقع الإلكترونية والصيانة", "تصميم المواقع وتطويرها وصيانة البرمجيات بشكل مستمر للشركات في الكويت والمنطقة."),
    ],
    "contact_eyebrow": "تواصل معنا", "contact_h2": "لديك سؤال أو مشروع؟",
    "contact_p": "راسلنا بخصوص تطبيقاتنا أو الشراكات أو مشاريع البرمجيات الخاصة. نرد عادةً خلال يومي عمل.",
    "contact_link": "الدعم والتواصل",
    "office": "المكتب",
    # apps
    "apps_title": "التطبيقات", "apps_desc": "التطبيقات والألعاب التي تنشرها ديفيجن 11 ستوديوز.",
    "apps_head_eyebrow": "تطبيقاتنا", "apps_head_h1": "تطبيقات ديفيجن 11 ستوديوز",
    "apps_head_lead": "كل التطبيقات والألعاب التي ننشرها.",
    "rated": "التصنيف العمري", "details": "التفاصيل", "privacy_policy": "سياسة الخصوصية", "support": "الدعم",
    "more_coming": "المزيد من التطبيقات قيد التطوير، منها لعبة أسئلة جماعية.",
    "features": "المزايا", "f_platforms": "المنصات", "f_price": "السعر", "f_age": "التصنيف العمري", "f_dev": "المطوّر",
    "terms_of_use": "شروط الاستخدام", "get_support": "الدعم", "policy_suffix": "— سياسة الخصوصية",
    # about
    "about_title": "من نحن", "about_desc": "تعرّف على ديفيجن 11 ستوديوز، استوديو برمجيات مستقل في مدينة الكويت.",
    "about_eyebrow": "من نحن", "about_h1": "عن ديفيجن 11 ستوديوز",
    "about_lead": "ديفيجن 11 ستوديوز استوديو برمجيات مستقل مقره مدينة الكويت. نصمم ونطوّر وننشر تطبيقات وألعاباً، ونطوّر برمجيات ومواقع إلكترونية حسب الطلب للعملاء.",
    "about_p": "تأسس الاستوديو عام 2026. نختار الأدوات والمنصات التي تناسب كل مشروع، وننشر حيثما يتواجد مستخدمونا. أول إصداراتنا {scorey}، تطبيق لتسجيل نتائج ألعاب الورق التقليدية والحديثة، و{artnest}، تطبيق إبداعي للتلوين والرسم لكل أفراد العائلة.",
    "values_h2": "ما يهمّنا",
    "values": [
        ("سرعة وموثوقية", "تطبيقات تفتح بسرعة، وتعمل دون اتصال حيثما أمكن، ولا تعيقك."),
        ("الخصوصية أولاً", "لا حاجة لإنشاء حساب. سجل الألعاب والرسومات تبقى على جهازك."),
        ("لغات متعددة", "تطبيقاتنا وهذا الموقع مصممة لدعم لغات متعددة، بدءاً بالعربية والإنجليزية."),
    ],
    # support
    "support_title": "الدعم", "support_desc": "الدعم والتواصل لتطبيقات ديفيجن 11 ستوديوز.",
    "support_eyebrow": "الدعم", "support_h1": "كيف يمكننا مساعدتك؟", "support_lead": "نرد عادةً خلال يومي عمل.",
    "contact_support": "تواصل مع الدعم",
    "support_p1": "راسلنا على {email} مع ذكر اسم التطبيق وطراز جهازك ووصف المشكلة. لقطات الشاشة تساعدنا كثيراً.",
    "support_p2": "للاستفسارات التجارية والشراكات ومشاريع العملاء، راسلنا على {dev} أو اتصل على {phone}.",
    "faq_h2": "أسئلة شائعة",
    "faq": [
        ("اشتريت «إزالة الإعلانات» وما زالت الإعلانات تظهر.", "افتح إعدادات التطبيق واضغط «استعادة المشتريات» وأنت مسجّل بنفس حساب Apple أو Google الذي استخدمته للشراء. إذا لم ينجح ذلك، راسلنا مع إيصال الشراء."),
        ("كيف أسترد المبلغ؟", "تتم عمليات الشراء عبر Apple أو Google. اطلب الاسترداد من <a href='https://reportaproblem.apple.com'>reportaproblem.apple.com</a> (لمتجر App Store) أو من سجل الطلبات في Google Play."),
        ("أين تُحفظ بياناتي؟ وهل يمكنني حذفها؟", "يُحفظ سجل ألعاب Scorey ورسومات ArtNest على جهازك فقط. يمكنك حذفها من داخل التطبيق أو بمسح بيانات التطبيق أو بحذفه. راجع سياسة الخصوصية لكل تطبيق للتفاصيل."),
        ("هل تطبيق ArtNest آمن للأطفال؟", "لا يحتاج ArtNest إلى حساب، والروابط الخارجية فيه محمية ببوابة أبوية."),
    ],
    "app_resources": "روابط التطبيقات", "about_app": "عن التطبيق",
    # terms
    "terms_title": "شروط الاستخدام", "terms_desc": "شروط استخدام تطبيقات وموقع ديفيجن 11 ستوديوز.",
    "legal_eyebrow": "قانوني", "last_updated": "آخر تحديث: 29 أكتوبر 2026",
    "terms_intro": "تسري هذه الشروط على التطبيقات التي تنشرها ديفيجن 11 ستوديوز («نحن») وعلى هذا الموقع. بتنزيلك تطبيقاتنا أو استخدامها فإنك توافق عليها.",
    "terms_body": [
        ("1. الترخيص", "نمنحك ترخيصاً شخصياً وغير حصري وغير قابل للتحويل لاستخدام تطبيقاتنا على الأجهزة التي تملكها أو تتحكم بها، وفقاً لهذه الشروط ولشروط خدمات Apple أو شروط خدمة Google Play بحسب الحال. كما تخضع التطبيقات المنزّلة من App Store لاتفاقية ترخيص المستخدم النهائي القياسية من Apple."),
        ("2. المشتريات", "تُباع المشتريات داخل التطبيق وتُعالج عبر Apple أو Google، وتخضع الأسعار والدفع والاسترداد واستعادة المشتريات لشروط المتجر."),
        ("3. الاستخدام المقبول", "لا يجوز نسخ تطبيقاتنا أو تعديلها أو الهندسة العكسية لها أو إعادة توزيعها أو العبث بها أو تجاوز أنظمة الأمان أو الإعلانات فيها أو استخدامها لأي غرض غير مشروع."),
        ("4. الإعلانات", "تعرض بعض التطبيقات إعلانات تقدمها شبكات خارجية، وتوضح سياسة الخصوصية لكل تطبيق كيفية تعاملها مع البيانات."),
        ("5. الخصوصية", "توضح سياسة الخصوصية لكل تطبيق، وإشعار الخصوصية الخاص بالموقع، كيفية تعاملنا مع المعلومات."),
        ("6. الملكية الفكرية", "التطبيقات ومحتواها وأسماؤها وشعاراتها مملوكة لديفيجن 11 ستوديوز أو للجهات المرخِّصة لها ومحمية بموجب القانون."),
        ("7. إخلاء المسؤولية", "تُقدَّم تطبيقاتنا «كما هي». النتائج والمحتوى للترفيه والتيسير فقط. وفي الحدود التي يسمح بها القانون، لا نتحمل المسؤولية عن أي خسارة غير مباشرة أو تبعية ناتجة عن استخدام التطبيقات."),
        ("8. التعديلات", "قد نحدّث هذه الشروط، وتُنشر النسخة السارية دائماً في هذه الصفحة."),
        ("9. القانون الواجب التطبيق", "تخضع هذه الشروط لقوانين دولة الكويت."),
        ("10. التواصل", "للاستفسار عن هذه الشروط: {email}."),
    ],
    "translation_note": "في حال وجود أي اختلاف بين النسختين العربية والإنجليزية من هذه الشروط، تُعتمد النسخة الإنجليزية.",
    # privacy
    "privacy_title": "الخصوصية", "privacy_desc": "معلومات الخصوصية لتطبيقات وموقع ديفيجن 11 ستوديوز.",
    "privacy_apps_h2": "سياسات خصوصية التطبيقات",
    "privacy_site_h2": "هذا الموقع",
    "privacy_site_p": "لا يستخدم هذا الموقع ملفات تعريف الارتباط أو أدوات التحليل، ولا يجمع أي معلومات شخصية.",
    "privacy_email_p": "إذا راسلتنا عبر البريد الإلكتروني، نستخدم رسالتك وعنوانك للرد عليك فقط.",
    "privacy_contact_h2": "التواصل",
    # 404
    "policy_en_only": "سياسة الخصوصية هذه متوفرة حالياً باللغة الإنجليزية فقط.",
    "nf_title": "الصفحة غير موجودة", "nf_lead": "الصفحة التي تبحث عنها غير موجودة.", "nf_home": "العودة إلى الرئيسية",
},
}

T["en"].update({
    "story_h2": "Our story",
    "stats": [("2", "Published apps"), ("Multi-platform", "Built for many devices"), ("EN · AR", "Languages, more coming"), ("2026", "Founded in Kuwait")],
    "contact_cards": [
        ("App support", "Questions or problems with Scorey or ArtNest. Include your device model and what happened."),
        ("Business enquiries", "Partnerships, client projects and custom software or website work."),
        ("Call us", "Prefer to talk? Call our office in Kuwait City."),
    ],
})
T["ar"].update({
    "story_h2": "قصتنا",
    "stats": [("2", "تطبيقات منشورة"), ("متعدد المنصات", "لأجهزة متعددة"), ("EN · AR", "اللغات، والمزيد قادم"), ("2026", "تأسس في الكويت")],
    "contact_cards": [
        ("دعم التطبيقات", "أسئلة أو مشاكل في Scorey أو ArtNest. اذكر طراز جهازك وما حدث."),
        ("الاستفسارات التجارية", "الشراكات ومشاريع العملاء وتطوير البرمجيات والمواقع حسب الطلب."),
        ("اتصل بنا", "تفضّل التحدث معنا؟ اتصل بمكتبنا في مدينة الكويت."),
    ],
})

# --------------------------------------------------------------------- apps
APPS = [
    {
        "slug": "scorey", "name": "Scorey", "icon": "scorey.png",
        "accent": "#FFBF00", "bg": "#1C3156",
        "ios": "https://apps.apple.com/app/scorey/id6761244968",
        "android": "https://play.google.com/store/apps/details?id=com.division11.scorey",
        "age": "13+",
        "text": {
            "en": {
                "tagline": "Digital card game scorecard", "category": "Utilities",
                "platforms": "iPhone, iPad and Android",
                "pricing": "Free with ads · optional one-time “Remove Ads” purchase",
                "summary": "Scorey replaces pen and paper at the card table. Enter each round and it keeps the running totals, the history and the winner — fast, accurate and anonymous.",
                "features": [
                    ("Instant calculation", "Enter points per round; Scorey handles the totals and shows a live preview of the running score."),
                    ("Many games built in", "Kout, Trix, Hand, Balot, Tarneeb, Sbeeta, Nthala, Domino, Rummy, Cribbage, Skyjo, Uno and a general scoresheet."),
                    ("Spectator mode", "Share a QR code so anyone on the same Wi-Fi can follow the scores live."),
                    ("Game history & sharing", "Every finished game is saved on the device and can be shared as a visual scorecard."),
                    ("Built-in rules", "Help guides with pictures explain each game’s rules and scoring."),
                    ("English & Arabic", "Full bilingual interface, including Arabic-Indic numerals."),
                ],
            },
            "ar": {
                "tagline": "سجل نتائج رقمي لألعاب الورق", "category": "أدوات",
                "platforms": "iPhone وiPad وAndroid",
                "pricing": "مجاني مع إعلانات · شراء اختياري لمرة واحدة «إزالة الإعلانات»",
                "summary": "يغنيك Scorey عن الورقة والقلم على طاولة اللعب. أدخل نتيجة كل جولة ويتولى هو حساب المجموع والسجل والفائز — بسرعة ودقة ودون الحاجة لحساب.",
                "features": [
                    ("حساب فوري", "أدخل نقاط كل جولة ويحسب Scorey المجموع مع معاينة مباشرة للنتيجة."),
                    ("ألعاب كثيرة مدمجة", "كوت، تركس، هند، بلوت، طرنيب، سبيتة، نذالة، دومينو، رومي، كريبج، سكاي جو، أونو، وورقة نتائج عامة."),
                    ("وضع المتفرج", "شارك رمز QR ليتابع أي شخص على نفس شبكة Wi-Fi النتائج مباشرة."),
                    ("سجل الألعاب والمشاركة", "تُحفظ كل لعبة منتهية على جهازك ويمكن مشاركتها كبطاقة نتائج مصوّرة."),
                    ("شرح القوانين", "أدلة مصوّرة تشرح قوانين كل لعبة وطريقة احتساب نقاطها."),
                    ("العربية والإنجليزية", "واجهة ثنائية اللغة بالكامل، مع دعم الأرقام العربية."),
                ],
            },
        },
    },
    {
        "slug": "artnest", "name": "ArtNest", "icon": "artnest.png",
        "accent": "#FFC86B", "bg": "#2A1B5C",
        "ios": "https://apps.apple.com/app/artnest-color-and-fun/id6761441675",
        "android": "https://play.google.com/store/apps/details?id=com.division11.artnest",
        "age": "4+",
        "text": {
            "en": {
                "tagline": "Color, draw & imagine", "category": "Education",
                "platforms": "iPhone, iPad and Android",
                "pricing": "Free · optional “Remove Ads” purchase",
                "summary": "ArtNest is a family-friendly creative studio with five ways to make art — from classic coloring pages to glowing neon drawings — in a safe, simple interface.",
                "features": [
                    ("Coloring book", "A large library of outlines across many themes to build motor skills and color recognition."),
                    ("Color by number", "Follow the guide to reveal finished artworks — relaxing and educational."),
                    ("Pixel coloring", "Grid-based pixel art with hints and progress tracking."),
                    ("Glow drawing", "A neon canvas where every stroke lights up."),
                    ("Free drawing", "Brushes, glitter pens, magic markers and a big sticker collection."),
                    ("Gallery & parental gate", "Artwork saves to an in-app gallery or the device; external links sit behind a parental gate."),
                ],
            },
            "ar": {
                "tagline": "لوّن وارسم وتخيّل", "category": "تعليم",
                "platforms": "iPhone وiPad وAndroid",
                "pricing": "مجاني · شراء اختياري «إزالة الإعلانات»",
                "summary": "ArtNest مرسم إبداعي مناسب للعائلة يقدّم خمس طرق لصنع الفن — من صفحات التلوين الكلاسيكية إلى الرسم المضيء — بواجهة بسيطة وآمنة.",
                "features": [
                    ("كتاب التلوين", "مكتبة كبيرة من الرسومات بمواضيع متعددة تنمّي المهارات الحركية والتعرف على الألوان."),
                    ("التلوين بالأرقام", "اتبع الأرقام لتكشف لوحات مكتملة — بطريقة ممتعة وتعليمية."),
                    ("تلوين البكسل", "فن البكسل على شبكة مربعات مع تلميحات وتتبع للتقدم."),
                    ("الرسم المضيء", "لوحة نيون تضيء فيها كل ضربة فرشاة."),
                    ("الرسم الحر", "فُرش وأقلام لامعة وأقلام سحرية ومجموعة كبيرة من الملصقات."),
                    ("المعرض والبوابة الأبوية", "تُحفظ الرسومات في معرض داخل التطبيق أو على الجهاز، والروابط الخارجية محمية ببوابة أبوية."),
                ],
            },
        },
    },
]

# ------------------------------------------------------------------ helpers
def t(lang, key):
    return T.get(lang, {}).get(key, T[DEFAULT][key])

def at(app, lang, key):
    return app["text"].get(lang, {}).get(key, app["text"][DEFAULT][key])

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def prefix(lang):
    return next(l["prefix"] for l in LANGS if l["code"] == lang)

def L(lang, path):
    return prefix(lang) + path

def ltr(s):
    return f'<bdi class="ltr">{s}</bdi>'

def mail(addr):
    return f'<a href="mailto:{addr}">{ltr(addr)}</a>'

def tel():
    return f'<a href="tel:{CO["phone_href"]}">{ltr(CO["phone"])}</a>'

def icon_html(app, size="lg"):
    if os.path.exists(os.path.join(ROOT, "brand", "apps", app["icon"])):
        return f'<img class="appicon {size}" src="/assets/apps/{app["icon"]}" alt="" width="120" height="120" loading="lazy">'
    return f'<div class="appicon mono {size}" style="--a:{app["accent"]};--b:{app["bg"]}" aria-hidden="true">{app["name"][0]}</div>'

def store_buttons(app, lang, cls=""):
    apple = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.9-.9-3.2-.8-1.6 0-3.1 1-4 2.4-1.7 3-.4 7.4 1.2 9.8.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.1-.8 1.5 0 1.9.8 3.2.8 1.3 0 2.1-1.2 2.9-2.4.9-1.4 1.3-2.7 1.3-2.8-.1 0-2.5-1-2.4-3.9zM14 5.5c.7-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1 .1 2.1-.6 2.8-1.4z"/></svg>'
    play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3.6 2.3c-.3.3-.4.7-.4 1.2v17c0 .5.1.9.4 1.2l9.5-9.7-9.5-9.7zm10.6 10.8 2.6 2.6-11.2 6.4 8.6-9zm0-2.2-8.6-9 11.2 6.4-2.6 2.6zm3.9-2 3 1.7c.9.5.9 1.3 0 1.8l-3 1.7-2.8-2.6 2.8-2.6z"/></svg>'
    # Store badge wording stays in English: Apple and Google require their official badge text.
    return (f'<div class="stores {cls}">'
            f'<a class="store" href="{app["ios"]}" rel="noopener">{apple}<span><small>Download on the</small>App Store</span></a>'
            f'<a class="store" href="{app["android"]}" rel="noopener">{play}<span><small>Get it on</small>Google Play</span></a>'
            f'</div>')

ICON_GLOBE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9S14.5 18.3 12 21c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>'
ICON_AUTO = '<svg class="theme-ico-auto" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17a8.5 8.5 0 0 0 0-17z" fill="currentColor"/></svg>'
ICON_SUN = '<svg class="theme-ico-light" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_MOON = '<svg class="theme-ico-dark" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>'

THEME_BOOT = "(function(){try{var t=localStorage.getItem('d11-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}})();"
THEME_TOGGLE = ("function d11Theme(){var r=document.documentElement,c=r.getAttribute('data-theme'),"
                "n=c===null?'light':c==='light'?'dark':null;"
                "if(n)r.setAttribute('data-theme',n);else r.removeAttribute('data-theme');"
                "try{n?localStorage.setItem('d11-theme',n):localStorage.removeItem('d11-theme')}catch(e){}}")

def logos():
    return ('<img class="logo logo-light" src="/assets/D11_Full_Logo_Color_On_Light.svg" alt="Division 11 Studios" width="167" height="40">'
            '<img class="logo logo-dark" src="/assets/D11_Full_Logo_Color_On_Dark.svg" alt="Division 11 Studios" width="167" height="40">')

PAGES = []  # (lang, path) for the sitemap

EXTERNAL = re.compile(r"""<a ([^>]*?)href=["'](https?://(?!www\.division11studios\.com)[^"']+)["']([^>]*)>""")

def external_new_tab(html):
    def fix(m):
        attrs = re.sub(r'\s*(rel|target)="[^"]*"', "", m.group(1) + m.group(3)).strip()
        attrs = (" " + attrs) if attrs else ""
        return f'<a href="{m.group(2)}" target="_blank" rel="noopener noreferrer"{attrs}>'
    return EXTERNAL.sub(fix, html)

def write(lang, path, html):
    html = external_new_tab(html)
    rel = L(lang, path).strip("/")
    out = os.path.join(OUT, rel, "index.html") if path != "/404" else os.path.join(OUT, "404.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    if path != "/404":
        PAGES.append((lang, path))

def page(lang, path, title, desc, body, active=None, hero=False):
    d = next(l for l in LANGS if l["code"] == lang)
    nav_items = [("/", "nav_home"), ("/apps/", "nav_apps"), ("/about/", "nav_about"), ("/support/", "nav_support")]
    nav = "".join(f'<a href="{L(lang, h)}"{" aria-current=\"page\"" if h == active else ""}>{t(lang, k)}</a>' for h, k in nav_items)
    langs_menu = "".join(
        f'<a href="{L(l["code"], path)}" hreflang="{l["code"]}" lang="{l["code"]}"{" aria-current=\"true\"" if l["code"] == lang else ""}>{l["name"]}</a>'
        for l in LANGS)
    alternates = "".join(f'<link rel="alternate" hreflang="{l["code"]}" href="{SITE}{L(l["code"], path)}">\n' for l in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{SITE}{path}">\n'
    full_title = f"{title} · {t(lang, 'brand')}" if title else t(lang, "home_title")
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": T["en"]["brand"],
          "alternateName": T["ar"]["brand"], "legalName": T["en"]["legal"], "url": SITE,
          "logo": SITE + "/assets/apple-touch-icon.png", "email": CO["support"], "telephone": CO["phone_href"],
          "foundingDate": "2026",
          "address": {"@type": "PostalAddress", "streetAddress": "Building 9, Street 133, Block 1",
                      "addressLocality": "Al Nahda, Kuwait City", "addressCountry": "KW"},
          "sameAs": [CO["instagram"], CO["tiktok"]]}
    fonts = "family=Inter:wght@400;500;600&family=Sora:wght@500;600;700"
    if lang == "ar":
        fonts += "&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700"
    html = f"""<!doctype html>
<html lang="{lang}" dir="{d['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<script>{THEME_BOOT}</script>
<meta name="description" content="{esc(desc)}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{SITE}{L(lang, path)}">
{alternates}<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{L(lang, path)}">
<meta property="og:image" content="{SITE}/assets/apple-touch-icon.png">
<meta property="og:locale" content="{'ar_KW' if lang == 'ar' else 'en_US'}">
<meta name="theme-color" content="#0A0630">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={CSS_VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{t(lang, 'skip')}</a>
<header class="site-header{' on-dark' if hero else ''}">
  <div class="wrap bar">
    <a class="brand" href="{L(lang, '/')}" aria-label="{t(lang, 'brand')}">{logos()}</a>
    <input type="checkbox" id="navtoggle" class="navtoggle" aria-label="{t(lang, 'menu')}">
    <nav class="nav" aria-label="{t(lang, 'menu')}">{nav}</nav>
    <div class="tools">
      <details class="lang"><summary class="tool" aria-label="{t(lang, 'language')}">{ICON_GLOBE}<span class="tool-label">{d['short']}</span></summary><div class="lang-menu">{langs_menu}</div></details>
      <button class="tool" type="button" onclick="d11Theme()" aria-label="{t(lang, 'theme')}" title="{t(lang, 'theme')}">{ICON_AUTO}{ICON_SUN}{ICON_MOON}</button>
    </div>
    <label for="navtoggle" class="burger" aria-hidden="true"><span></span><span></span><span></span></label>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <div class="foot-brand">{logos()}</div>
      <p class="muted small">{t(lang, 'tagline_footer')}</p>
      <p class="small"><a href="{CO['instagram']}" rel="noopener">Instagram</a> · <a href="{CO['tiktok']}" rel="noopener">TikTok</a></p>
    </div>
    <div>
      <h3>{t(lang, 'f_company')}</h3>
      <p class="small">{esc(t(lang, 'legal'))}</p>
    </div>
    <div>
      <h3>{t(lang, 'f_address')}</h3>
      <p class="small">{'<br>'.join(t(lang, 'addr'))}</p>
    </div>
    <div>
      <h3>{t(lang, 'f_contact')}</h3>
      <p class="small">{mail(CO['support'])}<br>{tel()}</p>
      <p class="small"><a href="{L(lang, '/privacy/')}">{t(lang, 'privacy')}</a> · <a href="{L(lang, '/terms/')}">{t(lang, 'terms')}</a></p>
    </div>
  </div>
  <div class="wrap legal-line small">© 2026 {esc(t(lang, 'legal').rstrip('.'))}. {t(lang, 'rights')} {esc(t(lang, 'legal_note'))}</div>
</footer>
<script>{THEME_TOGGLE}</script>
</body>
</html>
"""
    write(lang, path, html)

# -------------------------------------------------------------------- pages
def _svg(path):
    return f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'

ICONS = {
    "phone": _svg('<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>'),
    "game": _svg('<path d="M6.5 8h11a4 4 0 0 1 3.9 4.9l-.9 4a2.6 2.6 0 0 1-4.4 1.2L14 16h-4l-2.1 2.1a2.6 2.6 0 0 1-4.4-1.2l-.9-4A4 4 0 0 1 6.5 8z"/><path d="M8 11v3M6.5 12.5h3M15.5 12h.01M17.5 13.5h.01"/>'),
    "web": _svg('<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M2.5 8.5h19M6 6.3h.01M8.5 6.3h.01"/>'),
    "bolt": _svg('<path d="M13 2.5 4.5 13.5H12l-1 8 8.5-11H12l1-8z"/>'),
    "lock": _svg('<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>'),
    "lang": _svg('<path d="M4 5h8M8 3v2M10.5 5c-.7 3.8-3 6.6-6 8M6 8.5c1 2 2.8 3.6 5 4.5"/><path d="M13 21l4-9 4 9M14.5 18h5"/>'),
    "mail": _svg('<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3 6.5 9 6.5 9-6.5"/>'),
    "brief": _svg('<rect x="2.5" y="7" width="19" height="13" rx="2.5"/><path d="M8.5 7V5a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v2M2.5 12.5h19"/>'),
    "call": _svg('<path d="M5 3.5h3.2l1.6 4.2-2.1 1.4a11 11 0 0 0 7.2 7.2l1.4-2.1 4.2 1.6V19a1.9 1.9 0 0 1-2 1.9A16.5 16.5 0 0 1 3.1 5.5 1.9 1.9 0 0 1 5 3.5z"/>'),
}

def feature(h, p, icon=None, num=None):
    badge = f'<span class="badge">{ICONS[icon]}</span>' if icon else (f'<span class="badge num">{num:02d}</span>' if num else "")
    return f'<div class="feature">{badge}<h3>{h}</h3><p>{p}</p></div>'

def page_hero(eyebrow, h1, lead="", meta=""):
    lead = f'<p class="lead">{lead}</p>' if lead else ""
    meta = f'<p class="hero-meta">{meta}</p>' if meta else ""
    return f'<section class="page-hero"><div class="wrap"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1>{lead}{meta}</div></section>'

def home(lang):
    cards = "".join(f"""
    <article class="app-card">
      {icon_html(a)}
      <div>
        <h3><a href="{L(lang, '/' + a['slug'] + '/')}">{a['name']}</a></h3>
        <p class="tag">{at(a, lang, 'tagline')}</p>
        <p>{at(a, lang, 'summary')}</p>
        <p class="meta small">{at(a, lang, 'category')} · {at(a, lang, 'platforms')}</p>
        {store_buttons(a, lang, 'compact')}
      </div>
    </article>""" for a in APPS)
    what = "".join(feature(h, p, icon=i) for (h, p), i in zip(t(lang, "what"), ["phone", "game", "web"]))
    body = f"""
<section class="hero">
  <div class="wrap hero-inner">
    <p class="eyebrow">{t(lang, 'hero_eyebrow')}</p>
    <h1>{t(lang, 'hero_h1')}</h1>
    <p class="lead">{t(lang, 'hero_lead')}</p>
    <div class="cta"><a class="btn primary" href="{L(lang, '/apps/')}">{t(lang, 'cta_apps')}</a><a class="btn ghost" href="{L(lang, '/about/')}">{t(lang, 'cta_about')}</a></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">{t(lang, 'apps_eyebrow')}</p><h2>{t(lang, 'apps_h2')}</h2></div>
    <div class="app-grid">{cards}
    </div>
  </div>
</section>
<section class="section tint">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">{t(lang, 'what_eyebrow')}</p><h2>{t(lang, 'what_h2')}</h2></div>
    <div class="three">{what}</div>
  </div>
</section>
<section class="section">
  <div class="wrap contact-strip">
    <div>
      <p class="eyebrow">{t(lang, 'contact_eyebrow')}</p>
      <h2>{t(lang, 'contact_h2')}</h2>
      <p>{t(lang, 'contact_p')}</p>
      <a class="textlink" href="{L(lang, '/support/')}">{t(lang, 'contact_link')} {t(lang, 'arrow')}</a>
    </div>
    <address>
      <strong>{t(lang, 'office')}</strong><br>{'<br>'.join(t(lang, 'addr'))}<br><br>
      {mail(CO['support'])}<br>{tel()}
    </address>
  </div>
</section>"""
    page(lang, "/", "", t(lang, "home_desc"), body, active="/", hero=True)

def apps_page(lang):
    cards = "".join(f"""
    <article class="show-card" style="--a:{a['accent']};--b:{a['bg']}">
      <a class="show-banner" href="{L(lang, '/' + a['slug'] + '/')}">
        {icon_html(a, 'xl')}
        <div><h2>{a['name']}</h2><p>{at(a, lang, 'tagline')}</p></div>
      </a>
      <div class="show-body">
        <p>{at(a, lang, 'summary')}</p>
        <ul class="chips"><li>{at(a, lang, 'category')}</li><li>{at(a, lang, 'platforms')}</li><li>{t(lang, 'rated')} {ltr(a['age'])}</li></ul>
        {store_buttons(a, lang)}
        <p class="small links"><a href="{L(lang, '/' + a['slug'] + '/')}">{t(lang, 'details')} {t(lang, 'arrow')}</a><a href="{L(lang, '/' + a['slug'] + '/privacy/')}">{t(lang, 'privacy_policy')}</a></p>
      </div>
    </article>""" for a in APPS)
    body = f"""
{page_hero(t(lang, 'apps_head_eyebrow'), t(lang, 'apps_head_h1'), t(lang, 'apps_head_lead'))}
<section class="section"><div class="wrap">
  <div class="showcase">{cards}</div>
  <div class="coming"><span class="badge">{ICONS['game']}</span><p>{t(lang, 'more_coming')}</p></div>
</div></section>"""
    page(lang, "/apps/", t(lang, "apps_title"), t(lang, "apps_desc"), body, active="/apps/", hero=True)

def app_page(lang, a):
    feats = "".join(feature(h, p, num=i + 1) for i, (h, p) in enumerate(at(a, lang, "features")))
    body = f"""
<section class="app-hero" style="--a:{a['accent']};--b:{a['bg']}">
  <div class="wrap app-hero-inner">
    {icon_html(a, 'xl')}
    <div>
      <p class="eyebrow">{at(a, lang, 'category')}</p>
      <h1>{a['name']}</h1>
      <p class="app-tagline">{at(a, lang, 'tagline')}</p>
      <p class="lead">{at(a, lang, 'summary')}</p>
      {store_buttons(a, lang)}
    </div>
  </div>
</section>
<section class="section pull-up" style="--a:{a['accent']};--b:{a['bg']}"><div class="wrap">
  <dl class="facts raised">
    <div><dt>{t(lang, 'f_platforms')}</dt><dd>{at(a, lang, 'platforms')}</dd></div>
    <div><dt>{t(lang, 'f_price')}</dt><dd>{at(a, lang, 'pricing')}</dd></div>
    <div><dt>{t(lang, 'f_age')}</dt><dd>{ltr(a['age'])}</dd></div>
    <div><dt>{t(lang, 'f_dev')}</dt><dd>{t(lang, 'brand')}</dd></div>
  </dl>
</div></section>
<section class="section" style="--a:{a['accent']};--b:{a['bg']}"><div class="wrap"><div class="section-head"><p class="eyebrow">{a['name']}</p><h2>{t(lang, 'features')}</h2></div><div class="three app-feats">{feats}</div></div></section>
<section class="section tint"><div class="wrap">
  <div class="app-links">
    <a class="res-app" href="{L(lang, '/' + a['slug'] + '/privacy/')}"><span class="badge">{ICONS['lock']}</span><div><strong>{t(lang, 'privacy_policy')}</strong><br><span class="muted small">{a['name']} {t(lang, 'arrow')}</span></div></a>
    <a class="res-app" href="{L(lang, '/support/')}"><span class="badge">{ICONS['mail']}</span><div><strong>{t(lang, 'get_support')}</strong><br><span class="muted small">{ltr(CO['support'])}</span></div></a>
    <a class="res-app" href="{L(lang, '/terms/')}"><span class="badge">{ICONS['brief']}</span><div><strong>{t(lang, 'terms_of_use')}</strong><br><span class="muted small">{t(lang, 'brand')}</span></div></a>
  </div>
</div></section>"""
    page(lang, f"/{a['slug']}/", a["name"], f"{a['name']} — {at(a, lang, 'tagline')}. {at(a, lang, 'summary')}", body, active="/apps/", hero=True)

def about(lang):
    links = {a["slug"]: f'<a href="{L(lang, "/" + a["slug"] + "/")}">{a["name"]}</a>' for a in APPS}
    values = "".join(feature(h, p, icon=i) for (h, p), i in zip(t(lang, "values"), ["bolt", "lock", "lang"]))
    stats = "".join(f'<div class="stat"><span class="stat-n">{ltr(n)}</span><span class="stat-l">{l}</span></div>' for n, l in t(lang, "stats"))
    icons = "".join(f'<a href="{L(lang, "/" + a["slug"] + "/")}" aria-label="{a["name"]}">{icon_html(a)}</a>' for a in APPS)
    body = f"""
{page_hero(t(lang, 'about_eyebrow'), t(lang, 'about_h1'), t(lang, 'about_lead'))}
<section class="section"><div class="wrap about-grid">
  <div class="prose">
    <h2>{t(lang, 'story_h2')}</h2>
    <p>{t(lang, 'about_p').format(**links)}</p>
    <div class="icon-row">{icons}</div>
  </div>
  <div class="stats">{stats}</div>
</div></section>
<section class="section tint"><div class="wrap"><div class="section-head"><h2>{t(lang, 'values_h2')}</h2></div><div class="three">{values}</div></div></section>"""
    page(lang, "/about/", t(lang, "about_title"), t(lang, "about_desc"), body, active="/about/", hero=True)

def support(lang):
    chev = '<svg class="chev" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
    faq = "".join(f'<details class="faq"><summary>{q}{chev}</summary><p>{a}</p></details>' for q, a in t(lang, "faq"))
    c = t(lang, "contact_cards")
    cards = (f'<a class="contact-card" href="mailto:{CO["support"]}"><span class="badge">{ICONS["mail"]}</span><h3>{c[0][0]}</h3><p>{c[0][1]}</p><span class="cc-link">{ltr(CO["support"])}</span></a>'
             f'<a class="contact-card" href="mailto:{CO["dev"]}"><span class="badge">{ICONS["brief"]}</span><h3>{c[1][0]}</h3><p>{c[1][1]}</p><span class="cc-link">{ltr(CO["dev"])}</span></a>'
             f'<a class="contact-card" href="tel:{CO["phone_href"]}"><span class="badge">{ICONS["call"]}</span><h3>{c[2][0]}</h3><p>{c[2][1]}</p><span class="cc-link">{ltr(CO["phone"])}</span></a>')
    res = "".join(f'<div class="res-app">{icon_html(a)}<div><strong>{a["name"]}</strong><br><a href="{L(lang, "/" + a["slug"] + "/")}">{t(lang, "about_app")}</a> · <a href="{L(lang, "/" + a["slug"] + "/privacy/")}">{t(lang, "privacy_policy")}</a></div></div>' for a in APPS)
    body = f"""
{page_hero(t(lang, 'support_eyebrow'), t(lang, 'support_h1'), t(lang, 'support_lead'))}
<section class="section pull-up"><div class="wrap"><div class="three contact-cards">{cards}</div></div></section>
<section class="section"><div class="wrap two">
  <div>
    <h2>{t(lang, 'faq_h2')}</h2>
    {faq}
  </div>
  <aside class="card">
    <h2 class="h-small">{t(lang, 'app_resources')}</h2>
    {res}
    <p class="small"><a href="{L(lang, '/terms/')}">{t(lang, 'terms_of_use')}</a> · <a href="{L(lang, '/privacy/')}">{t(lang, 'privacy')}</a></p>
  </aside>
</div></section>"""
    page(lang, "/support/", t(lang, "support_title"), t(lang, "support_desc"), body, active="/support/", hero=True)

def legal_page(lang, path, title, desc, eyebrow, meta, inner):
    body = f"""
{page_hero(eyebrow, title, meta=meta)}
<section class="section legal-wrap pull-up"><div class="wrap narrow"><div class="paper prose">{inner}</div></div></section>"""
    page(lang, path, title, desc, body, hero=True)

def terms(lang):
    secs = "".join(f"<h2>{h}</h2><p>{p.format(email=mail(CO['support']))}</p>" for h, p in t(lang, "terms_body"))
    note = f'<p class="muted small">{t(lang, "translation_note")}</p>' if t(lang, "translation_note") else ""
    legal_page(lang, "/terms/", t(lang, "terms_title"), t(lang, "terms_desc"), t(lang, "legal_eyebrow"), t(lang, "last_updated"),
               f"<p class=\"lead dark\">{t(lang, 'terms_intro')}</p>{secs}{note}")

def privacy(lang):
    items = "".join(f'<a class="res-app" href="{L(lang, "/" + a["slug"] + "/privacy/")}">{icon_html(a)}<div><strong>{a["name"]}</strong><br><span class="muted small">{t(lang, "privacy_policy")} {t(lang, "arrow")}</span></div></a>' for a in APPS)
    legal_page(lang, "/privacy/", t(lang, "privacy_title"), t(lang, "privacy_desc"), t(lang, "legal_eyebrow"), t(lang, "last_updated"),
               f"""<h2 class="first">{t(lang, 'privacy_apps_h2')}</h2><div class="policy-list">{items}</div>
<h2>{t(lang, 'privacy_site_h2')}</h2><p>{t(lang, 'privacy_site_p')}</p>
<h2>{t(lang, 'privacy_contact_h2')}</h2><p>{mail(CO['support'])}</p>""")

def notfound():
    parts = "".join(
        f'<div lang="{l["code"]}" dir="{l["dir"]}" style="margin-bottom:24px"><h1>{t(l["code"], "nf_title")}</h1>'
        f'<p class="lead">{t(l["code"], "nf_lead")} <a href="{L(l["code"], "/")}">{t(l["code"], "nf_home")}</a></p></div>'
        for l in LANGS)
    body = f'<section class="page-hero"><div class="wrap"><p class="eyebrow">404</p>{parts}</div></section>'
    page(DEFAULT, "/404", t(DEFAULT, "nf_title"), t(DEFAULT, "nf_lead"), body, hero=True)

# ------------------------------------------------- app privacy policies
# The policy texts in policies/*.html are kept verbatim; only their body
# content is lifted into the site template. A policy may contain one block per
# language (<div id="content-en">, <div id="content-ar">); languages without a
# block show the English text.
def policy_blocks(src):
    with open(os.path.join(ROOT, src), encoding="utf-8") as f:
        h = f.read()
    blocks = {}
    for m in re.finditer(r'<div id="content-(\w+)"[^>]*>(.*?)</div>\s*(?=<div id="content-|</div>\s*<script|</div>\s*</body)', h, re.S):
        blocks[m.group(1)] = m.group(2)
    if not blocks:
        m = re.search(r'<div class="container">(.*)</div>\s*</body>', h, re.S)
        blocks["en"] = m.group(1)
    out = {}
    date_re = r'<p class="last-updated">(.*?)</p>|<p><strong>(Last Updated:[^<]*)</strong></p>'
    for code, body in blocks.items():
        title = re.search(r"<h1>(.*?)</h1>", body, re.S).group(1).strip()
        date = re.search(date_re, body, re.S)
        date = re.sub(r"</?strong>", "", date.group(1) or date.group(2)).strip() if date else ""
        body = re.sub(r"<h1>.*?</h1>", "", body, count=1, flags=re.S)
        body = re.sub(date_re, "", body, count=1, flags=re.S)
        body = re.sub(r'<div class="footer">.*?</div>', "", body, flags=re.S)
        out[code] = (title, date, body.strip())
    return out

def policy_page(lang, app, blocks):
    code = lang if lang in blocks else DEFAULT
    title, date, body = blocks[code]
    d = next(l for l in LANGS if l["code"] == code)
    note = "" if code == lang else f'<p class="note">{t(lang, "policy_en_only")}</p>'
    body = f"""
{page_hero(app['name'], title, meta=date)}
<section class="section legal-wrap pull-up"><div class="wrap narrow">{note}<div class="paper prose policy" lang="{code}" dir="{d['dir']}">{body}</div></div></section>"""
    page(lang, f"/{app['slug']}/privacy/", title, f"{title} — {t(lang, 'brand')}", body, active="/apps/", hero=True)

def statics():
    a = os.path.join(OUT, "assets")
    os.makedirs(os.path.join(a, "apps"), exist_ok=True)
    B = os.path.join(ROOT, "brand")
    shutil.copy(os.path.join(ROOT, "site.css"), os.path.join(a, "site.css"))
    for f in ["D11_Full_Logo_Color_On_Light.svg", "D11_Full_Logo_Color_On_Dark.svg",
              "D11_Pattern_Black_Background.webp", "apple-touch-icon.png"]:
        shutil.copy(os.path.join(B, f), os.path.join(a, f))
    shutil.copy(os.path.join(B, "favicon.svg"), os.path.join(a, "favicon.svg"))
    shutil.copy(os.path.join(B, "favicon.ico"), os.path.join(OUT, "favicon.ico"))
    for f in os.listdir(os.path.join(B, "apps")):
        shutil.copy(os.path.join(B, "apps", f), os.path.join(a, "apps", f))
    shutil.copy(os.path.join(ROOT, "app-ads.txt"), os.path.join(OUT, "app-ads.txt"))
    with open(os.path.join(OUT, "CNAME"), "w") as f: f.write("www.division11studios.com\n")
    with open(os.path.join(OUT, ".nojekyll"), "w") as f: f.write("")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = [L(lang, p) for lang, p in PAGES]
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{SITE}{u}</loc></url>\n")
        f.write("</urlset>\n")

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    for l in LANGS:
        c = l["code"]
        home(c); apps_page(c); about(c); support(c); terms(c); privacy(c)
        for x in APPS:
            app_page(c, x)
    notfound()
    for x in APPS:
        blocks = policy_blocks(f"policies/{x['slug']}.html")
        for l in LANGS:
            policy_page(l["code"], x, blocks)
    statics()
    print("built", sum(len(fs) for _, _, fs in os.walk(OUT)), "files")
