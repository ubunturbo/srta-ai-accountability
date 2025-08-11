import time

def test_module_imports():
    import srta  # noqa: F401

def test_basic_flow_smoke():
    # 例: SRTAArchitecture が存在する前提。名前が違う場合は調整してください
    from srta import SRTAArchitecture  # type: ignore
    srta = SRTAArchitecture()
    assert hasattr(srta, "add_design_principle")

def test_latency_relaxed_threshold():
    from srta import SRTAArchitecture  # type: ignore
    srta = SRTAArchitecture()
    sample = {"credit_score": 720, "income": 75000}
    # ウォームアップ
    if hasattr(srta, "process_and_explain"):
        srta.process_and_explain(sample)
        t0 = time.perf_counter()
        srta.process_and_explain(sample)
        dt_ms = (time.perf_counter() - t0) * 1000
        assert dt_ms < 1000, f"took {dt_ms:.1f}ms"
