-- Core Analysis Queries (based directly on data/movies.csv)

-- ========================================
-- I. Basic Statistics
-- ========================================

-- 保存名：GenreStats
SELECT
    g.GenreName AS Genre,
    COUNT(m.MovieID) AS MovieCount,
    ROUND(AVG(m.ImdbRating), 2) AS AvgRating,
    ROUND(
        AVG(NZ (m.USGross, 0) + NZ (m.IntlGross, 0)) / 1000000,
        2
    ) AS AvgWorldwideGross_M
FROM
    (
        Genres AS g
        INNER JOIN MovieGenres AS mg ON g.GenreID = mg.GenreID
    )
    INNER JOIN Movies AS m ON mg.MovieID = m.MovieID
GROUP BY
    g.GenreName
ORDER BY
    ROUND(AVG(m.ImdbRating), 2) DESC;

-- Query 2: Yearly movie production, rating and worldwide gross
-- 保存名：YearlyTrends
SELECT 
    m.[Year] AS ReleaseYear,
    COUNT(*) AS MovieCount,
    ROUND(AVG(m.ImdbRating), 2) AS AvgRating,
    ROUND(SUM(NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) AS TotalWorldwideGross_M
FROM Movies AS m
WHERE m.[Year] IS NOT NULL
GROUP BY m.[Year]
ORDER BY m.[Year];

-- Query 3: Movie details (core metrics only; Access SQL does not support STRING_AGG)
-- 保存名：MovieDetails
SELECT 
    m.MovieID,
    m.Title AS Title,
    m.ReleaseDate AS ReleaseDate,
    m.Runtime AS RuntimeHours,
    m.ImdbRating,
    m.Metascore,
    m.USGross,
    m.IntlGross,
    m.Budget,
    (NZ(m.USGross,0) + NZ(m.IntlGross,0)) AS WorldwideGross,
    IIF(m.Budget IS NULL OR m.Budget = 0, NULL,
        (NZ(m.USGross,0) + NZ(m.IntlGross,0)) / m.Budget) AS ROI,
    m.BechdelBinary,
    m.BechdelOrdinal,
    m.MenLines
FROM Movies AS m;

-- ========================================
-- II. Advanced Insights (no DailyBoxOffice / TotalBoxOffice; use us_gross/int_gross/budget)
-- ========================================

-- Query 4: Critically acclaimed but low box office
-- 保存名：CriticallyAcclaimed
SELECT 
    m.Title AS Title,
    m.ReleaseDate AS ReleaseDate,
    ROUND(m.ImdbRating, 2) AS ImdbRating,
    m.Metascore,
    ROUND((NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) AS WorldwideGross_M
FROM Movies AS m
WHERE m.ImdbRating >= 8.5
  AND (NZ(m.USGross,0) + NZ(m.IntlGross,0)) < 100000000
ORDER BY 
    ROUND(m.ImdbRating,2) DESC,
    ROUND((NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) ASC;

-- Query 5: Commercial hits (high box office, moderate rating)
-- 保存名：CommercialHits
SELECT 
    m.Title AS Title,
    m.ReleaseDate AS ReleaseDate,
    ROUND(m.ImdbRating, 2) AS ImdbRating,
    ROUND((NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) AS WorldwideGross_M
FROM Movies AS m
WHERE (NZ(m.USGross,0) + NZ(m.IntlGross,0)) >= 300000000
  AND (m.ImdbRating < 7.0 OR m.ImdbRating IS NULL)
ORDER BY 
    ROUND((NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) DESC;

-- Query 6: Top directors by average worldwide gross
-- 保存名：TopDirectors
SELECT 
    p.Name AS DirectorName,
    COUNT(m.MovieID) AS MovieCount,
    ROUND(AVG(m.ImdbRating), 2) AS AvgRating,
    ROUND(AVG(NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) AS AvgWorldwideGross_M,
    ROUND(SUM(NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) AS TotalWorldwideGross_M
FROM (People AS p
      INNER JOIN MovieDirectors AS md ON p.PersonID = md.PersonID)
      INNER JOIN Movies AS m ON md.MovieID = m.MovieID
GROUP BY p.Name
HAVING COUNT(m.MovieID) >= 2
ORDER BY 
    ROUND(AVG(NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) DESC;

-- Query 7: Top 250 movies by IMDb rating
-- 保存名：Top250Movies
SELECT TOP 250
    m.Title AS Title,
    m.ReleaseDate AS ReleaseDate,
    ROUND(m.ImdbRating, 2) AS ImdbRating,
    m.ImdbVotes,
    ROUND((NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) AS WorldwideGross_M
FROM Movies AS m
WHERE m.ImdbRating IS NOT NULL
ORDER BY m.ImdbRating DESC, m.ImdbVotes DESC;

-- Query 8: Box office champions by genre (using worldwide gross)
-- 保存名：GenreChampions
SELECT
    g.GenreName AS Genre,
    FIRST (m.Title) AS ChampionMovie,
    MAX(NZ (m.USGross, 0) + NZ (m.IntlGross, 0)) / 1000000 AS BoxOffice_M,
    ROUND(FIRST (m.ImdbRating), 2) AS ImdbRating,
    FIRST (m.ReleaseDate) AS ReleaseDate
FROM
    (
        Genres AS g
        INNER JOIN MovieGenres AS mg ON g.GenreID = mg.GenreID
    )
    INNER JOIN Movies AS m ON mg.MovieID = m.MovieID
GROUP BY
    g.GenreName;

-- Query 9: Actor statistics
-- 保存名：ActorStats
SELECT 
    p.Name AS ActorName,
    COUNT(m.MovieID) AS MovieCount,
    ROUND(AVG(m.ImdbRating), 2) AS AvgRating,
    ROUND(SUM(NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) AS TotalWorldwideGross_M
FROM (People AS p
      INNER JOIN MovieActors AS ma ON p.PersonID = ma.PersonID)
      INNER JOIN Movies AS m ON ma.MovieID = m.MovieID
GROUP BY p.Name
HAVING COUNT(m.MovieID) >= 2
ORDER BY 
    ROUND(SUM(NZ(m.USGross,0) + NZ(m.IntlGross,0)) / 1000000, 2) DESC;
