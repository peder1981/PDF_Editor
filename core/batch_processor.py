#!/usr/bin/env python3
"""
Advanced PDF Editor - Batch Processing Module
Handle multiple files and batch operations efficiently
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import threading
from tqdm import tqdm

from core.pdf_editor import PDFEditor, EditOperation


@dataclass
class BatchJob:
    """Represents a batch processing job"""
    input_path: str
    output_path: str
    operations: List[EditOperation]
    method: str = "exact"
    status: str = "pending"  # pending, processing, completed, failed
    error: Optional[str] = None
    replacements_made: int = 0


class BatchProcessor:
    """Handles batch processing of multiple PDF files"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.jobs: List[BatchJob] = []
        self.lock = threading.Lock()
        
    def add_job(self, input_path: str, output_path: str, operations: List[EditOperation], method: str = "exact") -> int:
        """Add a job to the batch queue"""
        with self.lock:
            job = BatchJob(
                input_path=input_path,
                output_path=output_path,
                operations=operations,
                method=method
            )
            self.jobs.append(job)
            return len(self.jobs) - 1
    
    def add_jobs_from_config(self, config_path: str) -> int:
        """Add multiple jobs from a configuration file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            jobs_added = 0
            for job_config in config.get('jobs', []):
                operations = []
                for op_config in job_config.get('operations', []):
                    operations.append(EditOperation(
                        search_text=op_config['search'],
                        replace_text=op_config['replace'],
                        case_sensitive=op_config.get('case_sensitive', False),
                        regex=op_config.get('regex', False)
                    ))
                
                self.add_job(
                    input_path=job_config['input'],
                    output_path=job_config['output'],
                    operations=operations,
                    method=job_config.get('method', 'exact')
                )
                jobs_added += 1
            
            return jobs_added
            
        except Exception as e:
            raise Exception(f"Error loading batch configuration: {e}")
    
    def process_directory(self, input_dir: str, output_dir: str, operations: List[EditOperation], 
                         method: str = "exact", pattern: str = "*.pdf") -> int:
        """Process all PDF files in a directory"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all PDF files matching pattern
        pdf_files = list(input_path.glob(pattern))
        
        jobs_added = 0
        for pdf_file in pdf_files:
            output_file = output_path / pdf_file.name
            self.add_job(str(pdf_file), str(output_file), operations, method)
            jobs_added += 1
        
        return jobs_added
    
    def _process_single_job(self, job: BatchJob) -> BatchJob:
        """Process a single job"""
        try:
            job.status = "processing"
            
            # Create PDF editor instance
            editor = PDFEditor()
            
            if not editor.load(job.input_path):
                job.status = "failed"
                job.error = "Failed to load PDF"
                return job
            
            # Perform operations based on method
            total_replacements = 0
            
            if job.method == "exact":
                for operation in job.operations:
                    count = editor.replace_text_exact(
                        operation.search_text,
                        operation.replace_text,
                        operation.case_sensitive
                    )
                    total_replacements += count
            elif job.method == "comprehensive":
                for operation in job.operations:
                    count = editor.replace_text_comprehensive(
                        operation.search_text,
                        operation.replace_text
                    )
                    total_replacements += count
            elif job.method == "structure":
                for operation in job.operations:
                    count = editor.replace_text_structure_preserving(
                        operation.search_text,
                        operation.replace_text
                    )
                    total_replacements += count
            elif job.method == "smart":
                for operation in job.operations:
                    count = editor.replace_text_smart(
                        operation.search_text,
                        operation.replace_text
                    )
                    total_replacements += count
            elif job.method == "heuristic":
                for operation in job.operations:
                    count = editor.replace_text_heuristic(
                        operation.search_text,
                        operation.replace_text
                    )
                    total_replacements += count
            elif job.method == "integral":
                for operation in job.operations:
                    count = editor.replace_text_integral(
                        operation.search_text,
                        operation.replace_text
                    )
                    total_replacements += count
            elif job.method == "template":
                for operation in job.operations:
                    count = editor.replace_text_template(
                        operation.search_text,
                        operation.replace_text
                    )
                    total_replacements += count
            else:
                # Use batch replace method
                results = editor.batch_replace(job.operations, job.method)
                total_replacements = sum(results.values())
            
            # Save the result
            if editor.save(job.output_path):
                job.status = "completed"
                job.replacements_made = total_replacements
            else:
                job.status = "failed"
                job.error = "Failed to save PDF"
            
            editor.close()
            
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
        
        return job
    
    def process_jobs(self, progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Process all jobs in the queue"""
        if not self.jobs:
            return {"total": 0, "completed": 0, "failed": 0, "results": []}
        
        results = {
            "total": len(self.jobs),
            "completed": 0,
            "failed": 0,
            "results": [],
            "total_replacements": 0
        }
        
        # Use ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {executor.submit(self._process_single_job, job): job for job in self.jobs}
            
            # Process results as they complete
            with tqdm(total=len(self.jobs), desc="Processing PDFs") as pbar:
                for future in as_completed(future_to_job):
                    job = future.result()
                    
                    if job.status == "completed":
                        results["completed"] += 1
                        results["total_replacements"] += job.replacements_made
                    else:
                        results["failed"] += 1
                    
                    results["results"].append({
                        "input": job.input_path,
                        "output": job.output_path,
                        "status": job.status,
                        "error": job.error,
                        "replacements": job.replacements_made,
                        "method": job.method
                    })
                    
                    pbar.update(1)
                    
                    if progress_callback:
                        progress_callback(job, results)
        
        return results
    
    def get_job_status(self, job_id: int) -> Optional[BatchJob]:
        """Get status of a specific job"""
        with self.lock:
            if 0 <= job_id < len(self.jobs):
                return self.jobs[job_id]
        return None
    
    def clear_jobs(self) -> None:
        """Clear all jobs from the queue"""
        with self.lock:
            self.jobs.clear()
    
    def save_results_report(self, results: Dict[str, Any], report_path: str) -> None:
        """Save batch processing results to a report file"""
        report = {
            "summary": {
                "total_jobs": results["total"],
                "completed_jobs": results["completed"],
                "failed_jobs": results["failed"],
                "success_rate": f"{(results['completed'] / results['total'] * 100):.1f}%" if results["total"] > 0 else "0%",
                "total_replacements": results["total_replacements"]
            },
            "details": results["results"]
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)


def create_sample_batch_config() -> str:
    """Create a sample batch configuration file"""
    config = {
        "jobs": [
            {
                "input": "documents/contract1.pdf",
                "output": "output/contract1_updated.pdf",
                "method": "exact",
                "operations": [
                    {
                        "search": "Old Company Name Inc.",
                        "replace": "New Company Name LLC",
                        "case_sensitive": True
                    },
                    {
                        "search": "2023",
                        "replace": "2024",
                        "case_sensitive": False
                    }
                ]
            },
            {
                "input": "documents/contract2.pdf", 
                "output": "output/contract2_updated.pdf",
                "method": "structure",
                "operations": [
                    {
                        "search": "John Doe",
                        "replace": "Jane Smith",
                        "case_sensitive": True
                    },
                    {
                        "search": "Manager",
                        "replace": "Director",
                        "case_sensitive": False
                    }
                ]
            }
        ]
    }
    
    config_path = "sample_batch_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_path


def main():
    """Example usage of batch processor"""
    # Create sample configuration
    config_path = create_sample_batch_config()
    print(f"Created sample configuration: {config_path}")
    
    # Initialize batch processor
    processor = BatchProcessor(max_workers=2)
    
    # Example: Add jobs manually
    operations = [
        EditOperation("Hello", "Hi", case_sensitive=False),
        EditOperation("World", "Universe", case_sensitive=False)
    ]
    
    # This would work if we had actual PDF files
    # processor.add_job("input.pdf", "output.pdf", operations)
    
    # Example: Process directory
    # processor.process_directory("input_dir", "output_dir", operations)
    
    print("Batch processor ready!")
    print(f"Use: python -c \"from batch_processor import BatchProcessor; p = BatchProcessor(); p.add_jobs_from_config('{config_path}'); results = p.process_jobs(); print(results)\"")


if __name__ == "__main__":
    main()
