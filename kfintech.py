from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from config import IPO_NAME, KFINTECH, PAN_NUMBER
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from datetime import datetime

svg_file = './allotment_results.svg'
results_data = []


def create_svg_file(data):
    """Create SVG file with allotment results"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="auto" viewBox="0 0 1000 600">
  <style>
    .header { font-size: 24px; font-weight: bold; fill: #333; }
    .title { font-size: 18px; font-weight: bold; fill: #555; }
    .row-header { font-size: 14px; font-weight: bold; fill: #fff; }
    .row-data { font-size: 13px; fill: #333; }
    .row-allotted { fill: #4CAF50; }
    .row-not-allotted { fill: #f44336; }
    .timestamp { font-size: 12px; fill: #999; }
    rect { stroke: #ddd; stroke-width: 1; }
  </style>
  
  <rect width="1000" height="600" fill="#f9f9f9"/>
  
  <text x="20" y="40" class="header">IPO Allotment Results</text>
  <text x="20" y="65" class="timestamp">Generated: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</text>
  
  <!-- Table Header -->
  <rect x="10" y="85" width="980" height="40" class="row-header" fill="#333"/>
  <text x="20" y="110" class="row-header">PAN</text>
  <text x="200" y="110" class="row-header">Name</text>
  <text x="550" y="110" class="row-header">Status</text>
  <text x="750" y="110" class="row-header">Allotted</text>
  <text x="900" y="110" class="row-header">Applied</text>
  
  <!-- Divider -->
  <line x1="10" y1="130" x2="990" y2="130" stroke="#ddd" stroke-width="2"/>
  
'''

    y_pos = 150
    for idx, item in enumerate(data):
        row_height = 35
        bg_color = '#f0f0f0' if idx % 2 == 0 else '#ffffff'
        status_color = '#4CAF50' if item['status'] and 'Allotted' in item['status'] else '#f44336'
        
        svg_content += f'''  <!-- Row {idx + 1} -->
  <rect x="10" y="{y_pos}" width="980" height="{row_height}" fill="{bg_color}"/>
  <text x="20" y="{y_pos + 25}" class="row-data">{item['pan']}</text>
  <text x="200" y="{y_pos + 25}" class="row-data">{item['name'] or 'N/A'}</text>
  <text x="550" y="{y_pos + 25}" class="row-data" fill="{status_color}">{item['status'] or 'N/A'}</text>
  <text x="750" y="{y_pos + 25}" class="row-data">{item['allotted'] or 'N/A'}</text>
  <text x="900" y="{y_pos + 25}" class="row-data">{item['applied'] or 'N/A'}</text>
  
'''
        y_pos += row_height
    
    svg_content += '''</svg>'''
    
    try:
        with open(svg_file, 'w', encoding='utf-8') as file:
            file.write(svg_content)
        print(f"Results saved to {svg_file}")
    except Exception as e:
        print(f"Error writing SVG file: {e}")


def parse_allotment_response(html):
    """Parse the response HTML and extract name and allotment status"""
    soup = BeautifulSoup(html, 'html.parser')
    
    result = {
        'name': None,
        'status': None,
        'allotted': None,
        'applied': None
    }
    
    try:
        status_chip = soup.find('span', class_='MuiChip-label')
        if status_chip:
            result['status'] = status_chip.text.strip()
        all_text = soup.get_text()
    
        name_match = soup.find(string=lambda text: text and 'Name:' in text)
        if name_match:
            parent = name_match.find_parent()
            name_tag = parent.find_next('b')
            if name_tag:
                result['name'] = name_tag.text.strip()
        
        allotted_match = soup.find(string=lambda text: text and 'Allotted:' in text)
        if allotted_match:
            parent = allotted_match.find_parent()
            allotted_tag = parent.find_next('b')
            if allotted_tag:
                result['allotted'] = allotted_tag.text.strip()
        
        applied_match = soup.find(string=lambda text: text and 'Applied:' in text)
        if applied_match:
            parent = applied_match.find_parent()
            applied_tag = parent.find_next('b')
            if applied_tag:
                result['applied'] = applied_tag.text.strip()
        
    except Exception as e:
        print(f"Error parsing response: {e}")
    
    return result


def save_to_results(pan, name, status, allotted, applied):
    """Add result to in-memory list"""
    results_data.append({
        'pan': pan,
        'name': name,
        'status': status,
        'allotted': allotted,
        'applied': applied
    })
    print(f"Recorded: {pan} - {name} - {status}")


def ipo_allotment(link, pan=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    
    try:
        ipo_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "demo-multiple-name"))
        )
        ipo_dropdown.click()
        time.sleep(1)
        dropdown_options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-value]"))
        )
        
        selected = False
        for option in dropdown_options:
            if IPO_NAME.upper() in option.text.upper():
                option.click()
                selected = True
                print(f"Selected: {option.text}")
                break
        
        if not selected:
            print(f"Could not find IPO option matching '{IPO_NAME}'")
        
        time.sleep(1)
    except Exception as e:
        print(f"Error selecting IPO: {e}")
        driver.quit()
        return None
    
    try:
        pan_radio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='PAN']"))
        )
        pan_radio.click()
        time.sleep(0.5)
    except Exception as e:
        print(f"Error selecting PAN option: {e}")
    
    if pan:
        try:
            pan_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "outlined-start-adornment"))
            )
            pan_input.clear()
            pan_input.send_keys(pan)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error entering PAN: {e}")
    
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button'].content-button"))
        )
        submit_button.click()
        
        time.sleep(3)
        
        response_html = driver.page_source
        
        parsed = parse_allotment_response(response_html)
        
        save_to_results(pan, parsed['name'], parsed['status'], parsed['allotted'], parsed['applied'])
        
        return parsed
        
    except Exception as e:
        print(f"Error submitting form: {e}")
        return None

if isinstance(PAN_NUMBER, list):
    for pan in PAN_NUMBER:
        print(f"\n--- Processing PAN: {pan} ---")
        ipo_allotment(KFINTECH, pan)
        time.sleep(2)
else:
    ipo_allotment(KFINTECH, PAN_NUMBER)

create_svg_file(results_data)