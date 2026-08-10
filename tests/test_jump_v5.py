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

    print("1. Page loaded")

    # Create a new page
    print("\n2. Creating a new page...")
    page.locator('#btn-add-page').click()
    page.wait_for_timeout(500)

    # Select template and confirm
    template_cards = page.locator('.template-select-card').all()
    if len(template_cards) > 0:
        template_cards[0].click()
        page.wait_for_timeout(300)
        page.locator('#btn-add-page-confirm').click()
        page.wait_for_timeout(500)
        print("   Page created")

    # Click Components tab
    print("\n3. Opening Components tab...")
    page.locator('.editor-side-tab[data-panel="components"]').click()
    page.wait_for_timeout(500)

    # Add carousel component
    print("\n4. Adding carousel component...")
    page.evaluate('''() => {
        const dropzone = document.querySelector('.canvas-drop-zone');
        if (!dropzone) return;
        const event = new DragEvent('drop', {
            bubbles: true,
            cancelable: true,
            dataTransfer: new DataTransfer()
        });
        event.dataTransfer.setData('text/plain', 'carousel');
        event.dataTransfer.setData('application/x-editor-drag-kind', 'component');
        dropzone.dispatchEvent(event);
    }''')
    page.wait_for_timeout(500)

    # Check floors using correct selector
    floors = page.locator('.canvas-floor-card').all()
    print(f"   Floors: {len(floors)}")

    if len(floors) > 0:
        # Select the carousel floor
        carousel_floor = page.locator('.canvas-floor-card[data-floor-id*="carousel"]').first
        if carousel_floor.count() > 0:
            print("   Found carousel floor")
            carousel_floor.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(output_dir, 'test-floor-selected.png'))
            print("   Selected carousel floor")

            # Check properties panel
            print("\n5. Testing jump type functionality...")

            # Find jump type select
            jump_selects = page.locator('select[class*="jump"]').all()
            print(f"   Jump selects: {len(jump_selects)}")

            if len(jump_selects) > 0:
                jump_select = jump_selects[0]
                print(f"   Jump select class: {jump_select.get_attribute('class')}")

                # Test Category
                print("\n=== Testing Category (分类) ===")
                jump_select.select_option('category')
                page.wait_for_timeout(300)

                cat_input = page.locator('.searchable-dropdown-input').first
                if cat_input.count() > 0:
                    cat_input.click()
                    page.wait_for_timeout(500)
                    page.screenshot(path=os.path.join(output_dir, 'test-category-click.png'))

                    dropdown = page.locator('.searchable-dropdown.open')
                    modal = page.locator('.modal.show')

                    if dropdown.count() > 0:
                        print("   CORRECT: Dropdown panel opened")
                    elif modal.count() > 0:
                        print("   INCORRECT: Modal opened (should be dropdown)")
                        print(f"   Modal ID: {modal.get_attribute('id')}")
                    else:
                        print("   Neither dropdown nor modal visible")

                    page.keyboard.press('Escape')
                    page.wait_for_timeout(200)

                # Test Brand
                print("\n=== Testing Brand (品牌) ===")
                jump_select.select_option('brand')
                page.wait_for_timeout(300)

                brand_input = page.locator('.searchable-dropdown-input').first
                if brand_input.count() > 0:
                    brand_input.click()
                    page.wait_for_timeout(500)
                    page.screenshot(path=os.path.join(output_dir, 'test-brand-click.png'))

                    dropdown = page.locator('.searchable-dropdown.open')
                    modal = page.locator('.modal.show')

                    if dropdown.count() > 0:
                        print("   CORRECT: Dropdown panel opened")
                    elif modal.count() > 0:
                        print("   INCORRECT: Modal opened (should be dropdown)")
                    else:
                        print("   Neither visible")

                    page.keyboard.press('Escape')
                    page.wait_for_timeout(200)

                # Test Tag
                print("\n=== Testing Tag (标签) ===")
                jump_select.select_option('tag')
                page.wait_for_timeout(300)

                tag_input = page.locator('.searchable-dropdown-input').first
                if tag_input.count() > 0:
                    tag_input.click()
                    page.wait_for_timeout(500)
                    page.screenshot(path=os.path.join(output_dir, 'test-tag-click.png'))

                    dropdown = page.locator('.searchable-dropdown.open')
                    modal = page.locator('.modal.show')

                    if dropdown.count() > 0:
                        print("   CORRECT: Dropdown panel opened")
                    elif modal.count() > 0:
                        print("   INCORRECT: Modal opened (should be dropdown)")
                    else:
                        print("   Neither visible")

                    page.keyboard.press('Escape')
                    page.wait_for_timeout(200)

                # Test Product (should open modal)
                print("\n=== Testing Product (should open modal) ===")
                jump_select.select_option('product')
                page.wait_for_timeout(300)

                product_input = page.locator('.product-select-wrapper input').first
                if product_input.count() > 0:
                    product_input.click()
                    page.wait_for_timeout(500)
                    page.screenshot(path=os.path.join(output_dir, 'test-product-click.png'))

                    modal = page.locator('.modal.show')
                    if modal.count() > 0:
                        print("   CORRECT: Modal opened for product selection")
                    else:
                        print("   INCORRECT: Modal did not open")
            else:
                print("   No jump selects found")
                # Debug
                all_selects = page.locator('select').all()
                print(f"   All select elements: {len(all_selects)}")
                for s in all_selects[:10]:
                    cls = s.get_attribute('class') or ''
                    id_attr = s.get_attribute('id') or ''
                    print(f"     class={cls} id={id_attr}")
        else:
            print("   Carousel floor not found")
            # List all floors
            for f in floors:
                floor_id = f.get_attribute('data-floor-id')
                print(f"   Floor ID: {floor_id}")
    else:
        print("   No floors found")

    page.screenshot(path=os.path.join(output_dir, 'test-final.png'))
    browser.close()
    print("\n=== Test Complete ===")