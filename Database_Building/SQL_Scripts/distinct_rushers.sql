select distinct concat(game_id,rusher_player_id) as sid,rusher_player_name, posteam,
  0 as attempts,0 as le,0 as lt,0 as lg,0 as m,0 as re,0 as rt,0 as rg,0 as tds,0 as fmb
  from nfl_pbp where play_type = 'run'
