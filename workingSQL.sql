select distinct(pbp.game_id),pbp.home_team,game_date 
  from nfl_pbp pbp

select game_id, posteam, sum(yards_gained) as rush_yds, sum(rush_attempt) as rush_att,sum(rush_touchdown) as rush_tds
  from nfl_pbp
  where posteam = home_team
  and play_type = 'run'
group by game_id

select posteam,pass_length,sum(yards_gained)
  from nfl_db.nfl_pbp pbp
  where pbp.season = 2009
  and pbp.week = 1
  and pbp.play_type = 'pass'
  and pbp.sack = 0
  and pbp.incomplete_pass = 0
group by season,week,posteam,pass_length

select * from nfl_pbp limit 5

update nfl_pbp set posteam='JAX' where posteam='JAC';
update nfl_pbp set home_team='JAX' where home_team='JAC';
update nfl_pbp set away_team='JAX' where away_team='JAC'

select * 
  from nfl_pbp 
  where play_type = 'pass'
  and game_date = '2009-09-13'
  and interception = 1

select game_id,posteam,sum(yards_gained)
  from nfl_pbp
  where play_type='pass'
  and pass_length = 'short'
  and posteam=home_team

select game_id,posteam,sum(yards_gained) as home_short_passyds
  from nfl_pbp
  where play_type='pass'
  and pass_length = 'short'
  and posteam=home_team
  group by game_id,posteam

select game_id,posteam,sum(yards_gained) as home_deep_passyds
  from nfl_pbp
  where play_type='pass'
  and pass_length = 'deep'
  and posteam=home_team
  group by game_id,posteam

select game_id,
       posteam,
       sum(sack) as sacks,
       sum(interception) as interceptions,
       sum(pass_attempt) as pass_att,
       sum(pass_touchdown) as pass_tds,
       sum(complete_pass) as completions
  from nfl_pbp
  where play_type = 'pass'
  and posteam = home_team
  group by game_id

select game_id,
  case
    when home_abbrev='DEN' then home_rush_yds
    else away_rush_yds
  end as rush_yds
  from nfl_gameinfo
  where schedule_season=2013
  and( home_abbrev='DEN' or away_abbrev='DEN')
  order by cast(schedule_week as int)

  select * from nfl_skillpoints limit 5