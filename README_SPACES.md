---
title: AI Executive Agent
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🤖 AI Executive Agent - وكيل ذكاء اصطناعي متقدم

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4)](https://ai.google.dev/)

**نظام وكيل ذكاء اصطناعي متقدم مع تنفيذ مستقل للمهام، توليد الكود، وتحليل البيانات**

[📚 التوثيق](https://github.com/aboref3at99-tech/AI-Executive-Agent) | [🐛 الإبلاغ عن مشكلة](https://github.com/aboref3at99-tech/AI-Executive-Agent/issues)

</div>

---

## ✨ الميزات الرئيسية

<table>
<tr>
<td width="50%">

### 🧠 تنفيذ مستقل
- تخطيط تلقائي للمهام
- تنفيذ متعدد الخطوات  
- تحسين ذاتي

</td>
<td width="50%">

### 💻 توليد الكود
- Python من اللغة الطبيعية
- إضافة اختبارات تلقائية
- توثيق الكود

</td>
</tr>
<tr>
<td>

### 📊 تحليل البيانات
- تحليل إحصائي متقدم
- استخراج الرؤى
- توليد التقارير

</td>
<td>

### ⚡ معالجة مجمعة
- تنفيذ متوازي
- تتبع التقدم
- إدارة الأخطاء

</td>
</tr>
</table>

---

## 🚀 البدء السريع (3 خطوات)

### 1️⃣ تكوين API Key

اذهب إلى **Settings** → **Variables and secrets** وأضف:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

احصل على المفتاح من: [Google AI Studio](https://makersuite.google.com/app/apikey)

### 2️⃣ انتظر البناء

يستغرق البناء **5-10 دقائق** ⏱️

### 3️⃣ ابدأ الاستخدام!

افتح Dashboard وجرّب الميزات! 🎉

---

## 🎯 حالات الاستخدام

<details>
<summary><b>🔧 أتمتة المهام</b></summary>

```
المهمة: "قم بتحليل ملف CSV وأنشئ تقرير PDF"
النتيجة: تنفيذ كامل تلقائي مع تقرير شامل
```
</details>

<details>
<summary><b>💡 توليد الكود</b></summary>

```
الطلب: "اكتب دالة لحساب تسلسل فيبوناتشي مع اختبارات"
النتيجة: كود + اختبارات + توثيق
```
</details>

<details>
<summary><b>📈 تحليل البيانات</b></summary>

```
البيانات: ملف Excel بمبيعات الشركة
النتيجة: رؤى + رسوم بيانية + توصيات
```
</details>

<details>
<summary><b>⚡ معالجة مجمعة</b></summary>

```
المهام: [تحليل1, تحليل2, تحليل3]
النتيجة: تنفيذ متوازي سريع
```
</details>

---

## 📊 لوحة التحكم

### الواجهة الرئيسية

- **📈 إحصاءات لحظية**: مهام منفذة، معدل نجاح، زمن متوسط
- **🎯 تنفيذ تفاعلي**: نماذج سهلة لكل نوع مهمة
- **📝 سجل التنفيذ**: آخر 20 عملية مع التفاصيل
- **⚡ تحديثات فورية**: WebSocket للتحديثات اللحظية

### نقاط النهاية API

| النقطة | الوصف |
|--------|-------|
| `/` | لوحة التحكم الرئيسية |
| `/docs` | توثيق API التفاعلي |
| `/health` | فحص الصحة |
| `/metrics` | مقاييس الأداء |
| `/ws` | WebSocket للتحديثات |

---

## 🛠️ التكنولوجيا

<table>
<tr>
<td align="center"><b>LLM</b></td>
<td>Google Gemini Pro</td>
</tr>
<tr>
<td align="center"><b>Framework</b></td>
<td>LangChain + LangGraph + CrewAI</td>
</tr>
<tr>
<td align="center"><b>API</b></td>
<td>FastAPI + WebSockets</td>
</tr>
<tr>
<td align="center"><b>Storage</b></td>
<td>ChromaDB</td>
</tr>
<tr>
<td align="center"><b>Monitoring</b></td>
<td>Comet ML + Opik (اختياري)</td>
</tr>
</table>

---

## ⚙️ المتغيرات الاختيارية

لتفعيل ميزات متقدمة، أضف:

```bash
# Comet ML للمراقبة
COMET_API_KEY=your_comet_key
COMET_WORKSPACE=your_workspace
COMET_PROJECT_NAME=ai-executive-agent

# Opik للمراقبة
OPIK_API_KEY=your_opik_key
OPIK_WORKSPACE=your_workspace

# إعدادات إضافية
GEMINI_MODEL=gemini-pro
LOG_LEVEL=INFO
```

---

## 📚 التوثيق الكامل

- 📖 [دليل المستخدم الشامل](https://github.com/aboref3at99-tech/AI-Executive-Agent/blob/main/docs/OPENMANUS_GUIDE.md)
- 🎨 [دليل لوحة التحكم](https://github.com/aboref3at99-tech/AI-Executive-Agent/blob/main/docs/DASHBOARD_GUIDE.md)
- 🏗️ [معمارية النظام](https://github.com/aboref3at99-tech/AI-Executive-Agent/blob/main/AGENT_ARCHITECTURE.md)
- 🚀 [دليل النشر](https://github.com/aboref3at99-tech/AI-Executive-Agent/blob/main/HUGGINGFACE_DEPLOY.md)

---

## 💰 التكلفة

| المورد | التكلفة |
|---------|---------|
| Hugging Face Spaces | **مجاني** ✅ |
| Google Gemini API | **مجاني** ✅ |
| Comet ML | **مجاني** ✅ (اختياري) |
| Opik | **مجاني** ✅ (اختياري) |
| **المجموع** | **$0 / شهر** 🎉 |

---

## 🔒 الأمان والخصوصية

- ✅ لا يتم حفظ بياناتك على السيرفر
- ✅ جميع الأكواد مفتوحة المصدر
- ✅ يمكنك مراجعة الكود بالكامل
- ✅ API Keys مشفرة

---

## 🤝 المساهمة

نرحب بالمساهمات! 

1. Fork المشروع
2. أنشئ Branch جديد
3. قم بالتعديلات
4. افتح Pull Request

---

## 📝 الترخيص

MIT License - انظر [LICENSE](https://github.com/aboref3at99-tech/AI-Executive-Agent/blob/main/LICENSE)

---

## 🔗 الروابط المهمة

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/aboref3at99-tech/AI-Executive-Agent)
[![Issues](https://img.shields.io/badge/Issues-Report%20Bug-red?style=for-the-badge&logo=github)](https://github.com/aboref3at99-tech/AI-Executive-Agent/issues)
[![Pull Requests](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge&logo=github)](https://github.com/aboref3at99-tech/AI-Executive-Agent/pulls)

</div>

---

## 🎉 استمتع!

إذا أعجبك المشروع، لا تنسى إعطاءه ⭐ على GitHub!

<div align="center">

**صُنع بـ ❤️ بواسطة [@aboref3at99-tech](https://github.com/aboref3at99-tech)**

</div>
