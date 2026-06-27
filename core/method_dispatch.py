"""Shared method dispatch — eliminates duplicated if/elif chains across all UIs."""

from pdf_editor import PDFEditor


def apply_replacement(editor: PDFEditor, method: str, search_text: str,
                      replace_text: str, case_sensitive: bool = False) -> int:
    """Dispatch a replacement method by name. Returns replacement count.

    Raises ValueError if method is unknown.
    """
    dispatch = {
        "exact": lambda: editor.replace_text_exact(search_text, replace_text, case_sensitive),
        "comprehensive": lambda: editor.replace_text_comprehensive(search_text, replace_text),
        "structure": lambda: editor.replace_text_structure_preserving(search_text, replace_text),
        "smart": lambda: editor.replace_text_smart(search_text, replace_text),
        "heuristic": lambda: editor.replace_text_heuristic(search_text, replace_text),
        "integral": lambda: editor.replace_text_integral(search_text, replace_text),
        "template": lambda: editor.replace_text_template(search_text, replace_text),
        "layout-preserving": lambda: editor.replace_text_layout_preserving(search_text, replace_text, case_sensitive),
        "background-preserving": lambda: editor.replace_text_background_preserving(search_text, replace_text, case_sensitive),
    }
    fn = dispatch.get(method)
    if fn is None:
        raise ValueError(f"Unknown method: {method}")
    return fn()
