#!/usr/bin/env python3
"""
Advanced PDF Editor - Improved Font Preservation
Enhanced version with better font matching and preservation
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
    flags: int = 0
    ascender: float = 0.0
    descender: float = 0.0


@dataclass
class EditOperation:
    """Represents a text edit operation"""
    search_text: str
    replace_text: str
    page_num: Optional[int] = None
    case_sensitive: bool = False
    regex: bool = False


class ImprovedPDFEditor:
    """Improved PDF Editor with enhanced font preservation"""
    
    def __init__(self):
        self.document: Optional[fitz.Document] = None
        self.file_path: Optional[str] = None
        self.text_instances: List[TextInstance] = []
        self.font_mapping: Dict[str, str] = {}
        
    def load(self, file_path: str) -> bool:
        """Load a PDF document"""
        try:
            self.file_path = file_path
            self.document = fitz.open(file_path)
            self._extract_text_instances_enhanced()
            self._build_font_mapping()
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def _extract_text_instances_enhanced(self) -> None:
        """Extract all text instances with enhanced font information"""
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
                            # Extract enhanced font information
                            text_instance = TextInstance(
                                text=span["text"],
                                rect=fitz.Rect(span["bbox"]),
                                font=span["font"],
                                fontsize=span["size"],
                                color=span["color"],
                                page_num=page_num,
                                flags=span.get("flags", 0),
                                ascender=span.get("ascender", 0.0),
                                descender=span.get("descender", 0.0)
                            )
                            self.text_instances.append(text_instance)
    
    def _build_font_mapping(self) -> None:
        """Build a mapping of fonts available in the document"""
        if not self.document:
            return
            
        self.font_mapping.clear()
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            font_list = page.get_fonts()
            
            for font_info in font_list:
                font_ref = font_info[0]  # Font reference
                font_name = font_info[3]  # Font name
                font_type = font_info[1]  # Font type
                
                # Map font names to available fonts
                if font_name not in self.font_mapping:
                    self.font_mapping[font_name] = font_name
                
                # Create fallback mappings for common font variations
                base_name = font_name.split('-')[0] if '-' in font_name else font_name
                if base_name not in self.font_mapping:
                    self.font_mapping[base_name] = font_name
    
    def _get_best_font_match(self, original_font: str) -> str:
        """Get the best available font match for the original font"""
        # Try exact match first
        if original_font in self.font_mapping:
            return self.font_mapping[original_font]
        
        # Try base name match
        base_name = original_font.split('-')[0] if '-' in original_font else original_font
        if base_name in self.font_mapping:
            return self.font_mapping[base_name]
        
        # Try common font substitutions
        font_substitutions = {
            'Calibri': ['Calibri', 'Arial', 'Helvetica', 'helv'],
            'Arial': ['Arial', 'Helvetica', 'Calibri', 'helv'],
            'Helvetica': ['Helvetica', 'Arial', 'Calibri', 'helv'],
            'Times': ['Times-Roman', 'Times New Roman', 'times'],
            'TimesNewRoman': ['Times-Roman', 'Times', 'times']
        }
        
        for substitute_font in font_substitutions.get(base_name, []):
            if substitute_font in self.font_mapping:
                return self.font_mapping[substitute_font]
        
        # Fallback to system fonts
        return "helv"  # Helvetica fallback
    
    def replace_text_enhanced(self, search_text: str, replace_text: str, case_sensitive: bool = False) -> int:
        """Enhanced text replacement with improved font preservation"""
        if not self.document:
            return 0
            
        replacements = 0
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Search for text instances
            search_flags = 0 if case_sensitive else fitz.TEXT_INHIBIT_SPACES
            text_instances = page.search_for(search_text, flags=search_flags)
            
            for rect in text_instances:
                # Find the most accurate matching text instance
                matching_instance = self._find_best_text_match(rect, page_num, search_text)
                
                if matching_instance:
                    # Get the best font match
                    best_font = self._get_best_font_match(matching_instance.font)
                    
                    # Calculate appropriate font size (may need adjustment for different fonts)
                    adjusted_fontsize = self._calculate_adjusted_fontsize(
                        matching_instance.fontsize, 
                        matching_instance.font, 
                        best_font,
                        len(search_text),
                        len(replace_text)
                    )
                    
                    # Use redaction with enhanced font matching
                    try:
                        redact_annot = page.add_redact_annot(
                            rect,
                            text=replace_text,
                            fontname=best_font,
                            fontsize=adjusted_fontsize,
                            text_color=matching_instance.color,
                            fill=(1, 1, 1),  # White background
                            align=fitz.TEXT_ALIGN_LEFT
                        )
                        redact_annot.update()
                        replacements += 1
                        
                    except Exception as e:
                        # Fallback to structure preserving method
                        print(f"Font issue detected, using fallback method: {e}")
                        replacements += self._fallback_text_replacement(page, rect, replace_text, matching_instance)
                else:
                    # Use default properties if no match found
                    try:
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
                    except Exception:
                        # Last resort fallback
                        replacements += self._fallback_text_replacement(page, rect, replace_text)
            
            # Apply all redactions on this page
            page.apply_redactions()
        
        return replacements
    
    def _find_best_text_match(self, rect: fitz.Rect, page_num: int, search_text: str) -> Optional[TextInstance]:
        """Find the best matching text instance for a given rectangle"""
        best_match = None
        best_score = float('inf')
        
        for instance in self.text_instances:
            if instance.page_num != page_num:
                continue
            
            # Calculate distance score
            distance = abs(instance.rect.x0 - rect.x0) + abs(instance.rect.y0 - rect.y0)
            
            # Check if text content matches
            if search_text.lower() in instance.text.lower():
                # Prefer exact text matches
                if distance < best_score:
                    best_score = distance
                    best_match = instance
            elif distance < 2.0:  # Very close position match
                if distance < best_score:
                    best_score = distance
                    best_match = instance
        
        return best_match
    
    def _calculate_adjusted_fontsize(self, original_size: float, original_font: str, 
                                   new_font: str, original_length: int, new_length: int) -> float:
        """Calculate adjusted font size for different fonts and text lengths"""
        # Base adjustment for font differences
        font_adjustments = {
            'Calibri': 1.0,
            'Arial': 0.95,
            'Helvetica': 0.95,
            'helv': 0.95,
            'Times': 1.05,
            'times': 1.05
        }
        
        # Get adjustment factor for new font
        base_new_font = new_font.split('-')[0] if '-' in new_font else new_font
        font_factor = font_adjustments.get(base_new_font, 1.0)
        
        # Adjust for text length difference (if replacement text is much longer/shorter)
        if original_length > 0:
            length_ratio = new_length / original_length
            if length_ratio > 1.5:  # Much longer text
                length_factor = 0.9
            elif length_ratio < 0.7:  # Much shorter text
                length_factor = 1.1
            else:
                length_factor = 1.0
        else:
            length_factor = 1.0
        
        return original_size * font_factor * length_factor
    
    def _fallback_text_replacement(self, page, rect: fitz.Rect, replace_text: str, 
                                 matching_instance: Optional[TextInstance] = None) -> int:
        """Fallback method using direct text insertion"""
        try:
            # Remove old text by covering with white rectangle
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            
            # Insert new text
            if matching_instance:
                page.insert_text(
                    rect.tl,
                    replace_text,
                    fontsize=matching_instance.fontsize,
                    color=matching_instance.color
                )
            else:
                page.insert_text(
                    rect.tl,
                    replace_text,
                    fontsize=12,
                    color=(0, 0, 0)
                )
            return 1
        except Exception:
            return 0
    
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
    
    def close(self) -> None:
        """Close the document"""
        if self.document:
            self.document.close()
            self.document = None
        self.text_instances.clear()
        self.font_mapping.clear()


def main():
    """Test the improved PDF editor"""
    editor = ImprovedPDFEditor()
    
    # Example usage
    if editor.load("test.pdf"):
        print(f"Loaded document with {len(editor.text_instances)} text instances")
        print(f"Available fonts: {list(editor.font_mapping.keys())}")
        
        # Replace text with enhanced font preservation
        replacements = editor.replace_text_enhanced("old text", "new text")
        print(f"Made {replacements} replacements")
        
        editor.save("output_enhanced.pdf")
        editor.close()


if __name__ == "__main__":
    main()
