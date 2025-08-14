#!/usr/bin/env python3
"""
SRTA Performance Benchmark Runner
SRTA アーキテクチャ性能ベンチマーク実行システム

Purpose: 継続的性能測定・CI統合・論文用定量データ
Author: ubunturbo (Baptist Pastor & AI Researcher)
License: MIT
"""

import time
import psutil
import json
import csv
import statistics
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import memory_profiler
import cProfile
import pstats
import io

@dataclass
class BenchmarkConfig:
    """ベンチマーク設定"""
    name: str
    description: str
    iterations: int
    warmup_iterations: int
    target_function: str
    parameters: Dict[str, Any]
    timeout_seconds: int
    memory_profiling: bool
    cpu_profiling: bool

@dataclass
class BenchmarkResult:
    """ベンチマーク結果"""
    config_name: str
    avg_execution_time_ms: float
    min_execution_time_ms: float
    max_execution_time_ms: float
    std_execution_time_ms: float
    avg_memory_usage_mb: float
    peak_memory_usage_mb: float
    cpu_usage_percent: float
    throughput_ops_per_sec: float
    success_rate: float
    error_count: int
    timestamp: str
    profiling_data: Optional[Dict[str, Any]] = None

class PerformanceMonitor:
    """リアルタイム性能監視"""
    
    def __init__(self):
        self.monitoring = False
        self.metrics = []
        self.start_time = None
        
    def start_monitoring(self):
        """監視開始"""
        self.monitoring = True
        self.start_time = time.time()
        self.metrics = []
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """監視停止"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
        
    def _monitor_loop(self):
        """監視ループ"""
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory_info = psutil.virtual_memory()
                process = psutil.Process()
                process_memory = process.memory_info().rss / 1024 / 1024  # MB
                
                metric = {
                    'timestamp': time.time() - self.start_time,
                    'cpu_percent': cpu_percent,
                    'memory_usage_mb': process_memory,
                    'system_memory_percent': memory_info.percent
                }
                self.metrics.append(metric)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
            
            time.sleep(0.1)  # 100ms interval
    
    def get_summary(self) -> Dict[str, float]:
        """監視サマリー取得"""
        if not self.metrics:
            return {}
        
        cpu_values = [m['cpu_percent'] for m in self.metrics]
        memory_values = [m['memory_usage_mb'] for m in self.metrics]
        
        return {
            'avg_cpu_percent': statistics.mean(cpu_values),
            'max_cpu_percent': max(cpu_values),
            'avg_memory_mb': statistics.mean(memory_values),
            'peak_memory_mb': max(memory_values),
            'monitoring_duration': self.metrics[-1]['timestamp'] if self.metrics else 0
        }

class SRTABenchmarkRunner:
    """SRTA ベンチマーク実行システム"""
    
    def __init__(self, output_dir: str = "benchmarks/results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # ベンチマーク設定群
        self.benchmark_configs = self._create_benchmark_configs()
        
        # 結果保存
        self.results: List[BenchmarkResult] = []
        
        # 性能監視
        self.monitor = PerformanceMonitor()
        
    def _create_benchmark_configs(self) -> List[BenchmarkConfig]:
        """ベンチマーク設定群作成"""
        configs = []
        
        # 基本性能ベンチマーク
        configs.append(BenchmarkConfig(
            name="trace_engine_basic",
            description="Basic trace engine performance",
            iterations=100,
            warmup_iterations=10,
            target_function="benchmark_trace_engine",
            parameters={"depth": 5, "nodes": 100},
            timeout_seconds=30,
            memory_profiling=True,
            cpu_profiling=True
        ))
        
        # 意味解析ベンチマーク
        configs.append(BenchmarkConfig(
            name="semantic_analysis_performance",
            description="Semantic analysis performance under load",
            iterations=50,
            warmup_iterations=5,
            target_function="benchmark_semantic_analysis",
            parameters={"text_length": 1000, "complexity": "medium"},
            timeout_seconds=60,
            memory_profiling=True,
            cpu_profiling=False
        ))
        
        # 責任追跡ベンチマーク
        configs.append(BenchmarkConfig(
            name="responsibility_tracking_scale",
            description="Responsibility tracking scalability",
            iterations=200,
            warmup_iterations=20,
            target_function="benchmark_responsibility_tracking",
            parameters={"entities": 500, "relationships": 1000},
            timeout_seconds=120,
            memory_profiling=True,
            cpu_profiling=True
        ))
        
        # 統合システムベンチマーク
        configs.append(BenchmarkConfig(
            name="integrated_system_stress",
            description="Full SRTA system under stress",
            iterations=30,
            warmup_iterations=3,
            target_function="benchmark_integrated_system",
            parameters={"concurrent_requests": 10, "data_size": "large"},
            timeout_seconds=300,
            memory_profiling=True,
            cpu_profiling=True
        ))
        
        return configs
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """全ベンチマーク実行"""
        print("🏃‍♂️ Starting SRTA Performance Benchmarks")
        print("=" * 50)
        
        benchmark_summary = {
            "start_time": datetime.now().isoformat(),
            "benchmarks": [],
            "overall_performance": {},
            "success_count": 0,
            "failure_count": 0
        }
        
        for config in self.benchmark_configs:
            try:
                print(f"\n🔧 Running benchmark: {config.name}")
                print(f"   Description: {config.description}")
                print(f"   Iterations: {config.iterations}")
                
                result = self.run_single_benchmark(config)
                
                if result:
                    self.results.append(result)
                    benchmark_summary["benchmarks"].append({
                        "name": config.name,
                        "status": "success",
                        "avg_time_ms": result.avg_execution_time_ms,
                        "throughput": result.throughput_ops_per_sec,
                        "memory_mb": result.avg_memory_usage_mb
                    })
                    benchmark_summary["success_count"] += 1
                    
                    # 結果表示
                    print(f"   ✅ Avg Time: {result.avg_execution_time_ms:.2f}ms")
                    print(f"   ⚡ Throughput: {result.throughput_ops_per_sec:.1f} ops/sec")
                    print(f"   💾 Memory: {result.avg_memory_usage_mb:.1f}MB")
                    
                else:
                    benchmark_summary["benchmarks"].append({
                        "name": config.name,
                        "status": "failed"
                    })
                    benchmark_summary["failure_count"] += 1
                    print(f"   ❌ Failed")
                    
            except Exception as e:
                print(f"   💥 Error: {str(e)}")
                benchmark_summary["benchmarks"].append({
                    "name": config.name,
                    "status": "error",
                    "error": str(e)
                })
                benchmark_summary["failure_count"] += 1
        
        # 包括的性能サマリー
        benchmark_summary["overall_performance"] = self._calculate_overall_performance()
        benchmark_summary["end_time"] = datetime.now().isoformat()
        
        # 結果保存
        self.save_benchmark_results(benchmark_summary)
        
        # 最終レポート
        print(f"\n📊 Benchmark Summary:")
        print(f"   Total: {len(self.benchmark_configs)}")
        print(f"   Success: {benchmark_summary['success_count']}")
        print(f"   Failed: {benchmark_summary['failure_count']}")
        print(f"   Results: {self.output_dir}")
        
        return benchmark_summary
    
    def run_single_benchmark(self, config: BenchmarkConfig) -> Optional[BenchmarkResult]:
        """単一ベンチマーク実行"""
        
        execution_times = []
        memory_usages = []
        error_count = 0
        profiling_data = {}
        
        # ウォームアップ
        for _ in range(config.warmup_iterations):
            try:
                self._execute_benchmark_function(config.target_function, config.parameters)
            except:
                pass  # ウォームアップエラーは無視
        
        # メイン測定
        self.monitor.start_monitoring()
        
        # CPUプロファイリング開始
        if config.cpu_profiling:
            profiler = cProfile.Profile()
            profiler.enable()
        
        for i in range(config.iterations):
            try:
                # メモリプロファイリング
                if config.memory_profiling:
                    start_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                # 実行時間測定
                start_time = time.perf_counter()
                
                # ベンチマーク関数実行
                self._execute_benchmark_function(config.target_function, config.parameters)
                
                end_time = time.perf_counter()
                execution_time = (end_time - start_time) * 1000  # ms
                execution_times.append(execution_time)
                
                # メモリ使用量記録
                if config.memory_profiling:
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                    memory_usages.append(end_memory)
                
            except Exception as e:
                error_count += 1
                print(f"   Iteration {i+1} error: {str(e)}")
        
        # CPUプロファイリング終了
        if config.cpu_profiling:
            profiler.disable()
            s = io.StringIO()
            ps = pstats.Stats(profiler, stream=s)
            ps.sort_stats('cumulative')
            ps.print_stats(10)  # トップ10関数
            profiling_data['cpu_profile'] = s.getvalue()
        
        self.monitor.stop_monitoring()
        monitor_summary = self.monitor.get_summary()
        
        # 結果統計計算
        if not execution_times:
            return None
        
        avg_execution_time = statistics.mean(execution_times)
        min_execution_time = min(execution_times)
        max_execution_time = max(execution_times)
        std_execution_time = statistics.stdev(execution_times) if len(execution_times) > 1 else 0
        
        avg_memory = statistics.mean(memory_usages) if memory_usages else monitor_summary.get('avg_memory_mb', 0)
        peak_memory = max(memory_usages) if memory_usages else monitor_summary.get('peak_memory_mb', 0)
        
        throughput = 1000 / avg_execution_time if avg_execution_time > 0 else 0  # ops/sec
        success_rate = (config.iterations - error_count) / config.iterations
        
        # プロファイリングデータ追加
        if monitor_summary:
            profiling_data.update(monitor_summary)
        
        result = BenchmarkResult(
            config_name=config.name,
            avg_execution_time_ms=avg_execution_time,
            min_execution_time_ms=min_execution_time,
            max_execution_time_ms=max_execution_time,
            std_execution_time_ms=std_execution_time,
            avg_memory_usage_mb=avg_memory,
            peak_memory_usage_mb=peak_memory,
            cpu_usage_percent=monitor_summary.get('avg_cpu_percent', 0),
            throughput_ops_per_sec=throughput,
            success_rate=success_rate,
            error_count=error_count,
            timestamp=datetime.now().isoformat(),
            profiling_data=profiling_data
        )
        
        return result
    
    def _execute_benchmark_function(self, function_name: str, parameters: Dict[str, Any]):
        """ベンチマーク関数実行（Phase 2で実際のSRTA関数に置き換え）"""
        
        # 現在は模擬実行（実際のSRTA実装と接続後に置き換え）
        if function_name == "benchmark_trace_engine":
            # 模擬的なトレースエンジン処理
            depth = parameters.get("depth", 5)
            nodes = parameters.get("nodes", 100)
            # 計算集約的タスクの模擬
            result = sum(i * j for i in range(depth) for j in range(nodes // depth))
            
        elif function_name == "benchmark_semantic_analysis":
            # 模擬的な意味解析処理
            text_length = parameters.get("text_length", 1000)
            complexity = parameters.get("complexity", "medium")
            # 文字列処理の模擬
            text = "a" * text_length
            result = len(text.split()) * (2 if complexity == "high" else 1)
            
        elif function_name == "benchmark_responsibility_tracking":
            # 模擬的な責任追跡処理
            entities = parameters.get("entities", 500)
            relationships = parameters.get("relationships", 1000)
            # グラフ処理の模擬
            result = entities * relationships // 100
            
        elif function_name == "benchmark_integrated_system":
            # 模擬的な統合システム処理
            requests = parameters.get("concurrent_requests", 10)
            data_size = parameters.get("data_size", "medium")
            # 複合処理の模擬
            size_multiplier = {"small": 1, "medium": 10, "large": 100}.get(data_size, 10)
            result = requests * size_multiplier * 42
            
        else:
            raise ValueError(f"Unknown benchmark function: {function_name}")
        
        # 実際の処理時間を模擬するための小さな遅延
        time.sleep(0.001)  # 1ms
        
        return result
    
    def _calculate_overall_performance(self) -> Dict[str, float]:
        """包括的性能指標計算"""
        if not self.results:
            return {}
        
        all_times = [r.avg_execution_time_ms for r in self.results]
        all_memory = [r.avg_memory_usage_mb for r in self.results]
        all_throughput = [r.throughput_ops_per_sec for r in self.results]
        all_success_rates = [r.success_rate for r in self.results]
        
        return {
            "avg_response_time_ms": statistics.mean(all_times),
            "total_throughput_ops_per_sec": sum(all_throughput),
            "avg_memory_efficiency_mb": statistics.mean(all_memory),
            "overall_success_rate": statistics.mean(all_success_rates),
            "performance_stability": 1.0 - (statistics.stdev(all_times) / statistics.mean(all_times)) if len(all_times) > 1 else 1.0
        }
    
    def save_benchmark_results(self, summary: Dict[str, Any]):
        """ベンチマーク結果保存"""
        
        # 1. サマリー保存
        summary_file = self.output_dir / f"benchmark_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # 2. CSV形式（論文用）
        if self.results:
            csv_file = self.output_dir / "benchmark_results.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                # プロファイリングデータ除外（CSV用）
                results_dict = []
                for result in self.results:
                    result_dict = asdict(result)
                    result_dict.pop('profiling_data', None)
                    results_dict.append(result_dict)
                
                if results_dict:
                    writer = csv.DictWriter(f, fieldnames=results_dict[0].keys())
                    writer.writeheader()
                    writer.writerows(results_dict)
        
        # 3. 人間読み易いレポート
        self.generate_performance_report(summary)
        
        print(f"📄 Benchmark results saved to {self.output_dir}")
    
    def generate_performance_report(self, summary: Dict[str, Any]):
        """性能レポート生成"""
        report_file = self.output_dir / "performance_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# SRTA Performance Benchmark Report\n\n")
            f.write(f"**実行日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")
            
            # 全体サマリー
            f.write("## Executive Summary\n\n")
            overall = summary.get("overall_performance", {})
            f.write(f"- **平均レスポンス時間**: {overall.get('avg_response_time_ms', 0):.2f}ms\n")
            f.write(f"- **総スループット**: {overall.get('total_throughput_ops_per_sec', 0):.1f} ops/sec\n")
            f.write(f"- **メモリ効率**: {overall.get('avg_memory_efficiency_mb', 0):.1f}MB\n")
            f.write(f"- **成功率**: {overall.get('overall_success_rate', 0):.1%}\n")
            f.write(f"- **性能安定性**: {overall.get('performance_stability', 0):.3f}\n\n")
            
            # 個別ベンチマーク結果
            f.write("## Individual Benchmark Results\n\n")
            for benchmark in summary.get("benchmarks", []):
                if benchmark.get("status") == "success":
                    f.write(f"### {benchmark['name']}\n\n")
                    f.write(f"- **平均実行時間**: {benchmark.get('avg_time_ms', 0):.2f}ms\n")
                    f.write(f"- **スループット**: {benchmark.get('throughput', 0):.1f} ops/sec\n")
                    f.write(f"- **メモリ使用量**: {benchmark.get('memory_mb', 0):.1f}MB\n\n")
            
            f.write("## CI/CD Integration\n\n")
            f.write("このベンチマーク結果は継続的インテグレーションで自動実行され、\n")
            f.write("性能退化の早期検出とIEEE論文用データ収集に活用されます。\n")

def main():
    """メイン実行関数"""
    print("🚀 SRTA Benchmark Runner")
    print("Performance measurement for IEEE paper submission")
    print("=" * 55)
    
    runner = SRTABenchmarkRunner()
    
    try:
        summary = runner.run_all_benchmarks()
        
        print("\n🏆 Benchmark completed successfully!")
        print("📊 Ready for continuous performance monitoring!")
        return 0
        
    except Exception as e:
        print(f"❌ Benchmark execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())