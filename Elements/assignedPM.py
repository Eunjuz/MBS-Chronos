from selenium.webdriver.common.by import By

class AssignedPM_Labels:
    def __init__(self, driver):
        self.driver = driver

    @property
    def PMAssignments(self):
        return self.driver.find_element(By.XPATH, "//h1[normalize-space()='PM Assignments']")


class UnassignedProjects_Buttons:
    def __init__(self, driver):
        self.driver = driver

    @property
    def UnassignedProjects_Grid(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='p-4 border border-orange-200 bg-orange-50 rounded-lg'])[1]")

    @property
    def AssignPMButton(self):
        return self.driver.find_element(By.XPATH, "//button[normalize-space()='Assign PM']")


class UnassignedProjectsModal_Fields:
    def __init__(self, driver):
        self.driver = driver

    @property
    def Project(self):
        return self.driver.find_element(By.XPATH, "//select[@class='w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors border-gray-300 ']")

    @property
    def PM(self):
        return self.driver.find_element(By.CLASS_NAME, "p-4 border rounded-lg cursor-pointer transition-all border-gray-200 hover:border-blue-300")


from selenium.webdriver.common.by import By

class AssignedPM_Labels:
    def __init__(self, driver):
        self.driver = driver

    @property
    def PMAssignments(self):
        return self.driver.find_element(By.XPATH, "//h1[normalize-space()='PM Assignments']")


class UnassignedProjects_Buttons:
    def __init__(self, driver):
        self.driver = driver

    @property
    def UnassignedProjects_Grid(self):
        return self.driver.find_element(By.XPATH, "(//div[@class='p-4 border border-orange-200 bg-orange-50 rounded-lg'])[1]")

    @property
    def AssignPMButton(self):
        return self.driver.find_element(By.XPATH, "//button[normalize-space()='Assign PM']")


class UnassignedProjectsModal_Fields:
    def __init__(self, driver):
        self.driver = driver

    @property
    def Project(self):
        return self.driver.find_element(By.XPATH, "//select[@class='w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors border-gray-300 ']")

    @property
    def PM(self):
        return self.driver.find_element(By.CLASS_NAME, "p-4 border rounded-lg cursor-pointer transition-all border-gray-200 hover:border-blue-300")
 