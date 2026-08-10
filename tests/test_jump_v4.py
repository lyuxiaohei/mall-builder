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
    page.screenshot(path=os.path.join(output_dir, 'test-01-initial.png'))

    # Step 2: Click "+ 新增页面" button to create a page
    print("\n2. Creating a new page...")
    add_page_btn = page.locator('#btn-add-page')
    if add_page_btn.count() > 0:
        add_page_btn.click()
        page.wait_for_timeout(500)
        print("   Clicked add page button")
        page.screenshot(path=os.path.join(output_dir, 'test-02-add-page-modal.png'))

        # Check if modal appeared
        modal = page.locator('#modal-add-page.show')
        if modal.count() > 0:
            print("   Add page modal opened")

            # Select a template (step through the modal)
            # First, look for template cards to select
            template_cards = page.locator('.template-select-card').all()
            print(f"   Template cards: {len(template_cards)}")

            if len(template_cards) > 0:
                # Click first template card
                template_cards[0].click()
                page.wait_for_timeout(300)
                print("   Selected first template")

                # Click confirm button
                confirm_btn = page.locator('#btn-add-page-confirm')
                if confirm_btn.count() > 0:
                    confirm_btn.click()
                    page.wait_for_timeout(500)
                    print("   Confirmed page creation")
                    page.screenshot(path=os.path.join(output_dir, 'test-03-page-created.png'))

                    # Step 3: Click on "组件" tab
                    print("\n3. Clicking Components tab...")
                    comp_tab = page.locator('.editor-side-tab[data-panel="components"]')
                    if comp_tab.count() > 0:
                        comp_tab.click()
                        page.wait_for_timeout(500)
                        print("   Clicked Components tab")
                        page.screenshot(path=os.path.join(output_dir, 'test-04-components-tab.png'))

                        # Check available components
                        comp_items = page.locator('.component-item').all()
                        print(f"   Components: {len(comp_items)}")

                        # Step 4: Add a carousel component via drag-drop simulation
                        print("\n4. Adding carousel component...")

                        # Use JavaScript to simulate the drop
                        result = page.evaluate('''() => {
                            const dropzone = document.querySelector('.canvas-drop-zone');
                            if (!dropzone) return 'no dropzone';

                            const event = new DragEvent('drop', {
                                bubbles: true,
                                cancelable: true,
                                dataTransfer: new DataTransfer()
                            });
                            event.dataTransfer.setData('text/plain', 'carousel');
                            event.dataTransfer.setData('application/x-editor-drag-kind', 'component');
                            dropzone.dispatchEvent(event);

                            return 'drop dispatched';
                        }''')
                        print(f"   Drop result: {result}")
                        page.wait_for_timeout(500)
                        page.screenshot(path=os.path.join(output_dir, 'test-05-component-added.png'))

                        # Step 5: Check for floors on canvas
                        floors = page.locator('.canvas-floor').all()
                        print(f"   Floors after drop: {len(floors)}")

                        if len(floors) > 0:
                            # Click on the floor to select it
                            floors[0].click()
                            page.wait_for_timeout(500)
                            print("   Selected floor")
                            page.screenshot(path=os.path.join(output_dir, 'test-06-floor-selected.png'))

                            # Step 6: Check properties panel for jump config
                            print("\n5. Testing jump type functionality...")

                            # Find jump type select
                            jump_selects = page.locator('select[class*="jump"]').all()
                            print(f"   Jump selects: {len(jump_selects)}")

                            if len(jump_selects) > 0:
                                jump_select = jump_selects[0]
                                cls = jump_select.get_attribute('class')
                                print(f"   Jump select class: {cls}")

                                # Test Category
                                print("\n=== Testing Category ===")
                                jump_select.select_option('category')
                                page.wait_for_timeout(300)

                                cat_input = page.locator('.searchable-dropdown-input').first
                                if cat_input.count() > 0:
                                    cat_input.click()
                                    page.wait_for_timeout(500)
                                    page.screenshot(path=os.path.join(output_dir, 'test-07-category-click.png'))

                                    dropdown = page.locator('.searchable-dropdown.open')
                                    modal_el = page.locator('.modal.show')

                                    if dropdown.count() > 0:
                                        print("   CORRECT: Dropdown opened for category")
                                    elif modal_el.count() > 0:
                                        print("   INCORRECT: Modal opened (should be dropdown)")
                                    else:
                                        print("   Neither visible")

                                    page.keyboard.press('Escape')
                                    page.wait_for_timeout(200)

                                # Test Brand
                                print("\n=== Testing Brand ===")
                                jump_select.select_option('brand')
                                page.wait_for_timeout(300)

                                brand_input = page.locator('.searchable-dropdown-input').first
                                if brand_input.count() > 0:
                                    brand_input.click()
                                    page.wait_for_timeout(500)
                                    page.screenshot(path=os.path.join(output_dir, 'test-08-brand-click.png'))

                                    dropdown = page.locator('.searchable-dropdown.open')
                                    modal_el = page.locator('.modal.show')

                                    if dropdown.count() > 0:
                                        print("   CORRECT: Dropdown opened for brand")
                                    elif modal_el.count() > 0:
                                        print("   INCORRECT: Modal opened (should be dropdown)")
                                    else:
                                        print("   Neither visible")

                                    page.keyboard.press('Escape')
                                    page.wait_for_timeout(200)

                                # Test Tag
                                print("\n=== Testing Tag ===")
                                jump_select.select_option('tag')
                                page.wait_for_timeout(300)

                                tag_input = page.locator('.searchable-dropdown-input').first
                                if tag_input.count() > 0:
                                    tag_input.click()
                                    page.wait_for_timeout(500)
                                    page.screenshot(path=os.path.join(output_dir, 'test-09-tag-click.png'))

                                    dropdown = page.locator('.searchable-dropdown.open')
                                    modal_el = page.locator('.modal.show')

                                    if dropdown.count() > 0:
                                        print("   CORRECT: Dropdown opened for tag")
                                    elif modal_el.count() > 0:
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
                                    page.screenshot(path=os.path.join(output_dir, 'test-10-product-click.png'))

                                    modal_el = page.locator('.modal.show')
                                    if modal_el.count() > 0:
                                        print("   CORRECT: Modal opened for product")
                                    else:
                                        print("   INCORRECT: Modal did not open")
                            else:
                                print("   No jump selects found - debugging...")
                                all_selects = page.locator('select').all()
                                print(f"   All selects: {len(all_selects)}")
                                for s in all_selects[:5]:
                                    print(f"     {s.get_attribute('class')}")
                        else:
                            print("   No floors created - checking canvas...")
                            floor_list = page.locator('#canvas-floor-list')
                            print(f"   Floor list content: {floor_list.inner_html()[:200]}")
                    else:
                        print("   Components tab not found")
                else:
                    print("   Confirm button not found")
            else:
                print("   No template cards found")
        else:
            print("   Modal did not open")
    else:
        print("   Add page button not found")

    page.screenshot(path=os.path.join(output_dir, 'test-final.png'))
    browser.close()
    print("\n=== Test Complete ===")