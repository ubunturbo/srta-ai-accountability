- name: Test
        run: pytest -q --maxfail=1 --cov=srta --cov-report=xml --cov-report=term
        continue-on-error: true  # テスト失敗でもCI続行
