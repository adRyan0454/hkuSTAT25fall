-- ========================================
-- 1. 创建维度表
-- ========================================

-- 1.1 类型表 Genres（来自 movies.csv 中的 genre5 / genre_detailed）
CREATE TABLE Genres (
    GenreID AUTOINCREMENT PRIMARY KEY,
    GenreName TEXT(50) NOT NULL CONSTRAINT UQ_GenreName UNIQUE
);

-- 1.2 人员表 People（导演 / 编剧 / 演员公共表）
CREATE TABLE People (
    PersonID AUTOINCREMENT PRIMARY KEY,
    Name TEXT(255) NOT NULL
);

-- ========================================
-- 2. 创建主表
-- ========================================

-- 2.1 电影表 Movies（基于 data/movies.csv 的字段重建）
CREATE TABLE Movies (
    MovieID AUTOINCREMENT PRIMARY KEY,
    Title TEXT(255) NOT NULL,
    [Year] INTEGER,
    ReleaseDate DATETIME,
    Runtime DOUBLE,
    Genre5 TEXT(50),
    GenreDetailed TEXT(255),
    Rated TEXT(10),
    Language TEXT(100),
    Country TEXT(100),
    Metascore DOUBLE,
    ImdbRating DOUBLE,
    ImdbVotes LONG,
    ImdbID TEXT(20),
    BechdelBinary YESNO,
    BechdelOrdinal TEXT(20),
    USGross CURRENCY,
    IntlGross CURRENCY,
    Budget CURRENCY,
    MenLines DOUBLE,
    LinesData LONGTEXT 
);

-- ========================================
-- 3. 创建关系表（多对多）
-- ========================================

-- 3.1 电影-类型关联表 MovieGenres
CREATE TABLE MovieGenres (
    MovieID INTEGER NOT NULL,
    GenreID INTEGER NOT NULL,
    PRIMARY KEY (MovieID, GenreID)
);

-- 3.2 电影-导演关联表 MovieDirectors
CREATE TABLE MovieDirectors (
    MovieID INTEGER NOT NULL,
    PersonID INTEGER NOT NULL,
    PRIMARY KEY (MovieID, PersonID)
);

-- 3.3 电影-编剧关联表 MovieWriters（可选，用于 writer 字段拆分）
CREATE TABLE MovieWriters (
    MovieID INTEGER NOT NULL,
    PersonID INTEGER NOT NULL,
    PRIMARY KEY (MovieID, PersonID)
);

-- 3.4 电影-演员关联表 MovieActors
CREATE TABLE MovieActors (
    MovieID INTEGER NOT NULL,
    PersonID INTEGER NOT NULL,
    PRIMARY KEY (MovieID, PersonID)
);