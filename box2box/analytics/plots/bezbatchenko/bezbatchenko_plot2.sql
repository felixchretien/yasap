with tomatoes as (
    select team, season, sum(totalCompensation) as "teamTotalCompensation"
    from box2box.compensation
    group by team, season
)

select s.team, s.season, tomatoes.teamTotalCompensation, firstRound, secondRound, confFinal, mlsCup
from box2box.standings s
left join tomatoes
on s.team = tomatoes.team
and s.season = tomatoes.season