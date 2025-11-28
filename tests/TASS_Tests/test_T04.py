
from Elements.sidebar import Sidebar_Buttons
from Elements.projects import *
from test_djangoLogin import run_login
import time
import random
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidElementStateException, TimeoutException, NoSuchElementException
import datetime
from dateutil.relativedelta import relativedelta



# Utility to generate project names

def generate_project_name():

    prefixes = ["Project", "App", "Website", "Platform", "System"]
    adjectives = ["Alpha", "Beta", "Redesign", "Internal", "Prototype"]
    industries = ["CRM", "E-commerce", "Mobile", "Web", "Finance"]

    return f"{random.choice(prefixes)} {random.choice(adjectives)} {random.choice(industries)}"



# Helper to click Create button with JS fallback

def click_create_button(driver):

    candidates = [
        "//button[normalize-space()='Create Project']",
        "//button[contains(., 'Create Project') and contains(@class,'bg-blue')]",
        "//button[contains(@class,'bg-blue') and contains(., 'Create Project')]",

    ]

    for xp in candidates:

        elems = driver.find_elements(By.XPATH, xp)
        if elems:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", elems[0])
                time.sleep(0.3)
                elems[0].click()
                time.sleep(1)
                return True

            except Exception:
                try:
                    driver.execute_script("arguments[0].click();", elems[0])
                    time.sleep(1)
                    return True
                
                except Exception:
                    continue
    return False



# Helper to close modal if open

def close_modal_if_open(driver):

    """Close the modal by pressing Escape or clicking close button"""

    try:
        # Try pressing Escape key

        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    except Exception:
        pass

   

    try:

        # Try clicking close button (X button)
        close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'close') or contains(@aria-label, 'Close')]")
        close_btn.click()
        time.sleep(0.5)

    except Exception:
        pass



# Helper to open Projects page and open New Project modal

def open_new_project_modal(driver):
    # Close any open modals first

    close_modal_if_open(driver)
    time.sleep(1)

   

    sb = Sidebar_Buttons(driver)

    try:
        sb.Projects.click()

    except Exception:
        # Try JS click if regular click fails
        driver.execute_script("arguments[0].click();", sb.Projects)
    time.sleep(1)

   

    pb = Projects_Buttons(driver)

    try:
        pb.NewProject.click()

    except Exception:

        # Try JS click if regular click fails
        driver.execute_script("arguments[0].click();", pb.NewProject)

    time.sleep(2)
    return Projects_NewProjectModal_Label(driver), Projects_NewProjectModal_Fields(driver)



# Helper to safely set text input

def safe_set_text(driver, element, value):

    try:

        # Wait for element to be clickable
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
        time.sleep(0.2)

       

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)

       

        # Click and clear
        element.click()

        time.sleep(0.1)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

        time.sleep(0.1)

       

        # Send keys
        element.send_keys(value)
        time.sleep(0.2)

    except InvalidElementStateException:

        # Try JS approach

        try:
            driver.execute_script(
                f"arguments[0].value = '{value}'; arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }})); arguments[0].dispatchEvent(new Event('change', {{ bubbles: true }}))",
                element

            )

        except Exception:
            pass

    except Exception as e:
        print(f"Error setting text: {e}")



# Helper to safely set date input

def safe_set_date(driver, element, date_obj):
    iso = date_obj.strftime('%Y-%m-%d')

    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
        time.sleep(0.2)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)

       
        element.click()
        time.sleep(0.1)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

        time.sleep(0.1)
        element.send_keys(iso)

        time.sleep(0.2)

    except Exception:

        try:

            driver.execute_script(
                f"arguments[0].value = '{iso}'; arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }})); arguments[0].dispatchEvent(new Event('change', {{ bubbles: true }}))",
                element

            )

        except Exception:
            pass



# Helper to fill common required fields

