"""TICKET 1 — cost arithmetic, checked against hand-computed values."""

import pytest

from triage import pricing


def test_opus_55_matches_hand_computed():
    # 1,000,000 input @ $4.00/MTok = $4.00 ; 10,000 output @ $20.00/MTok = $0.20
    assert pricing.cost_usd("claude-opus-5-5", 1_000_000, 10_000) == pytest.approx(4.20)


def test_sonnet_matches_hand_computed():
    # 500,000 @ $2.00 = $1.00 ; 20,000 @ $10.00 = $0.20
    assert pricing.cost_usd("claude-sonnet-5", 500_000, 20_000) == pytest.approx(1.20)


def test_haiku_matches_hand_computed():
    # 100,000 @ $1.00 = $0.10 ; 2,000 @ $5.00 = $0.01
    assert pricing.cost_usd("claude-haiku-4-5", 100_000, 2_000) == pytest.approx(0.11)


def test_zero_tokens_costs_nothing():
    assert pricing.cost_usd("claude-opus-5", 0, 0) == 0.0


def test_unknown_model_raises_rather_than_guessing():
    # A typo must not silently price as some other model.
    with pytest.raises(KeyError):
        pricing.cost_usd("claude-opus-5-5-20260922", 100, 100)


def test_rate_table_records_when_it_was_taken():
    # A rate table with no date is one nobody can tell is stale.
    assert pricing.RATES_TAKEN_ON


def test_cost_of_response_reads_usage_off_the_object():
    class Usage:
        input_tokens = 1_000_000
        output_tokens = 10_000

    assert pricing.cost_of_response("claude-opus-5-5", Usage()) == pytest.approx(4.20)
