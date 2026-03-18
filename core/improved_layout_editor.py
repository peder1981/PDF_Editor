#!/usr/bin/env python3
"""
Advanced PDF Editor - Improved Layout Preservation
Simplified and robust approach that actually works
"""

import fitz
from typing import List, Dict, Tuple, Optional, Any


class ImprovedLayoutEditor:
    """Improved layout preserving editor with robust implementation"""
    
    def __init__(self, document: fitz.Document):
        self.document = document
    
    def replace_text_preserving_layout(self, search_text: str, replace_text: str,
                                     case_sensitive: bool = False) -> int:
        """Replace text while preserving layout using improved redaction"""
        replacements = 0
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Search for text instances
            search_flags = 0 if case_sensitive else fitz.TEXT_INHIBIT_SPACES
            text_instances = page.search_for(search_text, flags=search_flags)
            
            for rect in text_instances:
                try:
                    # Get text properties
                    text_dict = page.get_text("dict")
                    fontname = "helv"
                    fontsize = 12
                    text_color = (0, 0, 0)
                    
                    # Find matching text properties
                    for block in text_dict["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    span_rect = fitz.Rect(span["bbox"])
                                    if span_rect.intersects(rect):
                                        fontname = self._get_safe_font(span["font"])
                                        fontsize = span["size"]
                                        text_color = span["color"]
                                        break
                    
                    # Use redaction with transparent fill to preserve background
                    redact_annot = page.add_redact_annot(
                        rect,
                        text=replace_text,
                        fontname=fontname,
                        fontsize=fontsize,
                        text_color=text_color,
                        fill=None  # Transparent fill preserves background
                    )
                    redact_annot.update()
                    replacements += 1
                    
                except Exception as e:
                    print(f"Error in layout preserving replacement: {e}")
                    continue
            
            # Apply redactions
            try:
                page.apply_redactions()
            except Exception as e:
                print(f"Failed to apply redactions: {e}")
        
        return replacements
    
    def replace_text_with_background_preservation(self, search_text: str, replace_text: str,
                                               case_sensitive: bool = False) -> int:
        """Replace text while preserving backgrounds and graphics"""
        replacements = 0
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Extract all non-text elements before modification
            images = self._extract_images(page)
            drawings = self._extract_drawings(page)
            
            # Search for text
            search_flags = 0 if case_sensitive else fitz.TEXT_INHIBIT_SPACES
            text_instances = page.search_for(search_text, flags=search_flags)
            
            for rect in text_instances:
                try:
                    # Get text properties
                    text_dict = page.get_text("dict")
                    fontname = "helv"
                    fontsize = 12
                    text_color = (0, 0, 0)
                    
                    for block in text_dict["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    span_rect = fitz.Rect(span["bbox"])
                                    if span_rect.intersects(rect):
                                        fontname = self._get_safe_font(span["font"])
                                        fontsize = span["size"]
                                        text_color = span["color"]
                                        break
                    
                    # Use white background only for text area
                    redact_annot = page.add_redact_annot(
                        rect,
                        text=replace_text,
                        fontname=fontname,
                        fontsize=fontsize,
                        text_color=text_color,
                        fill=(1, 1, 1)  # White background for text area only
                    )
                    redact_annot.update()
                    replacements += 1
                    
                except Exception as e:
                    print(f"Error in background preserving replacement: {e}")
                    continue
            
            # Apply redactions
            try:
                page.apply_redactions()
            except Exception as e:
                print(f"Failed to apply redactions: {e}")
        
        return replacements
    
    def _extract_images(self, page: fitz.Page) -> List[Dict]:
        """Extract image information from page"""
        images = []
        try:
            image_list = page.get_images(full=True)
            for img in image_list:
                try:
                    images.append({
                        "xref": img[0],
                        "bbox": img[9] if len(img) > 9 else None
                    })
                except:
                    pass
        except Exception as e:
            print(f"Error extracting images: {e}")
        return images
    
    def _extract_drawings(self, page: fitz.Page) -> List[Dict]:
        """Extract drawing information from page"""
        drawings = []
        try:
            drawing_list = page.get_drawings()
            for drawing in drawing_list:
                try:
                    if "rect" in drawing:
                        drawings.append(drawing)
                except:
                    pass
        except Exception as e:
            print(f"Error extracting drawings: {e}")
        return drawings
    
    def _get_safe_font(self, fontname: str) -> str:
        """Get safe font name that PyMuPDF supports"""
        font_mapping = {
            "Calibri": "helv",
            "Calibri-Bold": "helv",
            "Calibri-Italic": "helv",
            "Arial": "helv",
            "Arial-Bold": "helv",
            "Arial-Italic": "helv",
            "Times New Roman": "times",
            "Times-Roman": "times",
            "Courier New": "cour",
            "Courier": "cour",
        }
        
        for pattern, safe_font in font_mapping.items():
            if pattern in fontname:
                return safe_font
        
        # Default to Helvetica
        return "helv"