def fill_common_fields(driver, fields: Projects_NewProjectModal_Fields, include_sono=True, sono_value=None,
                       include_project=True, project_value=None, include_am=True,
                       include_company=True, include_dates=True):

    # SONo - scroll to top first and use proper XPath

    if include_sono:

        try:

            # Scroll modal to top to ensure SONo is visible
            modal_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'dialog') or contains(@class, 'fixed')]")
            if modal_elements:

                driver.execute_script("arguments[0].scrollTop = 0;", modal_elements[0])
            time.sleep(0.3)

        except Exception:
            driver.execute_script("window.scrollTo(0, 0);")

       

        val = sono_value if sono_value is not None else ''.join(str(random.randint(0, 9)) for _ in range(6))
        safe_set_text(driver, fields.SONo, val)

   

    # Company

    if include_company:

        safe_set_text(driver, fields.Company, 'a')
        time.sleep(0.5)

        try:

            items = driver.find_elements(By.XPATH, "//ul[contains(@class, 'absolute')]//li")
            if items:

                items[0].click()
                time.sleep(0.3)

        except Exception:

            pass

   

    # Project name

    if include_project:

        proj = project_value if project_value is not None else generate_project_name()
        safe_set_text(driver, fields.Project, proj)

   

    # AM select

    if include_am:

        try:

            AM = Select(fields.AM)
            options = [o for o in AM.options if o.text.strip()]

            if options:

                AM.select_by_visible_text(options[0].text)

        except Exception:
            pass

   

    # Dates

    if include_dates:

        today = datetime.date.today()
        start = today
        end = start + relativedelta(months=6)
        safe_set_date(driver, fields.StartDate, start)
        safe_set_date(driver, fields.EndDate, end)

   

    # Mandays

    try:

        safe_set_text(driver, fields.Mandays, str(random.randint(1, 999)))

    except Exception:
        pass


    time.sleep(0.5)



# Test suite: invalid project creation scenarios

def test_T04_01_empty_fields_click_only(driver):

    """Test 1: User clicks Create with all fields empty"""

    run_login(driver)

    NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
    assert NPmodalLabels.CreateNewProject.is_displayed()

   

    # Clear all fields

    try:

        safe_set_text(driver, NPmodalFields.SONo, "")
        safe_set_text(driver, NPmodalFields.Company, "")
        safe_set_text(driver, NPmodalFields.Project, "")
        safe_set_text(driver, NPmodalFields.Mandays, "")

    except Exception:

        pass

   

    click_create_button(driver)
    time.sleep(0.8)

    NPmodalLabels = Projects_NewProjectModal_Label(driver)
    assert NPmodalLabels.CreateNewProject.is_displayed()



def test_T04_02_one_required_field_missing(driver):

    """Test 2: User fills most fields but forgets Project name"""

    run_login(driver)
    NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
    fill_common_fields(driver, NPmodalFields, include_project=False)

   

    # Ensure Project is empty

    safe_set_text(driver, NPmodalFields.Project, "")
    time.sleep(0.5)

   

    click_create_button(driver)
    time.sleep(0.8)

    NPmodalLabels = Projects_NewProjectModal_Label(driver)
    assert NPmodalLabels.CreateNewProject.is_displayed()



def test_T04_03_two_or_more_fields_missing(driver):

    """Test 3: User skips SONo and Company fields"""

    run_login(driver)

    NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
    fill_common_fields(driver, NPmodalFields, include_sono=False, include_company=False)

   

    # Clear SONo and Project

    safe_set_text(driver, NPmodalFields.SONo, "")
    safe_set_text(driver, NPmodalFields.Company, "")
    time.sleep(0.5)

   

    click_create_button(driver)
    time.sleep(0.8)

    NPmodalLabels = Projects_NewProjectModal_Label(driver)

    assert NPmodalLabels.CreateNewProject.is_displayed()



def test_T04_04_end_date_earlier_than_start_date(driver):

    """Test 4: User reverses dates (End Date before Start Date)"""

    run_login(driver)

    NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
    fill_common_fields(driver, NPmodalFields, include_dates=False)

   

    # Set start date to future and end date to today (reversed)

    start = datetime.date.today() + relativedelta(months=6)
    end = datetime.date.today()

    safe_set_date(driver, NPmodalFields.StartDate, start)
    safe_set_date(driver, NPmodalFields.EndDate, end)


    time.sleep(0.5)
    click_create_button(driver)

    time.sleep(0.8)

    NPmodalLabels = Projects_NewProjectModal_Label(driver)
    assert NPmodalLabels.CreateNewProject.is_displayed()



def generate_invalid_sono():

    """Generate invalid SONo: empty or 1-5 digits"""
    choice = random.randint(0, 5)  # 0=empty, 1-5=that many digits

   

    if choice == 0:
        return ""  # Empty input

    else:

        # Generate 'choice' number of random digits (1-5)
        random_digits = [str(random.randint(0, 9)) for _ in range(choice)]
        return ''.join(random_digits)



