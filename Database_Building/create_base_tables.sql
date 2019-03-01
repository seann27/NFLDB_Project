CREATE TABLE `games` 
(
	`id` varchar(255),
	`season` int,
	`week` int,
	`team_home` varchar(50),
	`team_away` varchar(50),
	`spread_vistor` float,
	`over_under` float,
	`points_home` int,
	`points_away` int
);

CREATE TABLE `players` 
(
	`id` varchar(255),
	`name` varchar(255),
	`team_id` varchar(255),
	`position` varchar(10)
);

CREATE TABLE `teams` 
(
	`id` varchar(255),
	`city` varchar(255),
	`name` varchar(255),
	`abbrev` varchar(3)
);

CREATE TABLE `offense` 
(
	`oid` int,
	`game_id` varchar(255),
	`player_id` varchar(255),
	`player_teamid` varchar(255),
	`pass_att` float,
	`pass_comp` float,
	`pass_yds` float,
	`pass_int` float,
	`rush_att` float,
	`rush_yds` float,
	`rush_tds` float,
	`rec_tgt` float,
	`rec` float,
	`rec_yds` float,
	`rec_tds` float,
	`pass_tds` float,
	`fmb_lost` float,
	`rtn_tds` float,
	`two_pts` float,
	`snapcount` int,
	`pct_snaps` float,
	`dk_points` float
);

CREATE TABLE `defense` 
(
	`did` int,
	`game_id` varchar(255),
	`team_id` varchar(255),
	`pass_yds_allow` float,
	`rush_yds_allow` float,
	`rec_yds_allow` float,
	`pass_tds_allow` int,
	`flex_tds_allow` int,
	`points_allow` int,
	`sacks` float,
	`interceptions` float,
	`def_points` float,
	`dk_points` float
);

ALTER TABLE `players` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`);

ALTER TABLE `offense` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`id`);

ALTER TABLE `offense` ADD FOREIGN KEY (`player_id`) REFERENCES `players` (`id`);

ALTER TABLE `defense` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`id`);

ALTER TABLE `defense` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`);

ALTER TABLE `games` ADD FOREIGN KEY (`team_home`) REFERENCES `teams` (`id`);

ALTER TABLE `games` ADD FOREIGN KEY (`team_away`) REFERENCES `teams` (`id`);
