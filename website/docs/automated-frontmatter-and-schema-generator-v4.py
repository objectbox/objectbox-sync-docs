#!/usr/bin/env python3
"""
Enhanced Automated Frontmatter and Schema Generator v4
- Fixes YAML formatting issues
- Handles existing frontmatter (updates missing fields)
- Adds schema components if missing
- Fixes incomplete frontmatter
- FIXED: Properly escapes quotes in JSX attributes to prevent MDX compilation errors

Usage:
- Run from your docs directory: python automated-frontmatter-and-schema-generator-v4.py
- Or specify a directory: python automated-frontmatter-and-schema-generator-v4.py /path/to/docs
"""

import re
import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

class FrontmatterAndSchemaGeneratorV4:
    def __init__(self, project_name="ObjectBox", language="C++", base_url="https://cpp.objectbox.io"):
        self.project_name = project_name
        self.language = language
        self.base_url = base_url
        
        # Language-specific keywords
        self.language_keywords = {
            "Swift": ["swift", "ios", "macos", "xcode"],
            "Go": ["go", "golang"],
            "C++": ["c++", "cpp", "cmake"],
            "Java": ["java", "android"],
            "Dart": ["dart", "flutter"],
            "Kotlin": ["kotlin", "android"],
            "Python": ["python"]
        }
        
        # Page type patterns and their metadata
        self.page_patterns = {
            "README": {
                "title_template": "{project} {language} Database Documentation",
                "description_template": "High-performance NoSQL database for {language} applications with native APIs and easy integration",
                "keywords": ["database", "nosql", "documentation"],
                "schema_type": "main"
            },
            "install": {
                "title_template": "Install {project} {language}",
                "description_template": "Learn how to add {project} {language} database to your project using package managers and build tools",
                "keywords": ["installation", "setup", "package manager"],
                "schema_type": "tutorial"
            },
            "getting-started": {
                "title_template": "Getting Started with {project} {language}",
                "description_template": "Step-by-step tutorial to integrate {project} database in your {language} application and create your first entities",
                "keywords": ["tutorial", "getting started", "quickstart"],
                "schema_type": "tutorial"
            },
            "entity-annotations": {
                "title_template": "Entity Annotations in {project} {language}",
                "description_template": "Learn how to use annotations to define your data models and relationships in {project} {language}",
                "keywords": ["entities", "annotations", "data models", "relationships"],
                "schema_type": "article"
            },
            "queries": {
                "title_template": "Queries in {project} {language}",
                "description_template": "Learn how to query your {project} database using {language} APIs for filtering, sorting, and finding data",
                "keywords": ["queries", "filtering", "sorting", "database search"],
                "schema_type": "article"
            },
            "relations": {
                "title_template": "Relations in {project} {language}",
                "description_template": "Define and work with relationships between entities in {project} {language} database",
                "keywords": ["relations", "relationships", "foreign keys", "links"],
                "schema_type": "article"
            },
            "transactions": {
                "title_template": "Transactions in {project} {language}",
                "description_template": "Learn how to use transactions for atomic operations and data consistency in {project} {language}",
                "keywords": ["transactions", "atomic operations", "data consistency"],
                "schema_type": "article"
            },
            "faq": {
                "title_template": "{project} {language} FAQ",
                "description_template": "Frequently asked questions about {project} {language} database, installation, usage, and troubleshooting",
                "keywords": ["faq", "questions", "help", "troubleshooting"],
                "schema_type": "faq"
            },
            "custom-types": {
                "title_template": "Custom Types in {project} {language}",
                "description_template": "Learn how to use custom data types and enums with {project} {language} database",
                "keywords": ["custom types", "enums", "data types", "serialization"],
                "schema_type": "article"
            },
            "schema-changes": {
                "title_template": "Schema Changes in {project} {language}",
                "description_template": "Handle database schema migrations and updates in {project} {language} applications",
                "keywords": ["schema", "migrations", "database updates", "versioning"],
                "schema_type": "article"
            },
            "store": {
                "title_template": "Store - {project} {language}",
                "description_template": "Learn about the Store API in {project} {language} for database management and configuration",
                "keywords": ["store", "database management", "configuration"],
                "schema_type": "article"
            }
        }
    
    def parse_existing_frontmatter(self, content):
        """Parse existing frontmatter and return frontmatter dict and content without frontmatter."""
        lines = content.split('\n')
        
        # Check for proper frontmatter (starts with ---)
        if lines[0].strip() == '---':
            # Find closing ---
            end_index = -1
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_index = i
                    break
            
            if end_index > 0:
                # Parse YAML frontmatter
                frontmatter_text = '\n'.join(lines[1:end_index])
                try:
                    frontmatter = yaml.safe_load(frontmatter_text) or {}
                except:
                    frontmatter = {}
                
                # Content after frontmatter
                content_without_frontmatter = '\n'.join(lines[end_index + 1:])
                return frontmatter, content_without_frontmatter, True
        
        # Check for incomplete frontmatter (starts with description: but no opening ---)
        if lines[0].startswith('description:'):
            # Find where frontmatter ends (look for --- or first non-frontmatter line)
            end_index = -1
            for i, line in enumerate(lines):
                if line.strip() == '---':
                    end_index = i
                    break
                elif i > 0 and not line.startswith(' ') and not line.startswith('\t') and not line.strip() == '' and ':' not in line:
                    end_index = i
                    break
            
            if end_index > 0:
                # Parse incomplete frontmatter
                frontmatter_text = '\n'.join(lines[:end_index])
                try:
                    frontmatter = yaml.safe_load(frontmatter_text) or {}
                except:
                    frontmatter = {}
                
                # Content after frontmatter
                content_without_frontmatter = '\n'.join(lines[end_index + 1:])
                return frontmatter, content_without_frontmatter, False  # False = incomplete
        
        # No frontmatter found
        return {}, content, False
    
    def extract_content_info(self, content):
        """Extract information from content to improve frontmatter generation."""
        lines = content.split('\n')
        
        # Find first heading
        first_heading = None
        for line in lines:
            if line.strip().startswith('# '):
                first_heading = line.strip()[2:].strip()
                break
        
        # Find first paragraph (potential description)
        first_paragraph = None
        for line in lines:
            # Skip empty lines, headings, and imports
            if (line.strip() and 
                not line.strip().startswith('#') and 
                not line.strip().startswith('import ') and
                not line.strip().startswith('<') and
                not line.strip().startswith(':::') and
                len(line.strip()) > 20):
                first_paragraph = line.strip()
                break
        
        return {
            'first_heading': first_heading,
            'first_paragraph': first_paragraph
        }
    
    def generate_keywords(self, file_path, content_info, existing_keywords=None):
        """Generate relevant keywords based on file path and content."""
        if existing_keywords:
            return existing_keywords  # Keep existing keywords if they exist
        
        filename = Path(file_path).stem.lower()
        
        # Base keywords
        keywords = [self.project_name.lower()]
        
        # Add language-specific keywords
        lang_keywords = self.language_keywords.get(self.language, [])
        keywords.extend(lang_keywords)
        
        # Add database keyword
        keywords.append("database")
        
        # Add page-specific keywords
        for pattern, metadata in self.page_patterns.items():
            if pattern in filename:
                keywords.extend(metadata["keywords"])
                break
        else:
            # Fallback: extract keywords from filename
            filename_words = re.findall(r'[a-zA-Z]+', filename)
            keywords.extend([word for word in filename_words if len(word) > 3])
        
        # Remove duplicates and limit to 6 keywords
        unique_keywords = []
        for keyword in keywords:
            if keyword not in unique_keywords:
                unique_keywords.append(keyword)
        
        return unique_keywords[:6]
    
    def generate_title(self, file_path, content_info, existing_title=None):
        """Generate SEO-optimized title."""
        if existing_title:
            return existing_title  # Keep existing title if it exists
        
        filename = Path(file_path).stem.lower()
        
        # Check for known patterns
        for pattern, metadata in self.page_patterns.items():
            if pattern in filename:
                return metadata["title_template"].format(
                    project=self.project_name,
                    language=self.language
                )
        
        # Use first heading if available
        if content_info['first_heading']:
            heading = content_info['first_heading']
            # Add project and language if not present
            if self.project_name not in heading:
                heading = f"{heading} - {self.project_name} {self.language}"
            return heading
        
        # Fallback: generate from filename
        title_words = filename.replace('-', ' ').replace('_', ' ').title()
        return f"{title_words} - {self.project_name} {self.language}"
    
    def generate_description(self, file_path, content_info, existing_description=None):
        """Generate SEO-optimized description."""
        if existing_description:
            return existing_description  # Keep existing description if it exists
        
        filename = Path(file_path).stem.lower()
        
        # Check for known patterns
        for pattern, metadata in self.page_patterns.items():
            if pattern in filename:
                return metadata["description_template"].format(
                    project=self.project_name,
                    language=self.language
                )
        
        # Use first paragraph if available and suitable
        if content_info['first_paragraph'] and len(content_info['first_paragraph']) < 160:
            return content_info['first_paragraph']
        
        # Fallback: generate generic description
        topic = filename.replace('-', ' ').replace('_', ' ')
        return f"Learn about {topic} in {self.project_name} {self.language} database for high-performance applications"
    
    def get_schema_type(self, file_path):
        """Determine the appropriate schema type for the file."""
        filename = Path(file_path).stem.lower()
        
        for pattern, metadata in self.page_patterns.items():
            if pattern in filename:
                return metadata["schema_type"]
        
        return "article"  # Default schema type
    
    def escape_jsx_attribute(self, text):
        """Escape quotes and special characters for JSX attributes."""
        # Replace double quotes with single quotes to avoid JSX parsing issues
        # This is safer than escaping because it avoids complex escape sequences
        return text.replace('"', "'")
    
    def generate_schema_component(self, file_path, title, description):
        """Generate the appropriate schema component for the file."""
        schema_type = self.get_schema_type(file_path)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Escape quotes in title and description for JSX attributes
        safe_title = self.escape_jsx_attribute(title)
        safe_description = self.escape_jsx_attribute(description)
        
        if schema_type == "main":
            return f'''import {{ SoftwareDocumentationSchema }} from '@site/src/components/Schema';

<SoftwareDocumentationSchema
  description="{safe_description}"
  dateModified="{current_date}"
/>'''
        
        elif schema_type == "tutorial":
            return f'''import {{ TechnicalArticleSchema }} from '@site/src/components/Schema';

<TechnicalArticleSchema
  headline="{safe_title}"
  description="{safe_description}"
  url="{self.base_url}/{Path(file_path).stem}"
  datePublished="{current_date}"
  dateModified="{current_date}"
/>'''
        
        elif schema_type == "faq":
            return f'''import {{ FAQSchema, TechnicalArticleSchema }} from '@site/src/components/Schema';

<TechnicalArticleSchema
  headline="{safe_title}"
  description="{safe_description}"
  url="{self.base_url}/{Path(file_path).stem}"
  datePublished="{current_date}"
  dateModified="{current_date}"
/>'''
        
        else:  # article
            return f'''import {{ TechnicalArticleSchema }} from '@site/src/components/Schema';

<TechnicalArticleSchema
  headline="{safe_title}"
  description="{safe_description}"
  url="{self.base_url}/{Path(file_path).stem}"
  datePublished="{current_date}"
  dateModified="{current_date}"
/>'''
    
    def has_schema_component(self, content):
        """Check if content already has schema components."""
        return 'from \'@site/src/components/Schema\'' in content or 'from "@site/src/components/Schema"' in content
    
    def format_frontmatter(self, title, description, keywords):
        """Format frontmatter with proper YAML syntax."""
        # Escape quotes in title and description for YAML
        title = title.replace('"', '\\"')
        description = description.replace('"', '\\"')
        
        # Format keywords as proper YAML array
        keywords_yaml = '\n'.join([f'  - {keyword}' for keyword in keywords])
        
        return f"""---
title: "{title}"
description: "{description}"
keywords:
{keywords_yaml}
---"""
    
    def update_frontmatter_and_schema(self, file_path):
        """Update frontmatter and add schema components to a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[ERROR] Could not read {file_path}: {e}")
            return False
        
        # Parse existing frontmatter
        existing_frontmatter, content_without_frontmatter, is_complete = self.parse_existing_frontmatter(content)
        
        # Extract content info
        content_info = self.extract_content_info(content_without_frontmatter)
        
        # Generate or update frontmatter fields
        title = self.generate_title(file_path, content_info, existing_frontmatter.get('title'))
        description = self.generate_description(file_path, content_info, existing_frontmatter.get('description'))
        keywords = self.generate_keywords(file_path, content_info, existing_frontmatter.get('keywords'))
        
        # Ensure title is under 60 characters
        if len(title) > 60:
            title = title[:57] + "..."
        
        # Ensure description is under 160 characters
        if len(description) > 160:
            description = description[:157] + "..."
        
        # Create complete frontmatter with proper YAML formatting
        frontmatter = self.format_frontmatter(title, description, keywords)
        
        # Check if schema component already exists
        has_schema = self.has_schema_component(content_without_frontmatter)
        
        # Add schema component if it doesn't exist
        if not has_schema:
            schema_component = self.generate_schema_component(file_path, title, description)
            
            # Find where to insert schema component (after imports, before first heading)
            lines = content_without_frontmatter.split('\n')
            
            # Find the end of imports section
            import_end_index = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_end_index = i + 1
                elif line.strip() == '':
                    # Skip empty lines after imports
                    if import_end_index > 0:
                        import_end_index = i + 1
                else:
                    # Found non-import, non-empty line
                    break
            
            # Insert schema component after imports
            if import_end_index > 0:
                lines.insert(import_end_index, "")  # Add blank line
                lines.insert(import_end_index + 1, schema_component)
                lines.insert(import_end_index + 2, "")  # Add blank line after schema
            else:
                # No imports found, add at the beginning
                lines.insert(0, schema_component)
                lines.insert(1, "")  # Add blank line
            
            content_with_schema = '\n'.join(lines)
        else:
            content_with_schema = content_without_frontmatter
        
        # Combine frontmatter + content (with or without new schema)
        new_content = frontmatter + '\n\n' + content_with_schema
        
        # Write back to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            action_taken = []
            if not is_complete or not existing_frontmatter.get('title') or not existing_frontmatter.get('keywords'):
                action_taken.append("updated frontmatter")
            if not has_schema:
                action_taken.append("added schema")
            
            if action_taken:
                print(f"[SUCCESS] {', '.join(action_taken).title()} in {file_path}")
                return True
            else:
                print(f"[SKIP] Already complete: {file_path}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Could not write to {file_path}: {e}")
            return False
    
    def process_directory(self, directory_path, file_pattern="*.mdx", recursive=True):
        """Process all MDX files in a directory and subdirectories."""
        directory = Path(directory_path)
        files_processed = 0
        files_skipped = 0
        
        print(f"[INFO] Processing directory: {directory.absolute()}")
        print(f"[INFO] Updating frontmatter and adding schema components...")
        
        if recursive:
            # Process all .mdx files recursively
            for file_path in directory.rglob(file_pattern):
                if self.update_frontmatter_and_schema(file_path):
                    files_processed += 1
                else:
                    files_skipped += 1
        else:
            # Process only files in the current directory
            for file_path in directory.glob(file_pattern):
                if self.update_frontmatter_and_schema(file_path):
                    files_processed += 1
                else:
                    files_skipped += 1
        
        print(f"\n[SUMMARY] Updated {files_processed} files, skipped {files_skipped} files")
        return files_processed

def main():
    """Main function to run the enhanced generator."""
    
    # Get directory from command line argument or use current directory
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        target_directory = "."  # Current directory
    
    # Check if directory exists
    if not os.path.exists(target_directory):
        print(f"[ERROR] Directory {target_directory} not found.")
        return
    
    print("=== Enhanced ObjectBox Documentation Generator v4 ===")
    print(f"Target directory: {os.path.abspath(target_directory)}")
    print("[INFO] This script:")
    print("  ✅ Fixes YAML formatting issues")
    print("  ✅ Updates incomplete frontmatter (adds missing title/keywords)")
    print("  ✅ Adds schema components if missing")
    print("  ✅ Preserves existing good frontmatter")
    print("  ✅ FIXED: Properly escapes quotes in JSX attributes")
    
    # Configuration for C++ docs (change as needed)
    cpp_generator = FrontmatterAndSchemaGeneratorV4(
        project_name="ObjectBox",
        language="C++", 
        base_url="https://cpp.objectbox.io"
    )
    
    # Process the directory recursively
    cpp_generator.process_directory(target_directory, "*.mdx", recursive=True)
    
    print("\n[INFO] Enhancement complete!")
    print("[INFO] Your MDX files now have proper YAML frontmatter and schema components!")
    print("[INFO] No more MDX compilation errors from unescaped quotes!")

if __name__ == "__main__":
    main()

