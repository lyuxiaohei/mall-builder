from playwright.sync_api import sync_playwright
import os
import time

# Output directory for screenshots
output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    print("1. Navigate to editor.html...")
    # Use file:// URL since the server is having issues with path
    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\preview\editor.html'
    page.goto(f'file://{file_path}')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Take screenshot
    page.screenshot(path=os.path.join(output_dir, 'page-initial.png'), full_page=True)
    print("   - Initial screenshot saved")

    # Get all buttons
    buttons = page.locator('button').all()
    print(f"\nButtons found ({len(buttons)}):")
    for btn in buttons[:20]:
        try:
            text = btn.inner_text()[:50]
            cls = btn.get_attribute('class') or ''
            print(f"  - '{text}' | class: {cls[:40]}")
        except:
            pass

    # Get all draggable elements
    draggables = page.locator('[draggable="true"]').all()
    print(f"\nDraggable elements ({len(draggables)}):")
    for d in draggables[:15]:
        try:
            text = d.inner_text()[:50]
            dt = d.get_attribute('data-type') or ''
            print(f"  - '{text}' | data-type: {dt}")
        except:
            pass

    # Get all elements with data-type attribute
    data_types = page.locator('[data-type]').all()
    print(f"\nElements with data-type ({len(data_types)}):")
    for dt in data_types[:30]:
        try:
            type_val = dt.get_attribute('data-type')
            text = dt.inner_text()[:40]
            print(f"  - data-type='{type_val}' | text: '{text}'")
        except:
            pass

    # Look for component library items
    comp_items = page.locator('.comp-lib-item, .component-item, .lib-item').all()
    print(f"\nComponent library items ({len(comp_items)}):")
    for ci in comp_items[:10]:
        try:
            text = ci.inner_text()
            print(f"  - '{text}'")
        except:
            pass

    # Get all select elements
    selects = page.locator('select').all()
    print(f"\nSelect elements ({len(selects)}):")
    for s in selects[:15]:
        try:
            cls = s.get_attribute('class') or ''
            id_attr = s.get_attribute('id') or ''
            print(f"  - class: '{cls[:50]}' | id: '{id_attr}'")
        except:
            pass

    # Get page structure - main panels
    print("\nMain panels/sections:")
    panels = ['component-library', 'canvas', 'props-panel', 'preview', 'sidebar', 'left-panel', 'right-panel']
    for panel in panels:
        loc = page.locator(f'.{panel}, #{panel}, [id*="{panel}"]')
        if loc.count() > 0:
            print(f"  - Found: {panel} ({loc.count()} elements)")

    # Look for the component library panel
    comp_lib = page.locator('.component-library-panel, #component-library-panel, .lib-panel')
    if comp_lib.count() > 0:
        print(f"\nComponent library panel found: {comp_lib.count()}")

    # Get all divs with class containing 'lib' or 'component'
    libs = page.locator('div[class*="lib"], div[class*="component"]').all()
    print(f"\nDivs with lib/component in class ({len(libs)}):")
    for lib in libs[:15]:
        try:
            cls = lib.get_attribute('class') or ''
            text = lib.inner_text()[:30]
            print(f"  - class: '{cls[:40]}' | text: '{text}'")
        except:
            pass

    browser.close()
    print("\nDone!")