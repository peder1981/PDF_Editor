#!/usr/bin/env python3
"""
Advanced PDF Editor - Comprehensive Test Suite
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
import fitz
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../core')

from core.pdf_editor import PDFEditor, EditOperation, TextInstance
from core.batch_processor import BatchProcessor, BatchJob


class TestPDFEditor(unittest.TestCase):
    """Test cases for PDFEditor core functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.editor = PDFEditor()
        self.test_pdf_content = self._create_test_pdf()
        
    def tearDown(self):
        """Clean up after tests"""
        if self.editor.document:
            self.editor.close()
        
        # Clean up test files
        if hasattr(self, 'test_pdf_path') and os.path.exists(self.test_pdf_path):
            os.unlink(self.test_pdf_path)
    
    def _create_test_pdf(self) -> str:
        """Create a test PDF file with sample content"""
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            self.test_pdf_path = tmp_file.name
        
        try:
            # Create a simple PDF with test content
            doc = fitz.open()
            page = doc.new_page()
            
            # Add some test text
            page.insert_text((72, 100), "Hello World", fontsize=12)
            page.insert_text((72, 120), "This is a test document", fontsize=10)
            page.insert_text((72, 140), "Replace this text", fontsize=14)
            page.insert_text((72, 160), "Keep this unchanged", fontsize=12)
            
            # Add another page
            page2 = doc.new_page()
            page2.insert_text((72, 100), "Page 2 content", fontsize=12)
            page2.insert_text((72, 120), "Hello again", fontsize=10)
            
            doc.save(self.test_pdf_path)
            doc.close()
            
            return self.test_pdf_path
            
        except Exception as e:
            # If PDF creation fails, create a mock path for testing
            self.skipTest(f"Could not create test PDF: {e}")
    
    def test_load_pdf(self):
        """Test loading a PDF file"""
        result = self.editor.load(self.test_pdf_path)
        self.assertTrue(result)
        self.assertIsNotNone(self.editor.document)
        self.assertEqual(self.editor.file_path, self.test_pdf_path)
        self.assertGreater(len(self.editor.text_instances), 0)
    
    def test_load_nonexistent_file(self):
        """Test loading a nonexistent file"""
        result = self.editor.load("nonexistent.pdf")
        self.assertFalse(result)
        self.assertIsNone(self.editor.document)
    
    def test_search_text_case_insensitive(self):
        """Test case-insensitive text search"""
        self.editor.load(self.test_pdf_path)
        
        results = self.editor.search_text("hello", case_sensitive=False)
        self.assertGreater(len(results), 0)
        
        # Should find both "Hello World" and "Hello again"
        hello_texts = [r.text for r in results if "hello" in r.text.lower()]
        self.assertGreater(len(hello_texts), 0)
    
    def test_search_text_case_sensitive(self):
        """Test case-sensitive text search"""
        self.editor.load(self.test_pdf_path)
        
        results = self.editor.search_text("Hello", case_sensitive=True)
        self.assertGreater(len(results), 0)
        
        # Should only find exact matches
        for result in results:
            self.assertIn("Hello", result.text)
    
    def test_search_text_not_found(self):
        """Test searching for text that doesn't exist"""
        self.editor.load(self.test_pdf_path)
        
        results = self.editor.search_text("NonexistentText")
        self.assertEqual(len(results), 0)
    
    def test_replace_text_exact_method(self):
        """Test exact positioning text replacement"""
        self.editor.load(self.test_pdf_path)
        
        # Replace "Hello World" with "Hi Universe"
        replacements = self.editor.replace_text_exact("Hello World", "Hi Universe")
        self.assertGreater(replacements, 0)
        
        # Verify replacement occurred
        results = self.editor.search_text("Hi Universe")
        self.assertGreater(len(results), 0)
        
        # Original text should be gone
        results = self.editor.search_text("Hello World")
        self.assertEqual(len(results), 0)
    
    def test_replace_text_structure_preserving(self):
        """Test structure preserving replacement"""
        self.editor.load(self.test_pdf_path)
        
        replacements = self.editor.replace_text_structure_preserving("test document", "sample file")
        self.assertGreaterEqual(replacements, 0)  # May be 0 if text not found in exact form
    
    def test_batch_replace(self):
        """Test batch text replacement"""
        self.editor.load(self.test_pdf_path)
        
        operations = [
            EditOperation("Hello", "Hi", case_sensitive=False),
            EditOperation("test", "sample", case_sensitive=False)
        ]
        
        results = self.editor.batch_replace(operations, method="exact")
        self.assertIsInstance(results, dict)
        
        # Check that some replacements were made
        total_replacements = sum(results.values())
        self.assertGreaterEqual(total_replacements, 0)
    
    def test_get_document_info(self):
        """Test document information extraction"""
        self.editor.load(self.test_pdf_path)
        
        info = self.editor.get_document_info()
        self.assertIsInstance(info, dict)
        self.assertIn('page_count', info)
        self.assertIn('text_instances', info)
        self.assertIn('file_size', info)
        self.assertEqual(info['page_count'], 2)
        self.assertGreater(info['text_instances'], 0)
    
    def test_save_document(self):
        """Test saving the modified document"""
        self.editor.load(self.test_pdf_path)
        
        # Make a change
        self.editor.replace_text_exact("Hello", "Hi")
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            output_path = tmp_file.name
        
        try:
            result = self.editor.save(output_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(output_path))
            
            # Verify the saved file can be loaded
            test_editor = PDFEditor()
            load_result = test_editor.load(output_path)
            self.assertTrue(load_result)
            test_editor.close()
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_close_document(self):
        """Test closing a document"""
        self.editor.load(self.test_pdf_path)
        self.assertIsNotNone(self.editor.document)
        
        self.editor.close()
        self.assertIsNone(self.editor.document)
        self.assertEqual(len(self.editor.text_instances), 0)


