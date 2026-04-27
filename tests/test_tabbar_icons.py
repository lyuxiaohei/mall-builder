from playwright.sync_api import sync_playwright
import os

output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    print("=== Testing Tabbar Icon Upload Feature ===")

    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\preview\editor.html'
    page.goto('file:///' + file_path.replace('\\', '/'))
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Create a sub page to enable tabbar
    print("\n1. Creating a sub page...")
    page.locator('.editor-side-tab[data-page-group="sub"]').click()
    page.wait_for_timeout(500)
    page.locator('#btn-add-page').click()
    page.wait_for_timeout(500)

    modal = page.locator('#modal-add-page.show')
    if modal.count() > 0:
        template_cards = page.locator('.template-select-card').all()
        if len(template_cards) > 0:
            template_cards[0].click()
            page.wait_for_timeout(300)
            page.locator('#btn-add-page-confirm').click()
            page.wait_for_timeout(500)

    print("   Sub page created")

    # Select bottom navigation
    print("\n2. Selecting the bottom navigation from page layout...")
    bottom_nav_item = page.locator('.page-layout-item[data-nav-type="bottom"]')
    if bottom_nav_item.count() > 0:
        bottom_nav_item.click()
        page.wait_for_timeout(500)
        print("   Clicked on bottom nav")

    # Check what's in the props panel
    print("\n3. Checking props panel content...")
    props_panel = page.locator('.editor-props')
    if props_panel.count() > 0:
        props_text = props_panel.inner_text()[:500]
        print(f"   Props panel text: {props_text[:300]}...")

    # Check for tab-config-list element
    tab_config_list = page.locator('#tab-config-list')
    print(f"\n   #tab-config-list exists: {tab_config_list.count() > 0}")

    if tab_config_list.count() > 0:
        tab_config_html = tab_config_list.inner_html()[:500]
        print(f"   #tab-config-list HTML: {tab_config_html[:300]}...")

    # Check for any tab-icon-* elements
    tab_icon_elements = page.locator('[class*="tab-icon"]').all()
    print(f"   Elements with tab-icon class: {len(tab_icon_elements)}")

    # Check for the specific library button by partial ID match
    library_buttons = page.locator('button[id*="library"]').all()
    print(f"   Buttons with 'library' in ID: {len(library_buttons)}")
    for btn in library_buttons[:5]:
        print(f"     - {btn.get_attribute('id')}")

    page.screenshot(path=os.path.join(output_dir, 'tabbar-test-final.png'))

    browser.close()
    print("\n=== Test Complete ===")