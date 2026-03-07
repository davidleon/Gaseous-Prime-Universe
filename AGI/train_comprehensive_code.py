"""
Enhanced Code Training with Comprehensive Code Samples

Trains the manifold on a diverse set of pure code samples covering:
- Functions and classes
- Data structures
- Algorithms
- Common programming patterns
"""

import sys
import os

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolving_chat_bot import EvolvingChatBot


def get_comprehensive_code_samples() -> list:
    """
    Get comprehensive code samples covering various programming concepts
    
    Returns:
        List of (code, description) tuples
    """
    return [
        # Functions
        ("def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)", "Recursive fibonacci"),
        
        ("def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)", "Quick sort algorithm"),
        
        ("def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1", "Binary search"),
        
        ("def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True", "Prime check"),
        
        ("def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a", "Greatest common divisor"),
        
        # Classes
        ("class Node:\n    def __init__(self, value):\n        self.value = value\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n    def append(self, value):\n        new_node = Node(value)\n        if not self.head:\n            self.head = new_node\n        else:\n            current = self.head\n            while current.next:\n                current = current.next\n            current.next = new_node", "Linked list implementation"),
        
        ("class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        if not self.is_empty():\n            return self.items.pop()\n    def is_empty(self):\n        return len(self.items) == 0", "Stack implementation"),
        
        ("class Queue:\n    def __init__(self):\n        self.items = []\n    def enqueue(self, item):\n        self.items.insert(0, item)\n    def dequeue(self):\n        if not self.is_empty():\n            return self.items.pop()\n    def is_empty(self):\n        return len(self.items) == 0", "Queue implementation"),
        
        ("class TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\nclass BinaryTree:\n    def __init__(self):\n        self.root = None\n    def insert(self, val):\n        if not self.root:\n            self.root = TreeNode(val)\n        else:\n            self._insert_recursive(self.root, val)\n    def _insert_recursive(self, node, val):\n        if val < node.val:\n            if node.left:\n                self._insert_recursive(node.left, val)\n            else:\n                node.left = TreeNode(val)\n        else:\n            if node.right:\n                self._insert_recursive(node.right, val)\n            else:\n                node.right = TreeNode(val)", "Binary tree"),
        
        # Algorithms
        ("def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr", "Bubble sort"),
        
        ("def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] < right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result", "Merge sort"),
        
        ("def matrix_multiply(A, B):\n    rows_A = len(A)\n    cols_A = len(A[0])\n    rows_B = len(B)\n    cols_B = len(B[0])\n    if cols_A != rows_B:\n        return None\n    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]\n    for i in range(rows_A):\n        for j in range(cols_B):\n            for k in range(cols_A):\n                result[i][j] += A[i][k] * B[k][j]\n    return result", "Matrix multiplication"),
        
        ("def depth_first_search(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    print(start)\n    for neighbor in graph.get(start, []):\n        if neighbor not in visited:\n            depth_first_search(graph, neighbor, visited)", "DFS traversal"),
        
        ("def breadth_first_search(graph, start):\n    visited = set([start])\n    queue = [start]\n    while queue:\n        node = queue.pop(0)\n        print(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)", "BFS traversal"),
        
        # Common patterns
        ("def memoize(func):\n    cache = {}\n    def wrapper(*args):\n        if args not in cache:\n            cache[args] = func(*args)\n        return cache[args]\n    return wrapper", "Memoization decorator"),
        
        ("def validate_email(email):\n    import re\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return re.match(pattern, email) is not None", "Email validation"),
        
        ("def flatten_list(nested_list):\n    result = []\n    for item in nested_list:\n        if isinstance(item, list):\n            result.extend(flatten_list(item))\n        else:\n            result.append(item)\n    return result", "Flatten nested list"),
        
        ("def remove_duplicates(lst):\n    seen = set()\n    result = []\n    for item in lst:\n        if item not in seen:\n            seen.add(item)\n            result.append(item)\n    return result", "Remove duplicates"),
        
        ("def count_occurrences(lst, target):\n    count = 0\n    for item in lst:\n        if item == target:\n            count += 1\n    return count", "Count occurrences"),
        
        ("def reverse_string(s):\n    return s[::-1]", "Reverse string"),
        
        ("def palindrome_check(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]", "Palindrome check"),
        
        ("def file_size(filepath):\n    import os\n    return os.path.getsize(filepath)", "Get file size"),
        
        ("def read_file_lines(filepath):\n    with open(filepath, 'r') as f:\n        return f.readlines()", "Read file lines"),
        
        ("def write_to_file(filepath, content):\n    with open(filepath, 'w') as f:\n        f.write(content)", "Write to file"),
        
        ("def parse_json(json_string):\n    import json\n    return json.loads(json_string)", "Parse JSON"),
        
        ("def format_date(date):\n    return date.strftime('%Y-%m-%d')", "Format date"),
        
        ("def calculate_average(numbers):\n    return sum(numbers) / len(numbers)", "Calculate average"),
        
        ("def find_max_min(lst):\n    return max(lst), min(lst)", "Find max and min"),
        
        ("def shuffle_list(lst):\n    import random\n    random.shuffle(lst)\n    return lst", "Shuffle list"),
        
        ("def is_even(n):\n    return n % 2 == 0", "Check if even"),
        
        ("def is_odd(n):\n    return n % 2 != 0", "Check if odd"),
        
        ("def absolute_value(n):\n    return abs(n)", "Absolute value"),
        
        ("def square_root(n):\n    return n ** 0.5", "Square root"),
        
        ("def power(base, exponent):\n    return base ** exponent", "Power function"),
        
        ("def round_number(n, decimals=2):\n    return round(n, decimals)", "Round number"),
        
        ("def generate_range(start, end, step=1):\n    return list(range(start, end, step))", "Generate range"),
        
        ("def sum_list(numbers):\n    return sum(numbers)", "Sum list"),
        
        ("def product_list(numbers):\n    result = 1\n    for num in numbers:\n        result *= num\n    return result", "Product of list"),
        
        ("def filter_list(lst, condition):\n    return [item for item in lst if condition(item)]", "Filter list"),
        
        ("def map_list(lst, function):\n    return [function(item) for item in lst]", "Map list"),
        
        ("def zip_lists(list1, list2):\n    return list(zip(list1, list2))", "Zip lists"),
        
        ("def sort_list(lst, reverse=False):\n    return sorted(lst, reverse=reverse)", "Sort list"),
        
        ("def split_string(s, delimiter):\n    return s.split(delimiter)", "Split string"),
        
        ("def join_strings(strings, delimiter):\n    return delimiter.join(strings)", "Join strings"),
        
        ("def capitalize_words(s):\n    return ' '.join(word.capitalize() for word in s.split())", "Capitalize words"),
        
        ("def remove_whitespace(s):\n    return s.replace(' ', '')", "Remove whitespace"),
        
        ("def count_words(s):\n    return len(s.split())", "Count words"),
        
        ("def check_substring(s, sub):\n    return sub in s", "Check substring"),
        
        ("def replace_text(s, old, new):\n    return s.replace(old, new)", "Replace text"),
        
        ("def trim_string(s):\n    return s.strip()", "Trim string"),
        
        ("def to_uppercase(s):\n    return s.upper()", "To uppercase"),
        
        ("def to_lowercase(s):\n    return s.lower()", "To lowercase"),
        
        ("def is_empty(s):\n    return len(s.strip()) == 0", "Check if empty"),
        
        ("def contains_digit(s):\n    return any(char.isdigit() for char in s)", "Contains digit"),
        
        ("def contains_alpha(s):\n    return any(char.isalpha() for char in s)", "Contains alpha"),
        
        ("def contains_special(s):\n    return any(not char.isalnum() for char in s)", "Contains special char"),
        
        ("def validate_number(s):\n    try:\n        float(s)\n        return True\n    except ValueError:\n        return False", "Validate number"),
    ]


