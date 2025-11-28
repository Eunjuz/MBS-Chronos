
from Elements.sidebar import Sidebar_Buttons
from Elements.assignedPM import *
from tests.PMO_Tests.test_PMOdjangoLogin import run_login
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
import datetime
import time
import random


#PMO Assign Projects to PM 

def test_09_01(driver): #Navigate to Projects

    sbButtons = Sidebar_Buttons(driver)
    assignedPMLabel = AssignedPM_Labels(driver)

    #Login
    run_login(driver)

    sbButtons.PMAssignments.click()
    time.sleep(1)
    assert driver.current_url == 'https://chronos.mgenesis.com/assignments'
    assert assignedPMLabel.PMAssignments.is_displayed()

def test_09_02(driver): #View and scroll to Unassigned projects
    test_09_01(driver)
    time.sleep(1)

    # Find the Unassigned Projects section heading
    try:
        unassigned_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Unassigned Projects')]"))
        )

        # Scroll the Unassigned Projects section into view
        driver.execute_script("arguments[0].scrollIntoView(true);", unassigned_section)
        time.sleep(1)

        # Verify it's displayed
        assert unassigned_section.is_displayed()
        print("✓ Successfully scrolled to Unassigned Projects section")

    except Exception as e:
        print(f"Error: Could not find Unassigned Projects section: {e}")
        raise

    # Optional: If you need to interact with the scrollable container
    try:
        scrollable_element = driver.find_element(By.XPATH, "//div[@class='h-full overflow-y-auto pr-4']")
        assert scrollable_element.is_displayed()
        print("✓ Scrollable container is visible")
    except Exception as e:
        print(f"Warning: Scrollable container not found: {e}")

def test_09_03(driver): #Click Assign PM on an Unassigned Project and verify modal
    unassignedPMButtons = UnassignedProjects_Buttons(driver)

    test_09_02(driver)
    time.sleep(1)

    unassignedPMButtons.AssignPMButton.click()
    time.sleep(1)

    # Verify that the project details modal is displayed
    try:
        project_details_modal = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='flex items-center justify-between p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50']"))
        )
        assert project_details_modal.is_displayed()
        print("✓ Project details modal is displayed")
    except Exception as e:
        print(f"Error: Project details modal not displayed: {e}")
        raise

def test_09_04(driver): #Assign Project to a PM
    test_09_03(driver)
    time.sleep(1)

    # Select a project from the dropdown --------------------------------------------------------------------
    project = Select(UnassignedProjectsModal_Fields(driver).Project)
    projectOptions = project.options
    projectRandom = random.choice(projectOptions)
    project.select_by_visible_text(projectRandom.text)
    time.sleep(2)


    # Assign to Project Manager by Clicking -----------------------------------------------------------------
    num_to_select = random.randint(1, len(Select(UnassignedProjectsModal_Fields(driver).PM).options))
    selected_indices = random.sample(num_to_select)

    # Loop through the randomly selected indices
    for i in selected_indices:
        xpath = f"(//input[@type='radio'])[{i}]"



        radio = driver.find_element(By.XPATH, xpath)

        # Scroll radio into view
        driver.execute_script("arguments[0].scrollIntoView(true);", radio)
        time.sleep(0.3)  # small delay to allow scrolling

        # Click if not already selected
        if not radio.is_selected():
            radio.click()