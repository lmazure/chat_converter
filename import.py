import json
from datetime import datetime
import os
import sys
import argparse

def convert_chat_to_html(json_data):
    """
    Convert Google Chat JSON data to formatted HTML
    
    Args:
        json_data (str): JSON string containing chat data
        
    Returns:
        str: Formatted HTML string
    """
    # Parse JSON data
    try:
        chat_data = json.loads(json_data)
    except json.JSONDecodeError:
        return "Error: Invalid JSON data"
    
    # HTML template
    html_output = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Chat History</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .sender { font-weight: bold; margin-bottom: 5px; }
            .timestamp { color: #666; font-size: 0.8em; }
            .content { margin-top: 5px; }
            .attachment { margin-top: 5px; color: #0066cc; }
        </style>
    </head>
    <body>
        <h1>Chat History</h1>
        <div class="chat-container">
    """
    
    # Process each message
    for message in chat_data.get('messages', []):
        timestamp = message.get('created_date', '')
        author = message.get('creator', {}).get('name', 'Unknown')
        content = message.get('text', '')
        id = message.get('message_id', '')
        
        message_html = f"""
        <div class="message">
            <span class="sender">{author}</span> - <span class="timestamp">{timestamp}</span>
            <div class="content">{content}</div>
        """
        
        # Handle attachments if present
        attachments = message.get('attached_files', [])
        if attachments:
            for attachment in attachments:
                message_html += f'<a class="attachment" href="">📎 Attachment: {attachment.get("export_name", "Unknown file")}</a>'
        
        message_html += "</div>"
        html_output += message_html
    
    # Close HTML tags
    html_output += """
        </div>
    </body>
    </html>
    """
    
    return html_output

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert Google Chat JSON to HTML')
    parser.add_argument('directory', help='Directory containing messages.json')
    args = parser.parse_args()
    
    # Construct input file path
    json_path = os.path.join(args.directory, 'messages.json')
    
    # Output file will be in current directory
    output_path = 'chat_history.html'
    
    # Verify input file exists
    if not os.path.exists(json_path):
        print(f"Error: messages.json not found in {args.directory}")
        sys.exit(1)
    
    try:
        # Read JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        
        # Convert to HTML
        html_content = convert_chat_to_html(json_data)
        
        # Write HTML file to current directory
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Successfully converted chat history to: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
