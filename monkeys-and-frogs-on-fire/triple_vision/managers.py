import arcade


class GameManager:

    def __init__(self) -> None:
        self.enemies = arcade.SpriteList()
        self.player_projectiles = arcade.SpriteList()
        self.enemy_projectiles = arcade.SpriteList()

    def draw(self) -> None:
        self.enemies.draw()
        self.player_projectiles.draw()
        self.enemy_projectiles.draw()

    def create_enemy(self, enemy_class, *args, **kwargs) -> None:
        enemy = enemy_class(self, *args, **kwargs)
        self.enemies.append(enemy)
        return enemy

    def update(self, delta_time: float = 1/60) -> None:
        for enemy in self.enemies:
            for projectile in self.player_projectiles:
                if arcade.check_for_collision(projectile, enemy):
                    enemy.hit(
                        projectile.dmg,
                        projectile,
                        projectile.throwback_force,
                        tuple()
                    )
                    projectile.kill()

        self.enemies.update()
        self.player_projectiles.update()
        self.enemy_projectiles.update()
