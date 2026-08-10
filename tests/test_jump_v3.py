from playwright.sync_api import sync_playwright
import os

output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    print("=== Testing Jump Type Dropdown Functionality ===")

    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\preview\editor.html'
    page.goto('file:///' + file_path.replace('\\', '/'))
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    print("1. Initial page loaded")
    page.screenshot(path=os.path.join(output_dir, 'test-01-initial.png'))

    print("2. Clicking on the Components tab...")
    comp_tab = page.locator('.editor-side-tab[data-panel="components"]')
    if comp_tab.count() > 0:
        comp_tab.click()
        page.wait_for_timeout(1000)
        print("   Clicked Components tab")
        page.screenshot(path=os.path.join(output_dir, 'test-02-components-tab.png'))

        comp_items = page.locator('.component-item').all()
        print(f"   Found {len(comp_items)} components")
        for ci in comp_items[:10]:
            comp_type = ci.get_attribute('data-component-type')
            text = ci.inner_text()[:50]
            print(f"     type={comp_type} text={text}")

        print("3. Adding a component to canvas...")
        carousel_item = page.locator('.component-item[data-component-type="carousel"]').first
        if carousel_item.count() == 0:
            carousel_item = page.locator('.component-item[data-component-type="icon-nav"]').first

        if carousel_item.count() > 0:
            comp_type = carousel_item.get_attribute('data-component-type')
            print(f"   Using component: {comp_type}")

            page.evaluate('''() => {
                const component = document.querySelector('.component-item[data-component-type="carousel"], .component-item[data-component-type="icon-nav"]');
                const dropzone = document.querySelector('.canvas-floor-dropzone, .canvas-floors, .canvas-body');
                if (!component || !dropzone) return;
                const dragStartEvent = new DragEvent('dragstart', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: new DataTransfer()
                });
                dragStartEvent.dataTransfer.setData('text/plain', component.dataset.componentType);
                dragStartEvent.dataTransfer.setData('application/x-editor-drag-kind', 'component');
                component.dispatchEvent(dragStartEvent);
                const dropEvent = new DragEvent('drop', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dragStartEvent.dataTransfer
                });
                dropzone.dispatchEvent(dropEvent);
            }''')

            page.wait_for_timeout(500)
            print("   Component dropped")
            page.screenshot(path=os.path.join(output_dir, 'test-03-component-added.png'))

            print("4. Selecting the added floor...")
            floors = page.locator('.canvas-floor').all()
            print(f"   Found {len(floors)} floors")

            if len(floors) > 0:
                floors[0].click()
                page.wait_for_timeout(500)
                print("   Selected floor")
                page.screenshot(path=os.path.join(output_dir, 'test-04-floor-selected.png'))

                print("5. Checking properties panel...")
                jump_selects = page.locator('select[class*="jump"]').all()
                print(f"   Jump type selects: {len(jump_selects)}")

                if len(jump_selects) > 0:
                    jump_select = jump_selects[0]
                    cls = jump_select.get_attribute('class')
                    print(f"   Jump select class: {cls}")

                    print("\n=== Testing Category ===")
                    jump_select.select_option('category')
                    page.wait_for_timeout(300)
                    page.screenshot(path=os.path.join(output_dir, 'test-06-category.png'))

                    cat_input = page.locator('.searchable-dropdown-input').first
                    if cat_input.count() > 0:
                        cat_input.click()
                        page.wait_for_timeout(500)
                        page.screenshot(path=os.path.join(output_dir, 'test-07-category-click.png'))

                        dropdown = page.locator('.searchable-dropdown.open')
                        modal = page.locator('.modal.show')

                        if dropdown.count() > 0 and dropdown.is_visible():
                            print("  CORRECT: Dropdown appeared for category")
                        elif modal.count() > 0 and modal.is_visible():
                            print("  INCORRECT: Modal appeared for category (should be dropdown)")
                        else:
                            print("  Neither visible")

                        page.keyboard.press('Escape')
                        page.wait_for_timeout(300)

                    print("\n=== Testing Brand ===")
                    jump_select.select_option('brand')
                    page.wait_for_timeout(300)
                    page.screenshot(path=os.path.join(output_dir, 'test-08-brand.png'))

                    brand_input = page.locator('.searchable-dropdown-input').first
                    if brand_input.count() > 0:
                        brand_input.click()
                        page.wait_for_timeout(500)
                        page.screenshot(path=os.path.join(output_dir, 'test-09-brand-click.png'))

                        dropdown = page.locator('.searchable-dropdown.open')
                        modal = page.locator('.modal.show')

                        if dropdown.count() > 0 and dropdown.is_visible():
                            print("  CORRECT: Dropdown appeared for brand")
                        elif modal.count() > 0 and modal.is_visible():
                            print("  INCORRECT: Modal appeared for brand (should be dropdown)")
                        else:
                            print("  Neither visible")

                        page.keyboard.press('Escape')
                        page.wait_for_timeout(300)

                    print("\n=== Testing Tag ===")
                    jump_select.select_option('tag')
                    page.wait_for_timeout(300)
                    page.screenshot(path=os.path.join(output_dir, 'test-10-tag.png'))

                    tag_input = page.locator('.searchable-dropdown-input').first
                    if tag_input.count() > 0:
                        tag_input.click()
                        page.wait_for_timeout(500)
                        page.screenshot(path=os.path.join(output_dir, 'test-11-tag-click.png'))

                        dropdown = page.locator('.searchable-dropdown.open')
                        modal = page.locator('.modal.show')

                        if dropdown.count() > 0 and dropdown.is_visible():
                            print("  CORRECT: Dropdown appeared for tag")
                        elif modal.count() > 0 and modal.is_visible():
                            print("  INCORRECT: Modal appeared for tag (should be dropdown)")
                        else:
                            print("  Neither visible")

                        page.keyboard.press('Escape')
                        page.wait_for_timeout(300)

                    print("\n=== Testing Product (should open modal) ===")
                    jump_select.select_option('product')
                    page.wait_for_timeout(300)
                    page.screenshot(path=os.path.join(output_dir, 'test-12-product.png'))

                    product_input = page.locator('.product-select-wrapper input').first
                    if product_input.count() > 0:
                        product_input.click()
                        page.wait_for_timeout(500)
                        page.screenshot(path=os.path.join(output_dir, 'test-13-product-click.png'))

                        modal = page.locator('.modal.show')
                        if modal.count() > 0 and modal.is_visible():
                            print("  CORRECT: Modal appeared for product")
                        else:
                            print("  INCORRECT: Modal did not appear for product")
                else:
                    print("   No jump selects found")
                    all_selects = page.locator('select').all()
                    print(f"   All selects: {len(all_selects)}")
                    for s in all_selects[:10]:
                        print(f"     {s.get_attribute('class')}")
        else:
            print("   No suitable component found")
    else:
        print("   Components tab not found")

    page.screenshot(path=os.path.join(output_dir, 'test-final.png'))
    browser.close()
    print("\n=== Test Complete ===")