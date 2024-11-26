from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def close_popups(driver):
    """
    Detect and log the presence of pop-ups or ads dynamically using XPath selectors.
    This function skips closing pop-ups.
    """
    try:
        # Example XPath for typical pop-up close buttons
        popups = driver.find_elements(By.XPATH, '//button[contains(@class, "close")]')
        if popups:
            print(f"Detected {len(popups)} pop-up(s), but skipping close action.")
        else:
            print("No pop-ups detected.")
    except Exception as e:
        print(f"Error while detecting pop-ups: {e}")

def main():
    try:
        driver = webdriver.Chrome()
        driver.get('https://internshala.com')
        time.sleep(5)
        close_popups(driver)

        # Login
        login_button_xpath = '//*[@id="header"]/div/nav/div[3]/button[2]'
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, login_button_xpath))).click()
        print("Login button clicked.")

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modal_email"]')))
        driver.find_element(By.XPATH, '//*[@id="modal_email"]').send_keys('manojnasanam@gmail.com')
        driver.find_element(By.XPATH, '//*[@id="modal_password"]').send_keys('sanam@123456789')
        time.sleep(10)
        driver.find_element(By.XPATH, '//*[@id="modal_login_submit"]').click()
        print("Login submitted.")

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="internships-nav"]/i')))
        print("Login successful.")

        # Navigate to internships section
        internships_tab_xpath = '//*[@id="internships_new_superscript"]'
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, internships_tab_xpath))).click()
        print("Navigated to internships section.")

        # Apply filters for specific internships
        filtered_url = "https://internshala.com/internships/work-from-home-cloud-computing,cyber-security,design,front-end-development,software-development,ui-ux,web-development-internships"
        driver.get(filtered_url)
        print("Navigated to the filtered internships page.")

        # Wait for job list container
        container_xpath = '//*[@id="internship_list_container_1"]'
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Find all job elements
        job_elements_xpath = f'{container_xpath}/*[starts-with(@id, "individual_internship_")]'
        job_elements = driver.find_elements(By.XPATH, job_elements_xpath)

        print(f"Found {len(job_elements)} jobs listed.")

        # Get the current window handle (original tab)
        original_window = driver.current_window_handle

        # Process each job
        for index, job in enumerate(job_elements, start=1):
            try:
                # Scroll to job element and click
                driver.execute_script("arguments[0].scrollIntoView(true);", job)
                job.click()
                print(f"Opened Job {index} details.")
                close_popups(driver)

                # Switch to new tab if job opens in a new tab
                WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))  # Wait for new tab to open
                new_window_handles = driver.window_handles
                if len(new_window_handles) > 1:
                    # Switch to the new tab
                    for handle in new_window_handles:
                        if handle != original_window:
                            driver.switch_to.window(handle)
                            break
                    print(f"Switched to new tab for Job {index}.")

                # Apply for the job
                try:
                    apply_button_xpath = '//*[@id="easy_apply_button"]'
                    apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, apply_button_xpath)))
                    driver.execute_script("arguments[0].click();", apply_button)
                    print(f"Clicked 'Apply Now' for Job {index}.")
                except TimeoutException:
                    print(f"'Apply Now' button not found for Job {index}. Skipping...")
                    driver.close()  # Close the new tab
                    driver.switch_to.window(original_window)  # Switch back to the original tab
                    continue  # Skip to the next job

                # Submit application
                try:
                    submit_button_xpath = '//*[@id="submit"]'
                    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
                    driver.execute_script("arguments[0].click();", submit_button)
                    print(f"Clicked 'Submit' for Job {index}.")
                except TimeoutException:
                    print(f"'Submit' button not found for Job {index}. Skipping...")
                    driver.close()  # Close the new tab
                    driver.switch_to.window(original_window)  # Switch back to the original tab
                    continue  # Skip to the next job

                time.sleep(2)

                # Close the new tab and switch back to the original window
                driver.close()  # Close the new tab
                driver.switch_to.window(original_window)  # Switch back to the original tab
                print(f"Closed the tab for Job {index} and returned to job listings.")

            except Exception as e:
                print(f"Error processing Job {index}: {e}. Moving to next job.")
                driver.switch_to.window(original_window)  # Ensure we're back on the original tab

        print("Successfully applied to all jobs!")

    except TimeoutException as te:
        print(f"Timeout error occurred: {te}")
    except NoSuchElementException as ne:
        print(f"Element not found: {ne}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Script execution completed.")
        driver.quit()

if __name__ == "__main__":
    main()
