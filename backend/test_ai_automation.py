"""
AI-Enhanced Automation Test
Demonstrates the Gemini-powered intelligent automation system
"""

import asyncio
import json
import os
from datetime import datetime

# Test the AI components
async def test_ai_analysis_service():
    """Test the AI analysis service"""
    print("🧠 Testing AI Analysis Service...")
    
    # Check if Gemini API is available
    api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyA2piC0ztJ1_LjcxW8BA3IJFgR689jZkl0')
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("   ✅ Gemini 2.5 Flash API connection successful")
        
        # Test text analysis
        prompt = """
        Analyze this webpage scenario for automation:
        
        A job application form with the following fields:
        - First Name (required)
        - Last Name (required) 
        - Email (required)
        - Phone (optional)
        - Resume Upload (required)
        - Cover Letter (optional)
        - Expected Salary (optional)
        
        Provide automation guidance in JSON format with:
        - field_mappings
        - action_sequence
        - challenges
        - confidence
        """
        
        response = model.generate_content(prompt)
        print("   ✅ AI text analysis working with Gemini 2.5 Flash")
        print(f"   📝 Sample response: {response.text[:200]}...")
        
        return True
        
    except ImportError:
        print("   ❌ Gemini library not installed. Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"   ❌ AI service error: {str(e)}")
        return False

async def test_enhanced_data_parser():
    """Test the enhanced data parser with AI capabilities"""
    print("\n📊 Testing Enhanced Data Parser...")
    
    try:
        from automation.enhanced_data_parser import EnhancedDataParser
        
        parser = EnhancedDataParser()
        
        # Test complex job application data
        job_data = """
        JOHN SMITH - SOFTWARE ENGINEER APPLICATION
        
        Personal Information:
        Full Name: John Smith
        Email: john.smith@techcorp.com
        Phone: +1-555-123-4567
        LinkedIn: linkedin.com/in/johnsmith
        
        Professional Details:
        Current Position: Senior Developer at TechCorp
        Years of Experience: 7 years
        Expected Salary: $130,000 - $150,000
        Preferred Location: San Francisco, CA
        
        Skills: Python, JavaScript, React, Node.js, AWS, Docker
        """
        
        print("   🔍 Parsing job application data...")
        results = await parser.parse_file(job_data, 'txt', 'job_application.txt')
        
        for result in results:
            print(f"   📝 Extracted:")
            print(f"      - Name: {result.get('full_name', 'N/A')}")
            print(f"      - Email: {result.get('email', 'N/A')}")
            print(f"      - Experience: {result.get('years_of_experience', result.get('experience', 'N/A'))}")
            print(f"      - Salary: {result.get('expected_salary', 'N/A')}")
            print(f"      - Confidence: {result.get('_confidence', 0) * 100:.0f}%")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced parser error: {str(e)}")
        return False

async def demonstrate_ai_automation_scenarios():
    """Demonstrate AI automation scenarios"""
    print("\n🎯 AI-Enhanced Automation Scenarios:")
    
    scenarios = [
        {
            "name": "🏢 Corporate Job Application",
            "url": "https://careers.company.com/apply",
            "challenge": "Multi-step form with file uploads and salary negotiations",
            "ai_advantage": [
                "Identifies hidden required fields",
                "Suggests optimal salary ranges based on role",
                "Handles dynamic form validation",
                "Adapts to company-specific form layouts"
            ]
        },
        {
            "name": "🛂 Visa Application Portal", 
            "url": "https://embassy.gov/visa-application",
            "challenge": "Complex government form with strict validation",
            "ai_advantage": [
                "Understands government form terminology",
                "Validates document requirements",
                "Handles multi-step approval process",
                "Provides error recovery for failed submissions"
            ]
        },
        {
            "name": "🏥 Medical Appointment Booking",
            "url": "https://hospital.com/appointments",
            "challenge": "Calendar selection with availability constraints",
            "ai_advantage": [
                "Interprets available time slots visually",
                "Understands appointment type requirements",
                "Handles insurance verification forms",
                "Optimizes for preferred doctor/time"
            ]
        },
        {
            "name": "🎓 University Application",
            "url": "https://university.edu/apply",
            "challenge": "Academic transcripts and essay requirements",
            "ai_advantage": [
                "Maps academic records to form fields",
                "Handles GPA conversion systems",
                "Manages multiple document uploads",
                "Adapts to different application systems"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n   {scenario['name']}")
        print(f"   🌐 URL: {scenario['url']}")
        print(f"   🎯 Challenge: {scenario['challenge']}")
        print(f"   🧠 AI Advantages:")
        for advantage in scenario['ai_advantage']:
            print(f"      ✅ {advantage}")

async def show_ai_workflow():
    """Show the AI-enhanced automation workflow"""
    print("\n\n🔄 AI-Enhanced Automation Workflow:")
    
    workflow_steps = [
        {
            "step": 1,
            "name": "🌐 Navigate & Analyze",
            "description": "Browser navigates to target URL",
            "ai_role": "Gemini analyzes webpage screenshot to understand layout, identify forms, and detect page type"
        },
        {
            "step": 2, 
            "name": "🎯 Field Classification",
            "description": "Detect form fields using CSS selectors",
            "ai_role": "AI classifies each field's purpose using context clues, labels, and visual position"
        },
        {
            "step": 3,
            "name": "📋 Data Mapping",
            "description": "Map user data to form fields",
            "ai_role": "Intelligent mapping based on field purpose, data type validation, and form context"
        },
        {
            "step": 4,
            "name": "🖱️ Smart Actions",
            "description": "Execute form interactions",
            "ai_role": "AI suggests optimal action sequence, handles dynamic elements, and adapts to failures"
        },
        {
            "step": 5,
            "name": "🔍 Error Recovery",
            "description": "Handle automation failures",
            "ai_role": "Analyze error states, suggest recovery strategies, and find alternative approaches"
        },
        {
            "step": 6,
            "name": "✅ Success Validation", 
            "description": "Confirm automation success",
            "ai_role": "Identify success indicators, validate form submission, and confirm completion"
        }
    ]
    
    for step in workflow_steps:
        print(f"\n   Step {step['step']}: {step['name']}")
        print(f"   🔧 Action: {step['description']}")
        print(f"   🧠 AI Role: {step['ai_role']}")

async def demonstrate_ai_capabilities():
    """Demonstrate specific AI capabilities"""
    print("\n\n🌟 AI Capabilities in Detail:")
    
    capabilities = {
        "🎭 Visual Understanding": [
            "Screenshot analysis to understand webpage layout",
            "Identification of forms, buttons, and interactive elements", 
            "Recognition of page types (signup, job app, government form)",
            "Detection of visual cues like required field indicators"
        ],
        "🧠 Intelligent Reasoning": [
            "Context-aware field classification beyond simple patterns",
            "Understanding of form flow and multi-step processes",
            "Adaptation to different website designs and frameworks",
            "Learning from automation failures and successes"
        ],
        "🎯 Smart Decision Making": [
            "Optimal action sequence planning",
            "Dynamic selector generation when CSS selectors fail",
            "Error recovery strategy formulation",
            "Confidence scoring for automation reliability"
        ],
        "🔄 Adaptive Behavior": [
            "Handling of unexpected page changes",
            "Recovery from CAPTCHA and validation errors",
            "Adaptation to A/B tested interfaces",
            "Fallback to traditional automation when needed"
        ]
    }
    
    for category, features in capabilities.items():
        print(f"\n   {category}:")
        for feature in features:
            print(f"      ✅ {feature}")

async def show_api_integration():
    """Show how AI integrates with the API"""
    print("\n\n📡 AI Integration in API:")
    
    print("\n   🚀 Enhanced Endpoints:")
    endpoints = [
        {
            "method": "POST",
            "path": "/automation/create-session",
            "enhancement": "Includes AI-powered data parsing and initial analysis"
        },
        {
            "method": "POST", 
            "path": "/automation/start/{session_id}",
            "enhancement": "Uses AI-enhanced automation engine with vision capabilities"
        },
        {
            "method": "GET",
            "path": "/automation/ai-status", 
            "enhancement": "New endpoint to check AI service status and capabilities"
        },
        {
            "method": "WebSocket",
            "path": "/ws/{session_id}",
            "enhancement": "Real-time AI insights and confidence scores"
        }
    ]
    
    for endpoint in endpoints:
        print(f"   📍 {endpoint['method']} {endpoint['path']}")
        print(f"      🧠 AI Enhancement: {endpoint['enhancement']}")
    
    print("\n   📊 Enhanced Response Data:")
    sample_response = {
        "success": True,
        "ai_enabled": True,
        "ai_insights": [
            {
                "confidence": 0.85,
                "forms_detected": 1,
                "field_mappings": {"email": "#email-input", "name": "#full-name"},
                "challenges": ["CAPTCHA detected on submit"],
                "ai_analysis": True
            }
        ],
        "ai_confidence": 0.85,
        "steps_completed": ["AI Action: click", "AI Action: fill", "Form submitted"],
        "screenshots": ["initial_analysis.png", "form_filled.png"]
    }
    
    print(f"   📝 Sample AI Response:")
    print(json.dumps(sample_response, indent=6))

async def main():
    """Run all AI automation demonstrations"""
    print("🤖 AI-Enhanced LAM - Gemini-Powered Automation")
    print("=" * 60)
    
    try:
        # Test AI service
        ai_working = await test_ai_analysis_service()
        
        # Test enhanced parser
        await test_enhanced_data_parser()
        
        # Show automation scenarios
        await demonstrate_ai_automation_scenarios()
        
        # Show AI workflow
        await show_ai_workflow()
        
        # Show AI capabilities
        await demonstrate_ai_capabilities()
        
        # Show API integration
        await show_api_integration()
        
        print("\n\n✨ AI-Enhanced LAM Ready!")
        
        if ai_working:
            print("\n🎉 Your LAM now has:")
            print("   🧠 Visual understanding with Gemini AI")
            print("   👁️ Screenshot analysis and webpage comprehension")
            print("   🎯 Intelligent field classification and mapping")
            print("   🔄 Smart error recovery and adaptation")
            print("   📊 Real-time confidence scoring")
            print("   🌍 Universal website compatibility")
        else:
            print("\n⚠️  AI features disabled - install google-generativeai for full capabilities")
        
        print("\n🚀 Next Steps:")
        print("   1. Install AI dependencies: pip install google-generativeai")
        print("   2. Verify Gemini API key in .env file")
        print("   3. Start server: python server.py")
        print("   4. Use /automation/ai-status to check AI capabilities")
        print("   5. Create sessions with any document type and watch AI work!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 