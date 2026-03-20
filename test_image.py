"""
Test script - Test Tongyi Wanxiang image generation
"""

import sys
import os
import time
import requests

sys.path.append('.')
from config import TONGYI_API_KEY

API_KEY = 'sk-329c712504264f1bb4f9c24d58e8c4b9'
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

def generate_image(prompt, output_path="output/test.png"):
    """Generate image"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"
    }
    
    payload = {
        "model": "qwen-image",
        "input": {"prompt": prompt},
        "parameters": {"size": "1024*1024"}
    }
    
    payload = {
        "model": "qwen-image",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "size": "1024*1024"
        }
    }
    
    print("Generating image...")
    print(f"Prompt: {prompt}")
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        print(f"API response: {result}")
        
        task_id = result.get("output", {}).get("task_id")
        if not task_id:
            print("Failed to get task_id")
            return None
        
        print(f"Task ID: {task_id}")
        
        image_url = wait_for_result(task_id, headers)
        if image_url:
            return download_image(image_url, output_path)
        
        return None
        
    except Exception as e:
        print(f"Generation failed: {e}")
        return None


def wait_for_result(task_id, headers, max_wait=180):
    """Poll for result"""
    status_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    
    for i in range(max_wait // 10):
        try:
            response = requests.get(status_url, headers=headers, timeout=30)
            result = response.json()
            
            status = result.get("output", {}).get("task_status")
            print(f"Status check {i+1}: {status}")
            
            if status == "SUCCEEDED":
                results = result.get("output", {}).get("results", [])
                if results:
                    return results[0].get("url")
                return None
            elif status == "FAILED":
                print("Task failed:", result)
                return None
            
            time.sleep(10)
        except Exception as e:
            print(f"Query failed: {e}")
            time.sleep(10)
    
    return None


def download_image(url, path):
    """Download image"""
    try:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        with open(path, "wb") as f:
            f.write(response.content)
        
        print(f"Image saved: {path}")
        return path
    except Exception as e:
        print(f"Download failed: {e}")
        return None


def test_shadow_puppet():
    """Test shadow puppet image generation"""
    
    prompts = [
        "Traditional Chinese shadow puppet, warrior character with sword, intricate cut-out patterns, leather texture, ancient Chinese style",
        "Traditional Chinese shadow puppet, old wise man with long beard, flowing robes, gentle smile, shadow puppet art style",
        "Traditional Chinese shadow puppet, ancient village scene with traditional architecture, large tree, peaceful atmosphere"
    ]
    
    os.makedirs("output", exist_ok=True)
    
    for i, prompt in enumerate(prompts):
        print(f"\n{'='*50}")
        print(f"Test {i+1}/{len(prompts)}")
        print('='*50)
        
        output_path = f"output/test_{i+1}.png"
        result = generate_image(prompt, output_path)
        
        if result:
            print(f"[OK] Image saved: {result}")
        else:
            print(f"[FAIL] Image generation failed")


if __name__ == "__main__":
    test_shadow_puppet()
