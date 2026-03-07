#!/usr/bin/env python3
"""
iFlow Interactive Chinese Learning System
Uses actual iFlow CLI prompts to analyze student performance and provide targeted teaching
"""

import subprocess
import json
import random
import os
from typing import Dict, List, Tuple
from datetime import datetime

class ChineseStudent:
    """Student learning Chinese with iFlow as teacher"""
    
    def __init__(self):
        self.vocabulary = {
            "你好": {"attempts": 0, "correct": 0},
            "世界": {"attempts": 0, "correct": 0},
            "朋友": {"attempts": 0, "correct": 0},
            "爱": {"attempts": 0, "correct": 0},
            "和平": {"attempts": 0, "correct": 0},
            "快乐": {"attempts": 0, "correct": 0},
            "希望": {"attempts": 0, "correct": 0},
            "梦想": {"attempts": 0, "correct": 0},
            "学习": {"attempts": 0, "correct": 0},
            "知识": {"attempts": 0, "correct": 0},
            "智慧": {"attempts": 0, "correct": 0},
            "真理": {"attempts": 0, "correct": 0},
            "美丽": {"attempts": 0, "correct": 0},
            "和谐": {"attempts": 0, "correct": 0}
        }
        
        self.lessons_learned = 0
        self.correct_responses = 0
        self.weak_words = []
        self.strong_words = []
        self.recent_mistakes = []
        
    def record_attempt(self, word: str, correct: bool):
        """Record a learning attempt"""
        if word not in self.vocabulary:
            self.vocabulary[word] = {"attempts": 0, "correct": 0}
        
        self.vocabulary[word]["attempts"] += 1
        self.lessons_learned += 1
        
        if correct:
            self.vocabulary[word]["correct"] += 1
            self.correct_responses += 1
        else:
            self.recent_mistakes.append(word)
            if len(self.recent_mistakes) > 10:
                self.recent_mistakes.pop(0)
    
    def get_performance_data(self) -> Dict:
        """Get performance data for iFlow analysis"""
        # Calculate word accuracy
        word_performance = {}
        for word, data in self.vocabulary.items():
            if data["attempts"] > 0:
                accuracy = data["correct"] / data["attempts"]
                word_performance[word] = {
                    "accuracy": accuracy,
                    "attempts": data["attempts"],
                    "correct": data["correct"]
                }
        
        # Identify weak and strong words
        self.weak_words = [
            word for word, perf in word_performance.items() 
            if perf["accuracy"] < 0.7 and perf["attempts"] >= 2
        ]
        self.strong_words = [
            word for word, perf in word_performance.items() 
            if perf["accuracy"] >= 0.8 and perf["attempts"] >= 2
        ]
        
        overall_accuracy = self.correct_responses / self.lessons_learned if self.lessons_learned > 0 else 0.0
        
        return {
            "overall_accuracy": overall_accuracy,
            "lessons_learned": self.lessons_learned,
            "correct_responses": self.correct_responses,
            "word_performance": word_performance,
            "weak_words": self.weak_words,
            "strong_words": self.strong_words,
            "recent_mistakes": self.recent_mistakes
        }


