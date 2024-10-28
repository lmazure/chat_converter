# Conversion of a Google Chat workspace into a HTML file

## Use Google Takeout to retriev your chats
1) Go on [Google Takeout](https://takeout.google.com/)
2) Unselect all products
3) Select "Google Chat"
4) Click "Next step" at the bottom of the page
5) Select:
- "Send the download link by email"
- "Single exportation"
- Format = ZIP
- File size = 10G
6) Click "Create export"

## Get the workpace data
1) Once you have received the link, download the ZIP file.
2) Navigate in it and look for the folder containing the workspace (if the URL of the workspace is `https://mail.google.com/chat/u/0/#chat/space/AAAA2mKCqoY` the folder is `Takeout/Google Chat/Groups/Space AAAA2mKCqoY`).
3) Extract it from the ZIP, for example on your desktop.

## Generate the HTML file
Run the script
```bash
python convertToHtml.py /c/Users/johndoe/Desktop/Space\ AAAA2mKCqoY/
```
This creates a single HTML file `chat_history.html` in the current directory. This one contains the whole workspace data.
