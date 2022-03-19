import os
import time

from genetic2048.game import Game2048


def play_game() -> tuple[bool, int, int, int]:  # is victory ; number of moves; score; maximum
    game = Game2048()
    res = None
    while True:
        result1 = game.make_move(game.Move.DOWN)
        if result1 not in game.MoveResult.GAME_CONTINUES:
            res = result1
            break

        result2 = game.make_move(game.Move.RIGHT)
        if result2 not in game.MoveResult.GAME_CONTINUES:
            res = result2
            break

        if result1 == game.MoveResult.NOTHING and result2 == game.MoveResult.NOTHING:
            result3 = game.make_move(game.Move.LEFT)
            if result3 not in game.MoveResult.GAME_CONTINUES:
                res = result3
                break
            if result3 == game.MoveResult.NOTHING:
                result4 = game.make_move(game.Move.UP)
                if result4 not in game.MoveResult.GAME_CONTINUES:
                    res = result4
                    break

    return res == Game2048.MoveResult.VICTORY, game.get_number_of_moves(), game.get_score(), game.get_max_value()


if __name__ == '__main__':
    show_low = True

    num = 0
    victory_count = 0
    count1024 = 0
    count512 = 0
    count256 = 0
    count128 = 0
    count64 = 0
    score_count = 0
    maximum = 0
    time_ = 0
    time__ = time.time()
    while True:
        try:
            is_vic, moves, score, maxi = play_game()
            num += 1
            score_count += score
            if maxi > maximum:
                maximum = maxi
            if maxi >= 64:
                count64 += 1
            if maxi >= 128:
                count128 += 1
            if maxi >= 256:
                count256 += 1
            if maxi >= 512:
                count512 += 1
            if maxi >= 1024:
                count1024 += 1
            if is_vic:
                victory_count += 1

            if (time.time() - time_) > 30:
                time_ = time.time()
                os.system('clear')
                print()
                print('Games played:', num)
                print('Games per second:', num/(time.time() - time__))
                print('Victory count:', victory_count)
                print('1024 count:', count1024)
                print('Victory percent:', str((victory_count/num)*100) + '%')
                print('1024 percent:', str((count1024/num)*100) + '%')
                print('512 percent:', str((count512/num)*100) + '%')
                if show_low:
                    print('256 percent:', str((count256/num)*100) + '%')
                    print('128 percent:', str((count128/num)*100) + '%')
                    print('64 percent:', str((count64/num)*100) + '%')
                print('Average score:', score_count/num)
                print('Current max:', maximum)
        except KeyboardInterrupt:
            break
    print('STOPPED')
