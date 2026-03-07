import os
import subprocess
import time

def get_module_name(file_path):
    # Convert path like 'Gpu/Core/Base/API.lean' to 'Gpu.Core.Base.API'
    module_name = file_path.replace('.lean', '').replace(os.sep, '.')
    return module_name

def benchmark():
    lean_files = []
    # Walk while skipping the .lake folder
    for root, dirs, files in os.walk('.'):
        if '.lake' in dirs:
            dirs.remove('.lake') # skip it
        for file in files:
            if file.endswith('.lean') and file not in ['lakefile.lean', 'Main.lean']:
                # Get path relative to current dir
                rel_path = os.path.relpath(os.path.join(root, file), start='.')
                lean_files.append(rel_path)
    
    lean_files.sort()
    
    results = []
    log_file = "build_benchmark.log"
    
    with open(log_file, "w") as f:
        f.write(f"🚀 Benchmarking {len(lean_files)} Lean files...\n")
        f.write("-" * 60 + "\n")
        f.flush()
        
        print(f"🚀 Benchmarking {len(lean_files)} Lean files...")
        print("-" * 60)
        
        for i, lean_file in enumerate(lean_files):
            module = get_module_name(lean_file)
            status_msg = f"[{i+1}/{len(lean_files)}] Compiling {module}..."
            print(status_msg, end='', flush=True)
            
            start_time = time.time()
            try:
                # Use a 3-second timeout per file
                process = subprocess.run(['lake', 'build', module], 
                                       capture_output=True, 
                                       text=True,
                                       timeout=3)
                end_time = time.time()
                duration = end_time - start_time
                
                if process.returncode == 0:
                    result_line = f" ✅ {duration:.2f}s"
                    results.append((module, duration, "Success"))
                else:
                    # Capture the error output for failed files
                    result_line = f" ❌ {duration:.2f}s (Failed)"
                    results.append((module, duration, "Failed"))
                    f.write(f"\nError for {module}:\n{process.stderr}\n")
            except subprocess.TimeoutExpired:
                end_time = time.time()
                duration = end_time - start_time
                result_line = f" ⏰ {duration:.2f}s (TIMEOUT)"
                results.append((module, duration, "Timeout"))
            except Exception as e:
                result_line = f" 💥 Error: {e}"
                results.append((module, 0, "Error"))
                
            print(result_line)
            f.write(status_msg + result_line + "\n")
            f.flush()
            
        f.write("-" * 60 + "\n")
        f.write("📊 TOP 10 SLOWEST FILES:\n")
        results.sort(key=lambda x: x[1], reverse=True)
        for module, duration, status in results[:10]:
            f.write(f"{duration:7.2f}s | {status:7} | {module}\n")

if __name__ == "__main__":
    benchmark()
