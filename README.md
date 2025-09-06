# PyWA MCP Server

A comprehensive Model Context Protocol (MCP) server that exposes full WhatsApp Business API functionality using the PyWA library.

## Features

This MCP server provides **18 WhatsApp tools** organized into four categories:

### Messaging Tools (12)
- **Text & Media**: `send_message`, `send_image`, `send_video`, `send_document`, `send_audio`, `send_sticker`
- **Location & Contacts**: `send_location`, `request_location`, `send_contact`
- **Interactions**: `send_reaction`, `remove_reaction`, `upload_media`

### Interactive Tools (2)
- **Interactive Messages**: `send_message_with_buttons`, `send_message_with_list`

### Template Tools (2)
- **Template Messaging**: `send_template`, `get_templates`

### Status Tools (2)
- **Message Status**: `mark_message_as_read`, `indicate_typing`

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure WhatsApp credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your WhatsApp Cloud API credentials
   ```

3. **Run the server:**
   ```bash
   # Production mode
   uv run python server.py
   
   # Development mode with Web UI (recommended for testing)
   uv run fastmcp dev --ui-port 6275 server.py
   ```

## Configuration

Set these environment variables:
- `WHATSAPP_PHONE_ID` - Your WhatsApp Business phone number ID
- `WHATSAPP_TOKEN` - Your WhatsApp Cloud API access token

Get these from your [Meta Developer Console](https://developers.facebook.com/).

## Development & Testing

### Web UI (Recommended for Development)
Test your WhatsApp tools interactively with the FastMCP Inspector:

```bash
uv run fastmcp dev --ui-port 6275 server.py
```

Open http://localhost:6275 in your browser to:
- View all 15+ WhatsApp tools
- Test messaging, buttons, lists, templates
- See real-time API calls and responses
- Debug with comprehensive error messages

### Testing with Real WhatsApp
1. Get WhatsApp Business API credentials from [Meta Developer Console](https://developers.facebook.com/)
2. Add test phone numbers in your Meta Developer Console
3. Use the Web UI to send messages to test numbers
4. Verify messages appear in WhatsApp

## Claude Desktop Integration

### Quick Setup (One Command)
Install directly in Claude Desktop config:

```json
{
  "mcpServers": {
    "pywa-whatsapp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Jem-HR/pywa-mcp-server.git",
        "pywa-mcp-server"
      ],
      "env": {
        "WHATSAPP_PHONE_ID": "your_phone_id",
        "WHATSAPP_TOKEN": "your_token"
      }
    }
  }
}
```

This automatically downloads and runs the server without manual installation.

### Manual Configuration

1. **Locate Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add server configuration:**
   ```json
   {
     "mcpServers": {
       "pywa-whatsapp": {
         "command": "uv",
         "args": [
           "run",
           "python",
           "/path/to/pywa-mcp-server/server.py"
         ],
         "env": {
           "WHATSAPP_PHONE_ID": "your_phone_number_id",
           "WHATSAPP_TOKEN": "your_whatsapp_cloud_api_token"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Verify connection:** Look for the 🔨 hammer icon in Claude Desktop

### Using WhatsApp Tools in Claude Desktop

Once connected, you can ask Claude to:

**Send Messages:**
```
Send a WhatsApp message to +1234567890 saying "Hello from Claude!"
```

**Create Interactive Buttons:**
```
Send a WhatsApp message with buttons asking "Are you available?" 
with Yes/No options to +1234567890
```

**Build Menu Lists:**
```
Create a WhatsApp menu for a restaurant with sections for Main Courses 
and Beverages, send to +1234567890
```

**Show Typing Indicators:**
```
Show typing indicator for WhatsApp message ID wamid.XXX to let the user 
know I'm preparing a response
```

**Send Media:**
```
Send an image from URL https://example.com/image.jpg with caption 
"Check this out!" to +1234567890
```

**Use Templates:**
```
Send the "welcome_message" template in English to +1234567890
```

### Available WhatsApp Tools in Claude

Claude has access to these WhatsApp capabilities:

**📝 Messaging (12 tools):**
- `send_message` - Text messages with headers/footers
- `send_image` - Images with captions
- `send_video` - Videos with captions  
- `send_document` - Files with custom names
- `send_audio` - Audio messages
- `send_sticker` - WebP stickers
- `send_location` - GPS coordinates
- `request_location` - Ask user for location
- `send_contact` - Contact cards
- `send_reaction` - Emoji reactions
- `remove_reaction` - Remove reactions
- `upload_media` - Upload files to WhatsApp

**🎛️ Interactive (2 tools):**
- `send_message_with_buttons` - Up to 3 reply buttons
- `send_message_with_list` - Selection lists with sections

**📋 Templates (2 tools):**
- `send_template` - Pre-approved template messages
- `get_templates` - List available templates

**⚡ Status (2 tools):**
- `mark_message_as_read` - Mark messages as read
- `indicate_typing` - Show typing indicator

## Architecture

The server uses a modular architecture:
- **server.py** - Main MCP server using FastMCP framework
- **tools/messaging.py** - Text, media, location, contact, and reaction tools
- **tools/interactive.py** - Button, list, catalog, and flow message tools
- **tools/templates.py** - Template messaging and authentication tools

All tools follow consistent patterns:
- Async implementation for optimal performance
- Comprehensive error handling with success/error responses
- Direct mapping to PyWA library methods
- Full type safety and parameter validation

## Tool Examples

### send_message
Send a text message to a WhatsApp user.
```python
{
  "to": "+1234567890",
  "text": "Hello from PyWA MCP Server!",
  "preview_url": true,
  "reply_to_message_id": "optional_message_id"
}
```

### send_button_message
Send an interactive message with reply buttons.
```python
{
  "to": "+1234567890",
  "text": "Choose an option:",
  "buttons": [
    {"id": "option1", "title": "Option 1"},
    {"id": "option2", "title": "Option 2"}
  ],
  "header": "Quick Actions",
  "footer": "Select one option"
}
```

### send_template
Send a pre-approved template message.
```python
{
  "to": "+1234567890",
  "template": "hello_world",
  "language": "en",
  "components": [
    {
      "type": "body",
      "parameters": [
        {"type": "text", "text": "John Doe"}
      ]
    }
  ]
}
```

## Troubleshooting

### Common Issues

**❌ "Missing required environment variables"**
- Ensure `.env` file exists with `WHATSAPP_PHONE_ID` and `WHATSAPP_TOKEN`
- Check values are correct from Meta Developer Console

**❌ "Cannot import name 'X' from pywa.types"**
- Run `uv sync` to update dependencies
- PyWA version must be >=3.0.0

**❌ "401 Unauthorized" from WhatsApp API**
- Verify your `WHATSAPP_TOKEN` is current and has proper permissions
- Check token hasn't expired in Meta Developer Console

**❌ Claude Desktop doesn't show tools**
- Check `claude_desktop_config.json` syntax is valid JSON
- Ensure file paths are absolute, not relative
- Restart Claude Desktop after config changes
- Look for 🔨 hammer icon to confirm connection

**❌ "Typing indicator failed"**
- `indicate_typing` requires a valid message ID from an incoming message
- Cannot use with arbitrary message IDs - must be from actual WhatsApp messages received

### Debug Mode

Enable detailed logging by setting environment variable:
```bash
export PYTHONPATH=/path/to/pywa-mcp-server
LOGLEVEL=DEBUG uv run python server.py
```

### Getting Help

- Check the [PyWA Documentation](https://pywa.readthedocs.io/) for WhatsApp API details
- Review [Meta Developer Console](https://developers.facebook.com/) for API setup
- Test tools individually using the Web UI before Claude Desktop integration

## License

MIT