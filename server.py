#!/usr/bin/env python3
"""
PyWA MCP Server - A comprehensive MCP server exposing WhatsApp messaging functionality.

This server provides tools for:
- Text and media messaging (images, videos, documents, audio, stickers)
- Location sharing and contact cards
- Interactive messages (buttons, lists, catalogs, products)
- Template messages with media and parameters
- Message reactions and status updates
"""

import logging
import os
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP
from pywa import WhatsApp
from tools import register_all_tools

# Load environment variables from .env file
load_dotenv()

# Configure logging to stderr (not stdout per MCP requirements)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("PyWA WhatsApp Server")

# Global WhatsApp client instance
wa_client: Optional[WhatsApp] = None


def get_whatsapp_client() -> WhatsApp:
    """Get or create WhatsApp client instance."""
    global wa_client
    
    if wa_client is None:
        # Get configuration from environment variables
        phone_id = os.getenv("WHATSAPP_PHONE_ID")
        token = os.getenv("WHATSAPP_TOKEN")
        
        if not phone_id or not token:
            raise ValueError(
                "Missing required environment variables: WHATSAPP_PHONE_ID and WHATSAPP_TOKEN"
            )
        
        wa_client = WhatsApp(
            phone_id=phone_id,
            token=token
        )
        logger.info("WhatsApp client initialized")
    
    return wa_client


# Initialize WhatsApp client and register tools on startup
try:
    client = get_whatsapp_client()
    logger.info("WhatsApp client configuration validated")
    
    # Register all tools from modules
    register_all_tools(mcp, client)
    logger.info("All tools registered successfully")
    
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    logger.error("Please set WHATSAPP_PHONE_ID and WHATSAPP_TOKEN environment variables")


if __name__ == "__main__":
    mcp.run()