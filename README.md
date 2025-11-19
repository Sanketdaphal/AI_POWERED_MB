# 🎨 AI-Powered Moodboard Generator (MVP)
### DES646 Mid-Term Assessment • Team: **D-for-Design**
![Moodboard Generator Banner](https://github.com/Sanketdaphal/AI_POWERED_MB/blob/main/Immage.png)

👉 [Click here to open the Moodboard Generator](http://172.23.12.190:8501/)


The **AI-Powered Moodboard Generator** reduces the time designers spend building moodboards by automatically generating **color palettes, design styles, and visual cues** from natural-language design briefs.

This Minimum Viable Product (MVP) is optimized for **stability, reproducibility, and deployment** on Streamlit Community Cloud.

---

## 🚀 Project Aim

To develop an AI-powered web application that automatically generates **personalized moodboards** from natural language design briefs — reducing ideation time for designers by **40–50%**.

---

## ⚙️ Technical Approach (MVP)

| Component | Methodology Implemented | Status |
|----------|--------------------------|--------|
| **Framework** | Streamlit (Python) | ✅ Complete |
| **NLP Method** | NLTK keyword extraction & stopword parsing | ✅ Complete (Simplified for robustness) |
| **Color Generation** | Rule-based HSV algorithms across 8+ mood/style categories | ✅ Complete |
| **Image System** | Placeholder images using `placehold.co` | ✅ Complete |
| **Deployment** | Streamlit Community Cloud setup | 🚀 Ready |

---

## 📦 Installation & Setup

### **Prerequisites**
- Python **3.8+**
- Git
### 2. Create and Activate a Virtual Environment

Create a clean Python environment to isolate project dependencies.

```bash
# Create environment
python -m venv venv

# Activate on Windows (Command Prompt / PowerShell)
.\venv\Scripts\activate

# Activate on macOS/Linux
# source venv/bin/activate
### 3. Install Dependencies

Install all required Python packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py

