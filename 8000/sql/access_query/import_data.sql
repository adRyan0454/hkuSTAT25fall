-- ========================================
-- 1. 从 CSV 建立/刷新“临时导入表”
--
--   1.1 MoviesStage 对应 movies_clean.csv
--   1.2 PeopleLinksStage 对应 raw_people_links.csv
--
-- ========================================
-- 2. 维度表：Studios
--
--   从 MoviesStage 中抽取去重后的 studio 名称
-- ========================================

INSERT INTO Studios (StudioName)
SELECT DISTINCT
    s.studio AS StudioName
FROM MoviesStage AS s
WHERE
    s.studio IS NOT NULL
    AND s.studio <> ""
    -- 排除明显不是公司名的“纯数字 / 纯数字+小数点”的脏值
    AND NOT (s.studio Like "#*" AND s.studio Not Like "*[A-Za-z]*")
    -- 排除被错读成 studio 的 IMDb id
    AND s.studio Not Like "tt#######"
    -- 排除明显是语言/国家的值
    AND UCase(s.studio) Not In ("ENGLISH", "USA");


-- ========================================
-- 3. 主表：Movies
--
--   说明：
--     - 用 Title + Year 与后续关系表对齐（raw_people_links 也是这两个字段作键）
--     - StudioID 通过 Studios 维表查找
--     - BechdelBinary 在 CSV 中是 True/False 字符串，Access 会自动转为 Yes/No
-- ========================================

INSERT INTO Movies (
    Title,
    [Year],
    ReleaseDate,
    Runtime,
    Genre5,
    GenreDetailed,
    Rated,
    [Language],
    Country,
    Metascore,
    ImdbRating,
    ImdbVotes,
    ImdbID,
    StudioID,
    BechdelBinary,
    BechdelOrdinal,
    USGross,
    IntlGross,
    Budget,
    MenLines,
    LinesData
)
SELECT
    s.title,
    s.year,
    CDate(s.release_date) AS ReleaseDate,
    s.runtime,
    s.genre5,
    s.genre_detailed,
    s.rated,
    s.[language],
    s.country,
    s.metascore,
    s.imdb_rating,
    s.imdb_votes,
    s.imdb_id,
    d.StudioID,
    s.bechdel_binary,
    s.bechdel_ordinal,
    s.us_gross,
    s.int_gross,
    s.budget,
    s.men_lines,
    s.lines_data
FROM
    MoviesStage AS s
    LEFT JOIN Studios AS d
        ON s.studio = d.StudioName;


-- ========================================
-- 4. 维度表：Genres 以及关系表 MovieGenres
--
--   现在直接基于 Movies 表中的 Genre5 字段来重建：
--     - Genres.GenreName     <- Movies.Genre5 去重
--     - MovieGenres(MovieID, GenreID)
-- ========================================

-- 4.0 可选：先清空旧的类型与关系数据（按需注释）
DELETE FROM MovieGenres;
DELETE FROM Genres;

-- 4.1 Genres：按 Movies.Genre5 去重
INSERT INTO Genres (GenreName)
SELECT DISTINCT
    m.Genre5 AS GenreName
FROM Movies AS m
WHERE m.Genre5 IS NOT NULL AND m.Genre5 <> "";


-- 4.2 MovieGenres：直接用 Movies.MovieID 回连 Genres
INSERT INTO MovieGenres (MovieID, GenreID)
SELECT
    m.MovieID,
    g.GenreID
FROM Movies AS m
INNER JOIN Genres AS g
    ON g.GenreName = m.Genre5
WHERE m.Genre5 IS NOT NULL AND m.Genre5 <> "";


-- ========================================
-- 5. 维度表：People
--
--   从 PeopleLinksStage 中抽取所有 person_name 去重
-- ========================================

INSERT INTO People (Name)
SELECT DISTINCT
    l.person_name AS Name
FROM PeopleLinksStage AS l
WHERE l.person_name IS NOT NULL AND l.person_name <> "";


-- ========================================
-- 6. 关系表：MovieDirectors / MovieWriters / MovieActors
--
--   逻辑：
--     - 用 (title, year) 从 PeopleLinksStage 连接到 Movies
--     - 用 person_name 从 PeopleLinksStage 连接到 People
--     - 按 role_type 分别写入三个关系表
-- ========================================

-- 6.1 导演关系：MovieDirectors
INSERT INTO MovieDirectors (MovieID, PersonID)
SELECT DISTINCT
    m.MovieID,
    p.PersonID
FROM
    (PeopleLinksStage AS l
        INNER JOIN Movies AS m
            ON m.Title = l.title
           AND m.[Year] = l.year)
    INNER JOIN People AS p
        ON p.Name = l.person_name
WHERE
    l.role_type = "Director";


-- 6.2 编剧关系：MovieWriters
INSERT INTO MovieWriters (MovieID, PersonID)
SELECT DISTINCT
    m.MovieID,
    p.PersonID
FROM
    (PeopleLinksStage AS l
        INNER JOIN Movies AS m
            ON m.Title = l.title
           AND m.[Year] = l.year)
    INNER JOIN People AS p
        ON p.Name = l.person_name
WHERE
    l.role_type = "Writer";


-- 6.3 演员关系：MovieActors
INSERT INTO MovieActors (MovieID, PersonID)
SELECT DISTINCT
    m.MovieID,
    p.PersonID
FROM
    (PeopleLinksStage AS l
        INNER JOIN Movies AS m
            ON m.Title = l.title
           AND m.[Year] = l.year)
    INNER JOIN People AS p
        ON p.Name = l.person_name
WHERE
    l.role_type = "Actor";


-- ========================================
-- 7. 可选：清理临时表（如果不再需要）
-- ========================================

-- DROP TABLE MoviesStage;
-- DROP TABLE PeopleLinksStage;
