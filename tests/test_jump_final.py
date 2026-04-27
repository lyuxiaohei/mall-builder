from playwright.sync_api import sync_playwright
import os

output_dir = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\docs'
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1400, "height": 900})

    print("=== Testing Jump Type Dropdown Functionality ===\n")

    file_path = r'C:\Users\Administrator\Documents\qoder_project\mall-builder-prototype\preview\editor.html'
    page.goto('file:///' + file_path.replace('\\', '/'))
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Create a new page
    print("1. Creating a new page...")
    page.locator('#btn-add-page').click()
    page.wait_for_timeout(500)
    page.locator('.template-select-card').first.click()
    page.wait_for_timeout(300)
    page.locator('#btn-add-page-confirm').click()
    page.wait_for_timeout(500)
    print("   Page created")

    # Click Components tab and add carousel
    print("\n2. Adding carousel component...")
    page.locator('.editor-side-tab[data-panel="components"]').click()
    page.wait_for_timeout(500)

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

    # Select the carousel floor
    carousel_floor = page.locator('.canvas-floor-card[data-floor-id*="carousel"]').first
    if carousel_floor.count() > 0:
        carousel_floor.click()
        page.wait_for_timeout(500)
        print("   Carousel component added and selected")

    # Test jump types
    print("\n3. Testing jump type functionality...")
    jump_select = page.locator('select.carousel-jump-type').first
    if jump_select.count() > 0:
        print("   Found jump type selector")

        # Test Category
        print("\n=== TEST 1: Category (分类) ===")
        jump_select.select_option('category')
        page.wait_for_timeout(300)

        # Check what appeared in the jump target area
        target_area = page.locator('.jump-target-wrapper').first
        print(f"   Target area HTML: {target_area.inner_html()[:200]}")

        # Find and click the searchable dropdown input
        cat_input = page.locator('.searchable-dropdown-input').first
        if cat_input.count() > 0:
            print(f"   Found dropdown input, placeholder: {cat_input.get_attribute('placeholder')}")
            cat_input.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(output_dir, 'test-category-click.png'))

            # Check what appeared
            dropdown = page.locator('.searchable-dropdown.open')
            modal = page.locator('.modal.show')

            print(f"   Dropdown visible: {dropdown.count() > 0}")
            print(f"   Modal visible: {modal.count() > 0}")

            if modal.count() > 0:
                modal_id = modal.get_attribute('id')
                print(f"   *** BUG FOUND: Modal '{modal_id}' opened instead of dropdown! ***")

            if dropdown.count() > 0:
                print("   CORRECT: Dropdown panel opened")

            # Close any open elements
            page.keyboard.press('Escape')
            page.wait_for_timeout(300)
            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

        # Test Brand
        print("\n=== TEST 2: Brand (品牌) ===")
        jump_select.select_option('brand')
        page.wait_for_timeout(300)

        # Check if any modals are still open
        open_modals = page.locator('.modal.show').all()
        print(f"   Open modals before click: {len(open_modals)}")

        brand_input = page.locator('.searchable-dropdown-input').first
        if brand_input.count() > 0:
            try:
                brand_input.click(timeout=2000)
            except Exception as e:
                print(f"   Click failed: {str(e)[:100]}")
                # Check what's blocking
                modal_blocking = page.locator('.modal.show').first
                if modal_blocking.count() > 0:
                    print(f"   Blocking modal: {modal_blocking.get_attribute('id')}")

            page.screenshot(path=os.path.join(output_dir, 'test-brand-click.png'))

            dropdown = page.locator('.searchable-dropdown.open')
            modal = page.locator('.modal.show')

            if dropdown.count() > 0:
                print("   CORRECT: Dropdown panel opened for brand")
            elif modal.count() > 0:
                print(f"   INCORRECT: Modal opened: {modal.get_attribute('id')}")
            else:
                print("   Nothing visible")

            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

        # Test Tag
        print("\n=== TEST 3: Tag (标签) ===")
        jump_select.select_option('tag')
        page.wait_for_timeout(300)

        tag_input = page.locator('.searchable-dropdown-input').first
        if tag_input.count() > 0:
            try:
                tag_input.click(timeout=2000)
            except:
                # Close any blocking modals first
                page.keyboard.press('Escape')
                page.wait_for_timeout(300)
                tag_input.click()

            page.screenshot(path=os.path.join(output_dir, 'test-tag-click.png'))

            dropdown = page.locator('.searchable-dropdown.open')
            modal = page.locator('.modal.show')

            if dropdown.count() > 0:
                print("   CORRECT: Dropdown panel opened for tag")
            elif modal.count() > 0:
                print(f"   INCORRECT: Modal opened: {modal.get_attribute('id')}")
            else:
                print("   Nothing visible")

            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

        # Test Product (should open modal)
        print("\n=== TEST 4: Product (单商品详情页) - Should open modal ===")
        jump_select.select_option('product')
        page.wait_for_timeout(300)

        product_input = page.locator('.product-select-wrapper input').first
        if product_input.count() > 0:
            try:
                product_input.click(timeout=2000)
            except:
                page.keyboard.press('Escape')
                page.wait_for_timeout(300)
                product_input.click()

            page.screenshot(path=os.path.join(output_dir, 'test-product-click.png'))

            modal = page.locator('.modal.show')
            if modal.count() > 0:
                print(f"   CORRECT: Modal opened: {modal.get_attribute('id')}")
            else:
                print("   INCORRECT: Modal did not open")

    page.screenshot(path=os.path.join(output_dir, 'test-final.png'))
    browser.close()
    print("\n=== Test Complete ===")