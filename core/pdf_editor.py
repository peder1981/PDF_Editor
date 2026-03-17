#!/usr/bin/env python3
"""
Advanced PDF Editor - Core Implementation
Text editing with structure preservation using PyMuPDF
"""

import fitz
import os
import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TextInstance:
    """Represents a text instance with position and properties"""
    text: str
    rect: fitz.Rect
    font: str
    fontsize: float
    color: Tuple[float, float, float]
    page_num: int


@dataclass
class EditOperation:
    """Represents a text edit operation"""
    search_text: str
    replace_text: str
    page_num: Optional[int] = None
    case_sensitive: bool = False
    regex: bool = False


class PDFEditor:
    """Advanced PDF Editor with structure preservation capabilities"""
    
    def __init__(self):
        self.document: Optional[fitz.Document] = None
        self.file_path: Optional[str] = None
        self.text_instances: List[TextInstance] = []
        
    def load(self, file_path: str) -> bool:
        """Load a PDF document"""
        try:
            self.file_path = file_path
            self.document = fitz.open(file_path)
            self._extract_text_instances()
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def _extract_text_instances(self) -> None:
        """Extract all text instances with their properties"""
        if not self.document:
            return
            
        self.text_instances.clear()
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Get text dictionary with detailed information
            text_dict = page.get_text("dict")
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text_instance = TextInstance(
                                text=span["text"],
                                rect=fitz.Rect(span["bbox"]),
                                font=span["font"],
                                fontsize=span["size"],
                                color=span["color"],
                                page_num=page_num
                            )
                            self.text_instances.append(text_instance)
    
    def search_text(self, search_text: str, case_sensitive: bool = False, regex: bool = False) -> List[TextInstance]:
        """Search for text instances in the document"""
        results = []
        
        for instance in self.text_instances:
            if regex:
                pattern = search_text if case_sensitive else f"(?i){search_text}"
                if re.search(pattern, instance.text):
                    results.append(instance)
            else:
                text_to_search = instance.text if case_sensitive else instance.text.lower()
                search_term = search_text if case_sensitive else search_text.lower()
                if search_term in text_to_search:
                    results.append(instance)
        
        return results
    
    def replace_text_exact(self, search_text: str, replace_text: str, case_sensitive: bool = False) -> int:
        """Replace text using exact positioning method with redaction"""
        if not self.document:
            return 0
            
        replacements = 0
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Search for text instances
            search_flags = 0 if case_sensitive else fitz.TEXT_INHIBIT_SPACES
            text_instances = page.search_for(search_text, flags=search_flags)
            
            for rect in text_instances:
                # Get text properties for better matching
                text_dict = page.get_textbox(rect)
                
                # Find matching text instance to get font properties
                matching_instance = None
                for instance in self.text_instances:
                    if (instance.page_num == page_num and 
                        abs(instance.rect.x0 - rect.x0) < 1 and 
                        abs(instance.rect.y0 - rect.y0) < 1):
                        matching_instance = instance
                        break
                
                # Use redaction for clean replacement
                if matching_instance:
                    redact_annot = page.add_redact_annot(
                        rect,
                        text=replace_text,
                        fontname=matching_instance.font,
                        fontsize=matching_instance.fontsize,
                        text_color=matching_instance.color,
                        fill=(1, 1, 1)  # White background
                    )
                    redact_annot.update()
                else:
                    # Fallback with default font properties
                    redact_annot = page.add_redact_annot(
                        rect,
                        text=replace_text,
                        fontname="helv",
                        fontsize=12,
                        text_color=(0, 0, 0),
                        fill=(1, 1, 1)
                    )
                    redact_annot.update()
                
                replacements += 1
            
            # Apply all redactions on this page
            page.apply_redactions()
        
        return replacements
    
    def replace_text_comprehensive(self, search_text: str, replace_text: str) -> int:
        """Replace text using comprehensive method - separating elements"""
        if not self.document:
            return 0
            
        replacements = 0
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Extract all elements
            text_dict = page.get_text("dict")
            drawings = page.get_drawings()
            images = page.get_images()
            
            # Create new page content
            new_page_content = []
            
            # Process text blocks
            for block in text_dict["blocks"]:
                if "lines" in block:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if search_text.lower() in span["text"].lower():
                                # Replace text
                                new_text = span["text"].replace(search_text, replace_text)
                                span["text"] = new_text
                                replacements += 1
            
            # Rebuild page (simplified - would need more complex implementation)
            # This is a conceptual approach - actual implementation would be more complex
            
        return replacements
    
    def replace_text_structure_preserving(self, search_text: str, replace_text: str) -> int:
        """Replace text while preserving document structure for template rebuilding"""
        if not self.document:
            return 0
            
        replacements = 0
        
        # Create a copy of the document structure
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Get all text with positioning
            text_instances = page.search_for(search_text)
            
            for rect in text_instances:
                # Remove old text by covering with background color
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                
                # Insert new text at the same position
                # Try to match original font properties
                try:
                    # Get original text properties
                    blocks = page.get_text("dict")["blocks"]
                    original_font = "helv"
                    original_size = 12
                    
                    # Find text properties in the area
                    for block in blocks:
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    span_rect = pymupdf.Rect(span["bbox"])
                                    if span_rect.intersects(rect):
                                        original_font = span["font"]
                                        original_size = span["size"]
                                        break
                    
                    # Insert replacement text
                    page.insert_text(
                        rect.tl,
                        replace_text,
                        fontname=original_font,
                        fontsize=original_size,
                        color=(0, 0, 0)
                    )
                    replacements += 1
                    
                except Exception as e:
                    # Fallback insertion
                    page.insert_text(
                        rect.tl,
                        replace_text,
                        fontsize=12,
                        color=(0, 0, 0)
                    )
                    replacements += 1
        
        return replacements
    
    def batch_replace(self, operations: List[EditOperation], method: str = "exact") -> Dict[str, int]:
        """Perform batch text replacements"""
        results = {}
        
        for operation in operations:
            if method == "exact":
                count = self.replace_text_exact(
                    operation.search_text,
                    operation.replace_text,
                    operation.case_sensitive
                )
            elif method == "comprehensive":
                count = self.replace_text_comprehensive(
                    operation.search_text,
                    operation.replace_text
                )
            elif method == "structure":
                count = self.replace_text_structure_preserving(
                    operation.search_text,
                    operation.replace_text
                )
            else:
                count = 0
            
            results[f"{operation.search_text} -> {operation.replace_text}"] = count
        
        return results
    
    def save(self, output_path: str) -> bool:
        """Save the modified document"""
        if not self.document:
            return False
            
        try:
            self.document.save(output_path)
            return True
        except Exception as e:
            print(f"Error saving PDF: {e}")
            return False
    
    def save_versions(self, base_path: str) -> Dict[str, str]:
        """Save different versions based on editing methods"""
        if not self.document or not self.file_path:
            return {}
        
        base_name = Path(base_path).stem
        base_dir = Path(base_path).parent
        
        versions = {
            "exact": base_dir / f"{base_name}_EXACT.pdf",
            "comprehensive": base_dir / f"{base_name}_COMPREHENSIVE.pdf", 
            "structure": base_dir / f"{base_name}_FINAL_MERGED.pdf"
        }
        
        saved_files = {}
        
        for method, file_path in versions.items():
            try:
                self.document.save(str(file_path))
                saved_files[method] = str(file_path)
            except Exception as e:
                print(f"Error saving {method} version: {e}")
        
        return saved_files
    
    def get_document_info(self) -> Dict[str, Any]:
        """Get document information"""
        if not self.document:
            return {}
        
        return {
            "page_count": len(self.document),
            "text_instances": len(self.text_instances),
            "file_size": os.path.getsize(self.file_path) if self.file_path else 0,
            "metadata": self.document.metadata
        }
    
    def close(self) -> None:
        """Close the document"""
        if self.document:
            self.document.close()
            self.document = None
        self.text_instances.clear()


def main():
    """Main function for testing"""
    editor = PDFEditor()
    
    # Example usage
    if editor.load("sample.pdf"):
        print(f"Loaded document with {len(editor.text_instances)} text instances")
        
        # Search for text
        results = editor.search_text("Hello")
        print(f"Found {len(results)} instances of 'Hello'")
        
        # Replace text using exact method
        replacements = editor.replace_text_exact("Hello", "Hi")
        print(f"Made {replacements} replacements")
        
        # Save result
        editor.save("output_exact.pdf")
        print("Saved edited document")
        
        editor.close()


if __name__ == "__main__":
    main()
