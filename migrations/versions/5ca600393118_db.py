"""db

Revision ID: 5ca600393118
Revises: 
Create Date: 2020-06-01 21:37:33.580294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ca600393118'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contract',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=64), nullable=True),
    sa.Column('is_arch', sa.String(length=120), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('paid', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contract_is_arch'), 'contract', ['is_arch'], unique=False)
    op.create_index(op.f('ix_contract_number'), 'contract', ['number'], unique=True)
    op.create_index(op.f('ix_contract_paid'), 'contract', ['paid'], unique=False)
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=64), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payment_number'), 'payment', ['number'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payment_number'), table_name='payment')
    op.drop_table('payment')
    op.drop_index(op.f('ix_contract_paid'), table_name='contract')
    op.drop_index(op.f('ix_contract_number'), table_name='contract')
    op.drop_index(op.f('ix_contract_is_arch'), table_name='contract')
    op.drop_table('contract')
    # ### end Alembic commands ###
