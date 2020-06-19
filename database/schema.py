import sqlalchemy as sa

metadata = sa.MetaData()

card = sa.Table(
    'card', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('group_id', sa.ForeignKey('card_group.id')),
    sa.Column('common_name', sa.String(255), unique=True, nullable=False),
    sa.Column('latin_name', sa.String(255)),
    sa.Column('artfakta_id', sa.Integer()))

card_group = sa.Table(
    'card_group', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(128), nullable=False, unique=True))

user = sa.Table(
    'user', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(255), nullable=False, unique=True))

card_weight = sa.Table(
    'card_weight', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('user_id', sa.ForeignKey('user.id'), nullable=False),
    sa.Column('card_id', sa.ForeignKey('card.id'), nullable=False),
    sa.Column('weight', sa.Float()))
