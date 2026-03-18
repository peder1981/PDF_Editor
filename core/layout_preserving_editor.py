#!/usr/bin/env python3
"""
Advanced PDF Editor - Layout Preservation Module
Preserves graphics, backgrounds, and layout elements while replacing text
"""

import fitz
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class PageElement:
    """Represents a visual element on the page"""
    element_type: str  # "image", "drawing", "background", "text"
    rect: fitz.Rect
    data: Any
    page_num: int


class LayoutPreservingEditor:
    """Advanced PDF editor that preserves all layout elements"""
    
    def __init__(self, document: fitz.Document):
        self.document = document
        self.page_elements: Dict[int, List[PageElement]] = {}
        
    def extract_page_elements(self, page_num: int) -> List[PageElement]:
        """Extract all visual elements from a page"""
        page = self.document[page_num]
        elements = []
        
        # 1. Extract images
        images = page.get_images()
        for img in images:
            try:
                xref = img[0]
                rect = img[1]
                elements.append(PageElement(
                    element_type="image",
                    rect=rect,
                    data={"xref": xref},
                    page_num=page_num
                ))
            except Exception as e:
                print(f"Error extracting image: {e}")
        
        # 2. Extract drawings (vector graphics, shapes, lines)
        try:
            drawings = page.get_drawings()
            for drawing in drawings:
                if "rect" in drawing:
                    elements.append(PageElement(
                        element_type="drawing",
                        rect=fitz.Rect(drawing["rect"]),
                        data=drawing,
                        page_num=page_num
                    ))
        except Exception as e:
            print(f"Error extracting drawings: {e}")
        
        # 3. Detect background colors
        try:
            # Get page background color from page properties
            if hasattr(page, 'colorspace'):
                bg_color = page.colorspace
                if bg_color:
                    elements.append(PageElement(
                        element_type="background",
                        rect=page.rect,
                        data={"color": bg_color},
                        page_num=page_num
                    ))
        except Exception as e:
            print(f"Error detecting background: {e}")
        
        # 4. Detect colored rectangles (likely backgrounds or highlights)
        try:
            for drawing in page.get_drawings():
                if "fill" in drawing and drawing["fill"] != (1, 1, 1):  # Not white
                    elements.append(PageElement(
                        element_type="background",
                        rect=fitz.Rect(drawing["rect"]),
                        data={"color": drawing["fill"], "type": "fill"},
                        page_num=page_num
                    ))
        except Exception as e:
            print(f"Error detecting colored backgrounds: {e}")
        
        self.page_elements[page_num] = elements
        return elements
    
    def replace_text_preserving_layout(self, search_text: str, replace_text: str, 
                                       case_sensitive: bool = False) -> int:
        """Replace text while preserving all layout elements"""
        replacements = 0
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Extract all page elements before modification
            elements = self.extract_page_elements(page_num)
            
            # Search for text instances
            search_flags = 0 if case_sensitive else fitz.TEXT_INHIBIT_SPACES
            text_instances = page.search_for(search_text, flags=search_flags)
            
            for rect in text_instances:
                # Get text properties
                text_dict = page.get_textbox(rect)
                
                # Find matching text instance for font properties
                matching_instance = None
                for instance in self._get_text_instances(page):
                    if (instance["rect"] == rect or 
                        self._rects_overlap(instance["rect"], rect)):
                        matching_instance = instance
                        break
                
                # Use advanced redaction that preserves background
                try:
                    if matching_instance:
                        # Detect background color at text position
                        bg_color = self._detect_background_color(page, rect, elements)
                        
                        # Create redaction annotation with original background color
                        redact_annot = page.add_redact_annot(
                            rect,
                            text=replace_text,
                            fontname=matching_instance.get("font", "helv"),
                            fontsize=matching_instance.get("size", 12),
                            text_color=matching_instance.get("color", (0, 0, 0)),
                            fill=bg_color if bg_color else (1, 1, 1)  # Preserve original background
                        )
                        redact_annot.update()
                    else:
                        # Fallback with default properties
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
                except Exception as e:
                    print(f"Advanced redaction failed: {e}")
                    continue
            
            # Apply redactions
            try:
                page.apply_redactions()
            except Exception as e:
                print(f"Failed to apply redactions: {e}")
        
        return replacements
    
    def replace_text_with_layer_preservation(self, search_text: str, replace_text: str,
                                             case_sensitive: bool = False) -> int:
        """Replace text using layer-based preservation method"""
        replacements = 0
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            
            # Create a copy of the page to preserve original elements
            temp_doc = fitz.open()
            temp_page = temp_doc.new_page(
                width=page.rect.width,
                height=page.rect.height
            )
            
            # 1. Copy all non-text elements first
            self._copy_non_text_elements(page, temp_page)
            
            # 2. Process text with replacements
            text_dict = page.get_text("dict")
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            original_text = span["text"]
                            
                            # Check if this text needs replacement
                            text_to_check = original_text if case_sensitive else original_text.lower()
                            search_term = search_text if case_sensitive else search_text.lower()
                            
                            if search_term in text_to_check:
                                # Replace text
                                new_text = original_text.replace(search_text, replace_text)
                                
                                # Insert replaced text with original properties
                                temp_page.insert_text(
                                    (span["bbox"][0], span["bbox"][1]),
                                    new_text,
                                    fontname=span["font"],
                                    fontsize=span["size"],
                                    color=span["color"]
                                )
                                replacements += 1
                            else:
                                # Keep original text
                                temp_page.insert_text(
                                    (span["bbox"][0], span["bbox"][1]),
                                    original_text,
                                    fontname=span["font"],
                                    fontsize=span["size"],
                                    color=span["color"]
                                )
            
            # Replace original page with modified version
            self.document.delete_page(page_num)
            self.document.insert_pdf(temp_doc, from_page=0, to_page=0, start_at=page_num)
            temp_doc.close()
        
        return replacements
    
    def _detect_background_color(self, page: fitz.Rect, text_rect: fitz.Rect, 
                                elements: List[PageElement]) -> Optional[Tuple[float, float, float]]:
        """Detect background color at text position"""
        for element in elements:
            if element.element_type == "background":
                if element.rect.contains(text_rect) or element.rect.intersects(text_rect):
                    return element.data.get("color")
        return None
    
    def _copy_non_text_elements(self, source_page: fitz.Page, target_page: fitz.Page):
        """Copy all non-text elements from source to target page"""
        # Copy images
        try:
            images = source_page.get_images(full=True)
            for img in images:
                try:
                    # images returns list of tuples (xref, smask, width, height, bpc, colorspace, alt_colorspace, name, filter, bbox)
                    xref = img[0]
                    bbox = img[9]  # bbox is at index 9
                    
                    # Extract image data
                    base_image = self.document.extract_image(xref)
                    
                    # Insert image with correct bbox
                    if bbox:
                        rect = fitz.Rect(bbox)
                        target_page.insert_image(rect, stream=base_image["image"])
                except Exception as e:
                    print(f"Error copying image: {e}")
        except Exception as e:
            print(f"Error getting images: {e}")
        
        # Copy drawings and vector graphics
        try:
            drawings = source_page.get_drawings()
            for drawing in drawings:
                # Use the correct method to insert drawings
                if "items" in drawing:
                    for item in drawing["items"]:
                        if item[0] == "re":  # Rectangle
                            target_page.draw_rect(item[1], color=item[2], fill=item[3], width=item[4])
                        elif item[0] == "l":  # Line
                            target_page.draw_line(item[1], item[2], color=item[3], width=item[4])
                        elif item[0] == "c":  # Curve
                            target_page.draw_curve(item[1], item[2], item[3], color=item[4], width=item[5])
                        elif item[0] == "qu":  # Quadratic curve
                            target_page.draw_quad(item[1], item[2], item[3], color=item[4], width=item[5])
        except Exception as e:
            print(f"Error copying drawings: {e}")
        
        # Copy page background color if exists
        try:
            if hasattr(source_page, 'colorspace') and source_page.colorspace:
                # Note: Page background color preservation is complex in PyMuPDF
                # This is a placeholder for advanced background preservation
                pass
        except Exception as e:
            print(f"Error copying background: {e}")
    
    def _get_text_instances(self, page: fitz.Page) -> List[Dict]:
        """Get all text instances with their properties"""
        instances = []
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        instances.append({
                            "text": span["text"],
                            "rect": fitz.Rect(span["bbox"]),
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"]
                        })
        
        return instances
    
    def _rects_overlap(self, rect1: fitz.Rect, rect2: fitz.Rect, tolerance: float = 2.0) -> bool:
        """Check if two rectangles overlap"""
        return (abs(rect1.x0 - rect2.x0) < tolerance and
                abs(rect1.y0 - rect2.y0) < tolerance)
