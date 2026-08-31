"""
test_trade_setup_full_pipeline.py

End-to-end integration test for Trade Setup
inside the complete AndyScanner pipeline.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_factory import PipelineFactory


def test_full_pipeline_trade_setup():

    pipeline = PipelineFactory.create()

    result = pipeline.run(
        "EURUSD",
        "M5",
    )

    print("=== FULL TRADE SETUP PIPELINE TEST ===")

    assert result.success is True, (
        f"Pipeline failed: {result.error}"
    )

    scan_result = result.metadata.get(
        "scan_result"
    )

    assert scan_result is not None, (
        "ScannerResult was not created."
    )

    assert scan_result.trade_setup is not None, (
        "TradeSetup was not passed into ScannerResult."
    )

    setup = scan_result.trade_setup

    print("Market:", setup.market)
    print("Timeframe:", setup.timeframe)
    print("Direction:", setup.direction)
    print("Entry:", setup.entry)
    print("Stop Loss:", setup.stop_loss)
    print("Take Profit:", setup.take_profit)
    print("Risk/Reward:", setup.risk_reward)
    print("Valid:", setup.valid)

    assert setup.market == "EURUSD"
    assert setup.timeframe == "M5"

    assert setup.direction in (
        "BUY",
        "STRONG BUY",
        "SELL",
        "STRONG SELL",
        "WAIT",
    )

    if setup.direction == "WAIT":

        assert setup.valid is False

    print()
    print(
        "PASS: Full Trade Setup pipeline integration verified."
    )


if __name__ == "__main__":

    try:

        test_full_pipeline_trade_setup()

    except AssertionError as error:

        print("FAIL: test_full_pipeline_trade_setup")
        print("     ", error)
        raise SystemExit(1)

    except Exception as error:

        print("FAIL: test_full_pipeline_trade_setup")
        print(
            f"      {type(error).__name__}: {error}"
        )
        raise SystemExit(1)
