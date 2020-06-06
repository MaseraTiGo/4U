# 20021
# step 1 zip
from random import choice, randrange


def select_random_single(xpath, start=1, end=0, driver=driver):
    sleep(randint(1, 2))
    element = driver.find_element_by_xpath(xpath)
    elements = element.find_elements_by_xpath('./option')
    if end:
        choice(elements[start: end]).click()
    else:
        choice(elements[start:]).click()


auto = AutoDo(driver)
auto.select_random_single = select_random_single

auto.wait_4_see('//*[text()="Get Started"]', 25)
auto.random_interval()
auto.click_origin('//*[text()="Get Started"]')

auto.random_interval()
ActionChains(driver).drag_and_drop_by_offset(auto.find_element_s('//*[@id="slider-3-h"]/span'), randrange(10, 900, 50), 0).perform()
auto.input_origin('//*[@id="first_name"]', First_Name)
auto.input_origin('//*[@id="last_name"]', Last_Name)
auto.input_origin('//*[@id="zip_code"]', Zip.zfill(5))
auto.input_origin('//*[@id="email"]', Email.lower())
phone = Home_Phone.ljust(10, "0")
try:
    auto.input_origin('//*[@id="home_phone_1"]', phone[:3])
    auto.input_origin('//*[@id="cell_phone_2"]', phone[3:6])
    auto.input_origin('//*[@id="cell_phone_3"]', phone[-4:])
except:
    pass



auto.click_origin('//*[@id="check_terms"]')
auto.random_interval()
auto.click_origin('//*[@id="short-form-submit-btn"]')

auto.wait_4_see('//*[contains(text(), "Step 2/4 - Contact Information")]')
auto.select_by_value('//*[@id="military"]', 'no')

auto.select_by_value('//*[@name="dob_date_month"]', int(Month_Of_Birth))
auto.select_by_value('//*[@name="dob_date_day"]', int(Day_Of_Birth))
auto.select_by_value('//*[@name="dob_date_year"]', int(Year_Of_Birth))

auto.input_origin('//*[@id="address"]', Address)
auto.input_origin('//*[@id="city"]', City)
auto.select_by_value('//*[@id="state"]', State_ab)
auto.select_random_single('//*[@id="own_rent"]')
auto.select_random_single('//*[@name="years_at_residence"]')
auto.select_random_single('//*[@name="months_at_residence"]')
try:
    auto.input_origin('//*[@id="home_phone_1"]', phone[:3])
    auto.input_origin('//*[@id="home_phone_2"]', phone[3:6])
    auto.input_origin('//*[@id="home_phone_3"]', phone[-4:])
except:
    pass
try:
    auto.input_origin('//*[@id="home_phone_mask"]', phone)
except:
    pass
auto.select_random_single('//*[@id="best_time_contact"]')
auto.select_by_value('//*[@id="driver_license_state"]', Drivers_License_State)
auto.input_origin('//*[@id="driver_license_or_state_id"]', Drivers_License.strip())
auto.random_interval()
auto.click_origin('//*[contains(text(), "Next")]')

auto.random_interval()
auto.wait_4_see('//*[contains(text(), "Step 3/4 - Employment Information")]')
auto.random_interval()
auto.select_by_value('//*[@id="monthly_income"]', randrange(3300, 6300, 100))
try:
    income = 'employed' if Income_Type and Income_Type.lower.startswith('emp') else 'benefits'
except:
    income = 'employed'
auto.select_by_value('//*[@id="income_type"]', income)
try:
    emp = Employer if Employer else Employer_Name
except:
    emp = 'sun'
auto.input_origin('//*[@id="employer_name"]', emp)
try:
    Position = Position if Position else Occupation
except:
    Position = 'worker'
auto.input_origin('//*[@id="job_title"]', Position)

auto.select_by_value('//*[@name="years_employed"]', Years_At_Job)
auto.select_by_value('//*[@name="months_employed"]', randint(1, 11))

phone = Work_Phone.ljust(10, "0")
try:
    auto.input_origin('//*[@id="work_phone_1"]', phone[:3])
    auto.input_origin('//*[@id="work_phone_2"]', phone[3:6])
    auto.input_origin('//*[@id="work_phone_3"]', phone[-4:])
except:
    pass
try:
    auto.input_origin('//*[@id="work_phone_mask"]', phone)
except:
    pass
auto.click_origin('//*[contains(text(), "Next")]')

auto.random_interval()
auto.wait_4_see('//*[contains(text(), "Step 4/4 - Bank Account Information")]')
auto.random_interval()
try:
    auto.select_by_value('//*[@id="bank_account_type"]', Account_Type.lower())
except:
    auto.select_by_value('//*[@id="bank_account_type"]', 'checking')

try:
    auto.select_by_value('//*[@id="direct_deposit"]', 1 if 'dir' in Paycheck_Type.lower() else 0)
except:
    auto.select_by_value('//*[@id="direct_deposit"]', 1)

auto.input_origin('//*[@id="routing_number"]', Routing_Number.zfill(9))
auto.input_origin('//*[@id="account_number"]', Account_Number)
ssn = SSN.zfill(9)
try:
    auto.input_origin('//*[@id="ssn_1"]', ssn[:3])
    auto.input_origin('//*[@id="ssn_2"]', ssn[3:5])
    auto.input_origin('//*[@id="ssn_4"]', ssn[-4:])
except:
    pass
try:
    auto.input_origin('//*[@id="ssn_mask"]', ssn)
except:
    pass
auto.select_random_single('//*[@id="pay_period"]')
auto.click_origin('//*[@id="next_pay_date"]')
auto.random_interval()
choice(auto.find_element_s('//*[contains(@data-handler, "selectDay")]', multi=True)).click()
auto.random_interval()
auto.click_origin('//*[contains(@type, "submit")]')
auto.random_interval(5, 6)
try:
    auto.wait_4_not_see('//*[contains(text(), "Please be Patient, We are Processing your Request")]', 3 * 60)
except:
    pass
else:
    pass
print('all done')