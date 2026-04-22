CREATE OR REFRESH streaming table `02_silver`.fact_reviews
(
  CONSTRAINT valid_sentiment EXPECT (sentiment in ('positive', 'neutral','negative')) on violation drop row,
  CONSTRAINT valid_rating EXPECT (rating >= 0) on violation drop row
)
AS
with sentiment_analysis as (
select 
  *,
  ai_query(
    'databricks-gpt-oss-20b',
    CONCAT(
        'Analyze the following review and return ONLY a valid JSON object with this exact structure: ',
        '{"sentiment": "<positive/neutral/negative>", ',
        '"issue_delivery": <true/false>, ',
        '"issue_delivery_reason": "<reason or empty string>", ',
        '"issue_food_quality": <true/false>, ',
        '"issue_food_quality_reason": "<reason or empty string>", ',
        '"issue_pricing": <true/false>, ',
        '"issue_pricing_reason": "<reason or empty string>", ',
        '"issue_portion_size": <true/false>, ',
        '"issue_portion_size_reason": "<reason or empty string>"}. ',
        'Rules: sentiment must be exactly one of: positive, neutral, negative. ',
        'Each issue field is true/false only. ',
        'Each reason field should contain a brief explanation if the issue is true, otherwise empty string. ',
        'Review text: ', review_text
      )
  ) as analysis
from stream(dbx_az_projects.`01_bronze`.reviews) )
select 
  review_id,
  order_id,
  customer_id,
  restaurant_id,
  review_timestamp,
  rating,
  review_text,
  analysis,
  get_json_object(analysis, '$.sentiment') as sentiment,
  get_json_object(analysis, '$.issue_delivery') as issue_delivery,
  get_json_object(analysis, '$.issue_delivery_reason') as issue_delivery_reason,
  get_json_object(analysis, '$.issue_food_quality') as issue_food_quality,
  get_json_object(analysis, '$.issue_food_quality_reason') as issue_food_quality_reason,
  get_json_object(analysis, '$.issue_pricing') as issue_pricing,
  get_json_object(analysis, '$.issue_pricing_reason') as issue_pricing_reason,
  get_json_object(analysis, '$.issue_portion_size') as issue_portion_size,
  get_json_object(analysis, '$.issue_portion_size_reason') as issue_portion_size_reason
from sentiment_analysis
;
