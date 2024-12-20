import json
import os
import sys
import argparse
from html import escape
import base64
from pathlib import Path

def convert_chat_to_html(dir, json_data):

    # Parse JSON data
    try:
        chat_data = json.loads(json_data)
    except json.JSONDecodeError:
        return "Error: Invalid JSON data"

    
    # Process each message
    records = []
    attachment_count = {}

    for message in chat_data.get('messages', []):
        state = message.get('message_state', '')
        timestamp = message.get('created_date', '')
        author = message.get('creator', {}).get('name', 'Unknown')
        content = message.get('text', '')
        id = message.get('message_id', '')
        id_parts = id.split('/')
        if id_parts[1] == id_parts[2]:
            parent_id = None
            message_id = id_parts[1]
        else:
            parent_id = id_parts[1]
            message_id = id_parts[2]

        if state == 'DELETED':
            message_html += '<div class="message"><span class="sender">deleted message</span></div>'
        else:  
            message_html = f"""
            <div class="message">
                {"→ " if parent_id is not None else ""}
                <span class="sender">{escape(author)}</span> - <span class="timestamp">{escape(timestamp)}</span>
                <div class="content">{escape(content).replace('\n', '<br>')}</div>
            """

        # Process reactions
        reactions = message.get('reactions', [])
        for reaction in reactions:
            emoji = reaction.get('emoji', {}).get('unicode', '')
            reactors = ', '.join(reaction.get('reactor_emails', []))
            message_html += f'<div class="reaction">{emoji} {reactors}</div>'

        # Process attachments
        attachments = message.get('attached_files', [])
        if attachments:
            for attachment in attachments:
                attach = attachment.get("export_name", "Unknown file")
                
                # Check and update the count of the attachment
                if attach in attachment_count:
                    attachment_count[attach] += 1
                else:
                    attachment_count[attach] = 0

                # Append count if necessary
                attach_name, attach_ext = os.path.splitext(attach)
                if attachment_count[attach] > 0:
                    if attachment_count[attach] > 0:
                        attach_name = f"{attach_name}({attachment_count[attach]})"
                        attach = f"{attach_name}{attach_ext}"
                
                # trunacte loog file names
                if len(attach) > 48:
                    attach_name = attach_name[0:47]
                    attach = attach_name + attach_ext

                message_html += f'    <div class="attachment">📎 Attachment: {attach}</div>'
                
                if attach_ext.lower() == '.png':
                    file_path = os.path.join(dir, attach)
                    with open(file_path, 'rb') as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    message_html += f'<img src="data:image/png;base64,{encoded_image}">'

                if attach_ext.lower() == '.jpg':
                    file_path = os.path.join(dir, attach)
                    with open(file_path, 'rb') as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    message_html += f'<img src="data:image/jpg;base64,{encoded_image}">'

                if attach_ext.lower() == '.log':
                    file_path = os.path.join(dir, attach)
                    with open(file_path, 'r', encoding='utf-8') as log_file:
                        log_content = log_file.read()
                    message_html += f'<details><summary>File content</summary><pre>{escape(log_content).replace('\n', '<br>')}</pre></details>'

        message_html += "</div>"

        records.append({ 'id': message_id, 'parent': parent_id, 'message': message_html })
    
    # HTML template
    html_output = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Chat History</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0 auto; padding: 20px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .sender { font-weight: bold; margin-bottom: 5px; }
            .reaction { color: #666; font-size: 0.8em; }
            .timestamp { color: #666; font-size: 0.8em; }
            .content { margin-top: 5px; }
            .attachment { margin-top: 5px; color: #8B0000; }
        </style>
    </head>
    <body>
        <h1>Chat History</h1>
        <div class="chat-container">
    """
    
    # Add messages to HTML output
    for record in records:
        if record['parent'] is None:
            html_output += record['message']
            for subrecord in records:
                if subrecord['parent'] == record['id']:
                    html_output += subrecord['message']

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
        html_content = convert_chat_to_html(args.directory, json_data)
        
        # Write HTML file to current directory
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Successfully converted chat history to: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
