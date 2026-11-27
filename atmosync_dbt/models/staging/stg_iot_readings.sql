
WITH source_data AS (

    SELECT
        RAW_PAYLOAD
    FROM {{ source('atmosync_raw', 'raw_events') }}

),

renamed AS (

    SELECT
        RAW_PAYLOAD:container_id::VARCHAR AS container_id,
        RAW_PAYLOAD:commodity::VARCHAR AS commodity,
        TRY_TO_TIMESTAMP_NTZ(
            RAW_PAYLOAD:timestamp::VARCHAR
        ) AS reading_timestamp,
        RAW_PAYLOAD:temperature::FLOAT AS temperature,
        RAW_PAYLOAD:humidity::FLOAT AS humidity,
        RAW_PAYLOAD:vibration::FLOAT AS vibration,
        RAW_PAYLOAD:lat::FLOAT AS latitude,
        RAW_PAYLOAD:lon::FLOAT AS longitude,
        CURRENT_TIMESTAMP() AS transformed_at

    FROM source_data

)

SELECT *
FROM renamed
WHERE
    container_id IS NOT NULL
    AND commodity IS NOT NULL
    AND reading_timestamp IS NOT NULL
    AND temperature IS NOT NULL
    AND humidity IS NOT NULL
