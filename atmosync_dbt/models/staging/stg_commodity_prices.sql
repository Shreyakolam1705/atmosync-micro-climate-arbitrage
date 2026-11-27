WITH source_data AS (

    SELECT
        RAW_PAYLOAD
    FROM {{ source('atmosync_raw', 'raw_commodity_prices') }}

),

renamed AS (

    SELECT
        RAW_PAYLOAD:commodity::VARCHAR AS commodity,
        RAW_PAYLOAD:timestamp::TIMESTAMP_NTZ AS price_timestamp,
        RAW_PAYLOAD:origin_price::FLOAT AS origin_price,
        RAW_PAYLOAD:secondary_market_price::FLOAT AS secondary_market_price,
        RAW_PAYLOAD:distance_to_market_km::FLOAT AS distance_to_market_km,
        RAW_PAYLOAD:currency::VARCHAR AS currency,
        RAW_PAYLOAD:price_unit::VARCHAR AS price_unit,
        CURRENT_TIMESTAMP() AS transformed_at

    FROM source_data

)

SELECT * FROM renamed