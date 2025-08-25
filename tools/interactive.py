"""Interactive tools for sending buttons, lists, and simple interactive messages."""

import logging
from typing import Optional, List, Dict, Any
from pywa import WhatsApp
from pywa.types import Button, SectionList, Section, SectionRow

logger = logging.getLogger(__name__)


def register_interactive_tools(mcp, wa_client: WhatsApp):
    """Register interactive messaging tools."""
    
    @mcp.tool()
    async def send_message_with_buttons(
        to: str,
        text: str,
        buttons: List[Dict[str, str]],
        header: Optional[str] = None,
        footer: Optional[str] = None,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a message with reply buttons (up to 3).
        
        CONSTRAINTS:
        - Maximum 3 buttons per message
        - Button title: max 20 characters
        - Button ID (callback_data): max 256 characters
        - Header text: max 60 characters (if provided)
        - Footer text: max 60 characters (if provided)
        
        EXAMPLE:
        {
          "to": "+1234567890",
          "text": "Choose an option:",
          "buttons": [
            {"id": "option_1", "title": "Yes"},
            {"id": "option_2", "title": "No"},
            {"id": "option_3", "title": "Maybe"}
          ],
          "header": "Quick Question",
          "footer": "Select one option"
        }
        
        Args:
            to: Phone number (with country code) or WhatsApp ID
            text: Message body text (main message content)
            buttons: List of buttons with 'id' and 'title' keys (max 3)
            header: Optional header text (appears above main text)
            footer: Optional footer text (appears below buttons)
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            # Validate constraints
            if len(buttons) > 3:
                return {"success": False, "error": "Maximum 3 buttons allowed"}
            
            if header and len(header) > 60:
                return {"success": False, "error": "Header text must be max 60 characters"}
                
            if footer and len(footer) > 60:
                return {"success": False, "error": "Footer text must be max 60 characters"}
            
            # Convert button dictionaries to PyWA Button objects
            button_objects = []
            for btn in buttons:
                if "id" not in btn or "title" not in btn:
                    return {"success": False, "error": "Each button must have 'id' and 'title' keys"}
                
                if len(btn["title"]) > 20:
                    return {"success": False, "error": f"Button title '{btn['title']}' exceeds 20 characters"}
                    
                if len(btn["id"]) > 256:
                    return {"success": False, "error": f"Button ID '{btn['id']}' exceeds 256 characters"}
                
                button_objects.append(Button(
                    title=btn["title"],
                    callback_data=btn["id"]
                ))
            
            result = wa_client.send_message(
                to=to,
                text=text,
                buttons=button_objects,
                header=header,
                footer=footer,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Message with buttons sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send message with buttons: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_message_with_list(
        to: str,
        text: str,
        button_text: str,
        sections: List[Dict[str, Any]],
        header: Optional[str] = None,
        footer: Optional[str] = None,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a message with a selection list.
        
        CONSTRAINTS:
        - Maximum 10 sections per list
        - Maximum 10 rows total across all sections
        - Button text: max 20 characters
        - Section title: max 24 characters
        - Row title: max 24 characters  
        - Row description: max 72 characters
        - Row ID (callback_data): max 200 characters
        - Header text: max 60 characters (if provided)
        - Footer text: max 60 characters (if provided)
        
        EXAMPLE:
        {
          "to": "+1234567890",
          "text": "Choose from our menu:",
          "button_text": "View Menu",
          "sections": [
            {
              "title": "Main Courses",
              "rows": [
                {"id": "burger", "title": "Burger", "description": "Beef burger with fries"},
                {"id": "pizza", "title": "Pizza", "description": "Margherita pizza"}
              ]
            },
            {
              "title": "Beverages", 
              "rows": [
                {"id": "coke", "title": "Coca Cola", "description": "Cold refreshing drink"},
                {"id": "water", "title": "Water", "description": "Still or sparkling"}
              ]
            }
          ],
          "header": "Restaurant Menu",
          "footer": "All items available today"
        }
        
        Args:
            to: Phone number (with country code) or WhatsApp ID  
            text: Message body text (main message content)
            button_text: Text shown on the list button (triggers the list)
            sections: List of sections, each with 'title' and 'rows' arrays
            header: Optional header text (appears above main text)
            footer: Optional footer text (appears below list button)
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            # Validate constraints
            if len(sections) > 10:
                return {"success": False, "error": "Maximum 10 sections allowed"}
                
            if len(button_text) > 20:
                return {"success": False, "error": "Button text must be max 20 characters"}
                
            if header and len(header) > 60:
                return {"success": False, "error": "Header text must be max 60 characters"}
                
            if footer and len(footer) > 60:
                return {"success": False, "error": "Footer text must be max 60 characters"}
            
            # Count total rows across all sections
            total_row_count = sum(len(section.get("rows", [])) for section in sections)
            if total_row_count > 10:
                return {"success": False, "error": "Maximum 10 rows total across all sections"}
            
            # Convert sections to PyWA Section objects
            section_objects = []
            
            for section_data in sections:
                if "rows" not in section_data:
                    return {"success": False, "error": "Each section must have a 'rows' array"}
                
                section_title = section_data.get("title", "")
                if len(section_title) > 24:
                    return {"success": False, "error": f"Section title '{section_title}' exceeds 24 characters"}
                
                rows = []
                for row_data in section_data["rows"]:
                    # Validate required fields
                    if "id" not in row_data or "title" not in row_data:
                        return {"success": False, "error": "Each row must have 'id' and 'title' keys"}
                    
                    # Validate constraints
                    if len(row_data["id"]) > 200:
                        return {"success": False, "error": f"Row ID '{row_data['id']}' exceeds 200 characters"}
                        
                    if len(row_data["title"]) > 24:
                        return {"success": False, "error": f"Row title '{row_data['title']}' exceeds 24 characters"}
                    
                    description = row_data.get("description", "")
                    if len(description) > 72:
                        return {"success": False, "error": f"Row description '{description}' exceeds 72 characters"}
                    
                    rows.append(SectionRow(
                        title=row_data["title"],
                        callback_data=row_data["id"],
                        description=description if description else None
                    ))
                
                if rows:  # Only add section if it has rows
                    section_objects.append(Section(
                        title=section_title,
                        rows=rows
                    ))
            
            # Create SectionList
            section_list = SectionList(
                button_title=button_text,
                sections=section_objects
            )
            
            result = wa_client.send_message(
                to=to,
                text=text,
                buttons=section_list,
                header=header,
                footer=footer,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Message with list sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send message with list: {str(e)}")
            return {"success": False, "error": str(e)}