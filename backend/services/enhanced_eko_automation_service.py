"""
Enhanced Eko Automation Service - Multi-Browser Session Management

Advanced automation service with multiple browser instances, parallel processing,
and sophisticated session management for university application automation.
"""

import asyncio
import json
import logging
import tempfile
import os
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class BrowserSessionType(Enum):
    ISOLATED = "isolated"        # Separate browser instances
    MULTI_TAB = "multi_tab"     # Multiple tabs in same browser
    PERSISTENT = "persistent"    # Persistent user data contexts
    CDP_CONNECT = "cdp_connect"  # Connect to existing browser via CDP

@dataclass
class BrowserSession:
    """Configuration for a browser session"""
    session_id: str
    session_type: BrowserSessionType
    headless: bool = True
    user_data_dir: Optional[str] = None
    cdp_endpoint: Optional[str] = None
    options: Dict[str, Any] = None

@dataclass
class UniversityApplicationTask:
    """Configuration for university application automation"""
    university_name: str
    application_url: str
    client_profile: Dict[str, Any]
    documents: List[str]
    session_id: Optional[str] = None
    priority: int = 1

class EnhancedEkoAutomationService:
    """Enhanced Eko automation service with multi-browser session support"""
    
    def __init__(self):
        self.eko_script_path = Path(__file__).parent / "eko_scripts"
        self.eko_script_path.mkdir(exist_ok=True)
        self.active_sessions: Dict[str, BrowserSession] = {}
        self.session_counter = 0
        
    async def initialize_eko_environment(self) -> bool:
        """Initialize enhanced Eko environment with multi-browser support"""
        try:
            # Check if Eko is installed
            result = await self._run_node_command(["npm", "list", "@eko-ai/eko"])
            if result["success"]:
                logger.info("Enhanced Eko framework is ready")
                return True
            
            # Install Eko with Node.js package
            logger.info("Installing enhanced Eko framework...")
            install_result = await self._run_node_command([
                "npm", "install", 
                "@eko-ai/eko", 
                "@eko-ai/eko-nodejs",
                "playwright"  # Required for browser automation
            ])
            
            if install_result["success"]:
                # Install browser binaries
                browser_install = await self._run_node_command([
                    "npx", "playwright", "install", "chromium"
                ])
                
                if browser_install["success"]:
                    logger.info("Enhanced Eko framework installed successfully")
                    return True
                else:
                    logger.error(f"Failed to install browser binaries: {browser_install['error']}")
                    return False
            else:
                logger.error(f"Failed to install Eko: {install_result['error']}")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing enhanced Eko environment: {str(e)}")
            return False
    
    def create_browser_session(
        self,
        session_type: BrowserSessionType = BrowserSessionType.ISOLATED,
        headless: bool = True,
        user_data_dir: Optional[str] = None,
        cdp_endpoint: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new browser session configuration"""
        self.session_counter += 1
        session_id = f"browser_session_{self.session_counter}"
        
        session = BrowserSession(
            session_id=session_id,
            session_type=session_type,
            headless=headless,
            user_data_dir=user_data_dir,
            cdp_endpoint=cdp_endpoint,
            options=options or {}
        )
        
        self.active_sessions[session_id] = session
        logger.info(f"Created browser session: {session_id} ({session_type.value})")
        
        return session_id
    
    async def create_parallel_university_applications(
        self,
        applications: List[UniversityApplicationTask],
        max_concurrent: int = 3,
        use_separate_browsers: bool = True
    ) -> Dict[str, Any]:
        """
        Process multiple university applications in parallel using multiple browser sessions
        
        Args:
            applications: List of university application tasks
            max_concurrent: Maximum number of concurrent browser sessions
            use_separate_browsers: Whether to use separate browser instances for each application
            
        Returns:
            Dictionary with results for each application
        """
        try:
            logger.info(f"Starting parallel processing of {len(applications)} university applications")
            
            # Create browser sessions if needed
            if use_separate_browsers:
                for i, app in enumerate(applications):
                    if not app.session_id:
                        session_id = self.create_browser_session(
                            session_type=BrowserSessionType.ISOLATED,
                            headless=True
                        )
                        app.session_id = session_id
            else:
                # Use multi-tab approach
                shared_session_id = self.create_browser_session(
                    session_type=BrowserSessionType.MULTI_TAB,
                    headless=True
                )
                for app in applications:
                    if not app.session_id:
                        app.session_id = shared_session_id
            
            # Generate the enhanced Eko script
            script_content = await self._generate_parallel_automation_script({
                "applications": [app.__dict__ for app in applications],
                "max_concurrent": max_concurrent,
                "browser_sessions": {sid: session.__dict__ for sid, session in self.active_sessions.items()},
                "llm_config": {
                    "provider": "anthropic",
                    "model": "claude-sonnet-4-20250514",
                    "apiKey": os.getenv("ANTHROPIC_API_KEY"),
                }
            })
            
            # Execute the parallel workflow
            result = await self._execute_eko_workflow(script_content)
            
            return {
                "success": True,
                "applications_processed": len(applications),
                "results": result.get("results", {}),
                "execution_time": result.get("execution_time"),
                "sessions_used": list(self.active_sessions.keys()),
                "metadata": result.get("metadata", {})
            }
            
        except Exception as e:
            logger.error(f"Error in parallel university applications: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "applications_attempted": len(applications)
            }
    
    async def monitor_multiple_portals_simultaneously(
        self,
        portals: List[Dict[str, Any]],
        monitoring_interval: int = 300  # 5 minutes
    ) -> Dict[str, Any]:
        """
        Monitor multiple university portals simultaneously using separate browser sessions
        
        Args:
            portals: List of portal configurations
            monitoring_interval: How often to check each portal (seconds)
            
        Returns:
            Monitoring results for all portals
        """
        try:
            logger.info(f"Starting simultaneous monitoring of {len(portals)} university portals")
            
            # Create dedicated browser sessions for monitoring
            monitoring_sessions = []
            for i, portal in enumerate(portals):
                session_id = self.create_browser_session(
                    session_type=BrowserSessionType.PERSISTENT,
                    headless=True,
                    user_data_dir=f"/tmp/monitoring_session_{i}"
                )
                monitoring_sessions.append(session_id)
                portal["session_id"] = session_id
            
            # Generate monitoring script
            script_content = await self._generate_monitoring_script({
                "portals": portals,
                "monitoring_interval": monitoring_interval,
                "browser_sessions": {sid: session.__dict__ for sid, session in self.active_sessions.items()},
                "llm_config": {
                    "provider": "anthropic",
                    "model": "claude-sonnet-4-20250514",
                    "apiKey": os.getenv("ANTHROPIC_API_KEY"),
                }
            })
            
            # Execute monitoring workflow
            result = await self._execute_eko_workflow(script_content)
            
            return {
                "success": True,
                "portals_monitored": len(portals),
                "monitoring_sessions": monitoring_sessions,
                "results": result.get("results", {}),
                "next_check": result.get("next_check"),
                "metadata": result.get("metadata", {})
            }
            
        except Exception as e:
            logger.error(f"Error in portal monitoring: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_intelligent_workflow_with_multiple_browsers(
        self,
        workflow_description: str,
        browser_requirements: Optional[List[Dict[str, Any]]] = None,
        coordination_strategy: str = "sequential"  # sequential, parallel, or adaptive
    ) -> Dict[str, Any]:
        """
        Create an intelligent workflow that automatically determines optimal browser usage
        
        Args:
            workflow_description: Natural language description of the workflow
            browser_requirements: Specific browser session requirements
            coordination_strategy: How to coordinate multiple browsers
            
        Returns:
            Workflow execution results
        """
        try:
            logger.info(f"Creating intelligent multi-browser workflow: {coordination_strategy}")
            
            # Analyze workflow and determine optimal browser strategy
            browser_strategy = await self._analyze_workflow_browser_requirements(
                workflow_description, browser_requirements
            )
            
            # Create required browser sessions
            session_ids = []
            for session_config in browser_strategy["sessions"]:
                session_id = self.create_browser_session(**session_config)
                session_ids.append(session_id)
            
            # Generate adaptive workflow script
            script_content = await self._generate_adaptive_workflow_script({
                "workflow_description": workflow_description,
                "coordination_strategy": coordination_strategy,
                "browser_strategy": browser_strategy,
                "browser_sessions": {sid: session.__dict__ for sid, session in self.active_sessions.items()},
                "llm_config": {
                    "provider": "anthropic",
                    "model": "claude-sonnet-4-20250514",
                    "apiKey": os.getenv("ANTHROPIC_API_KEY"),
                }
            })
            
            # Execute adaptive workflow
            result = await self._execute_eko_workflow(script_content)
            
            return {
                "success": True,
                "workflow_description": workflow_description,
                "coordination_strategy": coordination_strategy,
                "sessions_created": session_ids,
                "browser_strategy": browser_strategy,
                "results": result.get("results", {}),
                "execution_time": result.get("execution_time"),
                "metadata": result.get("metadata", {})
            }
            
        except Exception as e:
            logger.error(f"Error in intelligent workflow creation: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def cleanup_browser_sessions(self, session_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Clean up browser sessions"""
        try:
            sessions_to_cleanup = session_ids or list(self.active_sessions.keys())
            
            cleaned_sessions = []
            for session_id in sessions_to_cleanup:
                if session_id in self.active_sessions:
                    del self.active_sessions[session_id]
                    cleaned_sessions.append(session_id)
            
            logger.info(f"Cleaned up {len(cleaned_sessions)} browser sessions")
            
            return {
                "success": True,
                "cleaned_sessions": cleaned_sessions,
                "remaining_sessions": list(self.active_sessions.keys())
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up browser sessions: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _analyze_workflow_browser_requirements(
        self, 
        workflow_description: str, 
        browser_requirements: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Analyze workflow to determine optimal browser session strategy"""
        
        # Simple heuristics - in production this could use LLM analysis
        analysis = {
            "sessions": [],
            "coordination": "sequential",
            "estimated_duration": 300  # 5 minutes default
        }
        
        # Count university mentions to estimate browser needs
        universities = ["oxford", "cambridge", "imperial", "ucl", "kings", "edinburgh", "manchester"]
        university_count = sum(1 for uni in universities if uni.lower() in workflow_description.lower())
        
        if university_count > 1:
            # Multiple universities detected - use parallel processing
            analysis["coordination"] = "parallel"
            for i in range(min(university_count, 5)):  # Max 5 concurrent browsers
                analysis["sessions"].append({
                    "session_type": BrowserSessionType.ISOLATED,
                    "headless": True,
                    "options": {"args": ["--no-sandbox", "--disable-dev-shm-usage"]}
                })
        else:
            # Single university or general workflow - use multi-tab
            analysis["sessions"].append({
                "session_type": BrowserSessionType.MULTI_TAB,
                "headless": True,
                "options": {"args": ["--no-sandbox", "--disable-dev-shm-usage"]}
            })
        
        # Apply any specific browser requirements
        if browser_requirements:
            analysis["sessions"].extend(browser_requirements)
        
        return analysis
    
    async def _generate_parallel_automation_script(self, config: Dict) -> str:
        """Generate Eko script for parallel automation"""
        script_template = """
import { Eko, Agent, Log, LLMs } from "@eko-ai/eko";
import { BrowserAgent, FileAgent } from "@eko-ai/eko-nodejs";

const config = {config_json};

const llms = {{
  default: {{
    provider: config.llm_config.provider,
    model: config.llm_config.model,
    apiKey: config.llm_config.apiKey,
  }}
}};

async function createBrowserAgent(sessionConfig) {{
  const agent = new BrowserAgent();
  
  if (sessionConfig.session_type === 'isolated') {{
    agent.setHeadless(sessionConfig.headless);
    if (sessionConfig.options) {{
      agent.setOptions(sessionConfig.options);
    }}
  }} else if (sessionConfig.session_type === 'persistent') {{
    agent.setHeadless(sessionConfig.headless);
    if (sessionConfig.user_data_dir) {{
      agent.setOptions({{ 
        ...sessionConfig.options,
        userDataDir: sessionConfig.user_data_dir 
      }});
    }}
  }} else if (sessionConfig.session_type === 'cdp_connect') {{
    if (sessionConfig.cdp_endpoint) {{
      agent.setCdpWsEndpoint(sessionConfig.cdp_endpoint);
    }}
  }}
  
  return agent;
}}

async function executeParallelApplications() {{
  try {{
    const results = {{}};
    const agents = [];
    
    // Create browser agents for each session
    for (const [sessionId, sessionConfig] of Object.entries(config.browser_sessions)) {{
      const agent = await createBrowserAgent(sessionConfig);
      agents.push(agent);
    }}
    
    // Add file agent for document management
    agents.push(new FileAgent());
    
    const eko = new Eko({{ llms, agents }});
    
    // Process applications based on coordination strategy
    if (config.max_concurrent > 1) {{
      // Parallel processing
      const batches = [];
      for (let i = 0; i < config.applications.length; i += config.max_concurrent) {{
        batches.push(config.applications.slice(i, i + config.max_concurrent));
      }}
      
      for (const batch of batches) {{
        const batchPromises = batch.map(async (app, index) => {{
          const taskDescription = `
            Apply to ${{app.university_name}} using browser session ${{app.session_id}}:
            1. Navigate to ${{app.application_url}}
            2. Fill application form with client data: ${{JSON.stringify(app.client_profile)}}
            3. Upload documents: ${{app.documents.join(', ')}}
            4. Submit application and save confirmation
            5. Take screenshot of confirmation page
          `;
          
          try {{
            const result = await eko.run(taskDescription);
            return {{ 
              university: app.university_name,
              success: result.success,
              result: result.result,
              session_id: app.session_id
            }};
          }} catch (error) {{
            return {{ 
              university: app.university_name,
              success: false,
              error: error.message,
              session_id: app.session_id
            }};
          }}
        }});
        
        const batchResults = await Promise.all(batchPromises);
        batchResults.forEach(result => {{
          results[result.university] = result;
        }});
      }}
    }} else {{
      // Sequential processing
      for (const app of config.applications) {{
        const taskDescription = `
          Apply to ${{app.university_name}}:
          1. Navigate to ${{app.application_url}}
          2. Fill application form with client data
          3. Upload required documents
          4. Submit and save confirmation
        `;
        
        try {{
          const result = await eko.run(taskDescription);
          results[app.university_name] = {{
            success: result.success,
            result: result.result,
            session_id: app.session_id
          }};
        }} catch (error) {{
          results[app.university_name] = {{
            success: false,
            error: error.message,
            session_id: app.session_id
          }};
        }}
      }}
    }}
    
    console.log("EKO_RESULT:", JSON.stringify({{
      success: true,
      results: results,
      applications_processed: config.applications.length,
      execution_time: Date.now(),
      metadata: config
    }}));
    
  }} catch (error) {{
    console.log("EKO_ERROR:", JSON.stringify({{
      success: false,
      error: error.message,
      stack: error.stack
    }}));
  }}
}}

executeParallelApplications();
        """
        
        return script_template.replace("{config_json}", json.dumps(config))
    
    async def _generate_monitoring_script(self, config: Dict) -> str:
        """Generate Eko script for monitoring multiple portals"""
        script_template = """
import { Eko, Agent, Log, LLMs } from "@eko-ai/eko";
import { BrowserAgent, FileAgent, TimerAgent } from "@eko-ai/eko-nodejs";

const config = {config_json};

const llms = {{
  default: {{
    provider: config.llm_config.provider,
    model: config.llm_config.model,
    apiKey: config.llm_config.apiKey,
  }}
}};

async function executeMonitoring() {{
  try {{
    const results = {{}};
    const agents = [];
    
    // Create browser agents for monitoring
    for (const [sessionId, sessionConfig] of Object.entries(config.browser_sessions)) {{
      const agent = new BrowserAgent();
      agent.setHeadless(sessionConfig.headless);
      if (sessionConfig.user_data_dir) {{
        agent.setOptions({{ userDataDir: sessionConfig.user_data_dir }});
      }}
      agents.push(agent);
    }}
    
    // Add timer agent for scheduling
    agents.push(new TimerAgent());
    agents.push(new FileAgent());
    
    const eko = new Eko({{ llms, agents }});
    
    // Monitor each portal simultaneously
    const monitoringPromises = config.portals.map(async (portal) => {{
      const taskDescription = `
        Monitor university portal ${{portal.university}} at ${{portal.portal_url}}:
        1. Login using provided credentials
        2. Navigate to application status page
        3. Check for any status updates or changes
        4. Take screenshot if changes detected
        5. Extract relevant information
        6. Schedule next check in ${{config.monitoring_interval}} seconds
        
        Portal details: ${{JSON.stringify(portal)}}
      `;
      
      try {{
        const result = await eko.run(taskDescription);
        return {{
          portal: portal.university,
          session_id: portal.session_id,
          success: result.success,
          status: result.result,
          last_checked: new Date().toISOString()
        }};
      }} catch (error) {{
        return {{
          portal: portal.university,
          session_id: portal.session_id,
          success: false,
          error: error.message,
          last_checked: new Date().toISOString()
        }};
      }}
    }});
    
    const monitoringResults = await Promise.all(monitoringPromises);
    
    monitoringResults.forEach(result => {{
      results[result.portal] = result;
    }});
    
    console.log("EKO_RESULT:", JSON.stringify({{
      success: true,
      results: results,
      portals_monitored: config.portals.length,
      next_check: new Date(Date.now() + config.monitoring_interval * 1000).toISOString(),
      execution_time: Date.now(),
      metadata: config
    }}));
    
  }} catch (error) {{
    console.log("EKO_ERROR:", JSON.stringify({{
      success: false,
      error: error.message,
      stack: error.stack
    }}));
  }}
}}

executeMonitoring();
        """
        
        return script_template.replace("{config_json}", json.dumps(config))
    
    async def _generate_adaptive_workflow_script(self, config: Dict) -> str:
        """Generate Eko script for adaptive workflow with intelligent browser coordination"""
        script_template = """
import { Eko, Agent, Log, LLMs } from "@eko-ai/eko";
import { BrowserAgent, FileAgent } from "@eko-ai/eko-nodejs";

const config = {config_json};

const llms = {{
  default: {{
    provider: config.llm_config.provider,
    model: config.llm_config.model,
    apiKey: config.llm_config.apiKey,
  }}
}};

async function executeAdaptiveWorkflow() {{
  try {{
    const agents = [];
    
    // Create browser agents based on strategy
    for (const [sessionId, sessionConfig] of Object.entries(config.browser_sessions)) {{
      const agent = new BrowserAgent();
      
      // Configure browser agent based on session type
      agent.setHeadless(sessionConfig.headless);
      
      if (sessionConfig.options) {{
        agent.setOptions(sessionConfig.options);
      }}
      
      if (sessionConfig.cdp_endpoint) {{
        agent.setCdpWsEndpoint(sessionConfig.cdp_endpoint);
      }}
      
      agents.push(agent);
    }}
    
    // Add supporting agents
    agents.push(new FileAgent());
    
    const eko = new Eko({{ llms, agents }});
    
    // Execute workflow with intelligent coordination
    let taskDescription = config.workflow_description;
    
    // Enhance task description with browser coordination instructions
    if (config.coordination_strategy === 'parallel') {{
      taskDescription += `
      
      COORDINATION INSTRUCTIONS:
      - Use multiple browser sessions simultaneously
      - Process tasks in parallel where possible
      - Coordinate data sharing between sessions
      - Ensure no conflicts between browser instances
      `;
    }} else if (config.coordination_strategy === 'sequential') {{
      taskDescription += `
      
      COORDINATION INSTRUCTIONS:
      - Use browser sessions sequentially
      - Complete one task before starting the next
      - Maintain session state between tasks
      - Optimize for reliability over speed
      `;
    }} else {{
      taskDescription += `
      
      COORDINATION INSTRUCTIONS:
      - Adaptively choose between parallel and sequential processing
      - Optimize based on task complexity and requirements
      - Use multiple browsers when beneficial
      - Fall back to single browser if needed
      `;
    }}
    
    const result = await eko.run(taskDescription);
    
    console.log("EKO_RESULT:", JSON.stringify({{
      success: result.success,
      results: result.result,
      coordination_strategy: config.coordination_strategy,
      sessions_used: Object.keys(config.browser_sessions),
      execution_time: Date.now(),
      metadata: config
    }}));
    
  }} catch (error) {{
    console.log("EKO_ERROR:", JSON.stringify({{
      success: false,
      error: error.message,
      stack: error.stack
    }}));
  }}
}}

executeAdaptiveWorkflow();
        """
        
        return script_template.replace("{config_json}", json.dumps(config))
    
    async def _execute_eko_workflow(self, script_content: str) -> Dict[str, Any]:
        """Execute Eko workflow script (reusing from base service)"""
        try:
            # Write script to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            try:
                # Execute Node.js script
                result = await self._run_node_command(["node", script_path])
                
                if result["success"]:
                    # Parse Eko output
                    output_lines = result["output"].split('\n')
                    eko_result = None
                    
                    for line in output_lines:
                        if line.startswith("EKO_RESULT:"):
                            eko_result = json.loads(line[11:])
                            break
                        elif line.startswith("EKO_ERROR:"):
                            error_data = json.loads(line[10:])
                            raise Exception(error_data["error"])
                    
                    return eko_result or {"success": False, "error": "No result received"}
                else:
                    raise Exception(f"Node.js execution failed: {result['error']}")
                    
            finally:
                # Clean up temporary file
                os.unlink(script_path)
                
        except Exception as e:
            logger.error(f"Error executing enhanced Eko workflow: {str(e)}")
            raise
    
    async def _run_node_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run Node.js command and return result (reusing from base service)"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.eko_script_path
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode(),
                "error": stderr.decode(),
                "return_code": process.returncode
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1
            }

# Global enhanced service instance
enhanced_eko_service = EnhancedEkoAutomationService() 