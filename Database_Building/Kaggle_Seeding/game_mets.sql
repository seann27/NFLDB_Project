select game_id,
  spread_favorite,
  over_under_line,
  home_favorite,
  spread_result,
  OU_result,
  case
    when home_favorite=1 then home_rush_yds
    else away_rush_yds
  end as fav_rush_yds,
  case
    when home_favorite=1 then home_rush_att
    else away_rush_att
  end as fav_rush_att,
  case
    when home_favorite=1 then home_rush_tds
    else away_rush_tds
  end as fav_rush_tds,
  case
    when home_favorite=1 then home_short_pass_yds
    else away_short_pass_yds
  end as fav_short_pass_yds,
  case
    when home_favorite=1 then home_deep_pass_yds
    else away_deep_pass_yds
  end as fav_deep_pass_yds,
  case
    when home_favorite=1 then home_pass_tds
    else away_pass_tds
  end as fav_pass_tds,
  case
    when home_favorite=1 then home_pass_att
    else away_pass_att
  end as fav_pass_att,
  case
    when home_favorite=1 then home_completions
    else away_completions
  end as fav_completions,
  case
    when home_favorite=1 then home_sacked
    else away_sacked
  end as fav_sacked,
  case
    when home_favorite=1 then home_interceptions
    else away_interceptions
  end as fav_interceptions,
	case
		when home_favorite=1 then rush_skillpoints_home
		else rush_skillpoints_away
	end as fav_rush_skillpoints,
	case
		when home_favorite=1 then pass_skillpoints_home
		else pass_skillpoints_away
	end as fav_pass_skillpoints,
	case
		when home_favorite=0 then home_rush_yds
		else away_rush_yds
	end as und_rush_yds,
	case
		when home_favorite=0 then home_rush_att
		else away_rush_att
	end as und_rush_att,
	case
		when home_favorite=0 then home_rush_tds
		else away_rush_tds
	end as und_rush_tds,
	case
		when home_favorite=0 then home_short_pass_yds
		else away_short_pass_yds
	end as und_short_pass_yds,
	case
		when home_favorite=0 then home_deep_pass_yds
		else away_deep_pass_yds
	end as und_deep_pass_yds,
	case
		when home_favorite=0 then home_pass_tds
		else away_pass_tds
	end as und_pass_tds,
	case
		when home_favorite=0 then home_pass_att
		else away_pass_att
	end as und_pass_att,
	case
		when home_favorite=0 then home_completions
		else away_completions
	end as und_completions,
	case
		when home_favorite=0 then home_sacked
		else away_sacked
	end as und_sacked,
	case
		when home_favorite=0 then home_interceptions
		else away_interceptions
	end as und_interceptions,
	case
		when home_favorite=0 then rush_skillpoints_home
		else rush_skillpoints_away
	end as und_rush_skillpoints,
	case
		when home_favorite=0 then pass_skillpoints_home
		else pass_skillpoints_away
	end as und_pass_skillpoints
from nfl_gameinfo

select game_id,
          case
            when home_abbrev='DEN' then rush_skillpoints_home
            else rush_skillpoints_away
          end as rush_skillpoints,
          case
            when home_abbrev='DEN' then pass_skillpoints_home
            else pass_skillpoints_away
          end as pass_skillpoints
          from nfl_gameinfo
          where schedule_season= 2013
          and( home_abbrev='DEN' or away_abbrev='DEN')
          order by cast(schedule_week as int)
