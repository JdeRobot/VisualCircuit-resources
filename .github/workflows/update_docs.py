import json
import os
from bs4 import BeautifulSoup
import html

REGISTRY_PATH = 'marketplace/registry.json'
HTML_PATH = 'blockDocs/Blocks.html'
CUSTOM_BLOCKS_DIR = 'custom_blocks/'

def get_block_html(block_metadata, code, json_data):
    """Generates pdoc-styled HTML for a custom block, including the View Source button and port info"""
    name = block_metadata.get('name', 'CustomBlock')
    description = block_metadata.get('description', 'No description provided.')
    author = block_metadata.get('author', 'Unknown Author')
    version = block_metadata.get('version', '1.0.0')
    category = block_metadata.get('category', 'Custom')

    # Extract Ports and Parameters
    inputs = []
    outputs = []
    parameters = []
    
    if json_data:
        components = json_data.get('design', {}).get('graph', {}).get('blocks', [])
        for block in components:
            if block.get('type') == 'basic.code':
                ports = block.get('data', {}).get('ports', {})
                inputs = [p.get('name') for p in ports.get('in', [])]
                outputs = [p.get('name') for p in ports.get('out', [])]
                params_data = block.get('data', {}).get('params', [])
                parameters = [p.get('name') for p in params_data]
                break

    inputs_html = f"<p><strong>Inputs:</strong> {', '.join(inputs) if inputs else 'None'}</p>"
    outputs_html = f"<p><strong>Outputs:</strong> {', '.join(outputs) if outputs else 'None'}</p>"
    params_html = f"<p><strong>Parameters:</strong> {', '.join(parameters) if parameters else 'None'}</p>"

    escaped_code = html.escape(code)
    toggle_id = f"{name}-view-source".replace(" ", "-")

    html_content = f"""
    <section class="module-info custom-block">
        <h3 class="modulename" id="{name}">{name}</h3>
        <div class="docstring">
            <p><strong>Author:</strong> {author} | <strong>Version:</strong> {version} | <strong>Category:</strong> {category}</p>
            <p>{description}</p>
            {inputs_html}
            {outputs_html}
            {params_html}
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
        print("Could not find main class='pdoc' in HTML.")
        return

    custom_header_id = 'custom-blocks-marketplace'
    custom_header = soup.find('h2', id=custom_header_id)
    
    if not custom_header:
        custom_header = soup.new_tag('h2', id=custom_header_id)
        custom_header.string = 'Custom Marketplace Blocks'
        main_content.append(custom_header)

    for custom_section in soup.find_all('section', class_='custom-block'):
        custom_section.decompose()

    # Append all custom blocks from registry
    for block in registry.get('blocks', []):
        name = block.get('name', 'Unknown')
        
        json_filename = f"{name}.json"
        json_path = os.path.join(CUSTOM_BLOCKS_DIR, json_filename)
        
        code = "# Code not found"
        json_data = None
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    json_data = json.load(f)
                    components = json_data.get('design', {}).get('graph', {}).get('blocks', [])
                    for c in components:
                        if c.get('type') == 'basic.code':
                            code = c.get('data', {}).get('code', '')
                            break
            except Exception as e:
                print(f"Error parsing json for {name}: {e}")
            
        block_html = get_block_html(block, code, json_data)
        block_soup = BeautifulSoup(block_html, 'html.parser')
        main_content.append(block_soup)

    with open(HTML_PATH, 'w') as f:
        f.write(str(soup))

    print("Successfully updated Blocks.html with custom blocks from the marketplace.")

if __name__ == '__main__':
    main()
