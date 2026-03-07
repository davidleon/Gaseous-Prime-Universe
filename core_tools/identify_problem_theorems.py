import subprocess
import re
import json
import os

def find_theorem_at_line(file_path, line_num):
    full_path = f"core_formalization/{file_path}"
    if not os.path.exists(full_path):
        return "Unknown"
    try:
        with open(full_path, 'r') as f:
            lines = f.readlines()
            # Search backwards from line_num for "theorem" or "lemma" or "def" or "instance"
            for i in range(line_num - 1, -1, -1):
                if i >= len(lines): continue
                line = lines[i]
                match = re.search(r'(theorem|lemma|def|instance|axiom|structure)\s+([a-zA-Z0-9_]+)', line)
                if match:
                    return match.group(2)
    except Exception as e:
        return f"Error: {str(e)}"
    return "Unknown"

def get_failed_theorems():
    print("🔍 SCANNING FOR PROBLEM THEOREMS VIA LAKE BUILD...")
    
    # Run lake build and capture everything
    result = subprocess.run(['lake', 'build', 'Gpu'], 
                            cwd='core_formalization',
                            capture_output=True, 
                            text=True)
    
    output = result.stdout + result.stderr
    
    theorems = []
    
    # Regex to find theorem names in files that failed
    error_pattern = re.compile(r'error: (.*?\.lean):(\d+):(\d+): (.*)')
    
    for line in output.split('\n'):
        match = error_pattern.search(line)
        if match:
            file_path = match.group(1)
            line_num = int(match.group(2))
            error_msg = match.group(4)
            
            theorem_name = find_theorem_at_line(file_path, line_num)
            
            theorems.append({
                "file": file_path,
                "line": line_num,
                "error": error_msg,
                "theorem": theorem_name,
                "type": "error"
            })
            
    # Deduplicate and sort
    problem_report = {}
    for t in theorems:
        key = f"{t['file']}:{t['theorem']}"
        if key not in problem_report:
            problem_report[key] = t
            problem_report[key]["count"] = 1
        else:
            problem_report[key]["count"] += 1

    sorted_problems = sorted(problem_report.values(), key=lambda x: x['count'], reverse=True)
    
    with open("problem_theorems.json", "w") as f:
        json.dump(sorted_problems, f, indent=2)
        
    print(f"✅ IDENTIFIED {len(sorted_problems)} PROBLEM THEOREMS.")
    for p in sorted_problems[:10]:
        print(f"📍 {p['file']} -> {p['theorem']} ({p['count']} errors) - {p['error'][:50]}...")

if __name__ == "__main__":
    get_failed_theorems()
