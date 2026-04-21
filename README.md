# 🤖 LinkedIn Auto Apply Bot (Playwright)

Automate your LinkedIn job applications using Playwright. This project logs into LinkedIn, searches for relevant job roles, and applies automatically using the **Easy Apply** feature.

---

## 🚀 Features

* 🔐 Automated LinkedIn login
* 🔎 Job search based on keywords and location
* ⚡ Filters jobs with **Easy Apply** option
* 📄 Uploads resume and cover letter(if required)
* 🔁 Applies to multiple jobs in a loop
* 🧠 Configurable search criteria

---

## 🛠️ Tech Stack

* **Language:** Python
* **Automation:** Playwright
* **Browser:** Chromium (default)

---

## 📂 Project Structure

```
linkedin-auto-apply_playwright/
│── ai/
│   └── cover_letter_generator.py
│   └── cover_letter_pdf.py
│   └── pdf_generator.py
│   └── resume_customizer.py
│   └── cover_letter.pdf
│   └── resume.pdf
│── pages/
│   ├── apply_page.py
│   ├── login_page.py
│   └── search_page.py
│── utils/
│   ├── browser.py
│   ├── jobSearch.ts
│   └── apply.ts
│── config.yaml
│── jobs_applied.csv
│── main.py
│── README.md
│── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```Terminal
git clone https://github.com/DilendraBarman/linkedin_auto_apply_playwright.git
cd linkedin_auto_apply_playwright
```

### 2. Install requirements.txt

```Terminal
pip install -r requirements.txt
```

## 🔐 Configuration

Update your credentials and preferences in `config.yaml`:

```yaml
login:
  email: "your-email@example.com"
  password: "your-password"

search:
  keywords: "your-search-keywords-with-space"
  location: "your-location"
  easy_apply_only: true
  pages_to_scrape: no-of-pages-to-apply

resume_path: "ai/resume.pdf"
cover_letter_path: "ai/cover_letter.pdf"

ai:
  enabled: false ##true if using ai to customise resume
  output_dir: "ai/generated_docs"
  model: "gpt-4o-mini"
  generate_cover_letter: true
```

⚠️ **Important:**

* Do NOT commit your credentials to GitHub
* Use environment variables (`.env`) for better security

---

## ▶️ Running the Bot

```Terminal
pytest main.py
```

---

## 🧪 How It Works

1. Launches browser using Playwright
2. Logs into LinkedIn
3. Searches jobs using keywords & location
4. Filters jobs with **Easy Apply**
5. Opens each job
6. Clicks **Easy Apply**
7. Upload Resume & Cover Letter (if required)
8. Submits application

---

## ⚠️ Limitations

* Only supports **Easy Apply** jobs
* Complex forms (multi-step / custom questions) may fail
* CAPTCHA or security checks may block automation
* LinkedIn UI changes can break selectors

---

## 🧠 Future Improvements

* AI-based form filling
* Job matching using NLP
* Proxy support to avoid detection
* Logging & reporting dashboard

---

## 📸 Sample Output (Optional)

* Create CSV file with applied jobs

---

## 🛡️ Disclaimer

This project is for **educational purposes only**.

Automating LinkedIn actions may violate their Terms of Service. Use responsibly and at your own risk.

---

## 🙌 Contribution

Pull requests are welcome! For major changes, please open an issue first.

---

## ⭐ Support

If you find this project useful, give it a ⭐ on GitHub!
