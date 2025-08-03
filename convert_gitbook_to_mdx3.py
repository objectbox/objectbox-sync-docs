import re
import glob
import os
import sys
from pathlib import Path

print("Script starting...NEW SCRIPT 30.06.2025 14:33 - DEBUG ENHANCED")  # Debug print

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, 'website', 'docs')

def ensure_valid_frontmatter(content):
    """Ensure the file has valid frontmatter."""
    if content.startswith('---\n'):
        return content
    # Otherwise, try to extract a description
    match = re.search(r'^(.*?)\n\n', content, re.DOTALL)
    if match:
        description = match.group(1).strip()
        if not description.startswith('#'):
            frontmatter = f'---\ndescription: >\n  {description}\n---\n\n'
            content = content[len(match.group(0)):]
            return frontmatter + content
    return content

def find_docs_files_recursive(directory='.'):
    """Find all .md and .mdx files recursively in the given directory and subdirectories, excluding website/docs."""
    print(f"[DEBUG] FOLDER FIX: Searching recursively in directory: {directory}")
    all_files = []
    for ext in ['*.md', '*.mdx']:
        # Use ** for recursive search
        pattern = os.path.join(directory, '**', ext)
        files = glob.glob(pattern, recursive=True)
        print(f"[DEBUG] FOLDER FIX: Found {len(files)} {ext} files with pattern {pattern}")
        # Filter out files from website/docs directory
        files = [f for f in files if not f.startswith(os.path.join('website', 'docs')) and 'website' not in f]
        print(f"[DEBUG] FOLDER FIX: After filtering, {len(files)} files remain")
        all_files.extend(files)
    
    print(f"[DEBUG] FOLDER FIX: Total files found: {len(all_files)}")
    for file in all_files:
        print(f"[DEBUG] FOLDER FIX: - {file}")
    
    return all_files

def get_output_path(input_file, source_dir='.', output_dir='../website/docs'):
    """Generate output path maintaining folder structure."""
    # Get relative path from source directory
    rel_path = os.path.relpath(input_file, source_dir)
    
    # Change extension to .mdx
    if rel_path.endswith('.md'):
        rel_path = rel_path[:-3] + '.mdx'
    
    # Combine with output directory
    output_path = os.path.join(output_dir, rel_path)
    
    print(f"[DEBUG] FOLDER FIX: Input: {input_file} -> Output: {output_path}")
    
    return output_path


def extract_yaml_frontmatter(lines):
    if lines and lines[0].strip() == '---':
        fm = []
        for i, line in enumerate(lines):
            fm.append(line)
            if line.strip() == '---' and i > 0:
                return fm, lines[i+1:]
    return [], lines

def improved_escape_curly_braces(content):
    """Improved brace escaping that handles more edge cases."""
    print(f"[DEBUG] improved_escape_curly_braces called, found {content.count('{')} opening braces")
    lines = content.splitlines()
    result = []
    in_code_block = False
    in_jsx_block = False
    jsx_stack = []
    code_block_count = 0
    escaped_lines = 0
    
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Track code blocks
        if stripped.startswith('```'):
            print(f"[DEBUG] BACKTICK: Line {line_num} has code block markers: {stripped}")
            in_code_block = not in_code_block
            if in_code_block:
                code_block_count += 1
                print(f"[DEBUG] Code block {code_block_count} starts at line {line_num}")
            else:
                print(f"[DEBUG] Code block {code_block_count} ends at line {line_num}")
            result.append(line)
            continue
        
        if in_code_block:
            result.append(line)
            continue
        
        # Track JSX components
        jsx_open_matches = re.findall(r'<([A-Z][a-zA-Z0-9]*)', line)
        for tag in jsx_open_matches:
            jsx_stack.append(tag)
            in_jsx_block = True
        
        jsx_close_matches = re.findall(r'</([A-Z][a-zA-Z0-9]*)', line)
        for tag in jsx_close_matches:
            if jsx_stack and jsx_stack[-1] == tag:
                jsx_stack.pop()
            if not jsx_stack:
                in_jsx_block = False
        
        # Skip escaping in certain contexts
        should_skip = (
            in_jsx_block or
            stripped.startswith(('import ', 'export ')) or
            '{% ' in stripped or
            stripped.startswith(':::') or
            stripped.startswith('@tab ') or
            re.match(r'^<[A-Z]', stripped)
        )
        
        if should_skip:
            result.append(line)
        else:
            # Escape braces while preserving inline code
            parts = re.split(r'(`[^`]*`)', line)
            escaped_parts = []
            has_braces = False
            for part in parts:
                if part.startswith('`') and part.endswith('`'):
                    print(f"[DEBUG] BACKTICK: Line {line_num} has inline code with backticks: {part}")
                    escaped_parts.append(part)  # Preserve inline code
                else:
                    if '{' in part or '}' in part:
                        has_braces = True
                    escaped_parts.append(part.replace('{', '&#123;').replace('}', '&#125;'))
            if has_braces:
                escaped_lines += 1
            result.append(''.join(escaped_parts))
    
    print(f"[DEBUG] improved_escape_curly_braces: {code_block_count} code blocks found, {escaped_lines} lines escaped")
    remaining_braces = '\n'.join(result).count('{')
    print(f"[DEBUG] {remaining_braces} braces remain (should be in code blocks or JSX)")
    return '\n'.join(result)

