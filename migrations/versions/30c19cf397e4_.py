"""empty message

Revision ID: 30c19cf397e4
Revises: 
Create Date: 2020-12-28 00:53:04.856755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30c19cf397e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class',
    sa.Column('cid', sa.String(length=5), nullable=False),
    sa.Column('strength', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('cid')
    )
    op.create_table('room',
    sa.Column('rno', sa.Integer(), nullable=False),
    sa.Column('lab', sa.Boolean(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('no_of_sys', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('rno')
    )
    op.create_table('subject',
    sa.Column('sid', sa.Integer(), nullable=False),
    sa.Column('sname', sa.String(length=20), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('teach_hrs', sa.Integer(), nullable=False),
    sa.Column('learn_hrs', sa.Integer(), nullable=False),
    sa.Column('credits', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('sid'),
    sa.UniqueConstraint('sname')
    )
    op.create_table('class_room',
    sa.Column('rno', sa.Integer(), nullable=False),
    sa.Column('class', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['class'], ['class.cid'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['rno'], ['room.rno'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('rno', 'class')
    )
    op.create_table('employee',
    sa.Column('eid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('f_name', sa.String(length=60), nullable=True),
    sa.Column('m_name', sa.String(length=60), nullable=True),
    sa.Column('l_name', sa.String(length=60), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('workload', sa.Integer(), nullable=True),
    sa.Column('ph_no', sa.String(length=10), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['room.rno'], ),
    sa.PrimaryKeyConstraint('eid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('room_subj',
    sa.Column('rno', sa.Integer(), nullable=False),
    sa.Column('sid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rno'], ['room.rno'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['sid'], ['subject.sid'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('rno', 'sid')
    )
    op.create_table('subj_class',
    sa.Column('sid', sa.Integer(), nullable=False),
    sa.Column('class', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['class'], ['class.cid'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['sid'], ['subject.sid'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('sid', 'class')
    )
    op.create_table('class_emp',
    sa.Column('eid', sa.Integer(), nullable=False),
    sa.Column('class', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['class'], ['class.cid'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['eid'], ['employee.eid'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('eid', 'class')
    )
    op.create_table('emp_subj',
    sa.Column('eid', sa.Integer(), nullable=False),
    sa.Column('sid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eid'], ['employee.eid'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['sid'], ['subject.sid'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('eid', 'sid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emp_subj')
    op.drop_table('class_emp')
    op.drop_table('subj_class')
    op.drop_table('room_subj')
    op.drop_table('employee')
    op.drop_table('class_room')
    op.drop_table('subject')
    op.drop_table('room')
    op.drop_table('class')
    # ### end Alembic commands ###
