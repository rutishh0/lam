import asyncio
import random
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from fake_useragent import UserAgent
import json

logger = logging.getLogger(__name__)

class EnhancedBrowserAutomation:
    """Enhanced browser automation with anti-detection and retry mechanisms"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.ua = UserAgent()
        self.retry_count = 3
        self.retry_delay = 2
        
    async def initialize_stealth_browser(self) -> BrowserContext:
        """Initialize browser with advanced anti-detection measures"""
        try:
            self.playwright = await async_playwright().start()
            
            # Random user agent
            user_agent = self.ua.random
            
            # Launch arguments for stealth
            launch_args = [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--disable-features=VizDisplayCompositor',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080',
                '--start-maximized',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',
                '--disable-javascript',
                f'--user-agent={user_agent}'
            ]
            
            # Browser launch
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Set to True for production
                args=launch_args,
                channel='chrome'  # Use Chrome instead of Chromium
            )
            
            # Context with realistic settings
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=user_agent,
                locale='en-GB',
                timezone_id='Europe/London',
                permissions=['geolocation'],
                geolocation={'latitude': 51.5074, 'longitude': -0.1278},  # London
                color_scheme='light',
                device_scale_factor=1,
                is_mobile=False,
                has_touch=False,
                java_script_enabled=True,
                accept_downloads=True,
                ignore_https_errors=True,
                bypass_csp=True
            )
            
            # Advanced anti-detection scripts
            await self.context.add_init_script("""
                // Override navigator properties
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Mock languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-GB', 'en-US', 'en'],
                });
                
                // Mock plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable", enabledPlugin: Plugin},
                            1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable", enabledPlugin: Plugin},
                            description: "",
                            filename: "internal-nacl-plugin",
                            length: 2,
                            name: "Native Client"
                        }
                    ],
                });
                
                // Chrome specific
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                };
                
                // Permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // WebGL Vendor
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) {
                        return 'Intel Inc.';
                    }
                    if (parameter === 37446) {
                        return 'Intel Iris OpenGL Engine';
                    }
                    return getParameter(parameter);
                };
                
                // Battery API
                navigator.getBattery = () => Promise.resolve({
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: 1
                });
                
                // Connection info
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        rtt: 50,
                        downlink: 10,
                        saveData: false
                    })
                });
            """)
            
            logger.info("Stealth browser initialized successfully")
            return self.context
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            raise
    
    async def human_like_delay(self, min_ms: int = 100, max_ms: int = 300):
        """Add human-like random delay"""
        delay = random.randint(min_ms, max_ms) / 1000
        await asyncio.sleep(delay)
    
    async def human_like_typing(self, page: Page, selector: str, text: str, mistakes: bool = True):
        """Type text with human-like speed and occasional mistakes"""
        element = await page.wait_for_selector(selector, timeout=30000)
        await element.click()
        
        # Clear existing text
        await page.keyboard.press('Control+A')
        await page.keyboard.press('Delete')
        
        for char in text:
            # Occasional typos
            if mistakes and random.random() < 0.02:  # 2% chance of typo
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                await page.keyboard.type(wrong_char)
                await self.human_like_delay(100, 200)
                await page.keyboard.press('Backspace')
                await self.human_like_delay(50, 150)
            
            await page.keyboard.type(char)
            await self.human_like_delay(50, 150)
    
    async def random_mouse_movement(self, page: Page):
        """Simulate random mouse movements"""
        width = page.viewport_size['width']
        height = page.viewport_size['height']
        
        for _ in range(random.randint(2, 5)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            await page.mouse.move(x, y)
            await self.human_like_delay(100, 300)
    
    async def smart_wait_and_click(self, page: Page, selector: str, retries: int = 3):
        """Wait for element and click with retry logic"""
        for attempt in range(retries):
            try:
                # Random mouse movement before click
                await self.random_mouse_movement(page)
                
                # Wait for element
                element = await page.wait_for_selector(selector, timeout=30000)
                
                # Scroll element into view
                await element.scroll_into_view_if_needed()
                await self.human_like_delay()
                
                # Hover before clicking
                await element.hover()
                await self.human_like_delay(100, 200)
                
                # Click
                await element.click()
                logger.info(f"Successfully clicked element: {selector}")
                return True
                
            except Exception as e:
                logger.warning(f"Click attempt {attempt + 1} failed for {selector}: {str(e)}")
                if attempt < retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise
        
        return False
    
    async def handle_captcha(self, page: Page) -> bool:
        """Detect and handle CAPTCHA challenges"""
        # Check for common CAPTCHA indicators
        captcha_selectors = [
            'iframe[src*="recaptcha"]',
            'iframe[src*="hcaptcha"]',
            'div[class*="captcha"]',
            '#captcha',
            '.g-recaptcha'
        ]
        
        for selector in captcha_selectors:
            if await page.query_selector(selector):
                logger.warning(f"CAPTCHA detected: {selector}")
                # TODO: Integrate with 2captcha or anti-captcha service
                return False
        
        return True
    
    async def save_page_state(self, page: Page, filename: str):
        """Save page state for debugging"""
        try:
            # Screenshot
            await page.screenshot(path=f"debug_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            # HTML content
            content = await page.content()
            with open(f"debug_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html", 'w') as f:
                f.write(content)
                
            logger.info(f"Page state saved for {filename}")
        except Exception as e:
            logger.error(f"Failed to save page state: {str(e)}")
    
    async def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}") 