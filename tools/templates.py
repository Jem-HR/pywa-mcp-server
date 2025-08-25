"""Template tools for sending WhatsApp template messages."""

import logging
from typing import Optional, List, Dict, Any
from pywa import WhatsApp

logger = logging.getLogger(__name__)


def register_template_tools(mcp, wa_client: WhatsApp):
    """Register template-related tools."""
    
    @mcp.tool()
    async def send_template(
        to: str,
        name: str,
        language: str = "en",
        params: Optional[List[Dict[str, Any]]] = None,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a WhatsApp template message.
        
        Args:
            to: Phone number or WhatsApp ID
            name: Template name/ID
            language: Template language code (default: en)
            params: Optional template parameters (header, body, button components)
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_template(
                to=to,
                name=name,
                language=language,
                params=params or [],
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Template '{name}' sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {
                "success": True,
                "message_id": message_id,
                "template": name,
                "to": to,
            }
        except Exception as e:
            logger.error(f"Failed to send template: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def get_templates(
        limit: int = 100,
        *,
        name: Optional[str] = None,
    ) -> dict:
        """
        Get list of available WhatsApp templates.
        
        Args:
            limit: Maximum number of templates to return (default: 100)
            name: Optional template name filter
        
        Returns:
            Dictionary with templates list
        """
        try:
            # Note: PyWA's get_templates method signature may vary
            # This is a simplified implementation
            templates = wa_client.get_templates(
                limit=limit,
                name=name,
            )
            
            # Convert templates to simple format
            template_list = []
            for template in templates:
                template_data = {
                    "id": getattr(template, 'id', ''),
                    "name": getattr(template, 'name', ''),
                    "language": getattr(template, 'language', ''),
                    "status": getattr(template, 'status', ''),
                    "category": getattr(template, 'category', ''),
                }
                template_list.append(template_data)
            
            logger.info(f"Retrieved {len(template_list)} templates")
            return {
                "success": True,
                "templates": template_list,
                "count": len(template_list)
            }
        except Exception as e:
            logger.error(f"Failed to get templates: {str(e)}")
            return {"success": False, "error": str(e)}