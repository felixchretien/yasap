with chicken as (
    select season, team, sum(baseSalary) as "total"
    from box2box.compensation
    group by team, season
),

tomatoes as (
    select season, team, sum(baseSalary) as "dp_total"
    from box2box.compensation
    where dp = 1
    group by team, season
)

select tomatoes.season,
       tomatoes.team,
       dp_total,
       total,
       round((dp_total/total)*100, 2) as "dp_share"
from tomatoes
left join chicken
on tomatoes.team = chicken.team
and tomatoes.season = chicken.season
;