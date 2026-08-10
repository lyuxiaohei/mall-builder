from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\preview\editor.html'
    page.goto('file:///' + file_path.replace('\\', '/'))
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Click components tab
    page.locator('.editor-side-tab[data-panel="components"]').click()
    page.wait_for_timeout(500)

    # Get all component items
    comp_items = page.locator('.component-item').all()
    print(f'组件库中的组件数量: {len(comp_items)}')
    print('\n组件列表:')
    for ci in comp_items:
        comp_type = ci.get_attribute('data-component-type')
        name = ci.locator('strong').inner_text()
        print(f'  - {comp_type}: {name}')

    # Check if big-bg-image is hidden
    big_bg = page.locator('.component-item[data-component-type="big-bg-image"]')
    print(f'\n大背景图组件是否显示: {big_bg.count() > 0}')

    browser.close()