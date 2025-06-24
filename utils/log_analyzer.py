#!/usr/bin/env python3
"""
Log Analyzer - Phân tích log để tạo báo cáo thống kê
"""

import re
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter

def analyze_logs(log_file_path='logs/emotionai.log'):
    """Phân tích log file và tạo báo cáo"""
    print("📊 Log Analysis Report")
    print("=" * 50)
    
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📋 Total log entries: {len(lines)}")
        
        # Parse logs
        log_entries = []
        for line in lines:
            line = line.strip()
            if line:
                # Parse log format
                match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - ([^-]+) - (\w+) - (.+)', line)
                if match:
                    timestamp, logger, level, message = match.groups()
                    log_entries.append({
                        'timestamp': timestamp,
                        'logger': logger,
                        'level': level,
                        'message': message
                    })
        
        print(f"✅ Parsed entries: {len(log_entries)}")
        
        # Thống kê theo level
        level_stats = Counter(entry['level'] for entry in log_entries)
        print(f"\n📈 Log Levels:")
        for level, count in level_stats.most_common():
            print(f"   {level}: {count}")
        
        # Thống kê theo logger
        logger_stats = Counter(entry['logger'] for entry in log_entries)
        print(f"\n🔧 Loggers:")
        for logger, count in logger_stats.most_common():
            print(f"   {logger}: {count}")
        
        # Thống kê API calls
        api_calls = [entry for entry in log_entries if '💬 API call' in entry['message']]
        print(f"\n💬 API Calls: {len(api_calls)}")
        
        # Thống kê state transitions
        state_transitions = [entry for entry in log_entries if '🔄 State transition' in entry['message']]
        print(f"🔄 State Transitions: {len(state_transitions)}")
        
        # Thống kê emotions detected
        emotions_detected = [entry for entry in log_entries if '🎯 Emotion detected' in entry['message']]
        print(f"🎯 Emotions Detected: {len(emotions_detected)}")
        
        # Thống kê fragrances suggested
        fragrances_suggested = [entry for entry in log_entries if '🕯️ Fragrance suggested' in entry['message']]
        print(f"🕯️ Fragrances Suggested: {len(fragrances_suggested)}")
        
        # Thống kê errors
        errors = [entry for entry in log_entries if entry['level'] == 'ERROR']
        print(f"❌ Errors: {len(errors)}")
        
        if errors:
            print(f"\n🚨 Recent Errors:")
            for error in errors[-5:]:  # 5 errors gần nhất
                print(f"   {error['timestamp']}: {error['message']}")
        
        # Thống kê theo thời gian (nếu có đủ dữ liệu)
        if len(log_entries) > 10:
            print(f"\n⏰ Time Analysis:")
            try:
                first_time = datetime.strptime(log_entries[0]['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
                last_time = datetime.strptime(log_entries[-1]['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
                duration = last_time - first_time
                print(f"   Duration: {duration}")
                print(f"   Average entries per hour: {len(log_entries) / (duration.total_seconds() / 3600):.1f}")
            except Exception as e:
                print(f"   Time analysis error: {e}")
        
        # Tạo báo cáo JSON
        report = {
            'summary': {
                'total_entries': len(log_entries),
                'api_calls': len(api_calls),
                'state_transitions': len(state_transitions),
                'emotions_detected': len(emotions_detected),
                'fragrances_suggested': len(fragrances_suggested),
                'errors': len(errors)
            },
            'level_stats': dict(level_stats),
            'logger_stats': dict(logger_stats),
            'recent_errors': [{'timestamp': e['timestamp'], 'message': e['message']} for e in errors[-5:]]
        }
        
        # Lưu báo cáo
        with open('logs/analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analysis report saved to: logs/analysis_report.json")
        
        return report
        
    except FileNotFoundError:
        print(f"❌ Log file not found: {log_file_path}")
        return None
    except Exception as e:
        print(f"❌ Error analyzing logs: {e}")
        return None

def get_system_health():
    """Đánh giá sức khỏe hệ thống dựa trên logs"""
    print(f"\n🏥 System Health Check")
    print("=" * 30)
    
    try:
        with open('logs/analysis_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        summary = report['summary']
        errors = summary['errors']
        total_entries = summary['total_entries']
        
        # Tính tỷ lệ lỗi
        error_rate = (errors / total_entries * 100) if total_entries > 0 else 0
        
        print(f"📊 Total entries: {total_entries}")
        print(f"❌ Errors: {errors}")
        print(f"📈 Error rate: {error_rate:.2f}%")
        
        # Đánh giá sức khỏe
        if error_rate < 1:
            health_status = "🟢 EXCELLENT"
        elif error_rate < 5:
            health_status = "🟡 GOOD"
        elif error_rate < 10:
            health_status = "🟠 WARNING"
        else:
            health_status = "🔴 CRITICAL"
        
        print(f"🏥 Health Status: {health_status}")
        
        # Kiểm tra các metrics quan trọng
        api_calls = summary['api_calls']
        emotions_detected = summary['emotions_detected']
        fragrances_suggested = summary['fragrances_suggested']
        
        if api_calls > 0:
            emotion_detection_rate = (emotions_detected / api_calls * 100)
            fragrance_suggestion_rate = (fragrances_suggested / api_calls * 100)
            
            print(f"🎯 Emotion detection rate: {emotion_detection_rate:.1f}%")
            print(f"🕯️ Fragrance suggestion rate: {fragrance_suggestion_rate:.1f}%")
        
        return health_status
        
    except FileNotFoundError:
        print("❌ Analysis report not found. Run analyze_logs() first.")
        return "UNKNOWN"
    except Exception as e:
        print(f"❌ Error checking system health: {e}")
        return "ERROR"

if __name__ == "__main__":
    # Phân tích logs
    report = analyze_logs()
    
    if report:
        # Kiểm tra sức khỏe hệ thống
        health = get_system_health()
        
        print(f"\n" + "=" * 50)
        print("✅ Log analysis completed!") 