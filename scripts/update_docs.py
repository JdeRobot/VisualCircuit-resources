import json
import os
import glob
from bs4 import BeautifulSoup
import urllib.request
import html

REGISTRY_PATH = 'marketplace/registry.json'
HTML_PATH = 'blockDocs/Blocks.html'
CUSTOM_BLOCKS_DIR = 'custom_blocks/'

def extract_code_from_json(json_path):
    """Extracts Python code from the custom block JSON file"""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            components = data.get('design', {}).get('graph', {}).get('blocks', [])
            for block in components:
                if block.get('type') == 'basic.code':
                    return block.get('data', {}).get('code', '')
    except Exception as e:
        print(f"Error reading code from {json_path}: {e}")
    return "# Code could not be loaded."

def get_block_html(block_metadata, code):
    """Generates pdoc-styled HTML for a custom block, including the View Source button"""
    name = block_metadata.get('name', 'CustomBlock')
    description = block_metadata.get('description', 'No description provided.')
    author = block_metadata.get('author', 'Unknown Author')
    version = block_metadata.get('version', '1.0.0')
    category = block_metadata.get('category', 'Custom')

    # Escape the code for HTML display
    escaped_code = html.escape(code)
    toggle_id = f"{name}-view-source".replace(" ", "-")

    html_content = f"""
    <section class="module-info custom-block">
        <h3 class="modulename" id="{name}">{name}</h3>
        <div class="docstring">
            <p><strong>Author:</strong> {author} | <strong>Version:</strong> {version}</p>
            <p>{description}</p>
            <p><strong>Category:</strong> {category}</p>
        </div>
        
        <input id="{toggle_id}" class="view-source-toggle-state" type="checkbox" aria-hidden="true" tabindex="-1">
        <label class="view-source-button" for="{toggle_id}"><span>View Source</span></label>
        <div class="pdoc-code codehilite">
            <pre><span></span><code>{escaped_code}</code></pre>
        </div>
    </section>
    """
    return html_content

def main():
    if not os.path.exists(REGISTRY_PATH):
        print(f"Registry not found at {REGISTRY_PATH}")
        return

    if not os.path.exists(HTML_PATH):
        print(f"HTML documentation not found at {HTML_PATH}")
        return

    with open(REGISTRY_PATH, 'r') as f:
        registry = json.load(f)

    with open(HTML_PATH, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    main_content = soup.find('main', class_='pdoc')
    if not main_content:
        print("Could not find <main class='pdoc'> in HTML.")
        return

    # Create or find the Custom Blocks section header
    custom_header_id = 'custom-blocks-marketplace'
    custom_header = soup.find('h2', id=custom_header_id)
    
    if not custom_header:
        custom_header = soup.new_tag('h2', id=custom_header_id)
        custom_header.string = 'Custom Marketplace Blocks'
        main_content.append(custom_header)

    # Clear old custom blocks
    for custom_section in soup.find_all('section', class_='custom-block'):
        custom_section.decompose()

    # Append all custom blocks from registry
    for block in registry:
        name = block.get('name', 'Unknown')
        
        # Try to find the corresponding JSON file in custom_blocks/
        json_filename = f"{name}.json"
        json_path = os.path.join(CUSTOM_BLOCKS_DIR, json_filename)
        
        code = "# Code not found"
        if os.path.exists(json_path):
            code = extract_code_from_json(json_path)
            
        block_html = get_block_html(block, code)
        block_soup = BeautifulSoup(block_html, 'html.parser')
        main_content.append(block_soup)

    with open(HTML_PATH, 'w') as f:
        f.write(str(soup))

    print("Successfully updated Blocks.html with custom blocks from the marketplace.")

if __name__ == '__main__':
    main()
