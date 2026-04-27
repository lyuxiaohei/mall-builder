from playwright.sync_api import sync_playwright
import os

# Output directory for screenshots
output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900}")

    print("=== Testing Jump Type Dropdown Functionality ===\n")

    # Navigate to editor.html using file:// URL
    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\preview\editor.html'
    page.goto(f'file://{file_path}')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    print("1. Initial page loaded")
    page.screenshot(path=os.path.join(output_dir, 'test-01-initial.png'))

    # Step 2: Click on the "组件" (Components) tab in the sidebar
    print("\n2. Clicking on the '组件' tab...")
    # The tabs are: 主页面, 子页面, 组件
    comp_tab = page.locator('.editor-side-tab[data-panel="components"]')
    if comp_tab.count() > 0:
        comp_tab.click()
        page.wait_for_timeout(1000)
        print("   - Clicked '组件' tab")
        page.screenshot(path=os.path.join(output_dir, 'test-02-components-tab.png'))

        # Check what components are available
        comp_items = page.locator('.component-item').all()
        print(f"   - Found {len(comp_items)} components available")
        for ci in comp_items[:10]:
            try:
                comp_type = ci.get_attribute('data-component-type')
                text = ci.inner_text()[:50]
                print(f"     - type='{comp_type}' | text='{text}'")
            except:
                pass

        # Step 3: Drag a carousel/banner component to the canvas
        print("\n3. Dragging a component to the canvas...")

        # Find a carousel component (轮播图)
        carousel_item = page.locator('.component-item[data-component-type="carousel"]').first
        if carousel_item.count() == 0:
            # Try other names
            carousel_item = page.locator('.component-item[data-component-type="banner"]').first
        if carousel_item.count() == 0:
            # List all available component types
            print("   - Available component types:")
            for ci in comp_items:
                comp_type = ci.get_attribute('data-component-type')
                print(f"     - '{comp_type}'")

            # Use the first available component that might have jump config
            # icon-nav or carousel typically have jump config
            for ci in comp_items:
                comp_type = ci.get_attribute('data-component-type') or ''
                if 'carousel' in comp_type or 'banner' in comp_type or 'icon-nav' in comp_type or 'nav' in comp_type:
                    carousel_item = ci
                    print(f"   - Found component with jump config: '{comp_type}'")
                    break

        if carousel_item.count() > 0:
            # Find the drop zone (canvas area)
            drop_zone = page.locator('.canvas-floor-dropzone, .canvas-floors, #canvas-floors').first
            if drop_zone.count() == 0:
                drop_zone = page.locator('.canvas-body').first

            # Perform drag and drop
            carousel_item.hover()
            page.wait_for_timeout(200)

            # Use evaluate to perform drag event simulation
            page.evaluate('''() => {
                const component = document.querySelector('.component-item[data-component-type="carousel"], .component-item[data-component-type="icon-nav"]');
                const dropzone = document.querySelector('.canvas-floor-dropzone, .canvas-floors, .canvas-body');
                if (!component || !dropzone) return;

                // Simulate drag
                const dragStartEvent = new DragEvent('dragstart', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: new DataTransfer()
                });
                dragStartEvent.dataTransfer.setData('text/plain', component.dataset.componentType);
                dragStartEvent.dataTransfer.setData('application/x-editor-drag-kind', 'component');
                component.dispatchEvent(dragStartEvent);

                // Simulate drop
                const dropEvent = new DragEvent('drop', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dragStartEvent.dataTransfer
                });
                dropzone.dispatchEvent(dropEvent);
            }''')

            page.wait_for_timeout(500)
            print("   - Component dropped to canvas")
            page.screenshot(path=os.path.join(output_dir, 'test-03-component-added.png'))

            # Step 4: Select the added floor/component
            print("\n4. Selecting the added component...")
            floors = page.locator('.canvas-floor').all()
            print(f"   - Found {len(floors)} floors on canvas")

            if len(floors) > 0:
                # Click on the first floor to select it
                floors[0].click()
                page.wait_for_timeout(500)
                print("   - Selected the first floor")
                page.screenshot(path=os.path.join(output_dir, 'test-04-floor-selected.png'))

                # Step 5: Check the properties panel for jump configuration
                print("\n5. Checking properties panel for jump configuration...")
                props_panel = page.locator('.props-panel, .component-props-panel, #props-panel')
                if props_panel.count() > 0:
                    print("   - Properties panel found")
                    page.screenshot(path=os.path.join(output_dir, 'test-05-props-panel.png'))

                    # Find jump type selectors
                    jump_selects = page.locator('select[class*="jump"]').all()
                    print(f"   - Jump type selects: {len(jump_selects)}")
                    for js in jump_selects[:5]:
                        cls = js.get_attribute('class')
                        print(f"     - class: '{cls}'")

                    if len(jump_selects) > 0:
                        jump_select = jump_selects[0]

                        # Test Category (分类)
                        print("\n=== Testing 分类 (category) ===")
                        jump_select.select_option('category')
                        page.wait_for_timeout(300)
                        page.screenshot(path=os.path.join(output_dir, 'test-06-category-selected.png'))

                        # Find the category target input
                        cat_input = page.locator('.searchable-dropdown-input').first
                        if cat_input.count() > 0:
                            print("  - Category input found, clicking...")
                            cat_input.click()
                            page.wait_for_timeout(500)
                            page.screenshot(path=os.path.join(output_dir, 'test-07-category-click.png'))

                            # Check what appeared
                            dropdown = page.locator('.searchable-dropdown.open')
                            modal = page.locator('.modal.show')

                            if dropdown.count() > 0 and dropdown.is_visible():
                                print("  - ✅ CORRECT: Dropdown panel appeared")
                            elif modal.count() > 0 and modal.is_visible():
                                print("  - ❌ INCORRECT: Modal appeared (should be dropdown)")
                                print(f"    Modal ID: {modal.get_attribute('id')}")
                            else:
                                print("  - ⚠️ Neither dropdown nor modal visible")

                            page.keyboard.press('Escape')
                            page.wait_for_timeout(300)

                        # Test Brand (品牌)
                        print("\n=== Testing 品牌 (brand) ===")
                        jump_select.select_option('brand')
                        page.wait_for_timeout(300)
                        page.screenshot(path=os.path.join(output_dir, 'test-08-brand-selected.png'))

                        brand_input = page.locator('.searchable-dropdown-input').first
                        if brand_input.count() > 0:
                            print("  - Brand input found, clicking...")
                            brand_input.click()
                            page.wait_for_timeout(500)
                            page.screenshot(path=os.path.join(output_dir, 'test-09-brand-click.png'))

                            dropdown = page.locator('.searchable-dropdown.open')
                            modal = page.locator('.modal.show')

                            if dropdown.count() > 0 and dropdown.is_visible():
                                print("  - ✅ CORRECT: Dropdown panel appeared")
                            elif modal.count() > 0 and modal.is_visible():
                                print("  - ❌ INCORRECT: Modal appeared (should be dropdown)")
                            else:
                                print("  - ⚠️ Neither dropdown nor modal visible")

                            page.keyboard.press('Escape')
                            page.wait_for_timeout(300)

                        # Test Tag (标签)
                        print("\n=== Testing 标签 (tag) ===")
                        jump_select.select_option('tag')
                        page.wait_for_timeout(300)
                        page.screenshot(path=os.path.join(output_dir, 'test-10-tag-selected.png'))

                        tag_input = page.locator('.searchable-dropdown-input').first
                        if tag_input.count() > 0:
                            print("  - Tag input found, clicking...")
                            tag_input.click()
                            page.wait_for_timeout(500)
                            page.screenshot(path=os.path.join(output_dir, 'test-11-tag-click.png'))

                            dropdown = page.locator('.searchable-dropdown.open')
                            modal = page.locator('.modal.show')

                            if dropdown.count() > 0 and dropdown.is_visible():
                                print("  - ✅ CORRECT: Dropdown panel appeared")
                            elif modal.count() > 0 and modal.is_visible():
                                print("  - ❌ INCORRECT: Modal appeared (should be dropdown)")
                            else:
                                print("  - ⚠️ Neither dropdown nor modal visible")

                            page.keyboard.press('Escape')
                            page.wait_for_timeout(300)

                        # Test Product (单商品详情页) - should open modal
                        print("\n=== Testing 单商品详情页 (product) ===")
                        jump_select.select_option('product')
                        page.wait_for_timeout(300)
                        page.screenshot(path=os.path.join(output_dir, 'test-12-product-selected.png'))

                        product_input = page.locator('.product-select-wrapper input').first
                        if product_input.count() > 0:
                            print("  - Product input found, clicking...")
                            product_input.click()
                            page.wait_for_timeout(500)
                            page.screenshot(path=os.path.join(output_dir, 'test-13-product-click.png'))

                            modal = page.locator('.modal.show')
                            if modal.count() > 0 and modal.is_visible():
                                print("  - ✅ CORRECT: Modal appeared for product selection")
                            else:
                                print("  - ❌ INCORRECT: Modal did not appear")

                            page.keyboard.press('Escape')
                            page.wait_for_timeout(300)
                    else:
                        print("   - No jump type selects found")

                        # Debug: List all select elements
                        all_selects = page.locator('select').all()
                        print(f"   - All select elements: {len(all_selects)}")
                        for s in all_selects[:10]:
                            cls = s.get_attribute('class') or ''
                            id_attr = s.get_attribute('id') or ''
                            print(f"     - class: '{cls}' | id: '{id_attr}'")
                else:
                    print("   - Properties panel not found")
            else:
                print("   - No floors on canvas")
        else:
            print("   - No carousel/banner component found")
    else:
        print("   - '组件' tab not found")

    print("\n6. Final screenshot...")
    page.screenshot(path=os.path.join(output_dir, 'test-final.png'))

    browser.close()
    print("\n=== Test Complete ===")