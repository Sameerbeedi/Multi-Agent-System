# main.py
import sys
from agents.classifier_agent import classify_and_route
from utils.file_parser import read_file
from memory.memory_store import log_result

def main(file_path):
    content = read_file(file_path)
    file_format, intent, result = classify_and_route(file_path, content)

    log_result(file_path, file_format, intent, result)
    print("Classification:", file_format, intent)
    print("Output:\n", result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
    else:
        main(sys.argv[1])
