with chicken as (
    select season, team, sum(totalCompensation) as 'totalCompensation'
    from box2box.compensation
    where position='F'
    group by season, team
)

select teamName, s.season, goalsFor, totalCompensation
from box2box.standings as s
left join chicken
on chicken.team = s.team
and chicken.season = s.season
