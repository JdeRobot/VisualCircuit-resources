# VisualCircuit-blocks

## Contributing a Custom Block to the Marketplace

If you have built an amazing block and want to share it with the world, follow these steps to get it published on the Marketplace:

1. **Export Your Block**: Design your block in VisualCircuit and click Export Block. You will receive a `.json` and a `.vc3` file.
2. **Fork the Repository**: Fork this repository and clone it locally.
3. **Add Your Files**: Place both files inside the `custom_blocks/` folder.
4. **Submit a Pull Request**: Open a Pull Request using the exact structure below.

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
