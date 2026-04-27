from playwright.sync_api import sync_playwright
import os

# Output directory for screenshots
output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Use headless=False to see the interaction
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    print("1. Navigate to editor.html...")
    page.goto('http://localhost:3000/editor.html')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)  # Wait for initial setup

    # Take initial screenshot
    page.screenshot(path=os.path.join(output_dir, 'step1-initial.png'))
    print("   - Initial screenshot saved")

    print("2. Add a banner component to test jump configuration...")
    # Find and click the add component button
    # Look for the component library panel

    # Get the page content to find selectors
    page_content = page.content()

    # Try to find banner component in component library
    # Based on the code, components are in a library panel with drag capability

    # Look for "轮播图" or "banner" component button
    try:
        # First, let's check if there's a component list
        banner_btn = page.locator('text=轮播图').first
        if banner_btn.is_visible():
            banner_btn.click()
            print("   - Clicked 轮播图 button")
        else:
            # Try alternative: icon-nav or banner
            banner_btn = page.locator('[data-type="banner"]').first
            if banner_btn.is_visible():
                banner_btn.click()
                print("   - Clicked banner data-type button")
            else:
                # Look in component library panel
                comp_lib = page.locator('.component-library-item, .comp-item, [draggable="true"]')
                all_comps = comp_lib.all()
                print(f"   - Found {len(all_comps)} draggable components")
                for comp in all_comps[:5]:
                    text = comp.inner_text()
                    print(f"     - Component text: {text}")

                # Try clicking on first draggable that contains banner/carousel related text
                for comp in all_comps:
                    text = comp.inner_text()
                    if '轮播' in text or 'banner' in text.lower() or 'Banner' in text:
                        comp.click()
                        print(f"   - Clicked component: {text}")
                        break
    except Exception as e:
        print(f"   - Error finding banner: {e}")

    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(output_dir, 'step2-add-banner.png'))

    print("3. Now test the jump type selector...")
    # After adding banner, it should be selected and show properties panel
    # Find the jump type selector

    # Based on the code analysis, the jump type selector has class like 'carousel-jump-type'
    # or is within the properties panel

    props_panel = page.locator('.props-panel, .component-props-panel, #props-panel')
    if props_panel.is_visible():
        print("   - Properties panel is visible")

        # Find jump type select
        jump_select = page.locator('.carousel-jump-type, .jump-type-select, select[data-index]').first
        if jump_select.is_visible():
            print("   - Found jump type selector")

            # Test Category (分类)
            print("4. Testing 分类 (category) jump type...")
            jump_select.select_option('category')
            page.wait_for_timeout(500)

            # Now find the target input for category
            # This should be a searchable dropdown, NOT a modal
            cat_input = page.locator('.carousel-jump-target-display, .searchable-dropdown-input').first
            if cat_input.is_visible():
                print("   - Category target input found")
                cat_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'step3-category-click.png'))

                # Check if a dropdown panel appeared (correct) or modal appeared (incorrect)
                dropdown_panel = page.locator('.searchable-dropdown-panel, .searchable-dropdown.open')
                modal = page.locator('.modal.show, #modal-single-product.show')

                if dropdown_panel.is_visible():
                    print("   - CORRECT: Dropdown panel is visible")
                elif modal.is_visible():
                    print("   - INCORRECT: Modal appeared instead of dropdown")
                else:
                    print("   - Neither dropdown nor modal visible")
                    # Check what elements appeared
                    page.screenshot(path=os.path.join(output_dir, 'step3-category-state.png'))
            else:
                print("   - Category target input NOT found")

            # Close any open dropdown/modal
            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

            # Test Brand (品牌)
            print("5. Testing 品牌 (brand) jump type...")
            jump_select.select_option('brand')
            page.wait_for_timeout(500)

            brand_input = page.locator('.carousel-jump-target-display').first
            if brand_input.is_visible():
                print("   - Brand target input found")
                brand_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'step4-brand-click.png'))

                dropdown_panel = page.locator('.searchable-dropdown-panel, .searchable-dropdown.open')
                modal = page.locator('.modal.show')

                if dropdown_panel.is_visible():
                    print("   - CORRECT: Dropdown panel is visible")
                elif modal.is_visible():
                    print("   - INCORRECT: Modal appeared instead of dropdown")
                else:
                    print("   - Neither dropdown nor modal visible")

            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

            # Test Tag (标签)
            print("6. Testing 标签 (tag) jump type...")
            jump_select.select_option('tag')
            page.wait_for_timeout(500)

            tag_input = page.locator('.carousel-jump-target-display').first
            if tag_input.is_visible():
                print("   - Tag target input found")
                tag_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'step5-tag-click.png'))

                dropdown_panel = page.locator('.searchable-dropdown-panel, .searchable-dropdown.open')
                modal = page.locator('.modal.show')

                if dropdown_panel.is_visible():
                    print("   - CORRECT: Dropdown panel is visible")
                elif modal.is_visible():
                    print("   - INCORRECT: Modal appeared instead of dropdown")
                else:
                    print("   - Neither dropdown nor modal visible")

            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

            # Test Product (单商品详情页) - this SHOULD open a modal
            print("7. Testing 单商品详情页 (product) jump type - should open modal...")
            jump_select.select_option('product')
            page.wait_for_timeout(500)

            product_input = page.locator('.carousel-jump-target-display, .product-select-wrapper input').first
            if product_input.is_visible():
                print("   - Product target input found")
                product_input.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(output_dir, 'step6-product-click.png'))

                modal = page.locator('.modal.show, #modal-single-product.show')
                if modal.is_visible():
                    print("   - CORRECT: Modal appeared for product selection")
                else:
                    print("   - INCORRECT: Modal did not appear for product selection")
        else:
            print("   - Jump type selector NOT found")
            # Take screenshot of current state
            page.screenshot(path=os.path.join(output_dir, 'props-panel-state.png'))

            # List all select elements
            selects = page.locator('select').all()
            print(f"   - Found {len(selects)} select elements")
            for s in selects[:5]:
                try:
                    cls = s.get_attribute('class')
                    print(f"     - Select class: {cls}")
                except:
                    pass
    else:
        print("   - Properties panel NOT visible")

    print("8. Test complete. Final screenshot...")
    page.screenshot(path=os.path.join(output_dir, 'step-final.png'))

    browser.close()
    print("Browser closed. Test finished.")