#!/usr/bin/env sh
./tools/playgame.py --player_seed 42 --end_wait=0.25 --log_dir game_logs --turns 1000 --map_file tools/maps/example/tutorial1.map "$@" "python3 MyBot.py" "python tools/sample_bots/python/GreedyBot.py"
echo "\n\nContent of debug log:"
cat ./debug.txt