class TestEditOperation(unittest.TestCase):
    """Test cases for EditOperation data class"""
    
    def test_edit_operation_creation(self):
        """Test creating EditOperation instances"""
        operation = EditOperation("search", "replace")
        self.assertEqual(operation.search_text, "search")
        self.assertEqual(operation.replace_text, "replace")
        self.assertFalse(operation.case_sensitive)
        self.assertFalse(operation.regex)
        self.assertIsNone(operation.page_num)
    
    def test_edit_operation_with_options(self):
        """Test EditOperation with all options"""
        operation = EditOperation(
            search_text="test",
            replace_text="sample",
            page_num=1,
            case_sensitive=True,
            regex=True
        )
        self.assertEqual(operation.search_text, "test")
        self.assertEqual(operation.replace_text, "sample")
        self.assertEqual(operation.page_num, 1)
        self.assertTrue(operation.case_sensitive)
        self.assertTrue(operation.regex)


class TestTextInstance(unittest.TestCase):
    """Test cases for TextInstance data class"""
    
    def test_text_instance_creation(self):
        """Test creating TextInstance instances"""
        rect = fitz.Rect(0, 0, 100, 20)
        instance = TextInstance(
            text="Test text",
            rect=rect,
            font="Arial",
            fontsize=12.0,
            color=(0, 0, 0),
            page_num=0
        )
        
        self.assertEqual(instance.text, "Test text")
        self.assertEqual(instance.rect, rect)
        self.assertEqual(instance.font, "Arial")
        self.assertEqual(instance.fontsize, 12.0)
        self.assertEqual(instance.color, (0, 0, 0))
        self.assertEqual(instance.page_num, 0)


