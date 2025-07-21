#!/usr/bin/env python3
"""
Portal Gun Mod - Dump Log Analyzer
Analyzes the dump.log file for errors, warnings, and patterns
"""

import re
import os
from collections import Counter, defaultdict

def analyze_dump_log(file_path):
    """Analyze the dump log file and extract error information"""
    
    if not os.path.exists(file_path):
        print(f"❌ Dump file not found: {file_path}")
        return
    
    print(f"📊 Analyzing dump file: {file_path}")
    print("=" * 60)
    
    # Counters for different types of issues
    error_counter = Counter()
    warning_counter = Counter()
    portal_gun_messages = []
    exception_patterns = []
    job_errors = []
    recursive_calls = []
    
    # Pattern definitions
    patterns = {
        'portal_gun': r'\[Portal Gun\]',
        'error': r'(Error|Exception|Failed)',
        'warning': r'Warning',
        'job_error': r'JobUtility\.TryStartErrorRecoverJob',
        'stack_overflow': r'StackOverflowException',
        'null_reference': r'NullReferenceException',
        'argument_exception': r'ArgumentException',
        'try_reuse_portal': r'TryReuseExistingPortal',
        'harmony_patch': r'Patch_PathFollower_StartPath',
        'infinite_loop': r'(StartPath_Patch4.*){3,}',  # Multiple StartPath calls in sequence
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        total_lines = len(lines)
        print(f"📄 Total lines: {total_lines:,}")
        
        # Track consecutive identical calls for loop detection
        previous_line = ""
        consecutive_count = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Portal Gun specific messages
            if re.search(patterns['portal_gun'], line, re.IGNORECASE):
                portal_gun_messages.append((i, line))
            
            # Errors and exceptions
            if re.search(patterns['error'], line, re.IGNORECASE):
                error_type = extract_error_type(line)
                error_counter[error_type] += 1
                
                # Store exception patterns
                if 'Exception' in line:
                    exception_patterns.append((i, line))
            
            # Warnings
            if re.search(patterns['warning'], line, re.IGNORECASE):
                warning_type = extract_warning_type(line)
                warning_counter[warning_type] += 1
            
            # Job errors
            if re.search(patterns['job_error'], line, re.IGNORECASE):
                job_errors.append((i, line))
            
            # Detect potential infinite loops
            if re.search(patterns['try_reuse_portal'], line, re.IGNORECASE):
                recursive_calls.append((i, line))
            
            # Check for consecutive identical lines (loop detection)
            if line == previous_line:
                consecutive_count += 1
            else:
                if consecutive_count > 5:  # Report if same line repeats more than 5 times
                    print(f"🔄 Potential loop detected around line {i-consecutive_count}: {consecutive_count} identical calls")
                consecutive_count = 0
                previous_line = line
        
        # Print analysis results
        print_analysis_results(
            total_lines, error_counter, warning_counter, 
            portal_gun_messages, exception_patterns, 
            job_errors, recursive_calls
        )
        
        # Generate summary report
        generate_summary_report(file_path, total_lines, error_counter, warning_counter, len(portal_gun_messages))
        
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")

def extract_error_type(line):
    """Extract the type of error from the line"""
    error_patterns = [
        r'(\w*Exception)',
        r'(Error:\s*\w+)',
        r'(Failed\s+\w+)',
    ]
    
    for pattern in error_patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return "Unknown Error"

def extract_warning_type(line):
    """Extract the type of warning from the line"""
    if 'Portal Gun' in line:
        return "Portal Gun Warning"
    elif 'JobUtility' in line:
        return "Job Warning"
    elif 'PathFollower' in line:
        return "PathFollower Warning"
    else:
        return "Other Warning"

def print_analysis_results(total_lines, error_counter, warning_counter, 
                         portal_gun_messages, exception_patterns, 
                         job_errors, recursive_calls):
    """Print the analysis results in a formatted way"""
    
    print(f"\n🚨 ERRORS FOUND ({sum(error_counter.values())} total):")
    if error_counter:
        for error_type, count in error_counter.most_common():
            print(f"  • {error_type}: {count}")
    else:
        print("  ✅ No errors found")
    
    print(f"\n⚠️  WARNINGS FOUND ({sum(warning_counter.values())} total):")
    if warning_counter:
        for warning_type, count in warning_counter.most_common():
            print(f"  • {warning_type}: {count}")
    else:
        print("  ✅ No warnings found")
    
    print(f"\n🎯 PORTAL GUN MESSAGES ({len(portal_gun_messages)} total):")
    if portal_gun_messages:
        # Show first and last few portal gun messages
        print("  First few messages:")
        for line_num, message in portal_gun_messages[:5]:
            print(f"    Line {line_num}: {message[:100]}...")
        
        if len(portal_gun_messages) > 10:
            print("  ...")
            print("  Last few messages:")
            for line_num, message in portal_gun_messages[-5:]:
                print(f"    Line {line_num}: {message[:100]}...")
    else:
        print("  ℹ️  No Portal Gun messages found")
    
    print(f"\n🔧 JOB ERRORS ({len(job_errors)} total):")
    if job_errors:
        print(f"  Found {len(job_errors)} job error recovery attempts")
        # Show unique job error patterns
        job_patterns = set()
        for _, line in job_errors:
            if 'TryStartErrorRecoverJob' in line:
                job_patterns.add("TryStartErrorRecoverJob")
        for pattern in job_patterns:
            print(f"  • {pattern}")
    else:
        print("  ✅ No job errors found")
    
    print(f"\n🔄 POTENTIAL RECURSION ({len(recursive_calls)} total):")
    if recursive_calls:
        print(f"  Found {len(recursive_calls)} calls to TryReuseExistingPortal")
        print("  ⚠️  This may indicate infinite recursion in portal reuse logic")
    else:
        print("  ✅ No recursion detected")

def generate_summary_report(file_path, total_lines, error_counter, warning_counter, portal_messages):
    """Generate a summary report file"""
    
    report_path = file_path.replace('dump.log', 'dump_analysis_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Portal Gun Mod - Dump Log Analysis Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"File analyzed: {file_path}\n")
        f.write(f"Total lines: {total_lines:,}\n")
        f.write(f"Total errors: {sum(error_counter.values())}\n")
        f.write(f"Total warnings: {sum(warning_counter.values())}\n")
        f.write(f"Portal Gun messages: {portal_messages}\n\n")
        
        f.write("Top Errors:\n")
        for error_type, count in error_counter.most_common(10):
            f.write(f"  {error_type}: {count}\n")
        
        f.write("\nTop Warnings:\n")
        for warning_type, count in warning_counter.most_common(10):
            f.write(f"  {warning_type}: {count}\n")
    
    print(f"\n📄 Detailed report saved to: {report_path}")

def main():
    """Main function"""
    print("🚀 Portal Gun Mod - Dump Log Analyzer")
    print("=" * 50)
    
    # Try to find the dump.log file
    possible_paths = [
        'C:\\Users\\Mitch\\AppData\\LocalLow\\Ludeon Studios\\RimWorld by Ludeon Studios\\Player.log'
    ]
    
    dump_file = None
    for path in possible_paths:
        if os.path.exists(path):
            dump_file = path
            break
    
    if not dump_file:
        print("❌ Could not find dump.log file")
        print("Please ensure dump.log is in the same directory as this script")
        return
    
    analyze_dump_log(dump_file)
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