def fix_html_and_escape(content):
    """
    Comprehensive HTML fixing for MDX compatibility.
    This replaces the original fix_html_and_escape function.
    """
    import re
    
    print("[DEBUG] fix_html_and_escape called - COMPREHENSIVE VERSION")
    
    # Check for backticks in input
    backtick_count = content.count('`')
    print(f"[DEBUG] BACKTICK: fix_html_and_escape input has {backtick_count} backticks")
    
    # 1) Normalize <options>...</options>
    def opt(m):
        return f'```txt\n{m.group(1).strip()}\n```'
    content = re.sub(r'<options\b[^>]*>([\s\S]*?)</options>', opt, content, flags=re.IGNORECASE)

    # 2) Convert <pre><code> to code blocks
    def pre(m):
        attrs, code_attrs, code = m.group(1), m.group(2), m.group(3)
        lang = (re.search(r'language-(\w+)', attrs + code_attrs) or [None, None])[1] or ''
        txt = re.sub(r'<[^>]+>', '', code).strip()
        print(f"[DEBUG] BACKTICK: fix_html_and_escape creating code block with backticks")
        return f'```{lang}\n{txt}\n```'
    content = re.sub(r'<pre([^>]*)><code([^>]*)>([\s\S]*?)</code></pre>', pre, content, flags=re.IGNORECASE)

    # 3) Fix ALL unclosed HTML tags that need to be self-closed
    print("[DEBUG] Fixing unclosed HTML tags...")
    
    # Fix <br> tags - make them self-closing
    content = re.sub(r'<br(?!/>)', '<br/>', content)
    print(f"[DEBUG] Fixed <br> tags")
    
    # Fix <img> tags - make them self-closing (improved regex)
    content = re.sub(r'<img([^>]*?)(?<!/)>', r'<img\1/>', content)
    print(f"[DEBUG] Fixed <img> tags")
    
    # Fix <hr> tags - make them self-closing
    content = re.sub(r'<hr(?!\s*/>)(?![^>]*>)', '<hr/>', content)
    print(f"[DEBUG] Fixed <hr> tags")
    
    # Fix <input> tags - make them self-closing
    content = re.sub(r'<input([^>]*?)(?<!/)>', r'<input\1/>', content)
    print(f"[DEBUG] Fixed <input> tags")

    # 4) MINIMAL IMAGE PATH FIXES - Convert GitBook paths to Docusaurus paths
    print("[DEBUG] MINIMAL IMAGE PATH FIXES: Converting GitBook image paths...")
    
    # Fix image paths in markdown syntax: ![alt](path)
    content = re.sub(
        r'!\[([^\]]*)\]\((?:docs/|\.\./)\.gitbook/assets/([^)]+)\)', 
        r'![\1](/img/assets/\2)', 
        content
    )
    print(f"[DEBUG] MINIMAL FIX: Fixed GitBook markdown image syntax")
    
    # Fix image paths in HTML img src attributes
    content = re.sub(
        r'<img([^>]*?)src="(?:docs/|\.\./)\.gitbook/assets/([^"]+)"([^>]*?)/?>', 
        r'<img\1src="/img/assets/\2"\3/>', 
        content
    )
    print(f"[DEBUG] MINIMAL FIX: Fixed GitBook image src attributes")
    # Fix image paths starting with .gitbook/assets/
    content = re.sub(
        r'<img([^>]*?)src="\.gitbook/assets/([^"]+)"([^>]*?)/?>', 
        r'<img\1src="/img/assets/\2"\3/>', 
        content
    )

    print(f"[DEBUG] MINIMAL FIX: Fixed .gitbook/assets image paths")


    # --- EXTENSIONS: catch more variants ---
    # Markdown images with or without angle brackets and any relative path
    content = re.sub(
        r'!\[([^\]]*)\]\(\s*<?(?:\.?\.?/)*\.gitbook/assets/([^)>]+)>?\s*\)',
        r'![\1](/img/assets/\2)',
        content
    )
    # HTML <img> tags with any relative path and single/double quotes
    content = re.sub(
        r'<img([^>]*?)src=["\'](?:\.?\.?/)*\.gitbook/assets/([^"\'>\s]+)["\']([^>]*?)/?>',
        r'<img\1src="/img/assets/\2"\3/>',
        content
    )

    # 5) Convert figure+img to markdown (IMPROVED to prevent extra characters)
    def fig(m):
        img_tag = m.group(1)
        
        # Extract src and alt attributes from the img tag
        src_match = re.search(r'src="([^"]+)"', img_tag)
        alt_match = re.search(r'alt="([^"]*)"', img_tag)
        
        src = src_match.group(1) if src_match else ''
        alt = alt_match.group(1) if alt_match else ''
        
        # Fix the src path if it's a GitBook path
        if '.gitbook/assets' in src:
            # This handles paths like '.gitbook/assets/image.png'
            src = f'/img/assets/{src.split("/")[-1]}'
        elif 'gitbook/assets' in src:
            # This handles paths like 'docs/.gitbook/assets/image.png'
            src = re.sub(r'(?:docs/|\.\./)?\.gitbook/assets/', '/img/assets/', src)

        # Create a clean markdown image tag. This is the key change.
        # It ensures no extra characters from the original <figure> tag are left behind.
        return f'![{alt}]({src})'

    # The regex now correctly captures only the <img> tag inside the <figure>
    content = re.sub(r'<figure>\s*(<img[^>]+>)\s*(?:<figcaption>.*?</figcaption>)?\s*</figure>', fig, content, flags=re.IGNORECASE | re.DOTALL)

    # 6) Remove leftover HTML tags (this might be redundant now but is safe to keep)
    content = re.sub(r'</?(?:figure|figcaption)>', '', content)

    # 7) Fix any remaining problematic HTML in tables
    print("[DEBUG] Fixing table HTML...")
    
    # Fix span tags with GitBook custom attributes (convert to simple text)
    content = re.sub(
        r'<span data-gb-custom-inline[^>]*>([^<]*)</span>', 
        r'\1', 
        content
    )
    
    # Fix figcaption tags (convert to simple text or remove)
    content = re.sub(r'<figcaption[^>]*>(.*?)</figcaption>', r'*\1*', content, flags=re.DOTALL)

    # Check for backticks in output
    backtick_count_after = content.count('`')
    print(f"[DEBUG] BACKTICK: fix_html_and_escape output has {backtick_count_after} backticks (change: {backtick_count_after - backtick_count})")
    
    print("[DEBUG] fix_html_and_escape completed - COMPREHENSIVE VERSION")
    return content

def fix_gitbook_content_ref_to_cards(content):
    """
    Fix GitBook content-ref blocks by converting them to styled Docusaurus cards
    with improved button-like appearance and hover effects.
    """
    import re
    
    print("[DEBUG] fix_gitbook_content_ref_to_cards called")
    
    # Pattern to match GitBook content-ref blocks
    content_ref_pattern = r'{% content-ref url="([^"]*)" %}\s*\[([^\]]*)\]\([^)]*\)\s*{% endcontent-ref %}'
    
    def content_ref_to_card(match):
        url = match.group(1)
        link_text = match.group(2)
        
        print(f"[DEBUG] Converting content-ref to card: url='{url}', text='{link_text}'")
        
        # Convert .md to clean URL for Docusaurus routing
        if url.endswith('.md'):
            clean_url = url[:-3]
        elif url.endswith('.mdx'):
            clean_url = url[:-4]
        else:
            clean_url = url
        
        # Create a friendly title from the filename
        if clean_url == 'installation':
            card_title = 'Installation'
            card_description = 'Get ObjectBox library and generator set up in your project'
        elif clean_url == 'getting-started':
            card_title = 'How to get started'
            card_description = 'Learn the basics of using ObjectBox in your application'
        else:
            # Fallback: use the link text as title
            card_title = link_text.replace('.md', '').replace('-', ' ').title()
            card_description = f'Learn more about {card_title.lower()}'
        
        # Create a styled card component with custom classes for styling
        card_html = f'''<div className="custom-nav-card">
  <a href="/{clean_url}" className="custom-nav-card-link">
    <div className="custom-nav-card-content">
      <h3 className="custom-nav-card-title">{card_title}</h3>
      <p className="custom-nav-card-description">{card_description}</p>
    </div>
    <div className="custom-nav-card-arrow">›</div>
  </a>
</div>'''
        
        print(f"[DEBUG] Created styled card for: {card_title}")
        return card_html
    
    # Count content-ref blocks before conversion
    content_refs = re.findall(content_ref_pattern, content, flags=re.DOTALL)
    print(f"[DEBUG] Found {len(content_refs)} content-ref blocks to convert to cards")
    
    # Debug: Show what content-refs were found
    for i, (url, text) in enumerate(content_refs):
        print(f"[DEBUG] Content-ref {i+1}: url='{url}', text='{text}'")
    
    # Apply the conversion
    result = re.sub(content_ref_pattern, content_ref_to_card, content, flags=re.DOTALL)
    
    # Check for any remaining GitBook content-ref patterns
    remaining_refs = re.findall(r'{% content-ref|{% endcontent-ref %}', result)
    if remaining_refs:
        print(f"[DEBUG] WARNING: Found {len(remaining_refs)} unconverted content-ref elements")
    else:
        print("[DEBUG] SUCCESS: All GitBook content-ref blocks converted to styled cards")
    
    return result

