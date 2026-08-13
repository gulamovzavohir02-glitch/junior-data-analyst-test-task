-- PostgreSQL syntax.

-- Block 3, task 1: applicant position in the overall rating.
-- Applicants with equal scores share a rank; the next position is skipped.
SELECT
    id,
    scores,
    RANK() OVER (ORDER BY scores DESC) AS rating_position
FROM examination
ORDER BY rating_position, id;


-- Block 3, task 3: clients whose purchase total over the rolling last month
-- is below 5,000 rubles across all accounts.
-- Assumptions:
--   * 'PUR' is the code for a purchase;
--   * clients with zero purchases in the period must be included;
--   * "last month" means [CURRENT_DATE - 1 month, CURRENT_DATE].
SELECT
    a.client_id
FROM account AS a
LEFT JOIN "transaction" AS t
    ON t.account_id = a.id
    AND t.type = 'PUR'
    AND t.transaction_date >= CURRENT_DATE - INTERVAL '1 month'
    AND t.transaction_date <= CURRENT_DATE
GROUP BY a.client_id
HAVING COALESCE(SUM(t.amount), 0) < 5000
ORDER BY a.client_id;

-- If "made purchases" must exclude clients with zero purchases, add:
-- AND COUNT(t.id) > 0
-- to the HAVING clause.
