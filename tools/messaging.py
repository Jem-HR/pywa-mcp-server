"""Messaging tools for sending text, media, location, and contact messages."""

import logging
from typing import Optional, List, Iterable
from pywa import WhatsApp
from pywa.types import Button, Contact

logger = logging.getLogger(__name__)


def register_messaging_tools(mcp, wa_client: WhatsApp):
    """Register all messaging-related tools."""
    
    @mcp.tool()
    async def send_message(
        to: str,
        text: str,
        header: Optional[str] = None,
        footer: Optional[str] = None,
        *,
        preview_url: bool = False,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a text message to a WhatsApp user.
        
        Args:
            to: Phone number (with country code) or WhatsApp ID
            text: The text message content
            header: Optional header text (for interactive messages)
            footer: Optional footer text (for interactive messages)
            preview_url: Whether to show URL previews (default False)
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_message(
                to=to,
                text=text,
                header=header,
                footer=footer,
                preview_url=preview_url,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Message sent to {to}")
            # Extract just the message ID if result is a complex object
            message_id = getattr(result, 'id', str(result)) if result else None
            
            return {
                "success": True,
                "message_id": message_id,
                "to": to,
            }
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_image(
        to: str,
        image: str,
        caption: Optional[str] = None,
        footer: Optional[str] = None,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send an image message.
        
        Args:
            to: Phone number or WhatsApp ID
            image: Image URL or media ID
            caption: Optional image caption
            footer: Optional footer text
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_image(
                to=to,
                image=image,
                caption=caption,
                footer=footer,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Image sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send image: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_video(
        to: str,
        video: str,
        caption: Optional[str] = None,
        footer: Optional[str] = None,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a video message.
        
        Args:
            to: Phone number or WhatsApp ID
            video: Video URL or media ID
            caption: Optional video caption
            footer: Optional footer text
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_video(
                to=to,
                video=video,
                caption=caption,
                footer=footer,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Video sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send video: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_document(
        to: str,
        document: str,
        filename: Optional[str] = None,
        caption: Optional[str] = None,
        footer: Optional[str] = None,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a document message.
        
        Args:
            to: Phone number or WhatsApp ID
            document: Document URL or media ID
            filename: Optional filename for the document
            caption: Optional document caption
            footer: Optional footer text
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_document(
                to=to,
                document=document,
                filename=filename,
                caption=caption,
                footer=footer,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Document sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send document: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_audio(
        to: str,
        audio: str,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send an audio message.
        
        Args:
            to: Phone number or WhatsApp ID
            audio: Audio URL or media ID
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_audio(
                to=to,
                audio=audio,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Audio sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send audio: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_sticker(
        to: str,
        sticker: str,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a sticker message.
        
        Args:
            to: Phone number or WhatsApp ID
            sticker: Sticker URL or media ID (must be webp format)
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_sticker(
                to=to,
                sticker=sticker,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Sticker sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send sticker: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_location(
        to: str,
        latitude: float,
        longitude: float,
        name: Optional[str] = None,
        address: Optional[str] = None,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a location message.
        
        Args:
            to: Phone number or WhatsApp ID
            latitude: Latitude of the location
            longitude: Longitude of the location
            name: Optional location name
            address: Optional location address
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.send_location(
                to=to,
                latitude=latitude,
                longitude=longitude,
                name=name,
                address=address,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Location sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send location: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def request_location(
        to: str,
        text: str,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Request user's location.
        
        Args:
            to: Phone number or WhatsApp ID
            text: Message text asking for location
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            result = wa_client.request_location(
                to=to,
                text=text,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Location request sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to request location: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_contact(
        to: str,
        contact_name: str,
        contact_phone: str,
        *,
        reply_to_message_id: Optional[str] = None,
    ) -> dict:
        """
        Send a contact card.
        
        Args:
            to: Phone number or WhatsApp ID
            contact_name: Name of the contact
            contact_phone: Phone number of the contact
            reply_to_message_id: Message ID to reply to
        
        Returns:
            Dictionary with success status and message ID
        """
        try:
            # Create Contact object
            contact = Contact(
                name=Contact.Name(formatted_name=contact_name),
                phones=[Contact.Phone(phone=contact_phone)]
            )
            
            result = wa_client.send_contact(
                to=to,
                contact=contact,
                reply_to_message_id=reply_to_message_id,
            )
            
            logger.info(f"Contact sent to {to}")
            message_id = getattr(result, 'id', str(result)) if result else None
            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.error(f"Failed to send contact: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def send_reaction(
        to: str,
        emoji: str,
        message_id: str,
        *,
        sender: Optional[str] = None,
    ) -> dict:
        """
        Send a reaction to a message.
        
        Args:
            to: Phone number or WhatsApp ID
            emoji: Reaction emoji
            message_id: ID of message to react to
            sender: Optional sender phone ID
        
        Returns:
            Dictionary with success status
        """
        try:
            result = wa_client.send_reaction(
                to=to,
                emoji=emoji,
                message_id=message_id,
                sender=sender,
            )
            
            logger.info(f"Reaction sent to message {message_id}")
            result_data = str(result) if result else None
            return {"success": True, "result": result_data}
        except Exception as e:
            logger.error(f"Failed to send reaction: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def remove_reaction(
        to: str,
        message_id: str,
        *,
        sender: Optional[str] = None,
    ) -> dict:
        """
        Remove a reaction from a message.
        
        Args:
            to: Phone number or WhatsApp ID
            message_id: ID of message to remove reaction from
            sender: Optional sender phone ID
        
        Returns:
            Dictionary with success status
        """
        try:
            result = wa_client.remove_reaction(
                to=to,
                message_id=message_id,
                sender=sender,
            )
            
            logger.info(f"Reaction removed from message {message_id}")
            result_data = str(result) if result else None
            return {"success": True, "result": result_data}
        except Exception as e:
            logger.error(f"Failed to remove reaction: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def mark_message_as_read(
        message_id: str,
        *,
        sender: Optional[str] = None,
    ) -> dict:
        """
        Mark a message as read.
        
        Args:
            message_id: The WhatsApp message ID to mark as read
            sender: Optional phone ID
        
        Returns:
            Dictionary with success status
        """
        try:
            result = wa_client.mark_message_as_read(
                message_id=message_id,
                sender=sender,
            )
            
            logger.info(f"Message {message_id} marked as read")
            result_data = str(result) if result else None
            return {"success": True, "result": result_data}
        except Exception as e:
            logger.error(f"Failed to mark message as read: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def indicate_typing(
        message_id: str,
        *,
        sender: Optional[str] = None,
    ) -> dict:
        """
        Show typing indicator to WhatsApp user.
        
        This marks a message as read and displays a typing indicator to show
        the user that you are preparing a response. Best practice when it will
        take a few seconds to respond.
        
        IMPORTANT NOTES:
        - Typing indicator lasts max 25 seconds or until you send a message
        - Only use if you are actually going to respond  
        - Will be dismissed when you send the next message
        - Improves user experience for delayed responses
        
        EXAMPLE:
        {
          "message_id": "wamid.HBgNMjc2NTY4NjY5MDUVAgARGBI5QTNDMEM3RjVBMzY2Q0Y4AA=="
        }
        
        Args:
            message_id: The WhatsApp message ID to respond to (from incoming message)
            sender: Optional phone ID (defaults to client's phone ID)
        
        Returns:
            Dictionary with success status
        """
        try:
            result = wa_client.indicate_typing(
                message_id=message_id,
                sender=sender,
            )
            
            logger.info(f"Typing indicator shown for message {message_id}")
            # SuccessResult has a success boolean attribute
            success_status = getattr(result, 'success', bool(result))
            
            return {
                "success": True, 
                "typing_indicated": success_status,
                "message_id": message_id
            }
        except Exception as e:
            logger.error(f"Failed to indicate typing: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    @mcp.tool()
    async def upload_media(
        media_path: str,
        *,
        mime_type: Optional[str] = None,
    ) -> dict:
        """
        Upload media file to WhatsApp servers.
        
        Args:
            media_path: Path to media file
            mime_type: Optional MIME type
        
        Returns:
            Dictionary with media ID
        """
        try:
            media_obj = wa_client.upload_media(
                media=media_path,
                mime_type=mime_type,
            )
            
            logger.info("Media uploaded successfully")
            return {
                "success": True, 
                "media_id": str(media_obj),
                "media_type": type(media_obj).__name__
            }
        except Exception as e:
            logger.error(f"Failed to upload media: {str(e)}")
            return {"success": False, "error": str(e)}