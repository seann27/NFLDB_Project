from scrapers import PFR_Gamelinks,PFR_Gamepage

# test gamelinks object
err_gl = []
try:
	gl = PFR_Gamelinks(2019,6)
	links = gl.get_game_links()
except Exception as e:
	err_gl.append(e)
assert (len(err_gl) == 0), err_gl

# test gamepage object
err_pfrs = []
try:
	pfrs = PFR_Gamepage('https://www.pro-football-reference.com/boxscores/201310270den.htm')
except Exception as e:
	err_pfrs.append(e)
assert (len(err_pfrs) == 0), err_pfrs

# test get_total_offense()
err_off = []
try:
	off = pfrs.get_total_offense()
except Exception as e:
	err_off.append(e)
assert (len(err_off) == 0), err_off

# test get_receiving()
err_rec = []
try:
	rec = pfrs.get_receiving()
except Exception as e:
	err_rec.append(e)
assert (len(err_rec) == 0), err_rec

# test get_rushing()
err_rush = []
try:
	rush = pfrs.get_rushing()
except Exception as e:
	err_rush.append(e)
assert (len(err_rush) == 0), err_rush

# test get_defense()
err_defense = []
try:
	defense = pfrs.get_defense()
except Exception as e:
	err_defense.append(e)
assert (len(err_defense) == 0), err_defense

# test get_returns()
err_ret = []
try:
	ret = pfrs.get_returns()
except Exception as e:
	err_ret.append(e)
assert (len(err_ret) == 0), err_ret

# test get_home_snapcounts()
err_hsc = []
try:
	hsc = pfrs.get_home_snapcounts()
except Exception as e:
	err_hsc.append(e)
assert (len(err_hsc) == 0), err_hsc

# test get_vis_snapcounts()
err_vsc = []
try:
	vsc = pfrs.get_vis_snapcounts()
except Exception as e:
	err_vsc.append(e)
assert (len(err_vsc) == 0), err_vsc

# test get_gameinfo()
err_gi = []
try:
	gi = pfrs.get_gameinfo()
except Exception as e:
	err_gi.append(e)
assert (len(err_gi) == 0), err_gi

# test get_gameid()
err_gid = []
try:
	gid = pfrs.get_gameid()
except Exception as e:
	err_gid.append(e)
assert (len(err_gid) == 0), err_gid

# test get_gamedate()
err_gd = []
try:
	gd = pfrs.get_gamedate()
except Exception as e:
	err_gd.append(e)
assert (len(err_gd) == 0), err_gd