def train_comprehensive_code(bot: EvolvingChatBot, num_samples: int = 50):
    """
    Train bot on comprehensive code samples
    
    Args:
        bot: Evolving chat bot
        num_samples: Number of samples to train on
    """
    print("=" * 60)
    print("Training Manifold on Comprehensive Code Dataset")
    print("=" * 60)
    
    code_samples = get_comprehensive_code_samples()
    
    print(f"\nTotal code samples available: {len(code_samples)}")
    print(f"Training on {num_samples} samples\n")
    
    trained_count = 0
    for i, (code, description) in enumerate(code_samples[:num_samples]):
        try:
            print(f"  Training {i+1}/{num_samples}: {description}")
            
            # Train with adaptive repetition
            result = bot.trainer.train_with_adaptive_repetition(code)
            
            # Add to autoencoder
            manifold = bot.trainer.learner.encode_text(code)
            bot.autoencoder.decoder.add_text(code, manifold)
            
            trained_count += 1
            
            # Show progress
            if (i + 1) % 10 == 0:
                stats = bot.trainer.get_comprehensive_stats()
                print(f"    Progress: {i+1}/{num_samples}")
                print(f"    Avg epiplexity: {stats.get('avg_epiplexity', 0):.3f}")
                print(f"    Skill level: {stats.get('skill_level', 0):.2%}")
        
        except Exception as e:
            print(f"  Warning: Failed to train {description}: {e}")
    
    print(f"\n  ✓ Trained {trained_count} code samples")
    
    # Save trained bot
    save_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/code_comprehensive_bot.npz"
    bot.save_state(save_path)
    print(f"  ✓ Saved to: {save_path}\n")
    
    return trained_count


def test_code_generation(bot: EvolvingChatBot):
    """Test code generation capabilities"""
    print("=" * 60)
    print("Testing Code Generation")
    print("=" * 60 + "\n")
    
    test_prompts = [
        "Write a function to calculate factorial",
        "Create a class for a stack",
        "Implement binary search",
        "Define a function to check if a number is prime",
        "Write code to sort a list",
        "Create a function to reverse a string",
    ]
    
    for prompt in test_prompts:
        print(f"Prompt: {prompt}")
        response, metadata = bot.process_message(prompt)
        print(f"Epiplexity: {metadata['epiplexity']:.4f}")
        print(f"Response: {response}")
        print(f"{'-' * 60}\n")


def main():
    """Main function"""
    # Create bot
    bot = EvolvingChatBot(name="EVA", manifold_dim=12, quiet=True)
    
    # Train on comprehensive code
    trained_count = train_comprehensive_code(bot, num_samples=50)
    
    # Test code generation
    test_code_generation(bot)
    
    # Final statistics
    stats = bot.trainer.get_comprehensive_stats()
    print("=" * 60)
    print("Final Statistics")
    print("=" * 60)
    print(f"Total samples trained: {trained_count}")
    print(f"Total texts processed: {stats.get('proofs_processed', 0)}")
    print(f"Total completions: {stats.get('completions_learned', 0)}")
    print(f"Average epiplexity: {stats.get('avg_epiplexity', 0):.3f}")
    print(f"Skill level: {stats.get('skill_level', 0):.2%}")


if __name__ == "__main__":
    main()
    print("\n✓ Comprehensive code training complete!")
    sys.exit(0)