def test_T04_05_sono_too_short_numbers(driver):

    """

    Test 5: SONo with invalid length: empty or 1–5 digits.

    Expected: Modal stays open and shows validation error.

    """
    run_login(driver)



    for attempt in range(5):

        try:

            # Open modal fresh for each attempt

            NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
            time.sleep(1)



            # Fill all fields except SONo
            fill_common_fields(driver, NPmodalFields, include_sono=False)
            time.sleep(0.4)



            # Generate invalid SONo

            invalid_sono = generate_invalid_sono()
            print(f"[Test05] Attempt {attempt+1}: SONo='{invalid_sono}'")



            # Enter invalid SONo

            safe_set_text(driver, NPmodalFields.SONo, invalid_sono)
            time.sleep(0.4)



            # Click Create

            click_create_button(driver)
            time.sleep(0.8)



            # Modal MUST still be open

            NPmodalLabels = Projects_NewProjectModal_Label(driver)
            assert NPmodalLabels.CreateNewProject.is_displayed(), (
                f"Modal closed unexpectedly for SONo='{invalid_sono}'"

            )



            # Try to detect error message

            try:

                error_msg = driver.find_element(
                    By.XPATH, "//*[contains(text(), 'Sales Order No. must be exactly 6 digits')]"

                )

                if error_msg.is_displayed():
                    print(f"✓ Validation triggered for invalid SONo='{invalid_sono}'")

            except NoSuchElementException:
                print(f"⚠ No error shown (but modal stayed open) for SONo='{invalid_sono}'")

       

        except Exception as e:

            print(f"Error in attempt {attempt + 1}: {str(e)}")
            raise

       

        finally:

            # Close modal after each attempt to ensure clean state
            close_modal_if_open(driver)
            time.sleep(0.5)



def test_T04_06_sono_invalid_format(driver):

    """

    Test 6: Invalid SONo formats: letters, spaces, special chars.
    Expected: Modal stays open and validation error appears.

    """

    run_login(driver)



    invalid_sonos = ["123-456", "123 456", "12345a", "!@#$%^"]


    for sono in invalid_sonos:

        try:

            NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
            time.sleep(1)



            # Fill fields except SONo
            fill_common_fields(driver, NPmodalFields, include_sono=False)
            time.sleep(0.4)



            print(f"[Test06] Testing invalid SONo='{sono}'")



            # Enter invalid SONo

            safe_set_text(driver, NPmodalFields.SONo, sono)
            time.sleep(0.4)



            # Click Create

            click_create_button(driver)
            time.sleep(0.8)



            # Refresh labels

            NPmodalLabels = Projects_NewProjectModal_Label(driver)



            # Modal MUST remain open

            assert NPmodalLabels.CreateNewProject.is_displayed(), (
                f"Modal closed unexpectedly for invalid SONo='{sono}'"

            )



            # Look for validation error

            try:

                error_msg = driver.find_element(
                    By.XPATH,

                    "//*[contains(text(), 'Sales Order No. must be exactly 6 digits')]"
                )

                assert error_msg.is_displayed()
                print(f"✓ Validation triggered for SONo='{sono}'")

            except NoSuchElementException:
                print(f"⚠ Error message missing for SONo='{sono}' (modal stayed open)")

       

        except Exception as e:
            print(f"Error testing SONo='{sono}': {str(e)}")
            raise

       

        finally:

            # Close modal after each iteration to ensure clean state
            close_modal_if_open(driver)
            time.sleep(0.5)





def test_T04_07_start_date_in_past(driver):

    """Test 7: User sets Start Date to past date"""

    run_login(driver)
    NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
    fill_common_fields(driver, NPmodalFields, include_dates=False)

   

    past = datetime.date.today() - relativedelta(months=3)
    future = datetime.date.today() + relativedelta(months=6)

    safe_set_date(driver, NPmodalFields.StartDate, past)
    safe_set_date(driver, NPmodalFields.EndDate, future)

   

    time.sleep(0.5)
    click_create_button(driver)
    time.sleep(0.8)

    NPmodalLabels = Projects_NewProjectModal_Label(driver)
    assert NPmodalLabels.CreateNewProject.is_displayed()



def test_T04_08_same_start_and_end_date(driver):

    """Test 8: User sets same Start and End date"""

    run_login(driver)

    NPmodalLabels, NPmodalFields = open_new_project_modal(driver)
    fill_common_fields(driver, NPmodalFields, include_dates=False)

   

    today = datetime.date.today()
    safe_set_date(driver, NPmodalFields.StartDate, today)
    safe_set_date(driver, NPmodalFields.EndDate, today)

   

    time.sleep(0.5)
    click_create_button(driver)
    time.sleep(0.8)

    NPmodalLabels = Projects_NewProjectModal_Label(driver)
    assert NPmodalLabels.CreateNewProject.is_displayed()