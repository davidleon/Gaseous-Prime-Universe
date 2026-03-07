"""
Arithmetic Calculator Helper

Provides direct arithmetic calculation capabilities for the chat bot.
This bypasses the manifold limitations for exact arithmetic operations.
"""

import re
from typing import Optional, Tuple


class ArithmeticCalculator:
    """
    Calculator for arithmetic operations
    
    Supports: +, -, *, /, (, ), ^, %
    """
    
    def __init__(self):
        self.operator_mapping = {
            '+': 'add',
            '-': 'subtract',
            '*': 'multiply',
            '/': 'divide',
            '^': 'power',
            '%': 'modulo'
        }
    
    def calculate(self, expression: str) -> Optional[str]:
        """
        Calculate arithmetic expression
        
        Args:
            expression: Arithmetic expression string
            
        Returns:
            Result as string, or None if invalid
        """
        try:
            # Clean the expression
            cleaned = self._clean_expression(expression)
            
            if not cleaned:
                return None
            
            # Convert ^ to ** for exponentiation
            cleaned = cleaned.replace('^', '**')
            
            # Evaluate the expression safely
            result = eval(cleaned, {"__builtins__": {}}, {})
            
            # Format the result
            if isinstance(result, float):
                # Handle floating point precision
                if result.is_integer():
                    return str(int(result))
                else:
                    # Limit decimal places
                    return f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                return str(result)
                
        except Exception as e:
            return None
    
    def _clean_expression(self, expression: str) -> Optional[str]:
        """
        Clean and validate arithmetic expression
        
        Args:
            expression: Raw expression string
            
        Returns:
            Cleaned expression, or None if invalid
        """
        # Remove whitespace
        cleaned = expression.replace(' ', '')
        
        # Extract arithmetic part (everything after '=' or before '?')
        if '=' in cleaned:
            cleaned = cleaned.split('=')[0]
        elif '?' in cleaned:
            cleaned = cleaned.split('?')[0]
        
        # Remove 'Calculate:' prefix if present
        if cleaned.startswith('Calculate:'):
            cleaned = cleaned[10:]
        
        # Validate expression
        if not self._is_valid_expression(cleaned):
            return None
        
        return cleaned
    
    def _is_valid_expression(self, expression: str) -> bool:
        """
        Validate arithmetic expression
        
        Args:
            expression: Expression to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check if expression is empty
        if not expression:
            return False
        
        # Allowed characters
        allowed_chars = set('0123456789+-*/^%().')
        
        # Check for invalid characters
        if any(c not in allowed_chars for c in expression):
            return False
        
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            return False
        
        # Check for consecutive operators (except negative numbers)
        invalid_patterns = ['++', '--', '**', '//', '^^', '%%', '*/', '/*', 
                          '+-', '-+', '*+', '/+', '^+', '%+', 
                          '+*', '-*', '**', '/*', '%*', 
                          '+/', '-/', '*/', '//', '%/', 
                          '+^', '-^', '*^', '/^', '^^', '%^',
                          '+%', '-%', '*%', '/%', '^%', '%%']
        
        for pattern in invalid_patterns:
            if pattern in expression:
                return False
        
        # Check if expression starts or ends with invalid characters
        if expression[0] in '+*/^%':
            return False
        if expression[-1] in '+-*/^%':
            return False
        
        # Check if it looks like a number or expression
        # Must contain at least one digit
        if not any(c.isdigit() for c in expression):
            return False
        
        return True
    
    def solve_arithmetic_problem(self, problem: str) -> Optional[str]:
        """
        Solve an arithmetic problem
        
        Args:
            problem: Problem string (e.g., "7/12" or "Calculate: 7/12")
            
        Returns:
            Solution string, or None if invalid
        """
        result = self.calculate(problem)
        
        if result is not None:
            # Format as equation
            cleaned = self._clean_expression(problem)
            if cleaned:
                return f"{cleaned}={result}"
        
        return None
    
    def is_arithmetic_query(self, text: str) -> bool:
        """
        Check if text is an arithmetic query
        
        Args:
            text: Text to check
            
        Returns:
            True if arithmetic query, False otherwise
        """
        # Check for arithmetic patterns
        patterns = [
            r'Calculate:', r'Solve:', r'What is', r'=',
            r'\d+[\+\-\*\/\^\%]\d+',  # Simple operation
            r'\([^)]*\)[\+\-\*\/\^\%]'  # Parentheses followed by operator
        ]
        
        for pattern in patterns:
            if re.search(pattern, text):
                return True
        
        return False


# Global calculator instance
calculator = ArithmeticCalculator()


def calculate_arithmetic(text: str) -> Optional[str]:
    """
    Calculate arithmetic from text
    
    Args:
        text: Text containing arithmetic expression
        
    Returns:
        Result string, or None if not arithmetic or invalid
    """
    if calculator.is_arithmetic_query(text):
        return calculator.solve_arithmetic_problem(text)
    return None