def run_iflow_prompt(prompt: str, timeout: int = 30) -> str:
    """
    Launch iFlow with a prompt and get response
    
    Args:
        prompt: The prompt to send to iFlow
        timeout: Timeout in seconds
    
    Returns:
        iFlow's response
    """
    try:
        # Launch iFlow with the prompt
        result = subprocess.run(
            ["python3", "/home/davidl/Gaseous Prime Universe/AGI/agi_system.py", prompt],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: iFlow response timeout"
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_chinese_performance(student: ChineseStudent) -> Dict:
    """
    Use iFlow to analyze student's Chinese performance
    
    Args:
        student: The Chinese student
    
    Returns:
        Analysis results
    """
    performance_data = student.get_performance_data()
    
    # Create analysis prompt for iFlow
    prompt = f"""
分析学生的语文能力，识别出问题，并针对得进行课程教育。

学生语文学习数据:
- 总准确率: {performance_data['overall_accuracy']:.2%}
- 学习次数: {performance_data['lessons_learned']}
- 正确次数: {performance_data['correct_responses']}

各词汇表现:
{json.dumps(performance_data['word_performance'], indent=2, ensure_ascii=False)}

薄弱词汇: {performance_data['weak_words']}
掌握词汇: {performance_data['strong_words']}
最近错误: {performance_data['recent_mistakes']}

请分析:
1. 学生主要问题是什么?
2. 哪些词汇需要重点加强?
3. 应该优先教哪些新词汇?
4. 教学策略建议

请用JSON格式返回:
{{
    "problem_analysis": "主要问题描述",
    "weakness_areas": ["薄弱领域1", "薄弱领域2"],
    "priority_words": ["优先词汇1", "优先词汇2"],
    "teaching_strategy": "教学策略建议",
    "next_lesson_focus": "下一课重点"
}}
"""
    
    response = run_iflow_prompt(prompt)
    
    try:
        # Try to parse JSON response
        analysis = json.loads(response)
        return analysis
    except json.JSONDecodeError:
        # If not JSON, create simple analysis from response
        return {
            "problem_analysis": response,
            "weakness_areas": student.weak_words,
            "priority_words": student.weak_words[:3] if student.weak_words else ["你好"],
            "teaching_strategy": "需要更多练习",
            "next_lesson_focus": "基础词汇"
        }


def generate_targeted_lesson(student: ChineseStudent, analysis: Dict) -> Dict:
    """
    Generate targeted lesson based on iFlow's analysis
    
    Args:
        student: The Chinese student
        analysis: iFlow's analysis results
    
    Returns:
        Lesson data
    """
    # Get priority words from analysis
    priority_words = analysis.get("priority_words", ["你好"])
    
    # Select a word to teach
    if isinstance(priority_words, list) and len(priority_words) > 0:
        word = priority_words[0]
    else:
        word = "你好"
    
    # Get translation
    translations = {
        "你好": "hello", "世界": "world", "朋友": "friend", "爱": "love",
        "和平": "peace", "快乐": "joy", "希望": "hope", "梦想": "dream",
        "学习": "learn", "知识": "knowledge", "智慧": "wisdom", "真理": "truth",
        "美丽": "beautiful", "和谐": "harmony"
    }
    
    translation = translations.get(word, word)
    
    # Create targeted lesson based on analysis
    teaching_strategy = analysis.get("teaching_strategy", "基础练习")
    
    lesson_prompt = f"""
学生需要学习中文词汇: {word} ({translation})

教学策略: {teaching_strategy}

请生成一个有针对性的教学课程:
1. 解释这个词汇的含义
2. 给出2-3个使用例句
3. 提供练习问题
4. 给出教学反馈提示

请以JSON格式返回:
{{
    "word": "{word}",
    "translation": "{translation}",
    "meaning": "词汇含义",
    "examples": ["例句1", "例句2"],
    "practice_question": "练习问题",
    "teaching_tips": "教学提示"
}}
"""
    
    response = run_iflow_prompt(lesson_prompt)
    
    try:
        lesson_data = json.loads(response)
        return lesson_data
    except json.JSONDecodeError:
        # Fallback to simple lesson
        return {
            "word": word,
            "translation": translation,
            "meaning": f"The Chinese word for {translation}",
            "examples": [
                f"{word}! How are you?",
                f"我很{translation}。"
            ],
            "practice_question": f"Translate '{translation}' to Chinese",
            "teaching_tips": f"Remember: {word} means {translation}"
        }


def assess_student_response(student: ChineseStudent, lesson: Dict, response: str) -> Dict:
    """
    Use iFlow to assess student's response
    
    Args:
        student: The Chinese student
        lesson: The lesson data
        response: Student's response
    
    Returns:
        Assessment results
    """
    assessment_prompt = f"""
评估学生的中文回答。

课程内容:
- 词汇: {lesson['word']} ({lesson['translation']})
- 含义: {lesson.get('meaning', '')}
- 例句: {lesson.get('examples', [])}

学生回答: {response}

请评估:
1. 回答是否正确?
2. 理解程度如何?
3. 需要改进的地方?
4. 鼓励性反馈

请以JSON格式返回:
{{
    "correct": true/false,
    "score": 0.0-1.0,
    "understanding": "理解程度描述",
    "improvements": ["改进建议1", "改进建议2"],
    "feedback": "鼓励性反馈"
}}
"""
    
    result = run_iflow_prompt(assessment_prompt)
    
    try:
        assessment = json.loads(result)
        return assessment
    except json.JSONDecodeError:
        # Simple fallback assessment
        has_correct_char = lesson['word'] in response
        is_correct = has_correct_char or lesson['translation'].lower() in response.lower()
        return {
            "correct": is_correct,
            "score": 1.0 if is_correct else 0.5,
            "understanding": "Good effort" if is_correct else "Needs more practice",
            "improvements": ["Practice more examples"],
            "feedback": "Keep learning!" if is_correct else "Try again!"
        }


def run_interactive_chinese_learning(max_lessons: int = 100):
    """
    Run interactive Chinese learning with iFlow as teacher
    
    Args:
        max_lessons: Maximum number of lessons
    """
    print("="*80)
    print("iFlow INTERACTIVE CHINESE LEARNING SYSTEM")
    print("="*80)
    print("\n使用iFlow作为中文老师，分析学生能力并提供针对性教学")
    print(f"最大课程数: {max_lessons}")
    print("\n开始学习...\n")
    
    student = ChineseStudent()
    session_start = datetime.now()
    
    for lesson_num in range(1, max_lessons + 1):
        print(f"\n{'='*80}")
        print(f"课程 {lesson_num}/{max_lessons}")
        print(f"{'='*80}")
        
        # Every 10 lessons, ask iFlow to analyze performance
        if lesson_num % 10 == 1 or lesson_num == 1:
            print("\n[分析阶段] 让iFlow分析学生表现...")
            analysis = analyze_chinese_performance(student)
            
            print(f"\niFlow分析结果:")
            print(f"  问题分析: {analysis.get('problem_analysis', 'N/A')}")
            print(f"  薄弱领域: {analysis.get('weakness_areas', [])}")
            print(f"  优先词汇: {analysis.get('priority_words', [])}")
            print(f"  教学策略: {analysis.get('teaching_strategy', 'N/A')}")
            print(f"  下一课重点: {analysis.get('next_lesson_focus', 'N/A')}")
        
        # Generate targeted lesson based on analysis
        print("\n[教学阶段] 生成针对性课程...")
        lesson = generate_targeted_lesson(student, analysis if lesson_num % 10 == 1 or lesson_num == 1 else {})
        
        print(f"\n词汇: {lesson['word']} ({lesson['translation']})")
        print(f"含义: {lesson.get('meaning', 'N/A')}")
        print(f"例句:")
        for i, example in enumerate(lesson.get('examples', []), 1):
            print(f"  {i}. {example}")
        print(f"练习问题: {lesson.get('practice_question', 'N/A')}")
        
        # Generate student response (simulated)
        print(f"\n[学习阶段] 学生正在学习...")
        
        # Simulate student response (improves over time)
        performance_data = student.get_performance_data()
        student_skill = performance_data['overall_accuracy']
        
        # Student response generation (simulated)
        if random.random() < student_skill + 0.3:  # Chance to answer correctly
            if random.random() < 0.7:
                response = f"{lesson['word']}"
            else:
                response = f"这个意思是{lesson['translation']}"
        else:
            response = "我不确定"
        
        print(f"学生回答: {response}")
        
        # Assess response with iFlow
        print("\n[评估阶段] 让iFlow评估学生回答...")
        assessment = assess_student_response(student, lesson, response)
        
        # Record attempt
        student.record_attempt(lesson['word'], assessment.get('correct', False))
        
        # Display assessment
        is_correct = assessment.get('correct', False)
        score = assessment.get('score', 0.0)
        status = "✓" if is_correct else "✗"
        
        print(f"\niFlow评估:")
        print(f"  状态: {status} (得分: {score:.2f})")
        print(f"  理解程度: {assessment.get('understanding', 'N/A')}")
        print(f"  改进建议: {assessment.get('improvements', [])}")
        print(f"  反馈: {assessment.get('feedback', 'N/A')}")
        
        # Display current progress
        performance = student.get_performance_data()
        print(f"\n当前进度:")
        print(f"  总准确率: {performance['overall_accuracy']:.2%}")
        print(f"  已学词汇: {performance['lessons_learned']}")
        print(f"  薄弱词汇: {performance['weak_words']}")
        print(f"  掌握词汇: {performance['strong_words']}")
        
        # Small delay between lessons
        import time
        time.sleep(1)
    
    # Final summary
    session_end = datetime.now()
    duration = (session_end - session_start).total_seconds() / 60
    
    print(f"\n{'='*80}")
    print("学习完成!")
    print(f"{'='*80}")
    print(f"\n最终统计:")
    print(f"  总课程数: {max_lessons}")
    print(f"  学习时长: {duration:.1f} 分钟")
    
    final_performance = student.get_performance_data()
    print(f"  总准确率: {final_performance['overall_accuracy']:.2%}")
    print(f"  正确回答: {final_performance['correct_responses']}/{final_performance['lessons_learned']}")
    print(f"  已掌握词汇: {len(final_performance['strong_words'])}")
    print(f"  需加强词汇: {len(final_performance['weak_words'])}")
    
    print(f"\n词汇详细表现:")
    for word, perf in final_performance['word_performance'].items():
        status = "✓" if perf['accuracy'] >= 0.8 else "✗" if perf['accuracy'] < 0.5 else "~"
        print(f"  {status} {word}: {perf['accuracy']:.1%} ({perf['correct']}/{perf['attempts']})")
    
    print(f"\n✓ 学习会话完成!")


if __name__ == "__main__":
    # Run 100 lessons
    run_interactive_chinese_learning(max_lessons=100)
