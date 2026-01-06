#!/usr/bin/env python3
"""
Coinbase MCP Tools
Comprehensive tool system combining financial trading tools with advanced system tools
"""

import os
import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
import logging
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Coinbase-MCP-Server", version="2.0.0")

class ToolRegistry:
    """Registry for automatically discovering and managing MCP tools"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_metadata: Dict[str, Dict[str, Any]] = {}
        
    def discover_tools(self, tools_directory: Path) -> Dict[str, Callable]:
        """Automatically discover all tools in the tools directory"""
        discovered_tools = {}
        
        # Get all Python files in the tools directory
        tool_files = [f for f in tools_directory.glob("*.py") if f.name not in ["__init__.py"]]
        
        for tool_file in tool_files:
            module_name = tool_file.stem
            try:
                # Import the module
                spec = importlib.util.spec_from_file_location(
                    f"tools.{module_name}", 
                    tool_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for tool functions (functions that start with 'tool_' or have @tool decorator)
                for name, obj in inspect.getmembers(module):
                    if (inspect.isfunction(obj) and 
                        (name.startswith('tool_') or hasattr(obj, '_is_mcp_tool'))):
                        
                        tool_name_cleaned = name.replace('tool_', '') if name.startswith('tool_') else name
                        discovered_tools[tool_name_cleaned] = obj
                        
                        # Register with FastMCP
                        mcp.add_tool(obj, name=tool_name_cleaned)
                        
                        # Extract metadata
                        sig = inspect.signature(obj)
                        params_info = {}
                        for param_name, param_obj in sig.parameters.items():
                            params_info[param_name] = {
                                'annotation_str': str(param_obj.annotation) if param_obj.annotation != inspect.Parameter.empty else 'Any',
                                'default_str': str(param_obj.default) if param_obj.default != inspect.Parameter.empty else None,
                                'kind': str(param_obj.kind)
                            }
                        
                        return_annotation_str = str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else 'Any'

                        self.tool_metadata[tool_name_cleaned] = {
                            'module': module_name,
                            'function_name': name,
                            'docstring': inspect.getdoc(obj) or '',
                            'parameters': params_info,
                            'return_annotation': return_annotation_str,
                            'file': str(tool_file)
                        }
                        
                        logger.info(f"Discovered and registered tool: {tool_name_cleaned} from {module_name}")
                
                # Also look for class-based tools (classes that inherit from BaseTool)
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        hasattr(obj, '__bases__') and 
                        any('BaseTool' in str(base) for base in obj.__bases__)):
                        
                        # Find all async methods that don't start with '_'
                        for method_name, method_obj in inspect.getmembers(obj):
                            if (inspect.iscoroutinefunction(method_obj) and 
                                not method_name.startswith('_') and
                                method_name not in ['record_usage', 'get_workspace_context', 'is_safe_path']):
                                
                                tool_name = method_name
                                
                                # Create a wrapper function without 'self' for the tool registry
                                def create_method_wrapper(cls, method_name):
                                    async def wrapper(**kwargs):
                                        from pathlib import Path
                                        workspace_root = Path.cwd().parent if Path.cwd().name == 'tools' else Path.cwd()
                                        instance = cls(workspace_root)
                                        method = getattr(instance, method_name)
                                        return await method(**kwargs)
                                    wrapper.__name__ = method_name
                                    wrapper.__doc__ = method_obj.__doc__
                                    return wrapper
                                
                                # Replace the raw method with the wrapper
                                wrapped_method = create_method_wrapper(obj, method_name)
                                discovered_tools[tool_name] = wrapped_method
                                
                                # Register with FastMCP
                                mcp.add_tool(wrapped_method, name=tool_name)
                                
                                # Extract method signature, excluding 'self'
                                sig = inspect.signature(method_obj)
                                params_info = {}
                                for param_name, param_obj in sig.parameters.items():
                                    if param_name != 'self':
                                        params_info[param_name] = {
                                            'annotation_str': str(param_obj.annotation) if param_obj.annotation != inspect.Parameter.empty else 'Any',
                                            'default_str': str(param_obj.default) if param_obj.default != inspect.Parameter.empty else None,
                                            'kind': str(param_obj.kind)
                                        }
                                
                                return_annotation_str = str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else 'Any'

                                self.tool_metadata[tool_name] = {
                                    'module': module_name,
                                    'class_name': name,
                                    'function_name': method_name,
                                    'docstring': inspect.getdoc(method_obj) or '',
                                    'parameters': params_info,
                                    'return_annotation': return_annotation_str,
                                    'file': str(tool_file),
                                    'tool_type': 'class_method'
                                }
                                
                                logger.info(f"Discovered and registered class tool: {tool_name} from {name} in {module_name}")
                        
            except Exception as e:
                logger.error(f"Failed to import tool module {module_name}: {e}")
                continue
                
        self.tools.update(discovered_tools)
        return discovered_tools
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a specific tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all available tools"""
        return sorted(list(self.tools.keys()))
    
    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata about a specific tool"""
        return self.tool_metadata.get(name)

# Global registry instance
tool_registry = ToolRegistry()

def tool(func):
    """Decorator to mark a function as an MCP tool"""
    target_func = getattr(func, '__func__', func)
    target_func._is_mcp_tool = True
    return func

def register_tool(name: str, func: Callable):
    """Manually register a tool"""
    sig = inspect.signature(func)
    params_info = {}
    for param_name, param_obj in sig.parameters.items():
        params_info[param_name] = {
            'annotation_str': str(param_obj.annotation) if param_obj.annotation != inspect.Parameter.empty else 'Any',
            'default_str': str(param_obj.default) if param_obj.default != inspect.Parameter.empty else None,
            'kind': str(param_obj.kind)
        }
    return_annotation_str = str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else 'Any'

    tool_registry.tools[name] = func
    tool_registry.tool_metadata[name] = {
        'function_name': func.__name__,
        'docstring': inspect.getdoc(func) or '',
        'parameters': params_info,
        'return_annotation': return_annotation_str,
        'manually_registered': True
    }
    
    # Also register with FastMCP
    mcp.add_tool(func, name=name)
    logger.info(f"Manually registered tool: {name}")

# Auto-discover tools when this module is imported
_current_dir = Path(__file__).parent
if _current_dir.exists() and _current_dir.is_dir():
    logger.info(f"Discovering tools in: {_current_dir}")
    discovered = tool_registry.discover_tools(_current_dir)
    logger.info(f"Total tools discovered and registered: {len(discovered)}")

# Export the registry, MCP server, and important functions
__all__ = ['tool_registry', 'tool', 'register_tool', 'ToolRegistry', 'mcp'] 