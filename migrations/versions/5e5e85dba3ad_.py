"""empty message

Revision ID: 5e5e85dba3ad
Revises: 9e0583ef8579
Create Date: 2020-12-11 20:47:37.964132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e5e85dba3ad'
down_revision = '9e0583ef8579'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('rno', sa.Integer(), nullable=False),
    sa.Column('lab', sa.Boolean(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('no_of_sys', sa.Integer(), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.eid'], ),
    sa.PrimaryKeyConstraint('rno')
    )
    op.create_table('class_room',
    sa.Column('rno', sa.Integer(), nullable=False),
    sa.Column('class', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['class'], ['class.cid'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['rno'], ['room.rno'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('rno', 'class')
    )
    op.create_table('room_subj',
    sa.Column('rno', sa.Integer(), nullable=False),
    sa.Column('sid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rno'], ['room.rno'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['sid'], ['subject.sid'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('rno', 'sid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_subj')
    op.drop_table('class_room')
    op.drop_table('room')
    # ### end Alembic commands ###