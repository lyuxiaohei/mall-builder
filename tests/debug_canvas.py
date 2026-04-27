from playwright.sync_api import sync_playwright
import os

output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\preview\editor.html'
    page.goto('file:///' + file_path.replace('\\', '/'))
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    print("1. Page loaded")

    # Click components tab
    comp_tab = page.locator('.editor-side-tab[data-panel="components"]')
    comp_tab.click()
    page.wait_for_timeout(1000)

    # Get component types
    comp_items = page.locator('.component-item').all()
    print(f"Components available: {len(comp_items)}")
    for ci in comp_items:
        comp_type = ci.get_attribute('data-component-type')
        print(f"  - {comp_type}")

    # Try to find the canvas area and check what's there
    canvas = page.locator('.canvas, .editor-canvas, .canvas-body, #canvas')
    print(f"Canvas found: {canvas.count()}")

    # Check for existing floors
    floors_before = page.locator('.canvas-floor').all()
    print(f"Floors before: {len(floors_before)}")

    # Check for empty state
    empty_state = page.locator('.canvas-empty, .empty-state, .no-floors')
    print(f"Empty state found: {empty_state.count()}")

    # Look for an "add" button on the canvas
    add_btns = page.locator('.canvas button, .canvas-body button').all()
    print(f"Canvas buttons: {len(add_btns)}")
    for btn in add_btns[:5]:
        print(f"  - {btn.inner_text()[:30]}")

    # Check if there's a page already selected
    page_items = page.locator('.page-item').all()
    print(f"Page items: {len(page_items)}")

    # Get the page content after clicking components tab
    page.screenshot(path=os.path.join(output_dir, 'debug-components-tab.png'))

    # Click on first page item if exists
    if len(page_items) > 0:
        page_items[0].click()
        page.wait_for_timeout(500)
        print("Clicked first page item")
        page.screenshot(path=os.path.join(output_dir, 'debug-page-selected.png'))

        # Check floors again
        floors_after = page.locator('.canvas-floor').all()
        print(f"Floors after selecting page: {len(floors_after)}")

    # Let's check the canvas body HTML
    canvas_html = page.evaluate('() => document.querySelector(".canvas-body")?.innerHTML || "no canvas body"')
    print(f"Canvas body HTML length: {len(canvas_html)}")
    print(f"Canvas body preview: {canvas_html[:500]}")

    browser.close()