def enhanced_convert_gitbook_code_blocks_simple(content):
    """
    Enhanced version that handles ALL GitBook code block patterns, including:
    - Titles with inner quotes (FIXED)
    - Empty content preservation (FIXED)
    - Fallback for any remaining patterns (NEW)
    - Better error handling and debugging (NEW)
    - FIXED: "no such group" error with detailed debugging
    """
    import re
    
    print("[DEBUG] BACKTICK: convert_gitbook_code_blocks_simple input has {} backticks".format(content.count('`')))
    
    def code_block_replace(match):
        print(f"[DEBUG] code_block_replace called with {len(match.groups())} groups")
        
        # Debug: Print all groups
        for i in range(len(match.groups()) + 1):
            try:
                group_content = match.group(i)
                print(f"[DEBUG] Group {i}: '{group_content[:50]}{'...' if len(group_content) > 50 else ''}'")
            except IndexError:
                print(f"[DEBUG] Group {i}: <does not exist>")
        
        # FIXED: Safe group access with proper error handling
        try:
            # Different patterns have different group structures
            groups = match.groups()
            print(f"[DEBUG] Total groups available: {len(groups)}")
            
            if len(groups) == 2:
                # Pattern 2: title + content (no language)
                title = groups[0]
                language = ""
                code_content = groups[1]
                print(f"[DEBUG] Pattern 2 detected: title='{title}', content_length={len(code_content)}")
            elif len(groups) == 3:
                # Pattern 1: title + language + content
                title = groups[0]
                language = groups[1] if groups[1] else ""
                code_content = groups[2]
                print(f"[DEBUG] Pattern 1 detected: title='{title}', language='{language}', content_length={len(code_content)}")
            elif len(groups) == 1:
                # Pattern 3: just content (no title)
                title = ""
                language = groups[0] if groups[0] else ""
                code_content = groups[1] if len(groups) > 1 else ""
                print(f"[DEBUG] Pattern 3 detected: language='{language}', content_length={len(code_content)}")
            else:
                print(f"[DEBUG] ERROR: Unexpected group count: {len(groups)}")
                return match.group(0)  # Return original if unexpected structure
            
        except Exception as e:
            print(f"[DEBUG] ERROR in group access: {e}")
            return match.group(0)  # Return original on error
        
        print(f"[DEBUG] Processing code block - title: '{title}', language: '{language}', content length: {len(code_content)}")
        
        if not code_content.strip():
            print(f"[DEBUG] WARNING: Empty content detected for title: '{title}'")
        
        # Extract file extension from title to determine language
        if not language:
            language = "text"  # default for plain text content
            if title:
                if title.endswith('.fbs'):
                    language = "fbs"
                elif title.endswith('.cpp') or title.endswith('.hpp'):
                    language = "cpp"
                elif title.endswith('.c') or title.endswith('.h'):
                    language = "c"
                elif title.endswith('.cmake') or 'CMake' in title:
                    language = "cmake"
                elif title.endswith('.sh') or title.endswith('.bash'):
                    language = "sh"
                elif title.endswith('.py'):
                    language = "python"
                elif title.endswith('.js'):
                    language = "javascript"
                elif title.endswith('.go'):
                    language = "go"
                # For error messages, outputs, etc., keep "text"
        
        # Create proper code block with title
        if title:
            # Clean up title - remove inner quotes for markdown compatibility
            clean_title = title.replace('"', '')
            result = f'```{language} title="{clean_title}"\n{code_content}\n```'
            print(f"[DEBUG] Created code block with title: ```{language} title=\"{clean_title}\"")
        else:
            result = f'```{language}\n{code_content}\n```'
            print(f"[DEBUG] Created code block without title: ```{language}")
        
        print(f"[DEBUG] Code block creation successful")
        return result
    
    # PATTERN 1: {% code title="..." %} with language specified
    # FIXED: Use non-greedy matching for titles with inner quotes
    pattern1 = r'{% code title="(.*?)" %}\s*```([a-zA-Z]*)\s*\n(.*?)\n```\s*{% endcode %}'
    print(f"[DEBUG] Testing Pattern 1: {pattern1}")
    matches1 = re.findall(pattern1, content, flags=re.DOTALL)
    print(f"[DEBUG] Pattern 1 found {len(matches1)} matches")
    if matches1:
        for i, match in enumerate(matches1):
            print(f"[DEBUG] Pattern 1 Match {i+1}: title='{match[0]}', lang='{match[1]}', content_len={len(match[2])}")
    
    try:
        content = re.sub(pattern1, lambda m: code_block_replace(m), content, flags=re.DOTALL)
        print(f"[DEBUG] Pattern 1 substitution completed successfully")
    except Exception as e:
        print(f"[DEBUG] ERROR in Pattern 1 substitution: {e}")
    
    # PATTERN 2: {% code title="..." %} WITHOUT language (THE PROBLEMATIC CASE - FIXED)
    # FIXED: Use non-greedy matching for titles with inner quotes
    pattern2 = r'{% code title="(.*?)" %}\s*```\s*\n(.*?)\n```\s*{% endcode %}'
    print(f"[DEBUG] Testing Pattern 2: {pattern2}")
    matches2 = re.findall(pattern2, content, flags=re.DOTALL)
    print(f"[DEBUG] Pattern 2 found {len(matches2)} matches")
    if matches2:
        for i, match in enumerate(matches2):
            print(f"[DEBUG] Pattern 2 Match {i+1}: title='{match[0]}', content_len={len(match[1])}")
    
    try:
        content = re.sub(pattern2, lambda m: code_block_replace(m), content, flags=re.DOTALL)
        print(f"[DEBUG] Pattern 2 substitution completed successfully")
    except Exception as e:
        print(f"[DEBUG] ERROR in Pattern 2 substitution: {e}")
    
    # PATTERN 3: {% code %} blocks without titles
    pattern3 = r'{% code %}\s*```([a-zA-Z]*)\s*\n(.*?)\n```\s*{% endcode %}'
    print(f"[DEBUG] Testing Pattern 3: {pattern3}")
    matches3 = re.findall(pattern3, content, flags=re.DOTALL)
    print(f"[DEBUG] Pattern 3 found {len(matches3)} matches")
    if matches3:
        for i, match in enumerate(matches3):
            print(f"[DEBUG] Pattern 3 Match {i+1}: lang='{match[0]}', content_len={len(match[1])}")
    
    try:
        content = re.sub(pattern3, lambda m: code_block_replace(m), content, flags=re.DOTALL)
        print(f"[DEBUG] Pattern 3 substitution completed successfully")
    except Exception as e:
        print(f"[DEBUG] ERROR in Pattern 3 substitution: {e}")
    
    # PATTERN 4: Catch any remaining {% code %} patterns (fallback) - NEW
    remaining_patterns = re.findall(r'{% code[^}]*%}.*?{% endcode %}', content, flags=re.DOTALL)
    if remaining_patterns:
        print(f"[DEBUG] WARNING: Found {len(remaining_patterns)} unconverted code blocks:")
        for i, pattern in enumerate(remaining_patterns[:3]):  # Show first 3
            print(f"[DEBUG] Unconverted {i+1}: {pattern[:100]}...")
    else:
        print(f"[DEBUG] SUCCESS: All GitBook code blocks converted!")
    
    print("[DEBUG] BACKTICK: convert_gitbook_code_blocks_simple output has {} backticks".format(content.count('`')))
    return content

