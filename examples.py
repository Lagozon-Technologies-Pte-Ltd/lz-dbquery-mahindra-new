examples = [
{
    "input": "Show month-on-month growth in total jobs closed for financial year 2024",
    "query": """
        WITH MonthlyJobs AS (
            SELECT
                FORMAT_DATE('%b-%y', DATE_TRUNC(sd.`CLOSD_DATE`, MONTH)) AS `Month`,
                DATE_TRUNC(sd.`CLOSD_DATE`, MONTH) AS _Month_Start,
                ROUND(COUNT(sd.`RO_ID`), 1) AS `Jobs_Closed`
            FROM `prateekproject-450509.vehicle_reporting.sample_data` sd
            WHERE sd.`CLOSD_DATE` BETWEEN DATE('2024-04-01') AND DATE('2025-03-31')
            GROUP BY `Month`, _Month_Start
        )
        SELECT
            `Month`,
            `Jobs_Closed`,
            LAG(`Jobs_Closed`) OVER (ORDER BY _Month_Start) AS `Prev_Jobs_Closed`,
            CASE
                WHEN LAG(`Jobs_Closed`) OVER (ORDER BY _Month_Start) IS NULL OR LAG(`Jobs_Closed`) OVER (ORDER BY _Month_Start) = 0
                    THEN 'None'
                ELSE CONCAT(
                    ROUND(
                        ( (`Jobs_Closed` - LAG(`Jobs_Closed`) OVER (ORDER BY _Month_Start)) /
                          NULLIF(LAG(`Jobs_Closed`) OVER (ORDER BY _Month_Start), 0)
                        ) * 100, 1
                    ), '%'
                )
            END AS `Growth_Percentage`
        FROM MonthlyJobs
        ORDER BY _Month_Start;
    """,
    "contexts": " | ".join([
        "Table: vehicle_reporting.sample_data",
        "Columns: CLOSD_DATE, RO_ID",
        "Description: Shows month-on-month growth in total jobs closed for each month in FY 2024, including growth percentage."
    ])
},
{
    "input": "Show year-on-year growth in average initial parts estimate for July",
    "query": """
        WITH YearlyParts AS (
            SELECT
                EXTRACT(YEAR FROM sd.`RO_DATE`) AS `Year`,
                ROUND(AVG(sd.`INTL_QUTN_PART_AMNT`), 1) AS `Avg_Initial_Parts_Estimate`
            FROM `prateekproject-450509.vehicle_reporting.sample_data` sd
            WHERE EXTRACT(MONTH FROM sd.`RO_DATE`) = 7
            GROUP BY `Year`
        )
        SELECT
            `Year`,
            `Avg_Initial_Parts_Estimate`,
            LAG(`Avg_Initial_Parts_Estimate`) OVER (ORDER BY `Year`) AS `Prev_Year_Avg`,
            CASE
                WHEN LAG(`Avg_Initial_Parts_Estimate`) OVER (ORDER BY `Year`) IS NULL OR LAG(`Avg_Initial_Parts_Estimate`) OVER (ORDER BY `Year`) = 0
                    THEN 'None'
                ELSE CONCAT(
                    ROUND(
                        ( (`Avg_Initial_Parts_Estimate` - LAG(`Avg_Initial_Parts_Estimate`) OVER (ORDER BY `Year`)) /
                          NULLIF(LAG(`Avg_Initial_Parts_Estimate`) OVER (ORDER BY `Year`), 0)
                        ) * 100, 1
                    ), '%'
                )
            END AS `Growth_Percentage`
        FROM YearlyParts
        ORDER BY `Year`;
    """,
    "contexts": " | ".join([
        "Table: vehicle_reporting.sample_data",
        "Columns: RO_DATE, INTL_QUTN_PART_AMNT",
        "Description: Shows year-on-year growth in average initial parts estimate for the month of July."
    ])
},
{
    "input": "Show month-on-month growth in average labor discount percentage for each model in FY 2024",
    "query": """
        WITH ModelMonth AS (
            SELECT
                sd.`MODL_GROP_CD` AS `Model`,
                FORMAT_DATE('%b-%y', DATE_TRUNC(sd.`RO_DATE`, MONTH)) AS `Month`,
                DATE_TRUNC(sd.`RO_DATE`, MONTH) AS _Month_Start,
                ROUND(AVG(sd.`LABR_DISCNT_PERCNTG`), 1) AS `Avg_Labor_Discount_Percentage`
            FROM `prateekproject-450509.vehicle_reporting.sample_data` sd
            WHERE sd.`RO_DATE` BETWEEN DATE('2024-04-01') AND DATE('2025-03-31')
            GROUP BY sd.`MODL_GROP_CD`, `Month`, _Month_Start
        )
        SELECT
            `Model`,
            `Month`,
            `Avg_Labor_Discount_Percentage`,
            LAG(`Avg_Labor_Discount_Percentage`) OVER (PARTITION BY `Model` ORDER BY _Month_Start) AS `Prev_Month_Avg`,
            CASE
                WHEN LAG(`Avg_Labor_Discount_Percentage`) OVER (PARTITION BY `Model` ORDER BY _Month_Start) IS NULL OR LAG(`Avg_Labor_Discount_Percentage`) OVER (PARTITION BY `Model` ORDER BY _Month_Start) = 0
                    THEN 'None'
                ELSE CONCAT(
                    ROUND(
                        ( (`Avg_Labor_Discount_Percentage` - LAG(`Avg_Labor_Discount_Percentage`) OVER (PARTITION BY `Model` ORDER BY _Month_Start)) /
                          NULLIF(LAG(`Avg_Labor_Discount_Percentage`) OVER (PARTITION BY `Model` ORDER BY _Month_Start), 0)
                        ) * 100, 1
                    ), '%'
                )
            END AS `Growth_Percentage`
        FROM ModelMonth
        ORDER BY `Model`, _Month_Start;
    """,
    "contexts": " | ".join([
        "Table: vehicle_reporting.sample_data",
        "Columns: RO_DATE, MODL_GROP_CD, LABR_DISCNT_PERCNTG",
        "Description: Shows month-on-month growth in average labor discount percentage for each vehicle model in FY 2024."
    ])
},
{
    "input": "Show month-on-month growth in total initial quoted amount for all jobs in FY 2024",
    "query": """
        WITH MonthlyQuoted AS (
            SELECT
                FORMAT_DATE('%b-%y', DATE_TRUNC(sd.`RO_DATE`, MONTH)) AS `Month`,
                DATE_TRUNC(sd.`RO_DATE`, MONTH) AS _Month_Start,
                ROUND(SUM(sd.`INTL_QUTN_TOTL_AMNT`), 1) AS `Total_Quoted_Amount`
            FROM `prateekproject-450509.vehicle_reporting.sample_data` sd
            WHERE sd.`RO_DATE` BETWEEN DATE('2024-04-01') AND DATE('2025-03-31')
            GROUP BY `Month`, _Month_Start
        )
        SELECT
            `Month`,
            `Total_Quoted_Amount`,
            LAG(`Total_Quoted_Amount`) OVER (ORDER BY _Month_Start) AS `Prev_Month_Amount`,
            CASE
                WHEN LAG(`Total_Quoted_Amount`) OVER (ORDER BY _Month_Start) IS NULL OR LAG(`Total_Quoted_Amount`) OVER (ORDER BY _Month_Start) = 0
                    THEN 'None'
                ELSE CONCAT(
                    ROUND(
                        ( (`Total_Quoted_Amount` - LAG(`Total_Quoted_Amount`) OVER (ORDER BY _Month_Start)) /
                          NULLIF(LAG(`Total_Quoted_Amount`) OVER (ORDER BY _Month_Start), 0)
                        ) * 100, 1
                    ), '%'
                )
            END AS `Growth_Percentage`
        FROM MonthlyQuoted
        ORDER BY _Month_Start;
    """,
    "contexts": " | ".join([
        "Table: vehicle_reporting.sample_data",
        "Columns: RO_DATE, INTL_QUTN_TOTL_AMNT",
        "Description: Shows month-on-month growth in total initial quoted amount for all jobs in FY 2024."
    ])
}



]



from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings


def get_example_selector():
    """
    Returns a SemanticSimilarityExampleSelector object initialized with the given examples.
    """
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,  # Ensure `examples` is a list of dictionaries
        OpenAIEmbeddings(),
        Chroma,
        k=1,
        input_keys=["input"],  # Ensure that 'input' is a key in the examples
    )

    return example_selector

