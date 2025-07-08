"""
Test the Real Automation System
Demonstrates the intelligent form detection and filling capabilities
"""

import asyncio
import json
from automation.intelligent_automation import IntelligentFormAutomation
from automation.data_parser import DataParser

async def test_form_detection():
    """Test form detection on a real website"""
    print("🔍 Testing Form Detection...")
    
    automation = IntelligentFormAutomation()
    
    try:
        # Initialize browser
        await automation.initialize_stealth_browser()
        
        # Create a new page
        page = await automation.context.new_page()
        
        # Test on a simple form website
        test_url = "https://www.w3schools.com/html/tryit.asp?filename=tryhtml_form_submit"
        
        print(f"📌 Navigating to: {test_url}")
        await page.goto(test_url)
        
        # Switch to iframe if needed
        frames = page.frames
        result_frame = None
        if len(frames) > 1:
            # Find the result frame
            for frame in frames:
                if 'iframeResult' in frame.name:
                    result_frame = frame
                    break
        
        # Detect forms
        from automation.form_detection import FormFieldDetector
        detector = FormFieldDetector()
        
        # Use the frame if found, otherwise use the main page
        target_page = result_frame if result_frame else page
        forms = await detector.detect_all_forms(target_page)
        
        print(f"\n✅ Found {len(forms)} forms")
        
        for i, form in enumerate(forms):
            print(f"\n📝 Form {i + 1}:")
            print(f"   - Fields: {len(form['fields'])}")
            
            for field in form['fields']:
                print(f"   - {field.get('label', 'No label')} ({field.get('purpose', 'unknown')})")
                print(f"     Type: {field.get('type')}, Name: {field.get('name')}")
        
        # Close the main page (not the frame)
        await automation.context.pages[0].close()
        
    finally:
        await automation.cleanup()

async def test_data_parser():
    """Test data parsing from different formats"""
    print("\n📄 Testing Data Parser...")
    
    parser = DataParser()
    
    # Test CSV parsing
    csv_content = """First Name,Last Name,Email,Phone
John,Doe,john.doe@example.com,555-123-4567
Jane,Smith,jane.smith@example.com,555-987-6543"""
    
    print("\n🔹 Testing CSV parsing:")
    csv_results = await parser.parse_file(csv_content, 'csv')
    for result in csv_results:
        print(f"   - {result.get('full_name', 'N/A')} | {result.get('email', 'N/A')}")
    
    # Test text parsing
    text_content = """
    Contact Information:
    Name: Alice Johnson
    Email: alice.johnson@example.com
    Phone: (555) 246-8135
    Address: 123 Main Street, New York, NY 10001
    Company: Tech Corp
    """
    
    print("\n🔹 Testing text parsing:")
    text_results = await parser.parse_file(text_content, 'txt')
    for result in text_results:
        print(f"   Parsed data: {json.dumps(result, indent=2)}")

async def test_full_automation():
    """Test the complete automation flow"""
    print("\n🚀 Testing Full Automation Flow...")
    
    # Sample user data
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com",
        "phone": "555-123-4567",
        "address": "123 Test Street",
        "city": "Test City",
        "state": "CA",
        "zip_code": "12345"
    }
    
    automation = IntelligentFormAutomation()
    
    # You can test with any form website
    # For demo, we'll use a test form
    test_url = "https://demoqa.com/automation-practice-form"
    
    print(f"\n📌 Testing automation on: {test_url}")
    print(f"📝 Using data: {json.dumps(user_data, indent=2)}")
    
    result = await automation.automate_form_filling(
        url=test_url,
        user_data=user_data,
        session_id="test-session",
        progress_callback=lambda update: print(f"   Progress: {update['progress']}% - {update['status']}")
    )
    
    print(f"\n✅ Automation completed!")
    print(f"   - Success: {result['success']}")
    print(f"   - Forms detected: {result['forms_detected']}")
    print(f"   - Fields filled: {result['fields_filled']}")
    print(f"   - Errors: {result['errors']}")
    
    # Save screenshots if any
    if result['screenshots']:
        print(f"   - Screenshots captured: {len(result['screenshots'])}")

async def main():
    """Run all tests"""
    print("🎯 AI LAM - Real Automation System Test\n")
    print("=" * 50)
    
    try:
        # Test form detection
        await test_form_detection()
        
        # Test data parser
        await test_data_parser()
        
        # Test full automation
        # await test_full_automation()
        
        print("\n✨ All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 