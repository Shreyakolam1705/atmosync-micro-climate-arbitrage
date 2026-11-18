
import json
import random
from datetime import datetime, timezone
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
OUTPUT_FILE = BASE_DIR.parent / "data" / "generated" / "commodity_prices.jsonl"


def load_commodities():
    """Read unique commodity names from simulator config."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = json.load(file)

    containers = config.get("containers", [])

    if not containers:
        raise ValueError("No containers found in config.json")

    commodities = sorted({
        container["commodity"].strip().lower()
        for container in containers
        if container.get("commodity")
    })

    if not commodities:
        raise ValueError("No valid commodities found in config.json")

    return commodities


def generate_price(commodity):
    """Generate mock pricing data for one commodity."""

    origin_price = round(random.uniform(100, 300), 2)

    # Secondary market price is randomly 10% to 50% higher.
    secondary_market_price = round(
        origin_price * random.uniform(1.10, 1.50), 2
    )

    distance_to_market = round(random.uniform(50, 500), 2)

    return {
        "commodity": commodity,
        "timestamp": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ).replace("+00:00", "Z"),
        "origin_price": origin_price,
        "secondary_market_price": secondary_market_price,
        "distance_to_market_km": distance_to_market,
        "currency": "INR",
        "price_unit": "per_kg"
    }


def main():
    commodities = load_commodities()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    readings = [
        generate_price(commodity)
        for commodity in commodities
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for reading in readings:
            file.write(json.dumps(reading) + "\n")

    print("AtmoSync Mock Commodity Pricing Generator")
    print("-" * 45)

    for reading in readings:
        print(json.dumps(reading, indent=4))
        print("-" * 45)

    print(f"Generated pricing data for {len(readings)} commodity/commodities.")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