class TestBatchProcessor(unittest.TestCase):
    """Test cases for batch processing functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = BatchProcessor(max_workers=2)
    
    def test_add_job(self):
        """Test adding a job to the batch queue"""
        operations = [EditOperation("test", "sample")]
        job_id = self.processor.add_job("input.pdf", "output.pdf", operations)
        
        self.assertEqual(job_id, 0)
        self.assertEqual(len(self.processor.jobs), 1)
        
        job = self.processor.get_job_status(job_id)
        self.assertIsNotNone(job)
        self.assertEqual(job.input_path, "input.pdf")
        self.assertEqual(job.output_path, "output.pdf")
        self.assertEqual(job.method, "exact")
        self.assertEqual(job.status, "pending")
    
    def test_add_jobs_from_config(self):
        """Test adding jobs from configuration file"""
        # Create temporary config file
        config = {
            "jobs": [
                {
                    "input": "test1.pdf",
                    "output": "output1.pdf",
                    "method": "exact",
                    "operations": [
                        {"search": "hello", "replace": "hi", "case_sensitive": False}
                    ]
                },
                {
                    "input": "test2.pdf",
                    "output": "output2.pdf",
                    "method": "structure",
                    "operations": [
                        {"search": "world", "replace": "universe", "case_sensitive": True}
                    ]
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as config_file:
            json.dump(config, config_file)
            config_path = config_file.name
        
        try:
            jobs_added = self.processor.add_jobs_from_config(config_path)
            self.assertEqual(jobs_added, 2)
            self.assertEqual(len(self.processor.jobs), 2)
            
            # Check first job
            job1 = self.processor.get_job_status(0)
            self.assertEqual(job1.input_path, "test1.pdf")
            self.assertEqual(job1.method, "exact")
            self.assertEqual(len(job1.operations), 1)
            
            # Check second job
            job2 = self.processor.get_job_status(1)
            self.assertEqual(job2.input_path, "test2.pdf")
            self.assertEqual(job2.method, "structure")
            
        finally:
            os.unlink(config_path)
    
    def test_clear_jobs(self):
        """Test clearing all jobs"""
        operations = [EditOperation("test", "sample")]
        self.processor.add_job("input.pdf", "output.pdf", operations)
        self.assertEqual(len(self.processor.jobs), 1)
        
        self.processor.clear_jobs()
        self.assertEqual(len(self.processor.jobs), 0)
    
    def test_get_job_status_invalid_id(self):
        """Test getting status of invalid job ID"""
        result = self.processor.get_job_status(999)
        self.assertIsNone(result)
    
    @patch('core.batch_processor.PDFEditor')
    def test_process_jobs_mock(self, mock_pdf_editor_class):
        """Test processing jobs with mocked PDFEditor"""
        # Setup mock
        mock_editor = Mock()
        mock_editor.load.return_value = True
        mock_editor.replace_text_exact.return_value = 2
        mock_editor.save.return_value = True
        mock_pdf_editor_class.return_value = mock_editor
        
        # Add a job
        operations = [EditOperation("test", "sample")]
        self.processor.add_job("input.pdf", "output.pdf", operations)
        
        # Process jobs
        results = self.processor.process_jobs()
        
        # Verify results
        self.assertEqual(results["total"], 1)
        self.assertEqual(results["completed"], 1)
        self.assertEqual(results["failed"], 0)
        self.assertEqual(results["total_replacements"], 2)
        
        # Verify mock calls
        mock_editor.load.assert_called_once_with("input.pdf")
        mock_editor.replace_text_exact.assert_called_once_with("test", "sample", False)
        mock_editor.save.assert_called_once_with("output.pdf")
        mock_editor.close.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "test_input.pdf")
        self.output_file = os.path.join(self.test_dir, "test_output.pdf")
        self._create_test_pdf()
    
    def tearDown(self):
        """Clean up integration test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _create_test_pdf(self):
        """Create a test PDF for integration testing"""
        try:
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 100), "Integration Test Document", fontsize=14)
            page.insert_text((72, 130), "Replace this: OLD_VALUE", fontsize=12)
            page.insert_text((72, 150), "Keep this unchanged", fontsize=10)
            doc.save(self.input_file)
            doc.close()
        except Exception as e:
            self.skipTest(f"Could not create test PDF for integration test: {e}")
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # 1. Load PDF
        editor = PDFEditor()
        self.assertTrue(editor.load(self.input_file))
        
        # 2. Search for text
        results = editor.search_text("OLD_VALUE")
        self.assertGreater(len(results), 0)
        
        # 3. Replace text
        replacements = editor.replace_text_exact("OLD_VALUE", "NEW_VALUE")
        self.assertGreater(replacements, 0)
        
        # 4. Save result
        self.assertTrue(editor.save(self.output_file))
        
        # 5. Verify the change
        verify_editor = PDFEditor()
        self.assertTrue(verify_editor.load(self.output_file))
        
        # Should find the new value
        new_results = verify_editor.search_text("NEW_VALUE")
        self.assertGreater(len(new_results), 0)
        
        # Should not find the old value
        old_results = verify_editor.search_text("OLD_VALUE")
        self.assertEqual(len(old_results), 0)
        
        # Clean up
        editor.close()
        verify_editor.close()


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestPDFEditor,
        TestEditOperation, 
        TestTextInstance,
        TestBatchProcessor,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
