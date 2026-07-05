"""Initial tables schema definition

Revision ID: 001_initial_tables
Revises: None
Create Date: 2026-07-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. faculty_profiles table
    op.create_table(
        'faculty_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_faculty_profiles_id'), 'faculty_profiles', ['id'], unique=False)

    # 3. syllabi table
    op.create_table(
        'syllabi',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('course_name', sa.String(), nullable=True),
        sa.Column('course_code', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_syllabi_id'), 'syllabi', ['id'], unique=False)

    # 4. lesson_plans table
    op.create_table(
        'lesson_plans',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_plans_id'), 'lesson_plans', ['id'], unique=False)

    # 5. assignments table
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignments_id'), 'assignments', ['id'], unique=False)

    # 6. quizzes table
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quizzes_id'), 'quizzes', ['id'], unique=False)

    # 7. question_papers table
    op.create_table(
        'question_papers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('exam_type', sa.String(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_papers_id'), 'question_papers', ['id'], unique=False)

    # 8. bloom_taxonomy_reports table
    op.create_table(
        'bloom_taxonomy_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bloom_taxonomy_reports_id'), 'bloom_taxonomy_reports', ['id'], unique=False)

    # 9. co_mapping_reports table
    op.create_table(
        'co_mapping_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_co_mapping_reports_id'), 'co_mapping_reports', ['id'], unique=False)

    # 10. academic_quality_reports table
    op.create_table(
        'academic_quality_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('suggestions', sa.JSON(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_academic_quality_reports_id'), 'academic_quality_reports', ['id'], unique=False)

    # 11. generated_pdf_reports table
    op.create_table(
        'generated_pdf_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_url', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_pdf_reports_id'), 'generated_pdf_reports', ['id'], unique=False)

    # 12. agent_execution_logs table
    op.create_table(
        'agent_execution_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('agent_name', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('log_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_execution_logs_id'), 'agent_execution_logs', ['id'], unique=False)

    # 13. application_settings table
    op.create_table(
        'application_settings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('llm_provider', sa.String(), nullable=True),
        sa.Column('model_name', sa.String(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_application_settings_id'), 'application_settings', ['id'], unique=False)

    # 14. generation_histories table
    op.create_table(
        'generation_histories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('syllabus_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['syllabus_id'], ['syllabi.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generation_histories_id'), 'generation_histories', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('generation_histories')
    op.drop_table('application_settings')
    op.drop_table('agent_execution_logs')
    op.drop_table('generated_pdf_reports')
    op.drop_table('academic_quality_reports')
    op.drop_table('co_mapping_reports')
    op.drop_table('bloom_taxonomy_reports')
    op.drop_table('question_papers')
    op.drop_table('quizzes')
    op.drop_table('assignments')
    op.drop_table('lesson_plans')
    op.drop_table('syllabi')
    op.drop_table('faculty_profiles')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
