-- PostgreSQL syntax.

-- Block 3, task 1: applicant position in the overall rating.
-- Applicants with equal scores share a rank; the next position is skipped.
-- The task does not define tie handling. Use DENSE_RANK() instead if ranks
-- after ties must not have gaps.
SELECT
    id,
    scores,
    RANK() OVER (ORDER BY scores DESC NULLS LAST) AS rating_position
FROM examination
ORDER BY rating_position, id;


-- Block 3, task 3: clients whose purchase total over the rolling last month
-- is below 5,000 rubles across all accounts.
-- Assumptions:
--   * the real purchase code is not provided; 'PUR' is a placeholder example
--     that must be replaced with the production operation code;
--   * "made purchases" means at least one purchase in the period;
--   * "last month" means [CURRENT_DATE - 1 month, CURRENT_DATE].
SELECT
    a.client_id
FROM account AS a
JOIN "transaction" AS t
    ON t.account_id = a.id
WHERE t.type = 'PUR'
  AND t.transaction_date >= CURRENT_DATE - INTERVAL '1 month'
  AND t.transaction_date <= CURRENT_DATE
GROUP BY a.client_id
HAVING SUM(t.amount) < 5000
ORDER BY a.client_id;

-- If clients with zero purchases must also be included, use LEFT JOIN,
-- move the transaction filters into ON, and use:
-- HAVING COALESCE(SUM(t.amount), 0) < 5000
