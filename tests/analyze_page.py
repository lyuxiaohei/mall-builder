from playwright.sync_api import sync_playwright
import os

# Output directory for screenshots
output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    print("1. Navigate to editor.html...")
    page.goto('http://localhost:3000/editor.html')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Take screenshot
    page.screenshot(path=os.path.join(output_dir, 'page-initial.png'), full_page=True)

    # Get all buttons
    buttons = page.locator('button').all()
    print(f"\nButtons found ({len(buttons)}):")
    for btn in buttons[:20]:
        try:
            text = btn.inner_text()[:50]
            cls = btn.get_attribute('class') or ''
            print(f"  - '{text}' | class: {cls[:30]}")
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
    for dt in data_types[:20]:
        try:
            type_val = dt.get_attribute('data-type')
            text = dt.inner_text()[:30]
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
    for s in selects[:10]:
        try:
            cls = s.get_attribute('class') or ''
            id_attr = s.get_attribute('id') or ''
            print(f"  - class: '{cls}' | id: '{id_attr}'")
        except:
            pass

    # Get page structure - main panels
    print("\nMain panels/sections:")
    panels = ['component-library', 'canvas', 'props-panel', 'preview', 'sidebar', 'left-panel', 'right-panel']
    for panel in panels:
        loc = page.locator(f'.{panel}, #{panel}, [id*="{panel}"]')
        if loc.count() > 0:
            print(f"  - Found: {panel} ({loc.count()} elements)")

    # Check the HTML structure
    html_file = os.path.join(output_dir, 'page-structure.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(page.content())
    print(f"\nFull HTML saved to: {html_file}")

    browser.close()
    print("\nDone!")