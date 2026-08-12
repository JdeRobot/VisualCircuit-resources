# VisualCircuit-blocks

## Contributing a Custom Block to the Marketplace

If you have built an amazing block and want to share it with the world, follow these steps to get it published on the Marketplace:

1. **Build the Block**: Open VisualCircuit, construct your block's logic, and write your Python code inside the block.
2. **Edit Block Info**: Click the **Edit Info** button in VisualCircuit to carefully fill out your block's metadata (Name, Description, Author, Version, and Category).
3. **Export Files**: Click **Export Block**. This will download two files to your computer: a `.json` file (containing the code and port info) and a `.vc3` file (the graphical layout).
4. **Fork the Repository**: Fork this repository on GitHub and clone it locally.
5. **Add Your Files**: Place both the downloaded `.json` and `.vc3` files directly into the `custom_blocks/` folder.
6. **Submit a Pull Request**: Push your changes and open a Pull Request on GitHub using the exact structure below.

### Pull Request Structure
When opening your Pull Request on GitHub, please use the following structure in the description so maintainers can quickly review and merge your block:

**Description:**
```markdown
### 1. Author Name & Version
- **Name:** [Your Name / GitHub Username]
- **Version:** [e.g., 1.0.0]

### 2. One-line Description
[Provide a single sentence describing what this block does]

### 3. Libraries Used
[List any Python dependencies your block requires, e.g., numpy, opencv-python, or write "None"]

### 4. Full Workflow
[Explain the full workflow of how this block operates, which ROS nodes it interacts with, and how data is processed from input to output]
```
