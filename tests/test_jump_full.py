from playwright.sync_api import sync_playwright
import os

# Output directory for screenshots
output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Use headless=False to see the interaction
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    print("=== Testing Jump Type Dropdown Functionality ===\n")

    # Navigate to editor.html using file:// URL
    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder\preview\editor.html'
    page.goto(f'file://{file_path}')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)  # Wait for page initialization

    print("1. Initial page loaded")
    page.screenshot(path=os.path.join(output_dir, 'test-01-initial.png'))

    # Find component library tabs - there should be tabs like "基础组件" or "营销组件"
    tabs = page.locator('.editor-side-tab').all()
    print(f"\nFound {len(tabs)} tabs in sidebar")
    for t in tabs:
        try:
            text = t.inner_text()
            print(f"  - Tab: '{text}'")
        except:
            pass

    # Look for component types in the component panel
    # Based on the code analysis, there should be elements with data-type attributes
    comp_types = page.locator('[data-type]').all()
    print(f"\nFound {len(comp_types)} elements with data-type:")
    for c in comp_types:
        try:
            dt = c.get_attribute('data-type')
            cls = c.get_attribute('class') or ''
            print(f"  - data-type='{dt}' | class='{cls[:30]}'")
        except:
            pass

    # Step 2: Click on a component type to add it (e.g., banner/carousel)
    # Based on code analysis, there might be component types in a panel that needs to be clicked

    # First, let's check what tabs are available and click on the one that might have components
    # Try clicking on different tabs to find components
    print("\n2. Trying to find component library...")

    # Check if there's a component panel with items to click
    # The code shows elements with data-type like 'brand', 'tag', 'category', 'product'
    # These might be navigation types, not component types

    # Let's look for a "添加楼层" or similar button
    add_buttons = page.locator('button:has-text("添加"), button:has-text("+"), .empty-btn').all()
    print(f"\nFound {len(add_buttons)} add buttons")
    for ab in add_buttons[:5]:
        try:
            text = ab.inner_text()
            cls = ab.get_attribute('class') or ''
            print(f"  - Button: '{text[:20]}' | class='{cls[:30]}'")
        except:
            pass

    # Try to add a floor/component
    # Look for the "添加楼层" button
    try:
        add_floor_btn = page.locator('text=添加楼层').first
        if add_floor_btn.is_visible():
            print("\n3. Clicking '添加楼层' button...")
            add_floor_btn.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(output_dir, 'test-02-add-floor-click.png'))

            # Now check what options appear
            floor_types = page.locator('.floor-type-item, .component-type-item, [data-floor-type]').all()
            print(f"Found {len(floor_types)} floor type options")
            for ft in floor_types[:10]:
                try:
                    text = ft.inner_text()
                    print(f"  - Floor type: '{text}'")
                except:
                    pass

            # Click on banner/carousel if available
            carousel_option = page.locator('text=轮播图, text=Banner, text=图片轮播').first
            if carousel_option.is_visible():
                print("  - Clicking on carousel/banner option...")
                carousel_option.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'test-03-carousel-added.png'))
        else:
            print("  - '添加楼层' button not visible")
    except Exception as e:
        print(f"  - Error: {e}")

    # Alternative: Look for empty state button
    try:
        empty_btn = page.locator('.empty-btn').first
        if empty_btn.is_visible():
            print("\n3. Clicking empty state button to add content...")
            empty_btn.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(output_dir, 'test-02-empty-click.png'))
    except Exception as e:
        print(f"  - Empty button not found: {e}")

    # Step 4: Check the properties panel for jump configuration
    print("\n4. Checking properties panel for jump configuration...")

    # Look for the properties/props panel
    props_panel = page.locator('.props-panel, .component-props-panel, #props-panel, .editor-props-panel')
    if props_panel.count() > 0:
        print(f"  - Properties panel found ({props_panel.count()} elements)")
        page.screenshot(path=os.path.join(output_dir, 'test-04-props-panel.png'))

        # Find jump type selectors
        jump_selects = page.locator('.carousel-jump-type, .jump-type, select[class*="jump"]').all()
        print(f"  - Jump type selectors found: {len(jump_selects)}")
        for js in jump_selects:
            try:
                cls = js.get_attribute('class')
                idx = js.get_attribute('data-index')
                print(f"    - class='{cls}' | data-index='{idx}'")
            except:
                pass

        # If we found a jump type selector, test it
        if len(jump_selects) > 0:
            jump_select = jump_selects[0]
            print("\n5. Testing jump type selector...")

            # Test Category (分类)
            print("\n=== Testing 分类 (category) ===")
            jump_select.select_option('category')
            page.wait_for_timeout(300)
            page.screenshot(path=os.path.join(output_dir, 'test-05-category-selected.png'))

            # Find the category target input
            cat_input = page.locator('.carousel-jump-target-display, .searchable-dropdown-input').first
            if cat_input.is_visible():
                print("  - Category input found, clicking...")
                cat_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'test-06-category-input-click.png'))

                # Check what appeared: dropdown (correct) or modal (incorrect)
                dropdown = page.locator('.searchable-dropdown.open, .searchable-dropdown-panel')
                modal = page.locator('.modal.show, #modal-single-product.show')

                if dropdown.is_visible():
                    print("  - ✅ CORRECT: Dropdown panel appeared")
                elif modal.is_visible():
                    print("  - ❌ INCORRECT: Modal appeared (should be dropdown)")
                else:
                    print("  - ⚠️ Neither dropdown nor modal visible")

                # Get the actual element that appeared
                visible_elements = page.locator('.searchable-dropdown.open, .modal.show, [style*="display: block"], [style*="visibility: visible"]').all()
                print(f"  - Visible overlay elements: {len(visible_elements)}")
                for ve in visible_elements[:5]:
                    try:
                        cls = ve.get_attribute('class')
                        id_attr = ve.get_attribute('id')
                        print(f"    - class='{cls}' | id='{id_attr}'")
                    except:
                        pass

                page.keyboard.press('Escape')
                page.wait_for_timeout(300)

            # Test Brand (品牌)
            print("\n=== Testing 品牌 (brand) ===")
            jump_select.select_option('brand')
            page.wait_for_timeout(300)
            page.screenshot(path=os.path.join(output_dir, 'test-07-brand-selected.png'))

            brand_input = page.locator('.carousel-jump-target-display, .searchable-dropdown-input').first
            if brand_input.is_visible():
                print("  - Brand input found, clicking...")
                brand_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'test-08-brand-input-click.png'))

                dropdown = page.locator('.searchable-dropdown.open, .searchable-dropdown-panel')
                modal = page.locator('.modal.show')

                if dropdown.is_visible():
                    print("  - ✅ CORRECT: Dropdown panel appeared")
                elif modal.is_visible():
                    print("  - ❌ INCORRECT: Modal appeared (should be dropdown)")
                else:
                    print("  - ⚠️ Neither dropdown nor modal visible")

                page.keyboard.press('Escape')
                page.wait_for_timeout(300)

            # Test Tag (标签)
            print("\n=== Testing 标签 (tag) ===")
            jump_select.select_option('tag')
            page.wait_for_timeout(300)
            page.screenshot(path=os.path.join(output_dir, 'test-09-tag-selected.png'))

            tag_input = page.locator('.carousel-jump-target-display, .searchable-dropdown-input').first
            if tag_input.is_visible():
                print("  - Tag input found, clicking...")
                tag_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'test-10-tag-input-click.png'))

                dropdown = page.locator('.searchable-dropdown.open, .searchable-dropdown-panel')
                modal = page.locator('.modal.show')

                if dropdown.is_visible():
                    print("  - ✅ CORRECT: Dropdown panel appeared")
                elif modal.is_visible():
                    print("  - ❌ INCORRECT: Modal appeared (should be dropdown)")
                else:
                    print("  - ⚠️ Neither dropdown nor modal visible")

                page.keyboard.press('Escape')
                page.wait_for_timeout(300)

            # Test Product (单商品详情页) - this SHOULD open a modal
            print("\n=== Testing 单商品详情页 (product) - should open modal ===")
            jump_select.select_option('product')
            page.wait_for_timeout(300)
            page.screenshot(path=os.path.join(output_dir, 'test-11-product-selected.png'))

            product_input = page.locator('.carousel-jump-target-display, .product-select-wrapper input').first
            if product_input.is_visible():
                print("  - Product input found, clicking...")
                product_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'test-12-product-input-click.png'))

                modal = page.locator('.modal.show, #modal-single-product.show')
                if modal.is_visible():
                    print("  - ✅ CORRECT: Modal appeared for product selection")
                else:
                    print("  - ❌ INCORRECT: Modal did not appear for product")

                page.keyboard.press('Escape')
                page.wait_for_timeout(300)
        else:
            print("  - No jump type selectors found in properties panel")

            # Let's see what's in the properties panel
            print("\n  - Contents of properties panel:")
            props_items = page.locator('.props-panel *, .component-props-panel *').all()
            print(f"    - Total elements: {len(props_items)}")

            # Get inputs and selects
            inputs = props_panel.locator('input, select').all()
            print(f"    - Inputs/selects: {len(inputs)}")
            for inp in inputs[:10]:
                try:
                    cls = inp.get_attribute('class') or ''
                    typ = inp.get_attribute('type') or inp.evaluate('el => el.tagName')
                    id_attr = inp.get_attribute('id') or ''
                    print(f"      - type='{typ}' | class='{cls[:30]}' | id='{id_attr}'")
                except:
                    pass
    else:
        print("  - Properties panel not found")

    # Final state
    print("\n6. Final screenshot...")
    page.screenshot(path=os.path.join(output_dir, 'test-final.png'))

    browser.close()
    print("\n=== Test Complete ===")