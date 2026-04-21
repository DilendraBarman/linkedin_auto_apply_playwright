import pandas as pd
import time
from ai.resume_customizer import customize_resume
from ai.cover_letter_generator import generate_cover_letter
from ai.cover_letter_pdf import generate_cover_letter_pdf
from ai.pdf_generator import generate_resume_pdf
from ai.pdf_generator import generate_cover_letter_pdf
from playwright.sync_api import TimeoutError

def find_easy_apply_jobs(page, total_pages):
    all_links = []
    current_page = 1

    while current_page <= total_pages:
        # Wait for job list container
        page.wait_for_selector("#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list.jobs-semantic-search-list > ul", timeout=20000)
        jobs = page.locator("#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list.jobs-semantic-search-list > ul > li")
        print(f"🧾 Scraping page {current_page} with {jobs.count()} jobs...")
        for i in range(jobs.count()):
            card = jobs.nth(i)
            try:
                print("Processing the job card...")
                link_elem = card.locator("a")
                job_link = link_elem.get_attribute("href")
                if job_link and "linkedin.com/jobs/search-results" in job_link:
                    # all_links.append(job_link.split("?")[0])
                    print(f"  - Found job link: {len(job_link)} characters")
                    all_links.append(job_link)
            except:
                continue

        # Next page button
        try:
            next_btn = page.locator("button[aria-label='View next page']")
            if next_btn.is_enabled():
                next_btn.click()
                page.wait_for_timeout(4000)
                current_page += 1
            else:
                break
        except TimeoutError:
            break

    print(f"✅ Collected {len(all_links)} job links across {current_page} pages.")
    return list(dict.fromkeys(all_links))  # remove duplicates

def apply_jobs(page, links, resume_path, cover_letter_path, cfg):
    applied = []
    ai_enabled = cfg["ai"]["enabled"]

    for i, link in enumerate(links):
        print(f"➡️ Opening: {link}")
        page.goto(link)
        page.wait_for_selector("main", timeout=15000)
        time.sleep(3)

        try:
            apply_btn = page.locator("#jobs-apply-button-id:visible").first  # new 2025 selector
            if apply_btn.is_visible():
                # Extract job description
                desc = ""
                try:
                    desc_elem = page.locator("div.jobs-description-content__text--stretch")  # new 2025 selector
                    if desc_elem.is_visible():
                        desc = desc_elem.inner_text()
                except:
                    pass

                # AI Resume customization
                if ai_enabled and desc:
                    resume_out = f"{cfg['ai']['output_dir']}/resume_{i+1}.txt"
                    print("📝 Generating AI-customized resume...", resume_out)
                    custom_resume = customize_resume(desc, resume_out)
                    resume_to_upload = generate_resume_pdf(custom_resume, f"{cfg['ai']['output_dir']}/resume_{i+1}.pdf")
                else:
                    resume_to_upload = resume_path

                # AI Cover letter generation
                if ai_enabled and cfg["ai"]["generate_cover_letter"] and desc:
                    cover_out = f"{cfg['ai']['output_dir']}/cover_{i+1}.txt"

                    # Generate cover letter text with retry/fallback
                    cover_letter = generate_cover_letter(
                        job_description=desc,
                        resume_path=resume_path,  # optional, can be used for skill matching later
                        output_txt=cover_out,
                        model=cfg["ai"]["model"],
                        user_name="Dilendra Barman"
                    )
                    print("📝 Generating AI-generated cover letter...", cover_letter)
                    # Generate PDF from the .txt
                    cover_pdf = f"{cfg['ai']['output_dir']}/cover_{i+1}.pdf"
                    cover_pdf = generate_cover_letter_pdf(cover_letter, user_name="Dilendra Barman")

                else:
                    cover_pdf = cover_letter_path if cover_letter_path else None


                # Click Apply & upload resume
                apply_btn.click()
                page.wait_for_timeout(2000)
                print("🖱️ Clicked Apply button.")

                # file_input = page.locator("input[type='file']")
                # if file_input.is_visible():
                #     file_input.set_input_files(resume_to_upload)
                #     print("📄 Uploaded custom resume.")

                # --- Upload Resume ---
                try:
                    # Try to locate file inputs on the current page
                    file_inputs = page.locator("input[type='file']")
                    count = file_inputs.count()
                    print(f"📁 Found {count} file input fields on first page.")

                    if count == 0:
                        # No file inputs found — try navigating to next step
                        page.click("button[aria-label='Continue to next step']")
                        page.wait_for_selector("input[type='file']", state="attached", timeout=5000)
                        file_inputs = page.locator("input[type='file']")
                        count = file_inputs.count()
                        print(f"📁 Found {count} file input fields on next page.")

                    # Upload logic
                    if count == 1:
                        file_inputs.first.set_input_files(resume_to_upload)
                        print("📄 Uploaded resume.")
                    elif count >= 2 and cover_pdf:
                        file_inputs.nth(0).set_input_files(resume_to_upload)
                        file_inputs.nth(1).set_input_files(cover_pdf)
                        print("📄 Uploaded resume and cover letter.")
                    elif count >= 1:
                        file_inputs.first.set_input_files(resume_to_upload)
                        print("📄 Uploaded resume only.")
                    else:
                        print("⚠️ No file input fields found after navigation.")
                except Exception as e:
                    print(f"⚠️ Error uploading files: {e}")


                print(f"🟡 Review & submit manually: {link}")
                applied.append({
                    "job_link": link,
                    "resume_file": resume_to_upload,
                    "cover_letter_pdf": cover_pdf if ai_enabled else ""
                })
                page.wait_for_timeout(3000)
        except Exception as e:
            print(f"❌ Error applying to {link}: {e}")
            continue

    if applied:
        pd.DataFrame(applied).to_csv("jobs_applied.csv", mode="a", index=False)
        print(f"💾 Recorded {len(applied)} applications.")
