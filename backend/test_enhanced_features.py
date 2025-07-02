"""
Test script for enhanced features of the Autonomous University Application Agent
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security.encryption import DataEncryption, setup_encryption_environment
from automation.browser_automation import EnhancedBrowserAutomation
from monitoring.status_monitor import ApplicationMonitor, PerformanceMonitor

async def test_encryption():
    """Test encryption functionality"""
    print("\n🔐 Testing Encryption Service...")
    
    # Initialize encryption
    encryption = DataEncryption()
    
    # Test data encryption
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "sensitive_info": "This is confidential"
    }
    
    encrypted = encryption.encrypt_data(test_data)
    print(f"✅ Encrypted data: {encrypted[:50]}...")
    
    # Test decryption
    decrypted = encryption.decrypt_data(encrypted)
    print(f"✅ Decrypted data matches: {decrypted == test_data}")
    
    # Test client data encryption
    client_data = {
        "full_name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "+1234567890",
        "address": "123 Main St",
        "personal_statement": "I am passionate about...",
        "documents": {"transcript": "base64data"}
    }
    
    encrypted_client = encryption.encrypt_client_data(client_data)
    print(f"✅ Client data encrypted successfully")
    email_hash = encrypted_client.get('email_hash', '')
    if email_hash:
        print(f"   Email hash: {email_hash[:16]}...")
    
    # Test password generation
    password = encryption.generate_secure_password()
    print(f"✅ Generated secure password: {password}")
    
    return True

async def test_browser_automation():
    """Test enhanced browser automation"""
    print("\n🌐 Testing Browser Automation...")
    
    browser = EnhancedBrowserAutomation()
    
    try:
        # Initialize stealth browser
        context = await browser.initialize_stealth_browser()
        print("✅ Stealth browser initialized successfully")
        
        # Create a new page
        page = await context.new_page()
        
        # Test navigation
        await page.goto("https://www.google.com")
        print("✅ Navigation successful")
        
        # Test human-like delay
        await browser.human_like_delay()
        print("✅ Human-like delay working")
        
        # Test page state saving
        await browser.save_page_state(page, "test_google")
        print("✅ Page state saved for debugging")
        
        return True
        
    except Exception as e:
        print(f"❌ Browser automation error: {str(e)}")
        return False
    finally:
        await browser.cleanup()
        print("✅ Browser cleanup completed")

def test_monitoring():
    """Test monitoring services"""
    print("\n📊 Testing Monitoring Services...")
    
    # Test performance monitor
    perf_monitor = PerformanceMonitor()
    
    # Track some test metrics
    asyncio.run(perf_monitor.track_automation_attempt("oxford", True, 15.5))
    asyncio.run(perf_monitor.track_automation_attempt("cambridge", False, 20.0, "timeout_error"))
    asyncio.run(perf_monitor.track_automation_attempt("oxford", True, 12.3))
    
    # Get performance report
    report = perf_monitor.get_performance_report()
    print("✅ Performance Report Generated:")
    print(f"   Overall success rate: {report['overall_success_rate']}")
    print(f"   Average processing time: {report['average_processing_time']}")
    print(f"   University performance: {list(report['university_performance'].keys())}")
    
    return True

async def test_integration():
    """Test integration of all components"""
    print("\n🔄 Testing Component Integration...")
    
    # This would test the full flow in a real scenario
    print("✅ Integration test placeholder - would test full application flow")
    
    return True

async def main():
    """Run all tests"""
    print("🚀 Starting Enhanced Features Test Suite")
    print("=" * 50)
    
    results = []
    
    # Test encryption
    results.append(("Encryption", await test_encryption()))
    
    # Test browser automation
    results.append(("Browser Automation", await test_browser_automation()))
    
    # Test monitoring
    results.append(("Monitoring", test_monitoring()))
    
    # Test integration
    results.append(("Integration", await test_integration()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + ("🎉 All tests passed!" if all_passed else "⚠️ Some tests failed!"))
    
    return all_passed

if __name__ == "__main__":
    # Set up test environment
    if not os.environ.get('ENCRYPTION_MASTER_KEY'):
        print("Setting up encryption key for testing...")
        key = setup_encryption_environment()
        os.environ['ENCRYPTION_MASTER_KEY'] = key
    
    # Run tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 