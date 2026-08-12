import os
import json
from bs4 import BeautifulSoup
import html

REGISTRY_PATH = 'marketplace/registry.json'
HTML_PATH = 'blockDocs/Blocks.html'
CUSTOM_BLOCKS_DIR = 'custom_blocks/'
BLOCKS_DIR = 'blockDocs/Blocks/'

def get_template():
    # Use Blur.html as a template for the page structure
    template_path = os.path.join(BLOCKS_DIR, 'Blur.html')
    if not os.path.exists(template_path):
        # Fallback empty template if Blur is missing
        return "<html><body>{MAIN_CONTENT}</body></html>"
        
    with open(template_path, 'r') as f:
        html_content = f.read()
        
    main_start = html_content.find('<main class="pdoc">')
    main_end = html_content.find('</main>', main_start) + len('</main>')
    
    if main_start != -1 and main_end != -1:
        return html_content[:main_start] + "{MAIN_CONTENT}" + html_content[main_end:]
    return "<html><body>{MAIN_CONTENT}</body></html>"

def generate_block_page(block_metadata, code, json_data, template):
    name = block_metadata.get('name', 'CustomBlock')
    description = block_metadata.get('description', 'No description provided.')
    author = block_metadata.get('author', 'Unknown Author')
    version = block_metadata.get('version', '1.0.0')
    category = block_metadata.get('category', 'Custom')

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

    inputs_str = ', '.join(inputs) if inputs else 'None'
    outputs_str = ', '.join(outputs) if outputs else 'None'
    params_str = ', '.join(parameters) if parameters else 'None'

    escaped_code = html.escape(code)

    main_content = f"""<main class="pdoc">
    <section class="module-info">
        <h1 class="modulename">
            <a href="./../Blocks.html">Blocks</a><wbr>.{name}
        </h1>
    </section>
    <section id="section-intro">
        <div class="docstring">
            <p><strong>Author:</strong> {author} | <strong>Version:</strong> {version} | <strong>Category:</strong> {category}</p>
            <p>{description}</p>
            <p><strong>Inputs:</strong> {inputs_str}</p>
            <p><strong>Outputs:</strong> {outputs_str}</p>
            <p><strong>Parameters:</strong> {params_str}</p>
        </div>
    </section>
    <section>
        <h2 class="section-title" id="header-classes">Source Code</h2>
        <div class="pdoc-code codehilite"><pre><span></span><code>{escaped_code}</code></pre></div>
    </section>
</main>"""

    page_html = template.replace("{MAIN_CONTENT}", main_content)
    
    out_path = os.path.join(BLOCKS_DIR, f"{name}.html")
    with open(out_path, 'w') as f:
        f.write(page_html)
    print(f"Generated {out_path}")

def update_index(registry):
    with open(HTML_PATH, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Remove any old custom blocks injected previously
    custom_header = soup.find('h2', id='custom-blocks-marketplace')
    if custom_header:
        custom_header.decompose()
    for custom_section in soup.find_all('section', class_='custom-block'):
        custom_section.decompose()

    # Find the Submodules list
    submodules_header = soup.find('h2', string='Submodules')
    if not submodules_header:
        print("Could not find Submodules header in Blocks.html")
        return
        
    submodules_list = submodules_header.find_next_sibling('ul')
    if not submodules_list:
        print("Could not find Submodules list in Blocks.html")
        return

    # Add links for new blocks if they don't exist
    for block in registry.get('blocks', []):
        name = block.get('name', 'Unknown')
        link_href = f"Blocks/{name}.html"
        
        # Check if it already exists
        exists = False
        for a in submodules_list.find_all('a'):
            if a.get('href') == link_href:
                exists = True
                break
                
        if not exists:
            new_li = soup.new_tag('li')
            new_a = soup.new_tag('a', href=link_href)
            new_a.string = name
            new_li.append(new_a)
            submodules_list.append(new_li)
            print(f"Added link to Blocks.html: {name}")

    # Write the updated Blocks.html
    with open(HTML_PATH, 'w') as f:
        f.write(str(soup))
    print("Updated Blocks.html index")

def main():
    if not os.path.exists(REGISTRY_PATH):
        print(f"Registry not found at {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, 'r') as f:
        registry = json.load(f)

    template = get_template()

    # Generate individual pages
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
                
        generate_block_page(block, code, json_data, template)

    # Update index
    update_index(registry)

if __name__ == '__main__':
    main()
