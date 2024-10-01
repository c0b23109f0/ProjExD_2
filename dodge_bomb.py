import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))
accs = [a for a in range(1, 11)]


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん、または、爆弾のrect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def create_bomb_surfaces():
    accs = [a for a in range(1, 11)]
    bd_imgs = []
    for r in range(1, 11):
        bd_img = pg.Surface((20*r, 20*r))
        bd_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bd_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bd_imgs.append(bd_img)
    return accs, bd_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kc_img = pg.image.load("fig/8.png")
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()  #爆弾rectの抽出
    bd_rct.centerx = random.randint(0, WIDTH)
    bd_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  #爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    accs, bd_imgs = create_bomb_surfaces()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bd_rct):
            #こうかとんが重なっていたら
            blackout = pg.Surface((1100, 650))
            blackout.set_alpha(128)
            blackout.fill((0, 0, 0))
            screen.blit(blackout, (0, 0))
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", True, (255, 255, 255))
            screen.blit(txt, [400, 200])
            screen.blit(kc_img,[350, 200])
            screen.blit(kc_img,[720, 200])
            pg.display.update()
            time.sleep(5)
            

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        avx = vx * accs[min(tmr // 500, 9)]
        avy = vy * accs[min(tmr // 500, 9)]
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip((avx, avy))
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bd_img = bd_imgs[min(tmr // 500, 9)]
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
