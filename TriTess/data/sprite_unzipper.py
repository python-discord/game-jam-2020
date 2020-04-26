import zipfile


def extract_sprites_zip(zip_path='sprites.zip'):
    """
    this is an utility function that unzips and renames sprites from piskel programmically
    :param zip_path: path to zip file of the sprites
    """
    piece_list = ['pawn', 'rook', 'king', 'bishop', 'queen', 'knight']
    sprite_file_list = []
    for piece in piece_list:
        sprite_file_list.extend([f'sprite_{piece}{i}.png' for i in [0,2,1]])

    with zipfile.ZipFile(zip_path) as sprite_zip:
        for i, sprite_file in enumerate(sprite_zip.namelist()):
            with open(sprite_file_list[i], 'wb') as f:
                f.write(sprite_zip.read(sprite_file))


if __name__ == "__main__":
    extract_sprites_zip()