def fix_all_remaining_gitbook_blocks(content):
    """
    Final cleanup function to catch any remaining GitBook patterns that weren't converted.
    This is a fallback to ensure no GitBook syntax remains in the MDX files.
    ENHANCED: Now includes content-ref block handling.
    """
    import re
    
    print("[DEBUG] fix_all_remaining_gitbook_blocks called")
    
    # Count remaining GitBook patterns before cleanup
    remaining_code_blocks = re.findall(r'{% code[^}]*%}.*?{% endcode %}', content, flags=re.DOTALL)
    remaining_hints = re.findall(r'{% hint[^}]*%}.*?{% endhint %}', content, flags=re.DOTALL)
    remaining_tabs = re.findall(r'{% tabs %}.*?{% endtabs %}', content, flags=re.DOTALL)
    remaining_content_refs = re.findall(r'{% content-ref[^}]*%}.*?{% endcontent-ref %}', content, flags=re.DOTALL)
    remaining_page_refs = re.findall(r'{% page-ref[^}]*%}', content, flags=re.DOTALL)
    print(f"NEW!!!!!!!!!!!!!!!!![DEBUG] Found {len(remaining_page_refs)} remaining page-ref blocks")
    print("NEW!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("NEW!!!!!!!!!!!!!!!!!!!!!!!!!") 
    print(f"[DEBUG] Found {len(remaining_code_blocks)} remaining code blocks")
    print(f"[DEBUG] Found {len(remaining_hints)} remaining hint blocks")
    print(f"[DEBUG] Found {len(remaining_tabs)} remaining tab blocks")
    print(f"[DEBUG] Found {len(remaining_content_refs)} remaining content-ref blocks")
    
    # Fix remaining code blocks with simple conversion
    if remaining_code_blocks:
        print("[DEBUG] Converting remaining code blocks...")
        for i, block in enumerate(remaining_code_blocks[:3]):  # Show first 3
            print(f"[DEBUG] Remaining code block {i+1}: {block[:100]}...")
        
        # Simple pattern: {% code title="..." %} ... {% endcode %}
        pattern = r'{% code title="([^"]*)" %}\s*```?\s*\n?(.*?)\n?```?\s*{% endcode %}'
        def simple_code_replace(match):
            title = match.group(1)
            code_content = match.group(2).strip()
            clean_title = title.replace('"', '')
            return f'```text title="{clean_title}"\n{code_content}\n```'
        
        content = re.sub(pattern, simple_code_replace, content, flags=re.DOTALL)
        
        # Even simpler pattern: {% code %} ... {% endcode %}
        pattern2 = r'{% code %}\s*```?\s*\n?(.*?)\n?```?\s*{% endcode %}'
        def simple_code_replace2(match):
            code_content = match.group(1).strip()
            return f'```text\n{code_content}\n```'
        
        content = re.sub(pattern2, simple_code_replace2, content, flags=re.DOTALL)
    
    # Fix remaining hint blocks
    if remaining_hints:
        print("[DEBUG] Converting remaining hint blocks...")
        pattern = r'{% hint style="([^"]*)" %}\s*(.*?)\s*{% endhint %}'
        def hint_replace(match):
            style = match.group(1)
            hint_content = match.group(2).strip()
            
            style_map = {
                'info': 'info',
                'warning': 'warning', 
                'danger': 'danger',
                'success': 'tip',
                'tip': 'tip'
            }
            
            admonition_type = style_map.get(style, 'info')
            
            return f'''<div className="admonition admonition-{admonition_type}">
<div className="admonition-content">

{hint_content}

</div>
</div>'''
        
        content = re.sub(pattern, hint_replace, content, flags=re.DOTALL)
    
    # Fix remaining content-ref blocks (NEW!)
    if remaining_content_refs:
        print("[DEBUG] Converting remaining content-ref blocks...")
        for i, block in enumerate(remaining_content_refs[:3]):  # Show first 3
            print(f"[DEBUG] Remaining content-ref block {i+1}: {block[:100]}...")
        
        # Pattern to match GitBook content-ref blocks
        content_ref_pattern = r'{% content-ref url="([^"]*)" %}\s*\[([^\]]*)\]\([^)]*\)\s*{% endcontent-ref %}'
        
        def content_ref_replace(match):
            url = match.group(1)
            link_text = match.group(2)
            
            print(f"[DEBUG] Converting content-ref: url='{url}', text='{link_text}'")
            
            # Convert .md to .mdx for internal links, and remove .md/.mdx extension for Docusaurus routing
            if url.endswith('.md'):
                # Remove .md extension for Docusaurus internal links
                clean_url = url[:-3]
            elif url.endswith('.mdx'):
                # Remove .mdx extension for Docusaurus internal links
                clean_url = url[:-4]
            else:
                clean_url = url
            
            # Create a simple link
            result = f'[{link_text}]({clean_url})'
            
            print(f"[DEBUG] Converted to: {result}")
            return result
        
        content = re.sub(content_ref_pattern, content_ref_replace, content, flags=re.DOTALL)
    
    # Fix remaining page-ref blocks
    if remaining_page_refs:
        print("[DEBUG] Converting remaining page-ref blocks...")
        page_ref_pattern = r'{% page-ref page="([^"]*)" %}'
        def page_ref_replace(match):
            page_url = match.group(1)
            clean_url = page_url[:-3] if page_url.endswith('.md') else page_url
            link_text = clean_url.replace('-', ' ').title()
            return f'[{link_text}]({clean_url})'
        content = re.sub(page_ref_pattern, page_ref_replace, content, flags=re.DOTALL)
    
    # Fix remaining tab blocks
    if remaining_tabs:
        print("[DEBUG] Converting remaining tab blocks...")
        # This would need more complex handling, but for now just log them
        for i, block in enumerate(remaining_tabs[:3]):
            print(f"[DEBUG] Remaining tab block {i+1}: {block[:100]}...")
    
    # Final check
    final_remaining = re.findall(r'{% [^}]*%}', content)
    if final_remaining:
        print(f"[DEBUG] WARNING: Still have {len(final_remaining)} GitBook patterns after cleanup")
        for i, pattern in enumerate(final_remaining[:5]):
            print(f"[DEBUG] Still remaining {i+1}: {pattern}")
    else:
        print("[DEBUG] SUCCESS: All GitBook patterns cleaned up!")
    
    return content

def fix_gitbook_embed_blocks(content):
    """
    Convert GitBook embed blocks to proper markdown links.
    This function should be added to the conversion script.
    """
    import re
    
    print("[DEBUG] fix_gitbook_embed_blocks called")
    
    # Pattern to match GitBook embed blocks: {% embed url="..." %}
    embed_pattern = r'{% embed url="([^"]*)" %}'
    
    def embed_replace(match):
        url = match.group(1)
        
        print(f"[DEBUG] Converting embed block: {url}")
        
        # Create a descriptive link text based on the URL
        if 'vector-search' in url:
            link_text = 'Learn more about On-Device Vector Search'
        elif 'sync' in url:
            link_text = 'Learn more about Data Sync'
        elif 'getting-started' in url:
            link_text = 'Getting Started Guide'
        else:
            # Extract a reasonable link text from the URL
            path_parts = url.split('/')
            if path_parts:
                link_text = path_parts[-1].replace('-', ' ').title()
            else:
                link_text = 'Learn more'
        
        result = f'[{link_text}]({url})'
        print(f"[DEBUG] Converted embed to: {result}")
        return result
    
    # Count embed blocks before conversion
    embed_blocks = re.findall(embed_pattern, content)
    print(f"[DEBUG] Found {len(embed_blocks)} embed blocks to convert")
    
    # Debug: Show what embed blocks were found
    for i, url in enumerate(embed_blocks):
        print(f"[DEBUG] Embed block {i+1}: {url}")
    
    # Apply the conversion
    result = re.sub(embed_pattern, embed_replace, content)
    
    # Check for any remaining embed blocks
    remaining_embeds = re.findall(r'{% embed', result)
    if remaining_embeds:
        print(f"[DEBUG] WARNING: Found {len(remaining_embeds)} unconverted embed blocks")
    else:
        print("[DEBUG] SUCCESS: All GitBook embed blocks converted")
    
    return result

def extract_description_from_frontmatter(content):
    """
    Extract description from frontmatter and add it as page content AFTER the main heading.
    IMPROVED: Places description after the first # heading, not at the beginning.
    """
    import re
    
    print("[DEBUG] extract_description_from_frontmatter called")
    
    lines = content.split('\n')
    
    # Find frontmatter boundaries
    frontmatter_start = -1
    frontmatter_end = -1
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if frontmatter_start == -1:
                frontmatter_start = i
            elif frontmatter_end == -1:
                frontmatter_end = i
                break
    
    if frontmatter_start == -1 or frontmatter_end == -1:
        print("[DEBUG] No frontmatter found")
        return content
    
    # Extract description from frontmatter
    frontmatter_lines = lines[frontmatter_start+1:frontmatter_end]
    description_text = None
    
    # Look for description in frontmatter
    in_description = False
    description_lines = []
    
    for line in frontmatter_lines:
        if line.strip().startswith('description:'):
            # Handle single-line description
            if ':' in line and not line.strip().endswith('>-'):
                description_text = line.split(':', 1)[1].strip().strip('"\'')
                break
            else:
                # Multi-line description starts
                in_description = True
                continue
        elif in_description:
            if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                # End of description block
                break
            else:
                # Part of description
                description_lines.append(line.strip())
    
    if description_lines:
        description_text = ' '.join(description_lines).strip()
    
    if not description_text:
        print("[DEBUG] No description found in frontmatter")
        return content
    
    print(f"[DEBUG] Found description: {description_text[:50]}...")
    
    # Find the first main heading (# heading)
    main_heading_line = -1
    content_lines = lines[frontmatter_end+1:]  # Skip frontmatter
    
    for i, line in enumerate(content_lines):
        if line.strip().startswith('# ') and not line.strip().startswith('## '):
            main_heading_line = frontmatter_end + 1 + i
            print(f"[DEBUG] Found main heading at line {main_heading_line + 1}: {line.strip()}")
            break
    
    if main_heading_line == -1:
        print("[DEBUG] No main heading found, adding description at the beginning of content")
        # No main heading found, add description after frontmatter and imports
        insert_line = frontmatter_end + 1
        # Skip any import lines
        for i in range(frontmatter_end + 1, len(lines)):
            if lines[i].strip() and not lines[i].strip().startswith('import '):
                insert_line = i
                break
    else:
        # Add description after the main heading
        insert_line = main_heading_line + 1
    
    # Insert description after the main heading
    lines.insert(insert_line, '')  # Empty line
    lines.insert(insert_line + 1, description_text)
    lines.insert(insert_line + 2, '')  # Empty line after description
    
    print(f"[DEBUG] Added description as page content at line {insert_line + 2}")
    
    return '\n'.join(lines)

def fix_admonition_syntax(content):
    """
    Convert HTML admonition divs to proper Docusaurus admonition syntax.
    """
    import re
    
    print("[DEBUG] fix_admonition_syntax called")
    
    # Pattern to match HTML admonitions
    html_admonition_pattern = r'<div className="admonition admonition-(\w+)">\s*<div className="admonition-content">\s*(.*?)\s*</div>\s*</div>'
    
    def replace_admonition(match):
        admonition_type = match.group(1)
        content_text = match.group(2).strip()
        
        # Map admonition types
        type_mapping = {
            'info': 'info',
            'tip': 'tip', 
            'success': 'tip',
            'warning': 'warning',
            'danger': 'danger'
        }
        
        docusaurus_type = type_mapping.get(admonition_type, 'info')
        
        # Create proper Docusaurus admonition
        result = f':::{docusaurus_type}\n{content_text}\n:::'
        
        print(f"[DEBUG] Converted {admonition_type} admonition to Docusaurus syntax")
        return result
    
    # Apply the conversion
    result = re.sub(html_admonition_pattern, replace_admonition, content, flags=re.DOTALL)
    
    # Count conversions
    html_count = len(re.findall(r'<div className="admonition', content))
    docusaurus_count = len(re.findall(r':::', result))
    
    print(f"[DEBUG] Converted {html_count} HTML admonitions to Docusaurus syntax")
    
    return result

def fix_malformed_code_blocks(content):
    """Fix malformed code blocks that have duplicate markers or empty content."""
    
    print(f"[DEBUG] BACKTICK: fix_malformed_code_blocks input has {content.count('`')} backticks")
    
    # Fix duplicate code block markers
    content = re.sub(r'```(\w+)(\s+title="[^"]*")?\s*\n\s*\n\s*```(\w+)', r'```\1\2', content)
    
    # Fix empty code blocks
    content = re.sub(r'```\w*\s*\n\s*\n```\s*\n', '', content)
    
    # Fix code blocks with only whitespace
    content = re.sub(r'```(\w+)(\s+title="[^"]*")?\s*\n\s+\n```', '', content)
    
    print(f"[DEBUG] BACKTICK: fix_malformed_code_blocks output has {content.count('`')} backticks")
    return content

def escape_mdx_specials(content):
    """Escape special characters that can break MDX parsing."""
    print(f"[DEBUG] BACKTICK: escape_mdx_specials called - DISABLED to prevent backtick issues")
    print(f"[DEBUG] BACKTICK: escape_mdx_specials input has {content.count('`')} backticks")
    # DISABLED: This function was adding backticks to JSX attributes causing errors
    # return content unchanged for now
    print(f"[DEBUG] BACKTICK: escape_mdx_specials output has {content.count('`')} backticks (unchanged)")
    return content

def fix_html_entities(content):
    """Fix common HTML entity issues."""
    print(f"[DEBUG] BACKTICK: fix_html_entities input has {content.count('`')} backticks")
    # Fix escaped ampersands in URLs and text
    content = re.sub(r'&amp;', '&', content)
    print(f"[DEBUG] BACKTICK: fix_html_entities output has {content.count('`')} backticks")
    return content

def fix_mdx_list_dash(content):
    """Fix list formatting issues in MDX."""
    print(f"[DEBUG] BACKTICK: fix_mdx_list_dash input has {content.count('`')} backticks")
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Fix list items that start with weird characters
        if re.match(r'^\s*[•·‣⁃]\s', line):
            # Replace bullet characters with standard dash
            line = re.sub(r'^(\s*)[•·‣⁃]\s', r'\1- ', line)
        result.append(line)
    
    final_content = '\n'.join(result)
    print(f"[DEBUG] BACKTICK: fix_mdx_list_dash output has {final_content.count('`')} backticks")
    return final_content

def fix_mdx_problematic_characters(content):
    """
    Fix characters like <->, <-, <<, <--> that MDX interprets as JSX syntax.
    IMPORTANT: Skip frontmatter sections to avoid corrupting YAML.
    ENHANCED: Added <--> pattern detection and fixing.
    """
    import re
    
    print("[DEBUG] fix_mdx_problematic_characters called")
    
    lines = content.split('\n')
    
    # Find frontmatter boundaries
    frontmatter_start = -1
    frontmatter_end = -1
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if frontmatter_start == -1:
                frontmatter_start = i
            elif frontmatter_end == -1:
                frontmatter_end = i
                break
    
    # Count patterns before fixing (ENHANCED: Added <--> pattern)
    original_arrow_patterns = len(re.findall(r'<->', content))
    original_left_arrow_patterns = len(re.findall(r'<-(?!>)', content))
    original_double_left_patterns = len(re.findall(r'<<', content))
    original_double_arrow_patterns = len(re.findall(r'<-->', content))  # NEW: <--> pattern
    
    print(f"[DEBUG] Found {original_arrow_patterns} '<->' patterns")
    print(f"[DEBUG] Found {original_left_arrow_patterns} '<-' patterns")
    print(f"[DEBUG] Found {original_double_left_patterns} '<<' patterns")
    print(f"[DEBUG] Found {original_double_arrow_patterns} '<-->' patterns")  # NEW: Debug for <-->
    
    # Process lines, skipping frontmatter
    fixed_lines = []
    lines_fixed = 0
    
    for i, line in enumerate(lines):
        # Skip frontmatter lines
        if frontmatter_start != -1 and frontmatter_end != -1:
            if frontmatter_start <= i <= frontmatter_end:
                fixed_lines.append(line)
                continue
        
        # Fix problematic characters in non-frontmatter lines
        original_line = line
        
        # NEW: Fix <--> patterns FIRST (before <-> patterns to avoid conflicts)
        if '<-->' in line:
            line = re.sub(r'<-->', '`<-->`', line)
            print(f"[DEBUG] Fixed <--> pattern in line {i+1}")
        
        # Fix <-> patterns (bidirectional arrows)
        line = re.sub(r'<->', '`<->`', line)
        
        # Fix <- patterns (but not when part of <->)
        line = re.sub(r'<-(?!>)', '`<-`', line)
        
        # Fix << patterns
        line = re.sub(r'<<', '`<<`', line)
        
        if line != original_line:
            lines_fixed += 1
            print(f"[DEBUG] Fixed line {i+1}: '{original_line}' -> '{line}'")
        
        fixed_lines.append(line)
    
    result = '\n'.join(fixed_lines)
    
    # Count patterns after fixing (ENHANCED: Added <--> pattern)
    remaining_arrow_patterns = len(re.findall(r'<->', result))
    remaining_left_arrow_patterns = len(re.findall(r'<-(?!>)', result))
    remaining_double_left_patterns = len(re.findall(r'<<', result))
    remaining_double_arrow_patterns = len(re.findall(r'<-->', result))  # NEW: <--> pattern
    
    print(f"[DEBUG] After fixing: {remaining_arrow_patterns} '<->' patterns remain")
    print(f"[DEBUG] After fixing: {remaining_left_arrow_patterns} '<-' patterns remain")
    print(f"[DEBUG] After fixing: {remaining_double_left_patterns} '<<' patterns remain")
    print(f"[DEBUG] After fixing: {remaining_double_arrow_patterns} '<-->' patterns remain")  # NEW: Debug for <-->
    
    if frontmatter_start != -1 and frontmatter_end != -1:
        print(f"[DEBUG] Skipped frontmatter lines {frontmatter_start+1}-{frontmatter_end+1} to preserve YAML")
    
    if lines_fixed > 0:
        print(f"[DEBUG] Fixed {lines_fixed} lines with problematic characters")
    else:
        print("[DEBUG] No problematic characters found outside frontmatter")
    
    return result

def convert_gitbook_hints(content):
    """Convert GitBook hint blocks to Docusaurus admonitions."""
    import re
    
    print("[DEBUG] convert_gitbook_hints called")
    
    # Pattern for GitBook hints: {% hint style="info" %} ... {% endhint %}
    hint_pattern = r'{% hint style="([^"]*)" %}\s*(.*?)\s*{% endhint %}'
    
    def hint_replace(match):
        style = match.group(1)
        hint_content = match.group(2).strip()
        
        # Map GitBook styles to Docusaurus admonition types
        style_map = {
            'info': 'info',
            'warning': 'warning',
            'danger': 'danger',
            'success': 'tip',
            'tip': 'tip'
        }
        
        admonition_type = style_map.get(style, 'info')
        
        # Create Docusaurus admonition JSX
        result = f'''<div className="admonition admonition-{admonition_type}">
<div className="admonition-content">

{hint_content}

</div>
</div>'''
        
        print(f"[DEBUG] Converted hint: {style} -> {admonition_type}")
        return result
    
    # Apply the conversion
    content = re.sub(hint_pattern, hint_replace, content, flags=re.DOTALL)
    
    print("[DEBUG] convert_gitbook_hints completed")
    return content

def convert_gitbook_tabs(content):
    """
    Convert GitBook tabs to Docusaurus Tabs/TabItem components with proper C++ mapping.
    ENHANCED: Now propagates language context from tab titles to code blocks within tabs.
    """
    import re
    
    print("[DEBUG] convert_gitbook_tabs called")
    
    # Pattern to match GitBook tabs structure
    tabs_pattern = r'{% tabs %}\s*(.*?)\s*{% endtabs %}'
    tab_pattern = r'{% tab title="([^"]*)" %}\s*(.*?)\s*{% endtab %}'
    
    def extract_language_from_title(title):
        """Extract programming language from tab title."""
        title_lower = title.lower().strip()
        
        # Specific mappings for common cases
        if title_lower in ['c++', 'cpp']:
            return 'cpp'
        elif title_lower == 'c' or 'c without' in title_lower:
            return 'c'
        elif 'cmake' in title_lower:
            return 'cmake'
        elif 'bash' in title_lower or 'shell' in title_lower:
            return 'bash'
        elif 'python' in title_lower:
            return 'python'
        elif 'java' in title_lower:
            return 'java'
        elif 'swift' in title_lower:
            return 'swift'
        elif 'kotlin' in title_lower:
            return 'kotlin'
        elif 'dart' in title_lower:
            return 'dart'
        elif 'go' in title_lower or 'golang' in title_lower:
            return 'go'
        else:
            return None
    
    def fix_code_blocks_in_tab_content(tab_content, language_context):
        """Fix empty code blocks within tab content using language context."""
        if not language_context:
            return tab_content
        
        print(f"[DEBUG] Fixing code blocks in tab with language context: {language_context}")
        
        # Pattern to find empty code blocks (no language specified)
        empty_code_pattern = r'```\s*\n(.*?)\n```'
        
        def replace_empty_code_block(match):
            code_content = match.group(1)
            print(f"[DEBUG] Found empty code block, adding language '{language_context}': {code_content[:30]}...")
            return f'```{language_context}\n{code_content}\n```'
        
        # Apply the fix
        result = re.sub(empty_code_pattern, replace_empty_code_block, tab_content, flags=re.DOTALL)
        
        return result
    
    def tabs_replace(match):
        tabs_content = match.group(1)
        print(f"[DEBUG] Processing tabs block with content length: {len(tabs_content)}")
        
        # Find all individual tabs
        tabs = re.findall(tab_pattern, tabs_content, flags=re.DOTALL)
        print(f"[DEBUG] Found {len(tabs)} individual tabs")
        
        if not tabs:
            print("[DEBUG] WARNING: No tabs found in tabs block")
            return match.group(0)  # Return original if no tabs found
        
        # Generate unique values for each tab with proper C++ mapping
        tab_items = []
        used_values = []
        
        for i, (title, tab_content) in enumerate(tabs):
            print(f"[DEBUG] Processing tab {i+1}: title='{title}'")
            
            # Extract language context from title
            language_context = extract_language_from_title(title)
            print(f"[DEBUG] Extracted language context: {language_context}")
            
            # Fix code blocks within this tab using the language context
            if language_context:
                tab_content = fix_code_blocks_in_tab_content(tab_content, language_context)
            
            # Generate value from title with specific mappings
            title_lower = title.lower().strip()
            
            # Specific mappings for common cases
            if title_lower in ['c++', 'cpp']:
                value = 'cpp'
            elif title_lower == 'c' or 'c without' in title_lower:
                value = 'c'
            elif 'cmake' in title_lower and ('cpp' in title_lower or 'c++' in title_lower):
                value = 'cmakecpp'
            elif 'cmake' in title_lower:
                value = 'cmake'
            else:
                # General cleanup for other cases
                value = re.sub(r'[^a-zA-Z0-9]', '', title_lower)
                if not value:  # Empty value
                    value = f'tab{i+1}'
            
            print(f"[DEBUG] Generated value for '{title}': '{value}'")
            
            # Check for duplicates and fix them
            original_value = value
            counter = 1
            while value in used_values:
                value = f"{original_value}{counter}"
                counter += 1
                print(f"[DEBUG] Duplicate value detected! Changed '{original_value}' to '{value}'")
            
            used_values.append(value)
            print(f"[DEBUG] Final value for tab {i+1}: '{value}'")
            
            # Clean up tab content
            tab_content = tab_content.strip()
            
            tab_item = f'<TabItem value="{value}" label="{title}">\n\n{tab_content}\n\n</TabItem>'
            tab_items.append(tab_item)
        
        # Create the complete tabs structure
        tabs_jsx = f'<Tabs>\n' + '\n'.join(tab_items) + '\n</Tabs>'
        
        print(f"[DEBUG] Created tabs block with values: {used_values}")
        
        # Final duplicate check
        if len(used_values) != len(set(used_values)):
            duplicates = [x for x in used_values if used_values.count(x) > 1]
            print(f"[DEBUG] ERROR: Found duplicate values: {duplicates}")
        else:
            print(f"[DEBUG] SUCCESS: All tab values are unique")
        
        return tabs_jsx
    
    # Count tabs blocks before conversion
    tabs_blocks = re.findall(tabs_pattern, content, flags=re.DOTALL)
    print(f"[DEBUG] Found {len(tabs_blocks)} tabs blocks to convert")
    
    # Apply the conversion
    result = re.sub(tabs_pattern, tabs_replace, content, flags=re.DOTALL)
    
    # Final check for any remaining GitBook tabs
    remaining_tabs = re.findall(r'{% tabs %}|{% tab |{% endtab %}|{% endtabs %}', result)
    if remaining_tabs:
        print(f"[DEBUG] WARNING: Found {len(remaining_tabs)} unconverted tab elements")
    else:
        print("[DEBUG] SUCCESS: All GitBook tabs converted")
    
    print("[DEBUG] convert_gitbook_tabs completed")
    return result

def fix_text_code_blocks(content):
    """
    Fix code blocks that were converted to 'text' language by detecting the actual language.
    SAFER VERSION: Only fixes ```text blocks, avoids breaking existing working code blocks.
    """
    import re
    
    print("[DEBUG] fix_text_code_blocks called")
    
    # ONLY fix ```text blocks - don't touch other code blocks that might be working fine
    text_block_pattern = r'^```text\s*\n(.*?)\n```'
    
    def detect_language_and_replace(match):
        code_content = match.group(1).strip()
        
        # Language detection based on content patterns
        if any(keyword in code_content.lower() for keyword in [
            'cmake_minimum_required', 'project(', 'target_link_libraries', 
            'add_executable', 'find_package', 'fetchcontent'
        ]):
            language = 'cmake'
        elif any(keyword in code_content for keyword in [
            '#include', 'int main(', 'printf(', 'return 0'
        ]):
            language = 'c'
        elif any(keyword in code_content for keyword in [
            '#include', 'std::', 'namespace', 'class ', 'cout'
        ]):
            language = 'cpp'
        elif any(keyword in code_content.lower() for keyword in [
            'npm install', 'yarn add', 'package.json'
        ]):
            language = 'bash'
        elif any(keyword in code_content for keyword in [
            'curl ', 'wget ', 'sudo ', './configure'
        ]):
            language = 'bash'
        elif code_content.startswith('$') or code_content.startswith('./'):
            language = 'bash'
        else:
            # If we can't detect, use no language (plain code block)
            language = ''
        
        if language:
            result = f'```{language}\n{code_content}\n```'
            print(f"[DEBUG] Converted text block to {language}: {code_content[:30]}...")
        else:
            result = f'```\n{code_content}\n```'
            print(f"[DEBUG] Converted text block to plain code: {code_content[:30]}...")
        
        return result
    
    # Count text blocks before conversion
    text_blocks = re.findall(text_block_pattern, content, flags=re.DOTALL | re.MULTILINE)
    print(f"[DEBUG] Found {len(text_blocks)} ```text code blocks to fix")
    
    # Debug: Show what text blocks were found
    for i, block in enumerate(text_blocks):
        print(f"[DEBUG] Text block {i+1}: {block.strip()[:50]}...")
    
    # Apply the conversion ONLY to ```text blocks
    result = re.sub(text_block_pattern, detect_language_and_replace, content, flags=re.DOTALL | re.MULTILINE)
    
    # Count remaining text blocks
    remaining_text_blocks = re.findall(r'^```text\s*\n', result, flags=re.MULTILINE)
    print(f"[DEBUG] {len(remaining_text_blocks)} ```text blocks remain after conversion")
    
    if len(text_blocks) > 0:
        print(f"[DEBUG] Successfully converted {len(text_blocks) - len(remaining_text_blocks)} text blocks to proper languages")
    
    return result

def fix_internal_links(content):
    """
    Fix internal links that still point to .md files.
    Convert them to proper Docusaurus links without extensions.
    """
    import re
    
    print("[DEBUG] fix_internal_links called")
    
    # Pattern to find markdown links that point to .md files
    # Matches: [text](file.md) or [text](file.md#anchor)
    md_link_pattern = r'\[([^\]]*)\]\(([^)]*\.md(?:#[^)]*)?)[^)]*\)'
    
    def fix_link(match):
        link_text = match.group(1)
        link_url = match.group(2)
        
        print(f"[DEBUG] Found .md link: [{link_text}]({link_url})")
        
        # Handle anchors (e.g., file.md#section)
        if '#' in link_url:
            file_part, anchor_part = link_url.split('#', 1)
            # Remove .md extension from file part
            if file_part.endswith('.md'):
                clean_file = file_part[:-3]
            else:
                clean_file = file_part
            clean_url = f"{clean_file}#{anchor_part}"
        else:
            # No anchor, just remove .md extension
            if link_url.endswith('.md'):
                clean_url = link_url[:-3]
            else:
                clean_url = link_url
        
        result = f'[{link_text}]({clean_url})'
        print(f"[DEBUG] Fixed link: {result}")
        return result
    
    # Count .md links before conversion
    md_links = re.findall(md_link_pattern, content)
    print(f"[DEBUG] Found {len(md_links)} internal .md links to fix")
    
    # Debug: Show what links were found
    for i, (text, url) in enumerate(md_links[:5]):  # Show first 5
        print(f"[DEBUG] Link {i+1}: [{text}]({url})")
    
    # Apply the conversion
    result = re.sub(md_link_pattern, fix_link, content)
    
    # Count remaining .md links
    remaining_md_links = re.findall(r'\[([^\]]*)\]\(([^)]*\.md(?:#[^)]*)?)\)', result)
    print(f"[DEBUG] {len(remaining_md_links)} .md links remain after conversion")
    
    if len(md_links) > len(remaining_md_links):
        print(f"[DEBUG] Successfully fixed {len(md_links) - len(remaining_md_links)} internal links")
    
    return result

def fix_frontmatter_structure(content):
    """
    Simple and direct fix for frontmatter structure.
    Move ALL imports after frontmatter, regardless of current structure.
    """
    import re
    
    print("[DEBUG] fix_frontmatter_structure called")
    
    lines = content.split('\n')
    
    # Collect different sections
    jsx_imports = []
    frontmatter_lines = []
    content_lines = []
    
    # Find all JSX imports (anywhere in the file)
    for line in lines:
        if line.strip().startswith('import ') and ' from ' in line:
            jsx_imports.append(line)
            print(f"[DEBUG] Found JSX import: {line.strip()}")
    
    # Find frontmatter section
    frontmatter_start = -1
    frontmatter_end = -1
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if frontmatter_start == -1:
                frontmatter_start = i
            elif frontmatter_end == -1:
                frontmatter_end = i
                break
    
    if frontmatter_start != -1 and frontmatter_end != -1:
        print(f"[DEBUG] Found frontmatter from line {frontmatter_start+1} to {frontmatter_end+1}")
        # Extract frontmatter
        frontmatter_lines = lines[frontmatter_start:frontmatter_end+1]
        
        # Extract content (everything except imports and frontmatter)
        for i, line in enumerate(lines):
            # Skip frontmatter lines
            if frontmatter_start <= i <= frontmatter_end:
                continue
            # Skip import lines
            if line.strip().startswith('import ') and ' from ' in line:
                continue
            # Add everything else to content
            content_lines.append(line)
    else:
        print("[DEBUG] No frontmatter found")
        # No frontmatter - just separate imports from content
        for line in lines:
            if not (line.strip().startswith('import ') and ' from ' in line):
                content_lines.append(line)
    
    # Rebuild file in correct order
    result_lines = []
    
    # 1. Frontmatter first
    if frontmatter_lines:
        result_lines.extend(frontmatter_lines)
        result_lines.append('')  # Empty line after frontmatter
        print("[DEBUG] Added frontmatter at the top")
    
    # 2. JSX imports second
    if jsx_imports:
        result_lines.extend(jsx_imports)
        result_lines.append('')  # Empty line after imports
        print(f"[DEBUG] Added {len(jsx_imports)} JSX imports after frontmatter")
    
    # 3. Content last
    result_lines.extend(content_lines)
    
    result = '\n'.join(result_lines)
    
    # Verify the result
    result_lines_check = result.split('\n')
    first_non_empty = None
    for line in result_lines_check:
        if line.strip():
            first_non_empty = line.strip()
            break
    
    if first_non_empty == '---':
        print("[DEBUG] SUCCESS: Frontmatter is now at the top")
    else:
        print(f"[DEBUG] WARNING: First line is not frontmatter: '{first_non_empty}'")
    
    return result

def convert_file(input_file):
    """Convert a single file from GitBook MD to Docusaurus MDX."""
    print(f"[DEBUG] FOLDER FIX: Converting file: {input_file}")
    
    # Generate output path maintaining folder structure
    output_path = get_output_path(input_file, BASE_DIR, OUTPUT_ROOT)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    print(f"[DEBUG] FOLDER FIX: Created directory: {output_dir}")
    
    print(f'Converting {input_file} to {output_path}')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"[DEBUG] BACKTICK: Initial file content has {content.count('`')} backticks")
    
    content = ensure_valid_frontmatter(content)
    
    # FIXED ORDER: Code blocks FIRST, then escaping
    print("[DEBUG] Step 1: HTML fixes")
    content = fix_html_and_escape(content)  # No brace escaping here
    
    print("[DEBUG] Step 2: Code block conversion")
    content = enhanced_convert_gitbook_code_blocks_simple(content)
    
    print("[DEBUG] Step 3: Hints conversion")
    content = convert_gitbook_hints(content)
    
    print("[DEBUG] Step 4: Tabs conversion")
    content = convert_gitbook_tabs(content)
    
    print("[DEBUG] Step 5: HTML entities")
    content = fix_html_entities(content)
    
    print("[DEBUG] Step 6: Brace escaping (after code blocks)")
    content = improved_escape_curly_braces(content)  # NOW escape braces
    
    print("[DEBUG] Step 7: MDX specials - DISABLED")
    content = escape_mdx_specials(content)  # This is now a no-op but still called for debug

    print("[DEBUG] Step 8.5: Convert content-ref to cards")
    content = fix_gitbook_content_ref_to_cards(content)
    
    print("[DEBUG] Step 8: List fixes")
    content = fix_mdx_list_dash(content)

    print("[DEBUG] Step 9: Fix remaining GitBook blocks")
    content = fix_all_remaining_gitbook_blocks(content)

    print("[DEBUG] Step 9.5: Fix GitBook embed blocks")
    content = fix_gitbook_embed_blocks(content)

    print("[DEBUG] Step 10: Fix MDX problematic characters")
    content = fix_mdx_problematic_characters(content)

    print("[DEBUG] Step 10.5: Fix internal links")
    content = fix_internal_links(content)
    
    print(f"[DEBUG] BACKTICK: Final content before JSX imports has {content.count('`')} backticks")
    
    # Check for JSX components and determine file extension
    has_jsx = '<Tabs>' in content or '<TabItem>' in content or 'className="admonition"' in content
    
    # Always add JSX imports (won't hurt if unused)
    content = 'import Tabs from "@theme/Tabs"\nimport TabItem from "@theme/TabItem"\n\n' + content

    print("[DEBUG] Step 11: Fix frontmatter structure (final)")
    content = fix_frontmatter_structure(content)

    print(f"[DEBUG] BACKTICK: Final content after JSX imports has {content.count('`')} backticks")
    print(f"[DEBUG] Output: {output_path} (JSX detected: {has_jsx})")

    print("[DEBUG] Step 12: Extract description from frontmatter")
    content = extract_description_from_frontmatter(content)

    print("[DEBUG] Step 13: Fix admonition syntax")
    content = fix_admonition_syntax(content)

    print("[DEBUG] Step 14: Fix malformed code blocks")
    content = fix_malformed_code_blocks(content)

    print("[DEBUG] Step 15: Escape MDX specials")
    content = escape_mdx_specials(content)

    print("[DEBUG] Step 16: Fix text code blocks") 
    content = fix_text_code_blocks(content)
    
    # Check for problematic backticks in JSX attributes before writing
    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        if 'className=' in line and '`' in line:
            print(f"[DEBUG] BACKTICK: WARNING - Line {line_num} has backticks near className: {line.strip()}")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[DEBUG] FOLDER FIX: Successfully wrote file: {output_path}")
    except Exception as e:
        print(f"[DEBUG] FOLDER FIX: ERROR writing file {output_path}: {e}")

        
def main():
    """Main function to process all markdown files."""
    print("Starting GitBook to MDX conversion...")
    
    # Find all .md files in current directory (excluding website/docs)
    md_files = find_docs_files_recursive(BASE_DIR)


    
    if not md_files:
        print("No .md files found in current directory")
        return
    
    print(f"Found {len(md_files)} files to process:")
    for file in md_files:
        print(f"  - {file}")
    
    # Process each file - LET convert_file determine the output path
    for input_file in md_files:
        try:
            convert_file(input_file)  # ← FIXED: No output_file parameter at all
        except Exception as e:
            print(f"Error processing {input_file}: {e}")
            continue
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()